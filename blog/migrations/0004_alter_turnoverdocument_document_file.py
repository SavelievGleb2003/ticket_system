# Generated by Django 5.0.4 on 2025-02-24 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_turnoverdocument_status_folder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnoverdocument',
            name='document_file',
            field=models.FileField(blank=True, null=True, upload_to='blog/static/images/'),
        ),
    ]
