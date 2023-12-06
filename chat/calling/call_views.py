from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from chat import models
from django.db.models import Q
from rest_framework.response import Response
from utils.push_notifications import send_push_notification
import json

# reciever id, Return - nned to detech common rooms,
# send in notification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_receiver_fcm(request):
    receiver_id = request.data.get('receiver_id')
    type = request.data.get('type')
    receiver = models.User.objects.get(id=receiver_id)
    if receiver is not None:
        room_obj = models.Room.objects.filter(
            Q(creator=request.user, member=receiver) |
            Q(creator=receiver, member=request.user)
        ).first()

        data = {
            'type': type,
            'room_unique_id': room_obj.unique_id,
            'receiver_id': receiver_id,
            'sender_full_name': request.user.full_name,
            'sender_profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
        }

        for key, value in data.items():
            if not isinstance(value, str):
                data[key] = str(value)


        send_push_notification(
            user=receiver,
            title=f"{request.user.full_name}",
            body="Incoming call",
            data=data
        )

        return Response(data)
