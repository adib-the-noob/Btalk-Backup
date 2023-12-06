from rest_framework import serializers
from . import models

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications
        fields = [
            'id',
            'post',
            'message',
            'is_read',
        ]
