from rest_framework import serializers
from . import models


class FriendsSearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'full_name',
            'profile_picture',
        ]


class MessageAttachmentSerializers(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    class Meta:
        model = models.MessageAttachment
        fields = [
            'file_name',
            'file'
        ]

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]
    
class PreviousMessageSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    attachments = MessageAttachmentSerializers(many=True, read_only=True)
    sender_info = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    class Meta:
        model = models.Message
        fields = [
            'id',
            "room",
            'content',
            'created_at',
            'user',
            'attachments',
            'sender_info',
        ]

    def get_sender_info(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
        }

    def get_room(self, obj):
        return obj.room.unique_id