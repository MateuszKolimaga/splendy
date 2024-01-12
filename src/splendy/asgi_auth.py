from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.db import database_sync_to_async

from users.models import CustomUser


@database_sync_to_async
def get_user(token):
    try:
        user_id = Token.objects.get(key=token).user_id
        return CustomUser.objects.get(id=user_id)
    except (Token.DoesNotExist, CustomUser.DoesNotExist):
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_params = scope["query_string"].decode()
        token = query_params.split("=")[1] if "token" in query_params else None
        if token:
            scope["user"] = await get_user(token)
            close_old_connections()
        else:
            scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
