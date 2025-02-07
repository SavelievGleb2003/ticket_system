from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

import os

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=TurnoverDocument.Status.PUBLISHED)
        )

class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.APPROVED)


class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.REJECTED)


class UnderReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.UNDER_REVIEW)


class document_types(models.Model):
    type_name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.type_name


class Department(models.Model):
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)


class TurnoverDocument(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        UNDER_REVIEW = 'UR', 'Under Review'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'
        PUBLISHED = 'PB', 'Published'

    # Менеджеры
    objects = models.Manager()
    published = PublishedManager()
    under_review = UnderReviewManager
    approved = ApprovedManager
    rejected = RejectedManager

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    publish_by = models.DateTimeField(default=timezone.now)
    document_type = models.ForeignKey(document_types, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='blog/static/images/')
    slug = models.SlugField(max_length=250, unique_for_date='publish_by')
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )


    class Meta:
        ordering = ['-publish_by']
        indexes = [models.Index(fields=['-publish_by'])]

    def filename(self):
        return 'images/' + os.path.basename(self.document_file.name)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('TD:TD_detail', args=[self.publish_by.year, self.publish_by.month, self.publish_by.day, self.slug])







class Comment(models.Model):
    document = models.ForeignKey(TurnoverDocument, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering=['created_at']
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f'comment by {self.name} on {self.document}'