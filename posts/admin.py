from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'privacy', 'created_at', 'updated_at')
    search_fields = ('user__phone_number', 'title')
    list_filter = ('created_at', 'updated_at')

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PostAttachments)
admin.site.register(models.Reaction)
admin.site.register(models.Comment)