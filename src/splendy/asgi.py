"""
ASGI config for Splendy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "splendy.settings.prod")
django.setup()
#
from channels.routing import ProtocolTypeRouter, URLRouter
from splendy.asgi_auth import TokenAuthMiddlewareStack
from django.conf import settings

if settings.DEBUG:
    from django.core.asgi import get_asgi_application
import splendy.routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application() if settings.DEBUG else None,
        "websocket": TokenAuthMiddlewareStack(
            URLRouter(splendy.routing.websocket_urlpatterns)
        ),
    }
)
