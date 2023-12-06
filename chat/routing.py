from django.urls import path
from chat.consumers import chat_consumers, inbox_consumer
from chat.consumers import inbox_consumer
from posts.consumers import notification_consumers

ws_pattern = [
    path("ws/chat/<str:room_id>/", chat_consumers.ChatConsumer.as_asgi()),
    path("ws/inbox/", inbox_consumer.InboxConsumer.as_asgi()),
    path("ws/notification/", notification_consumers.NotificationConsumer.as_asgi()),
    path("ws/inbox/", inbox_consumer.InboxConsumer.as_asgi()),
]
