from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
import jwt

User = get_user_model()


class UserConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        qs = parse_qs(self.scope["query_string"].decode())
        token = qs.get("token", [None])[0]
        if not token:
            await self.close()
            return

        self.user = await self.get_user_from_token(token)
        if not self.user:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        await self.send_json({
            "event": "connected",
            "user_id": str(self.user.id),
            "message": "WebSocket connection established"
        })

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def story_event(self, event):
        await self.send_json(event["payload"])

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return User.objects.get(id=payload["user_id"])
        except Exception:
            return None
