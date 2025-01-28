# Generated by Django 5.0.4 on 2025-01-28 17:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='document_types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TurnoverDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.CharField(max_length=255)),
                ('document_file', models.FileField(upload_to='turnover_documents/')),
                ('slug', models.SlugField(max_length=250)),
                ('status', models.CharField(choices=[('DF', 'Draft'), ('UR', 'UnderReview'), ('A', 'Approved'), ('R', 'Rejected')], default='DF', max_length=2)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_post', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.document_types')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['-created_at'], name='blog_turnov_created_bd7545_idx')],
            },
        ),
    ]
