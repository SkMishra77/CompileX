"""
ASGI config for CompileX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import arena.routing as arena_routing
import executer.routing as executer_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CompileX.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        executer_routing.ws_urlpatterns +
        arena_routing.ws_urlpatterns
    )
})
