# Generated by Django 5.0.4 on 2025-03-06 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_ticket_screenshot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='screenshot',
        ),
        migrations.AddField(
            model_name='ticket',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='tickets/'),
        ),
    ]
