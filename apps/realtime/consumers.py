from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
import jwt


class UserConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        qs = parse_qs(self.scope["query_string"].decode())
        token = qs.get("token", [None])[0]
        if not token:
            await self.close()
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await database_sync_to_async(get_user_model().objects.get)(
                id=payload["user_id"]
            )
            self.user = user
        except Exception:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def story_event(self, event):
        await self.send_json(event["payload"])
