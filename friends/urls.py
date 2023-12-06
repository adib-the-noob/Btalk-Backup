from django.urls import path
from . import views

urlpatterns = [
    path('sync-contacts/', views.add_friend_by_sync, name='add_friend_by_sync'),
    path('get-all-friends/', views.get_friends, name='get_friends'),
]