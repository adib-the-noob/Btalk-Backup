from rest_framework import serializers

from . import models
from profiles.models import Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'password',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    
    email_or_phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    fcm_token = serializers.CharField(required=True)    
    device_type = serializers.CharField(required=True)
    
    def validate(self, attrs):
        email_or_phone_number = attrs.get('email_or_phone_number')
        password = attrs.get('password')

        if not email_or_phone_number:
            raise serializers.ValidationError('A email or phone number is required to login.')
        
        if not password:
            raise serializers.ValidationError('A password is required to login.')
        return attrs
    

class OtpVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(required=True)


class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField(required=True)


class ForgotPasswordOtpRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class ForgotPasswordOtpVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp = serializers.IntegerField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
