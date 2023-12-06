import django

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

User = get_user_model()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    @database_sync_to_async
    def get_user(self, token):
        try:
            token_obj = Token.objects.get(key=token)
            user = User.objects.get(pk=token_obj.user_id)
            return user
        except (Token.DoesNotExist, User.DoesNotExist):
            return AnonymousUser()

    async def __call__(self, scope, receive, send):
        token = scope['query_string'].decode().split('=')[1]
        scope['user'] = await self.get_user(token)
        return await self.inner(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
