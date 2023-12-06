from friends.models import Contacts
from django.db.models import Q
import json

def is_post_creator_friend(requested_user : int, post_creator : int):
    try:
        friend_obj = Contacts.objects.get(
            Q(user=requested_user)
        )
        data = friend_obj.contacts
        # search the user id in the contacts
        for user in data:
            if user['id'] == post_creator:
                return True
        return False

    except Exception as e:
        return False
    