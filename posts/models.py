from typing import Any, Dict, Iterable, Optional, Tuple
from django.db import models
from django.contrib.auth import get_user_model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import boto3
from django.conf import settings

from notifications.models import Notifications

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    
    POST_PRIVACY_CHOICES = (
        ('public', 'public'),
        ('friends', 'friends'),
        ('only me', 'only me'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.TextField()
    privacy = models.CharField(max_length=10, choices=POST_PRIVACY_CHOICES, default='public')


    def __str__(self):
        return f"{self.id} - {self.user} - {self.privacy} - {self.title[:25]}"

    def delete(self, *args, **kwargs):
        s3_client = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        for attachment in self.attachments.all():
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=attachment.image.name)
        super().delete(*args, **kwargs)

class PostAttachments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    image = models.ImageField(upload_to=f'post_attachments/')

    def __str__(self):
        return f"{self.post}"
    
    # def delete(self, *args, **kwargs):
    #     s3_client = boto3.client('s3',
    #         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #         region_name=settings.AWS_S3_REGION_NAME
    #     )
    #     s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=self.image.name)
    #     super().delete(*args, **kwargs)
        

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'like'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.reaction}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user.id != self.post.user.id:
            notification = Notifications.objects.create(
                user=self.post.user,
                message={
                        'type': 'reaction_notification',
                        'message': {
                            'post_id': self.post.id,
                            'post_title': self.post.title,
                            'user_id': self.user.id,
                            'user_full_name' : self.user.full_name,
                            'user_profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                            'reacted': True if self.reaction else False,
                        }
                    },
                    post=self.post,
                    is_read=False
                )
            
            async_to_sync(get_channel_layer().group_send)(
                f'inbox_{self.post.user.id}',
                {
                    'type': 'reaction_notification',
                        'message': {
                            'notification_id': int(notification.id),
                            'post_id': self.post.id,
                            'post_title': self.post.title[:25],
                            'user_id': self.user.id,
                            'user_full_name' : self.user.full_name,
                            'user_profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                            'reacted' : True if self.reaction else False,
                            'created_at': str(notification.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                        }
                    }
            )

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.post} - {self.comment[:25]}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user.id != self.post.user.id:
            notification = Notifications.objects.create(
                user=self.post.user,
                message={
                        'type': 'comment_notification',
                        'message': {
                            'post_id': self.post.id,
                            'post_title' : self.post.title,
                            'user_id': self.user.id,
                            'user_full_name' : self.user.full_name,
                            'user_profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                            'comment': self.comment[:25],
                        }
                    },
                    post=self.post,
                    is_read=False
                )
            
            async_to_sync(get_channel_layer().group_send)(
                f'inbox_{self.post.user.id}',
                {
                    'type': 'comment_notification', 
                    'message': {
                        'notification_id': int(notification.id),
                        'post_id': self.post.id,
                        'post_title' : self.post.title[:25],
                        'user_id': self.user.id,
                        'user_full_name' : self.user.full_name,
                        'user_profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
                        'comment': self.comment[:25],
                        'created_at': str(notification.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                    }
                }
            )
        