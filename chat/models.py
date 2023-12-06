from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

from uuid import uuid4
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message as FCMMessage

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)    

    def __str__(self):
        return f"{self.user.full_name} - {self.content} - {self.is_read == True and 'read' or 'unread'}"

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            # send to user except sender
            users = self.room.member.all().exclude(id=self.user.id)
            title = f"{self.user.full_name} messaged you"
            body = f"{self.content}"
            notification_type = "message_received"

            for user in users:
                devices = FCMDevice.objects.all().filter(user=user)
                for device in devices:
                    device.send_message(
                        FCMMessage(
                            data={
                                'sender_id': str(self.user.id),
                                'sender_full_name': str(self.user.full_name),
                                'room_unique_id': str(self.room.unique_id),
                                'message_created_at': str(self.created_at),
                                'notification_type': notification_type,
                            },
                            notification=Notification(
                                title=title,
                                body=body,
                            ),
                        )
                    )


            inbox_users = self.room.member.all()
            channel_layer = get_channel_layer()
            users_list = []
            for user in inbox_users:
                for member in self.room.member.all().exclude(id=user.id):
                    if self.room.room_type == 'private':     
                        users_list = []                  
                        users_list.append({
                            'id': member.id,
                            'full_name': member.full_name,
                            'profile_picture': member.profile_picture.url if member.profile_picture else None,
                        })
                    else:
                        users_list = []
                        users_list.append({
                            'id': self.user.id,
                            'full_name': self.user.full_name,
                            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                        })
                    users_list = dict(users_list[0])
                async_to_sync(channel_layer.group_send)(
                    f'inbox_{user.id}',
                    {
                        'type': 'inbox_message',
                        'message': {
                            'sender': users_list,
                            'room': {
                                'unique_id': str(self.room.unique_id),
                                'room_type': self.room.room_type,
                                'room_name': self.room.groups.first().room_name if self.room.groups.first() else None,
                                'room_picture': self.room.groups.first().room_picture.url if self.room.groups.first() else None,
                            },
                            'sender_id': self.user.id,
                            'content': self.content,
                            'is_read': self.is_read,
                            'created_at': str(self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                        }
                    }
                )

class Room(BaseModel):
    ROOM_TYPE = (
        ('private', 'Private'),
        ('public', 'Public'),
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    member = models.ManyToManyField(User, related_name='rooms')
    unique_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    room_type = models.CharField(max_length=255, choices=ROOM_TYPE, default='private')

    def __str__(self):
        return f"{self.unique_id} - {self.room_type} - {self.creator.full_name}"

class PublicGroupInfo(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='groups')
    room_name = models.CharField(max_length=255, null=True, blank=True)
    room_picture = models.ImageField(upload_to=f'group_pictures/', null=True, blank=True)

    def __str__(self):
        return f"group: {self.room_name} - {self.room.unique_id}"

    def save(self, *args, **kwargs):
        self.room.room_type = 'public'
        self.room.save()
        super().save(*args, **kwargs)

    
class MessageAttachment(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=f'message_attachments/', null=True, blank=True)

    def __str__(self):
        return f"{self.message.user.full_name} - {self.file.name}"

    class Meta:
        ordering = ['-created_at']
