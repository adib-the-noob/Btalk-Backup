from django.contrib import admin
from .models import (
    UserLocation, 
    Contacts,
    FriendRequest,
) 
# Register your models here.
admin.site.register(Contacts)
admin.site.register(FriendRequest)
admin.site.register(UserLocation)
