from rest_framework.permissions import BasePermission
from django.utils import timezone
from apps.users.models import Follow
from apps.stories.models import StoryAudience


class CanViewStory(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.deleted_at is not None or obj.expires_at < timezone.now():
            return False
        if obj.visibility == "public":
            return True
        if obj.visibility == "private":
            return obj.author_id == request.user.id
        if obj.visibility == "friends":
            is_follower = Follow.objects.filter(
                follower=request.user, followee=obj.author
                ).exists()

            in_audience = StoryAudience.objects.filter(
                story=obj, user=request.user
                ).exists()

            return is_follower or in_audience
        # return False
