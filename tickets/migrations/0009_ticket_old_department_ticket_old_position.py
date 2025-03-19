# Generated by Django 5.0.4 on 2025-03-19 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('tickets', '0008_ticket_closed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='old_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='old_department', to='account.department'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='old_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='old_position', to='account.position'),
        ),
    ]
