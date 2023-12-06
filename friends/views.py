from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from . import serializers, models
from utils.roomid import get_roomid


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_friend_by_sync(request):
    try:
        serializer = serializers.NewContactSerializer(data=request.data)
        if serializer.is_valid():
            contact_lists = serializer.validated_data['contact_lists']
            requested_user = request.user   # get the current user
            users = models.User.objects.filter(phone_number__in=contact_lists)
            friends = [user for user in users if user != requested_user]
            new_rooms = get_roomid(requested_user, friends)
            user_contact, _ = models.Contacts.objects.get_or_create(user=requested_user)

            # Collect all the room objects in a list
            rooms_list = []

            for room in new_rooms:
                rooms_list.append(room)

            # Assign the list of rooms to the 'contacts' attribute
            user_contact.contacts = rooms_list
            user_contact.save()
            return Response({
                'message': 'Contacts synced successfully!'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Do not touch this API. This is ready.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_friends(request):
    try:
        friends = models.Contacts.objects.filter(user=request.user)
        serializer = serializers.FriendSerializer(friends, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
