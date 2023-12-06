from chat.models import Room
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

def get_roomid(requested_user, friends: list):
    # get all the rooms for the friends, if the room exists, return the room id else create a new room and return the room id
    rooms = []
    for friend in friends:
        existing_room = Room.objects.filter(
            Q(creator=requested_user, member=friend) | Q(creator=friend, member=requested_user) & Q(
                room_type='private'))
        if existing_room.exists():
            room = existing_room.first()
            rooms.append({
                'room_id': str(room.unique_id),
                'id': friend.id,
                'full_name': friend.full_name,
                'profile_picture': friend.profile_picture.url if friend.profile_picture else None
            })
        else:
            room = Room.objects.create(
                creator=requested_user, room_type='private')
            room.member.add(friend, requested_user)
            room.save()
            rooms.append({
                'room_id': str(room.unique_id),
                'id': friend.id,
                'full_name': friend.full_name,
                'profile_picture': friend.profile_picture.url if friend.profile_picture else None   
            })
    return rooms
