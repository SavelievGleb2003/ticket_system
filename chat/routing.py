from django.urls import path
from chat.consumers import ChatConsumer
from tickets.consumers import TicketConsumer

wsPattern = [
    path("ws/chat/<int:ticket_id>/", ChatConsumer.as_asgi()),
    path("ws/tickets/", TicketConsumer.as_asgi()),
]