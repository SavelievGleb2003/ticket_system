from django.db import models

# Create your models here.
# chat/models.py

from django.db import models
from django.conf import settings
from tickets.models import Ticket  # импортируем тикет
from account.models import CustomUser

class Chat(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="chat"
    )
    participants = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for Ticket #{self.ticket.id}"

class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
