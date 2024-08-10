from django.urls import path

from executer.consumer import *

ws_urlpatterns = [
    path('pg/code_execute', PlayGroundCodeExecuterSocketConsumer.as_asgi()),
]
