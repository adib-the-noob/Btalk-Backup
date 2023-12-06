from rest_framework import status, views, permissions, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from . import serializers, models
from django.db.models import Q
from django.db.models import Max
from friends.models import Contacts


# move this to friends
class FriendsSearchAPIView(views.APIView):
    serializer_class = serializers.FriendsSearchSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.query_params.get("friendInfo")
            if search_query:
                friends = models.User.objects.filter(
                    Q(full_name__icontains=search_query)
                    | Q(phone_number__icontains=search_query)
                ).exclude(id=request.user.id)
                if friends.exists():
                    serializer = self.serializer_class(friends, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response([], status=status.HTTP_200_OK)
            # rest of the logic
            else:
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PreviousMessageAPIView(generics.GenericAPIView):
    serializer_class = serializers.PreviousMessageSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request):
        try:
            room_id = request.query_params.get("roomId")
            created_at = request.query_params.get("createdAt")
            if room_id is not None:
                # query last 20 messages before this time
                messages = models.Message.objects.filter(
                    room__unique_id=room_id, created_at__lte=created_at
                ).order_by("-created_at")[:20]
                # reverse all messages
                messages = messages[::-1]
                serializer = self.serializer_class(messages, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {
                    "message": "No Message found!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class InboxProfileAPIView(generics.GenericAPIView):
    # serializer_class = serializers.InboxProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, friendId: int):
        try:
            friend = models.User.objects.get(id=friendId)
            if friend is not None:
                exsisting_room = models.Room.objects.filter(
                    Q(creator=request.user, member=friend)
                    | Q(creator=friend, member=request.user) & Q(room_type="private")
                )
                if exsisting_room.exists():
                    room = exsisting_room.first()
                    return Response(
                        {
                            "room_id": room.unique_id,
                            "friend": {
                                "id": friend.id,
                                "full_name": friend.full_name,
                                "profile_picture": friend.profile_picture.url
                                if friend.profile_picture
                                else None,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    room = models.Room.objects.create(
                        creator=request.user, room_type="private"
                    )
                    room.member.add(friend, request.user)
                    room.save()
                    return Response(
                        {
                            "room_id": room.unique_id,
                            "friend": {
                                "id": friend.id,
                                "full_name": friend.full_name,
                                "profile_picture": friend.profile_picture.url
                                if friend.profile_picture
                                else None,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {
                    "message": "No User found! Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "No User found! Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class InboxRoomView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        messages = models.Message.objects.filter(
            Q(room__creator=request.user) | Q(room__member=request.user)
        )
        messages = (
            messages.values("room")
            .annotate(last_message=Max("created_at"))
            .order_by("-last_message")
        )
        if messages is not None:
            rooms = []
            for message in messages:
                room = models.Room.objects.get(id=message["room"])
                for member in room.member.all().exclude(id=request.user.id):
                    member = member
                last_message = (
                    models.Message.objects.filter(room=room)
                    .order_by("-created_at")
                    .first()
                )
                if room.room_type == "private":
                    data = {
                        "message": {
                            "sender": {
                                "id": member.id,
                                "full_name": member.full_name,
                                "profile_picture": member.profile_picture.url
                                if member.profile_picture
                                else None,
                            },
                            "room": {
                                "unique_id": room.unique_id,
                                "room_type": room.room_type,
                                "room_name": room.groups.first().room_name
                                if room.groups.first()
                                else None,
                                "room_picture": room.groups.first().room_picture.url
                                if room.groups.first()
                                else None,
                            },
                            "sender_id": last_message.user.id,
                            "content": last_message.content,
                            "is_read": last_message.is_read,
                            "created_at": last_message.created_at.strftime(
                                "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                        }
                    }
                else:
                    data = {
                        "message": {
                            "sender": {
                                "id": last_message.user.id,
                                "full_name": last_message.user.full_name,
                                "profile_picture": last_message.user.profile_picture.url if last_message.user.profile_picture else None,
                            },  
                            "room": {
                                "unique_id": room.unique_id,
                                "room_type": room.room_type,
                                "room_name": room.groups.first().room_name
                                if room.groups.first()
                                else None,
                                "room_picture": room.groups.first().room_picture.url
                                if room.groups.first()
                                else None,
                            },
                            "sender_id": last_message.user.id,
                            "content": last_message.content,
                            "is_read": last_message.is_read,
                            "created_at": last_message.created_at.strftime(
                                "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                        }
                    }

                rooms.append(data)
            return Response(rooms, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_400_BAD_REQUEST)
