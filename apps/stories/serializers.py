from rest_framework import serializers
from .models import Story, Reaction
from apps.users.serializers import UserSerializer


class StorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    file_path = serializers.CharField(read_only=True)  # for local storage
    expires_at = serializers.DateTimeField(read_only=True)  # 👈 make read-only

    class Meta:
        model = Story
        fields = [
            "id",
            "author",
            "text",
            "media_key",   # optional, can leave blank
            "file_path",   # local file path
            "visibility",
            "created_at",
            "expires_at",  # generated in perform_create
        ]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["id", "story", "user", "emoji", "created_at"]
