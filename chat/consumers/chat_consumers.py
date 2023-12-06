from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

import json

from .. import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        if not await self.room_exists():
            await self.close()
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def room_exists(self):
        return await sync_to_async(models.Room.objects.filter(unique_id=self.room_id).exists)()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = await self.save_message(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )


    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'send_message',
            'message': event['message']
        }))



    @database_sync_to_async
    def save_message(self, event, attachment=None):
        sender = self.scope['user'].pk
        sender_name = self.scope['user'].full_name
        sender_profile_image = self.scope['user'].profile_picture
        content = event['message']
        room_id = self.room_id
        sender = models.User.objects.get(pk=sender).pk
        room = models.Room.objects.get(
            unique_id=room_id
        )

        message_data = {
            'user_id': sender,
            'room_id': room.pk,
            'content': content,
            'is_read': False,
        }
        message_obj = models.Message.objects.create(**message_data)
        
        message_id = message_obj.pk
        created_at = timezone.localtime(message_obj.created_at)
        created_at = message_obj.created_at
        created_at = created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        is_read = message_obj.is_read

        serialized_message = {
                'message_id': message_id,
                'sender_id': sender,
                'sender_info': {
                    'full_name': sender_name,
                    'profile_picture': sender_profile_image.url if sender_profile_image else None,
                },
                'room' : {
                    'unique_id': room_id,
                    'room_type': room.room_type,
                    'room_name': room.groups.first().room_name if room.groups.first() else None,
                    'room_picture': room.groups.first().room_picture.url if room.groups.first() else None,
                },
                'content': content,
                'created_at': created_at,
                'is_read': is_read,
            }   
        
        return serialized_message
    

