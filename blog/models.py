from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

import os

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=TurnoverDocument.Status.PUBLISHED)
        )





class document_types(models.Model):
    type_name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.type_name


class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subfolders"
    )

    def __str__(self):
        return self.name


class TurnoverDocument(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # Менеджеры
    objects = models.Manager()
    published = PublishedManager()

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
    tags = TaggableManager()

    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")

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