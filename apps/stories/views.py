import os
import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import transaction, models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Story, StoryAudience, StoryView, Reaction
from .serializers import StorySerializer, ReactionSerializer
from .permissions import CanViewStory
from apps.users.models import Follow
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class LocalUploadView(viewsets.ViewSet):
    """
    Uploads a file locally instead of AWS S3.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"detail": "No file uploaded"}, status=400)

        if not uploaded_file.content_type.startswith(("image/", "video/")):
            return Response({"detail": "invalid content_type"}, status=400)

        # Create a unique path
        filename = f"stories/{request.user.id}/{uuid.uuid4()}_{uploaded_file.name}"
        path = default_storage.save(filename, ContentFile(uploaded_file.read()))

        return Response({"file_path": path}, status=201)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(deleted_at__isnull=True)
    serializer_class = StorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), CanViewStory()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        ttl = int(os.getenv("STORY_TTL_SECONDS", "86400"))
        expires_at = timezone.now() + timedelta(seconds=ttl)

        with transaction.atomic():
            story = serializer.save(author=self.request.user, expires_at=expires_at)
            audience_ids = self.request.data.get("audience_user_ids") or []
            if story.visibility == "friends" and audience_ids:
                StoryAudience.objects.bulk_create(
                    [StoryAudience(story=story, user_id=uid) for uid in audience_ids]
                )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{story.author.id}",
                {
                    "type": "story_event",
                    "payload": {
                        "event": "story_created",
                        "story_id": str(story.id),
                        "author_id": str(story.author.id),
                        "author_username": story.author.username,
                        "visibility": story.visibility,
                    },
                },
         )

            return story

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        story = self.get_object()
        story_view, created = StoryView.objects.get_or_create(
            story=story, viewer=request.user
        )

        if created:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{story.author.id}",
                {
                    "type": "story_event",
                    "payload": {
                        "event": "story_view",
                        "story_id": str(story.id),          # ✅ cast to str
                        "viewer_id": str(request.user.id),  # ✅ cast to str
                        "viewer_username": request.user.username,
                    },
                },
            )

        return Response(
            {
                "message": "Story marked as viewed",
                "story_id": str(story.id),        # ✅ cast to str
                "viewer_id": str(request.user.id) # ✅ cast to str
            },
            status=200,
        )

    @action(detail=True, methods=["post"])
    def reactions(self, request, pk=None):
        story = self.get_object()
        emoji = request.data.get("emoji")
        allowed = ["👍", "❤️", "😂", "😮", "😢", "🔥"]

        if emoji not in allowed:
            return Response({"detail": "invalid emoji"}, status=400)

        reaction = Reaction.objects.create(story=story, user=request.user, emoji=emoji)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{story.author.id}",
            {
                "type": "story_event",
                "payload": {
                    "event": "story_reaction",
                    "story_id": str(story.id),          # ✅ cast to str
                    "user_id": str(request.user.id),    # ✅ cast to str
                    "username": request.user.username,
                    "emoji": reaction.emoji,
                    "reaction_id": str(reaction.id),    # ✅ cast to str
                },
            },
        )

        return Response(
            {
                "message": "Reaction added",
                "story_id": str(story.id),
                "user_id": str(request.user.id),
                "emoji": reaction.emoji,
                "reaction_id": str(reaction.id),
            },
            status=201,
        )


    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def feed(self, request):
        now = timezone.now()
        followees = Follow.objects.filter(follower=request.user).values_list(
            "followee_id", flat=True
        )
        qs = Story.objects.filter(
            deleted_at__isnull=True, expires_at__gt=now
        ).filter(
            models.Q(visibility="public")
            | models.Q(author_id__in=followees)
            | models.Q(author=request.user)
        ).select_related("author").order_by("-created_at")

        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page or qs, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
