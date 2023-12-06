from rest_framework import serializers
from posts.models import Comment, Post

class CommentsSerializers(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'user_info',
            'post',
            'comment',
        ]
    
    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
        }
    
    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']
        comment = validated_data['comment']
        return Comment.objects.create(user=user, post=post, comment=comment)
    
    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.save()