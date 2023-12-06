from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.

User = get_user_model()

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('phone_number','full_name')
    list_filter = ('email', 'phone_number', 'is_active',)
    ordering = ('id',)
    list_display = ('__str__', 'email', 'username', 'is_active', 'verified', 'phone_number', 'is_online', 'last_online')
    fieldsets = (
        (None, {'fields': (
            'full_name',
            'email',
            'username',
            'phone_number',
            'profile_picture',
            'cover_photo',
            'password',
            )}),
        ('Permissions',
         {
             'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'verified',
                'is_online',
                'groups',
                'user_permissions'
             )
         }),
    )

    # fieldsets to add a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'full_name',
                'email',
                'phone_number',
                'profile_picture',
                'cover_photo',
                'password1',
                'is_active',
                'password2',
                'is_staff',
                'groups',
                'user_permissions'
                )}
         ),
    )


admin.site.register(User, UserAdminConfig)

from .models import Otp
admin.site.register(Otp)