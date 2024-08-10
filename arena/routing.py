from django.urls import path

from arena.consumer import *

ws_urlpatterns = [
    path('arena/code_execute', ArenaCodeExecuterSocketConsumer.as_asgi()),
]
