from rest_framework.permissions import BasePermission
from django.utils import timezone
from apps.users.models import Follow


class CanViewStory(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.deleted_at is not None or obj.expires_at < timezone.now():
            return False
        if obj.visibility == "public":
            return True
        if obj.visibility == "private":
            return obj.author_id == request.user.id
        if obj.visibility == "friends":
            return Follow.objects.filter(
                follower=request.user, followee=obj.author
            ).exists()
        return False
