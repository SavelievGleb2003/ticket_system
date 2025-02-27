from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from account.models import CustomUser, Department, Position
import datetime
import pytz


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets_created')
    accepted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets_accepted', null=True,
                                    blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)

    screenshot = models.ImageField(upload_to='tickets/screenshots', null=True, blank=True)
    # due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        assigned_info = self.accepted_by.username if self.accepted_by else "Unassigned"
        department_info = self.department.name if self.department else "No Department"
        position_info = self.position.title if self.position else "No Position"
        return f"{self.title} - {department_info} ({position_info}) - {self.status} - {assigned_info}"


    def to_dict(self):
        """Преобразует объект тикета в словарь для передачи через WebSocket"""
        kiev_tz = pytz.timezone('Europe/Kiev')
        created_at_kiev = self.created_at.astimezone(kiev_tz)
        accepted_at_kiev = self.accepted_at.astimezone(kiev_tz) if self.accepted_at else None

        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'status_display': self.get_status_display(),
            'created_by': self.created_by.username,
            'created_at': created_at_kiev.strftime('%H:%M'),
            'accepted_by': self.accepted_by.username if self.accepted_by else None,
            'accepted_at': accepted_at_kiev.strftime('%H:%M') if self.accepted_at else None,
            'department': self.department.name if self.department else None,
            'position': self.position.title if self.position else None,
        }


@receiver(post_save, sender=Ticket)
def ticket_post_save(sender, instance, created, **kwargs):
    """Отправляет уведомления при создании или обновлении тикета"""
    channel_layer = get_channel_layer()
    ticket_data = instance.to_dict()

    # Если это новый тикет
    if created:
        # Отправляем уведомление всем пользователям с тем же департаментом и должностью
        if instance.department and instance.position:
            async_to_sync(channel_layer.group_send)(
                f"department_{instance.department.id}_{instance.position.id}",
                {
                    "type": "ticket_created",
                    "ticket": ticket_data
                }
            )

        # Отправляем создателю
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.created_by.id}",
            {
                "type": "ticket_created",
                "ticket": ticket_data
            }
        )

    # Если тикет был принят в работу
    elif instance.status == 'in_progress' and instance.accepted_by:
        # Уведомление создателю
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.created_by.id}",
            {
                "type": "ticket_accepted",
                "ticket": ticket_data
            }
        )

        # Уведомление принявшему
        async_to_sync(channel_layer.group_send)(
            f"accepted_{instance.accepted_by.id}",
            {
                "type": "ticket_accepted",
                "ticket": ticket_data
            }
        )

    # Если тикет был закрыт
    elif instance.status == 'closed':
        # Уведомление создателю
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.created_by.id}",
            {
                "type": "ticket_closed",
                "ticket": ticket_data
            }
        )

        # Уведомление принявшему
        if instance.accepted_by:
            async_to_sync(channel_layer.group_send)(
                f"accepted_{instance.accepted_by.id}",
                {
                    "type": "ticket_closed",
                    "ticket": ticket_data
                }
            )