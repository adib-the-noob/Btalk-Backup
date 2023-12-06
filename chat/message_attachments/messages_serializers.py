from rest_framework import serializers
from .. import models

class AttachmentSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    room_id = serializers.CharField(max_length=255, required=True)
    file = serializers.FileField()
    