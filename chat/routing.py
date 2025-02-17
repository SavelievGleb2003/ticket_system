from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer


wsPattern = [path("ws/chat/<int:ticket_id>/", ChatConsumer.as_asgi())]
