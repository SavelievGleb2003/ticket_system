from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.models import Department

# Create your models here.

class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
