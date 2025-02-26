import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


User = get_user_model()


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        # Отклоняем анонимных пользователей
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # Загружаем пользователя с department и position
        self.user = await self.get_user(self.user.id)

        if self.user and self.user.department and self.user.position:
            self.department_group_name = f"department_{self.user.department.id}_{self.user.position.id}"
            await self.channel_layer.group_add(self.department_group_name, self.channel_name)

        self.user_group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        self.accepted_group_name = f"accepted_{self.user.id}"
        await self.channel_layer.group_add(self.accepted_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'department_group_name'):
            await self.channel_layer.group_discard(self.department_group_name, self.channel_name)

        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

        if hasattr(self, 'accepted_group_name'):
            await self.channel_layer.group_discard(self.accepted_group_name, self.channel_name)

    async def ticket_created(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ticket_created',
            'ticket': event['ticket']
        }))

    async def ticket_accepted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ticket_accepted',
            'ticket': event['ticket']
        }))

    async def ticket_closed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ticket_closed',
            'ticket': event['ticket']
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.select_related('department', 'position').filter(id=user_id).first()
