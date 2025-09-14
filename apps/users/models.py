from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    # Avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # changed from default
        blank=True,
        help_text="Groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",  # changed from default
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


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

    def __str__(self):
        return f"{self.follower} -> {self.followee}"
