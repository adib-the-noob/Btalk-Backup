from posts.consumers import notification_consumers
from django.urls import path

ws_pattern = [
    path("ws/notification/", notification_consumers.NotificationConsumer.as_asgi()),
]
