from django.contrib import admin
from . import models

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','content', 'room', 'created_at']
    search_fields = ['user__full_name', 'room__unique_id']
    list_filter = ['created_at']

admin.site.register(models.MessageAttachment)
admin.site.register(models.Room)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.PublicGroupInfo)


