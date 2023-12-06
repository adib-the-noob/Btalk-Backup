from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from posts.models import Reaction, Post

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def react_post(request, post_id : int):
    user = request.user
    reaction_obj = Reaction.objects.filter(post_id=post_id, user_id=user.id, reaction="like")
    if reaction_obj.exists():
        reaction_obj.delete()
        return Response({
            "reacted": False,
        })
    else:
        post_obj = Post.objects.get(id=post_id)
        reaction_obj = Reaction.objects.create(post_id=post_obj.id, user_id=user.id, reaction="like")
        return Response({
            "reacted": True,
        }, status=status.HTTP_201_CREATED)