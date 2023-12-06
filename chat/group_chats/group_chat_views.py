from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from . import group_serializer
from .. import models

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_group(request):
    try:
        serializer = group_serializer.CreatePublicRoomSerializer(data=request.data)
        if serializer.is_valid():
            room_name = serializer.validated_data['room_name']
            room_members = serializer.validated_data['room_members']
            room_picture = serializer.validated_data['room_picture'] if 'room_picture' in serializer.validated_data else None
            room_type = 'public'
            creator = request.user
            room = models.Room.objects.create(
                room_type=room_type,
                creator=creator,
            )
            room.member.add(*room_members, creator)
            room.save()
            group_info = models.PublicGroupInfo.objects.create(
                room=room,
                room_name=room_name,
                room_picture=room_picture,
            )
            return Response({
                'room_unique_id': room.unique_id,
                'room_picture': group_info.room_picture.url if group_info.room_picture else None,
                'message': 'Group created successfully',
            }, status=status.HTTP_201_CREATED)
        return Response({
            serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error': str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_all_groups(request):
    try:
        user = request.user
        groups = models.Room.objects.filter(
            room_type='public',
            member=user,
        )
        serializer = group_serializer.GroupsSerializers(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error' : str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def search_groups(request):
    try:
        user = request.user
        search = request.query_params.get('groupName', None)
        groups = models.Room.objects.filter(
            room_type='public',
            member=user,
            groups__room_name__icontains=search,
        )
        serializer = group_serializer.GroupsSerializers(groups, many=True)
        return Response({
            'groups': serializer.data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error' : str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
