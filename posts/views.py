from django.db.models import Q

from rest_framework import views, status
from rest_framework.response import Response
from . import models, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from utils.is_friend_checker import is_post_creator_friend

class PostCreateView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = serializers.PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.validated_data.get('title')
                attachments = serializer.validated_data.get('attachments')
                privacy = serializer.validated_data.get('privacy')
                post = models.Post.objects.create(
                    user=request.user,
                    title=title,
                    privacy=privacy
                )
                if attachments is not None:
                    for attachment in attachments:
                        models.PostAttachments.objects.create(
                            post=post,
                            image=attachment
                        )
                    return Response({
                        'message': 'Post created successfully.',
                        'data' : {
                            'id': post.id,
                            'title': post.title,
                            'privacy': post.privacy,
                            'attachments': [attachment.image.url for attachment in post.attachments.all()]
                        }
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    'message': 'Post created successfully.',
                    'data' : serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_post(request, pk):
    try:
        serializer = serializers.PostUpdateSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            privacy = serializer.validated_data.get('privacy')
            delete_attachments = serializer.validated_data.get('delete_attachments')
            new_attachments = request.FILES.getlist('new_attachments')

            post_obj = models.Post.objects.filter(id=pk, user=request.user).first()
            if post_obj:
                models.Post.objects.filter(id=pk).update(
                    title=title,
                    privacy=privacy
                )
                if delete_attachments == 'all':
                    for attachment in delete_attachments:
                        models.PostAttachments.objects.filter(post=post_obj.id).delete()
                if new_attachments is not None:
                    for attachment in new_attachments:
                        models.PostAttachments.objects.create(
                            post=post_obj,
                            image=attachment
                        )
                return Response({
                    'message': 'Post updated successfully.',
                    'id': post_obj.id,
                    'title': post_obj.title,
                    'privacy': post_obj.privacy,
                    'attachments': [attachment.image.url for attachment in post_obj.attachments.all()]
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'No post found.'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_post(request, pk):
    try:
        post_obj = models.Post.objects.filter(id=pk, user=request.user).first()
        if post_obj:
            post_obj.delete()
            return Response({
                'message': 'Post deleted successfully.'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'No post found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_timeline_posts(request, user_id : int=None):
    try:
        requested_user = request.user
        if user_id is not None:
            friend_checker = is_post_creator_friend(requested_user=requested_user, post_creator=user_id)
            if friend_checker:
                post_obj = models.Post.objects.filter(user__id=user_id).filter(privacy__in=['public', 'friends']).order_by('-created_at')  
            elif requested_user.id == user_id:
                post_obj = models.Post.objects.filter(user__id=user_id).order_by('-created_at')  
            else:
                post_obj = models.Post.objects.filter(user__id=user_id, privacy='public').order_by('-created_at')

            paginator = PageNumberPagination()
            paginator.page_size = 20
            post_obj = paginator.paginate_queryset(post_obj, request)
            serializer = serializers.PostSerializer(post_obj, many=True, context={'request': request})
            if serializer.data:
                return paginator.get_paginated_response(serializer.data)
            return Response(
                []
            , status=status.HTTP_200_OK)
        return Response({
            'message': 'User id is required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
