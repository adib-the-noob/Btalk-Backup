from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
import json
import datetime
from chat import models


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        self.user_group = f'inbox_{self.user.id}'
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )
        await self.accept()
        await self.get_user_status(
            user_id=self.user.id,
            active_status=True,
            last_online=datetime.datetime.now()
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )
        await self.get_user_status(
            user_id=self.user.id,
            active_status=False,
            last_online=datetime.datetime.now()
        )

    async def receive(self, text_data):
        pass
    
    @database_sync_to_async
    def get_user_status(self, user_id, active_status, last_online):
        user_obj = models.User.objects.filter(id=user_id).first()
        if user_obj is not None:
            user_obj.is_online = active_status
            user_obj.last_online = last_online
            user_obj.save()
        return None
    
    async def reaction_notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def comment_notification(self, event):
        await self.send(text_data=json.dumps(event))