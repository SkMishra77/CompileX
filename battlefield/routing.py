from django.urls import path

from battlefield.consumer import *

ws_urlpatterns = [
    path('battle/code_execute/<str:room_id>/', BattleCodeExecuterSocketConsumer.as_asgi()),
]
