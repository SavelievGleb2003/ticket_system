import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import PermissionDenied
from chat.models import Chat, ChatMessage
from tickets.models import Ticket
from account.models import CustomUser
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from tickets.models import Ticket

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.ticket_id = self.scope["url_route"]["kwargs"]["ticket_id"]

        # Проверяем, существует ли тикет
        ticket_exists = await self.check_ticket_exists(self.ticket_id)
        if not ticket_exists:
            await self.close()
            return

        # Проверяем, может ли пользователь участвовать в чате
        has_access = await self.check_user_accepted_by()
        if not has_access:
            await self.close()
            return

        self.room_group_name = f"chat_{self.ticket_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        # Сохранение сообщения в базе данных
        chat_message = await self.create_chat_message(message)
        response = {
            "sender": chat_message.sender.username,
            "message": chat_message.message,
            "timestamp": chat_message.timestamp.isoformat(),
        }

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_message", "message": response}
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    @database_sync_to_async
    def check_user_accepted_by(self):
        """Проверяет, имеет ли пользователь доступ к чату."""
        try:
            ticket = Ticket.objects.get(id=self.ticket_id)
            return self.user == ticket.created_by or self.user == ticket.accepted_by
        except Ticket.DoesNotExist:
            return False

    @database_sync_to_async
    def create_chat_message(self, message):
        """Создаёт сообщение в базе данных."""
        chat, _ = Chat.objects.get_or_create(ticket_id=self.ticket_id)
        return ChatMessage.objects.create(chat=chat, sender=self.user, message=message)

    @database_sync_to_async
    def check_ticket_exists(self, ticket_id):
        """Проверяет, существует ли тикет."""
        return Ticket.objects.filter(id=ticket_id).exists()