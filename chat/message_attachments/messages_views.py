from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from . import messages_serializers as serializers
from .. import models

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def send_attachement(request):

        serializer = serializers.AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            
            text = serializer.validated_data['message'] if 'message' in serializer.validated_data else None 
            file = serializer.validated_data['file']
            room_id = serializer.validated_data['room_id']
            
            room = models.Room.objects.get(unique_id=room_id)
            message = models.Message.objects.create(
                user=request.user,
                room=room,
                content=text
            )    
            message.save()
            attachment = models.MessageAttachment.objects.create(
                message=message,
                file=file,
            )
            attachment.save()

            attachments = {
                "file": attachment.file.url,
                "file_name" : attachment.file.name.split('/')[-1],
            }
            async_to_sync(get_channel_layer().group_send)(
                f'chat_{room_id}',
                {
                    'type': 'send_message',
                    'message': {
                        'sender_info': {
                            'id': request.user.id,
                            'full_name': request.user.full_name,
                            'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
                        },
                        'room': {
                            'unique_id': str(room.unique_id),
                            'room_type': room.room_type,
                            'room_name': room.groups.first().room_name if room.groups.first() else None,
                            'room_picture': room.groups.first().room_picture.url if room.groups.first() else None,
                        },
                        'sender_id': request.user.id,
                        'content': message.content,
                        'attachments': attachments,
                        'is_read': message.is_read,
                        'created_at': str(message.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                    }
                }
            )
            return Response({
                "type": "send_message",
                "sender_id": request.user.id,
                "sender_info": {
                    "full_name": request.user.full_name,
                    "profile_picture": request.user.profile_picture.url if request.user.profile_picture else None,
                },
                "message_id": message.id,
                "attachments": attachments,
                "content": message.content if message.content else None,
                "time_stamp": message.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "is_read": message.is_read,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
