from django.db import models
import os
# Create your models here.

from django.db import models
from account.models import CustomUser


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
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    screenshot = models.ImageField(upload_to='blog/static/screenshot/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filename(self):
        return 'screenshot/' + os.path.basename(self.screenshot.name)

    def __str__(self):
        return self.title
