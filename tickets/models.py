from django.db import models
import os
# Create your models here.

from django.db import models
from account.models import CustomUser, Department, Position


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
    accepted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets_accepted', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)


    screenshot = models.ImageField(upload_to='blog/static/screenshot/', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        assigned_info = self.assigned_to.username if self.assigned_to else "Unassigned"
        department_info = self.department.name if self.department else "No Department"
        position_info = self.position.title if self.position else "No Position"
        return f"{self.title} - {department_info} ({position_info}) - {self.status} - {assigned_info}"
