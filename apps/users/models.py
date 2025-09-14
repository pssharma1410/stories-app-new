from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    REQUIRED_FIELDS = ["email"]


class Follow(models.Model):
    follower = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="following"
    )
    followee = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followee")
