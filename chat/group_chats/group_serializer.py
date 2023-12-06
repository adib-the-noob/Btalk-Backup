from rest_framework import serializers
from .. import models

class CreatePublicRoomSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=100)
    room_members = serializers.ListField(child=serializers.CharField(max_length=100)) # ['1', '2', '3']
    room_picture = serializers.ImageField(required=False)





class GroupsSerializers(serializers.ModelSerializer):
    room_info = serializers.SerializerMethodField()
    class Meta:
        model = models.Room
        fields = [
            'id',
            'unique_id',
            'room_type',
            'room_info'
        ]
    def get_room_info(self, obj):
        try:
            group_info = models.PublicGroupInfo.objects.get(room=obj)
            return {
                'room_name': group_info.room_name,
                'room_picture': group_info.room_picture.url if group_info.room_picture else None,
            }
        except:
            return None