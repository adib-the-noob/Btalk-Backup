from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
import json
from .. import models


class InboxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        self.inbox_group = f'inbox_{self.user.id}'
        await self.channel_layer.group_add(
            self.inbox_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.inbox_group,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

    async def inbox_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))