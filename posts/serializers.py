from rest_framework import serializers
from . import models

class PostAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostAttachments
        fields = [
            'id',
            'image'
        ]
        

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    total_comments = serializers.SerializerMethodField(read_only=True)
    attachments = PostAttachmentsSerializer(many=True, read_only=True)
    is_reacted = serializers.SerializerMethodField(read_only=True)
    profile_picture = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)

    class Meta:
        model = models.Post
        fields = [
            'id',
            'user',
            'full_name',
            'profile_picture',
            'title',
            'created_at',
            'attachments',
            'total_likes',
            'total_comments',
            'is_reacted',
            'privacy'
        ]

    def get_profile_picture(self, obj):
        if obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_total_likes(self, obj):
        return obj.reactions.filter(reaction='like').count()
    
    def get_total_comments(self, obj):
        return obj.comments.count()
    
    def get_is_reacted(self, obj):
        return obj.reactions.filter(user=self.context['request'].user).exists()

class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    privacy = serializers.CharField(required=False)
    attachments = serializers.ListField(child=serializers.ImageField(), required=False)
    
class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    privacy = serializers.CharField(required=False)
    delete_attachments = serializers.CharField(required=False)
    new_attachments = serializers.ListField(child=serializers.ImageField(), required=False)
