"""
ASGI config for btalk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btalk.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from middlewares.middleware import TokenAuthMiddleware
from chat.routing import ws_pattern

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            ws_pattern
        )
    )
})
