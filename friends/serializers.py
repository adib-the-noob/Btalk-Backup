from rest_framework import serializers
from . import models

class NewContactSerializer(serializers.Serializer):
    contact_lists = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )


class FriendSerializer(serializers.ModelSerializer):
    # friend_info = serializers.SerializerMethodField()
    class Meta:
        model = models.Contacts
        fields = [
            'contacts',
        ]

    # def get_friend_info(self, obj):
    #     requested_user = self.context['request'].user
    #     if requested_user == obj.user1:
    #         other_user = obj.user2
    #         data = {
    #             "id": other_user.id,
    #             "full_name": other_user.full_name,
    #             "profile_pic":  other_user.profile_picture.url if other_user.profile_picture else None,
    #         }
    #         return data
    #     else:
    #         other_user = obj.user1
    #         data = {
    #             "id": other_user.id,
    #             "full_name": other_user.full_name,
    #             "profile_pic":  other_user.profile_picture.url if other_user.profile_picture else None,
    #         }
    #         return data