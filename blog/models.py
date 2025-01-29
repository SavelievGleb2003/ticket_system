from django.db import models
from django.conf import settings
from django.utils import timezone
import os

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=TurnoverDocument.Status.PUBLISHED)
        )

class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.Approved)


class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.Rejected)


class UnderReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TurnoverDocument.Status.UnderReview)


class document_types(models.Model):
    type_name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.type_name


class TurnoverDocument(models.Model):

    objects = models.Manager()
    published = PublishedManager()
    UnderReview = UnderReviewManager()
    Approved = ApprovedManager()
    Rejected = RejectedManager()

    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        UnderReview = ('UR', 'UnderReview')
        Approved = ('A', 'Approved')
        Rejected = ('R', 'Rejected')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auther = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_post')
    department = models.CharField(max_length=255) #?????????
    publish = models.DateTimeField(default=timezone.now)
    document_type = models.ForeignKey(document_types, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='turnover_documents/')
    slug = models.SlugField(max_length=250)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def filename(self):
        return os.path.basename(self.document_file.name)

    def __str__(self):
        return self.title
