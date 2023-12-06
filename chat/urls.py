from django.urls import path

from .group_chats import group_chat_views

from .message_attachments import messages_views
from . import views
from .calling import call_views

urlpatterns = [
    path('friends-search/', views.FriendsSearchAPIView.as_view(), name='friends-search'),
    path('inbox-profile/<int:friendId>/', views.InboxProfileAPIView.as_view(), name='inbox-profile'),
    path('fetch-inbox/', views.InboxRoomView.as_view(), name='fetch-inbox'),
    path('load-previous-message/', views.PreviousMessageAPIView.as_view(), name='previous-message'),

    # calling
    path('call-notification/', call_views.get_receiver_fcm),

    # group chat
    path('create-group/', group_chat_views.create_group, name='group-chat'),
    path('get-all-groups/', group_chat_views.get_all_groups, name='get-all-groups'),
    path('search-groups/', group_chat_views.search_groups, name='search-groups'),

    # One to one chat
    path('send-attachment/', messages_views.send_attachement, name='send-message'),
]