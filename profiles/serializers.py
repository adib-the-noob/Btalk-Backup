from rest_framework import serializers
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = models.Profile
        fields = [
            'user_info',
            'gender',
            'bio',
            'address',
        ]

    def create(self, validated_data):
        user = self.validated_data['user']
        gender = self.validated_data['gender']
        bio = self.validated_data['bio']
        address = self.validated_data['address']
        profile_obj = models.Profile.objects.create(
            user=user,
            gender=gender,
            bio=bio,
            address=address
        )
        return profile_obj

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
            'cover_photo': obj.user.cover_photo.url if obj.user.cover_photo else None,
            'is_online': obj.user.is_online,
        }
    

class CoverPhotoSerializer(serializers.Serializer):
    cover_photo = serializers.FileField()