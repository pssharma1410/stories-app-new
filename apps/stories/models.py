import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Story(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("friends", "Friends"),
        ("private", "Private"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    text = models.TextField(blank=True, null=True)
    media_key = models.CharField(max_length=1024, blank=True, null=True)
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="public"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)


class StoryAudience(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="audience")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("story", "user")


class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="views")
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("story", "viewer")


class Reaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
