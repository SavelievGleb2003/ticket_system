from django.contrib import admin
from .models import Ticket
# Register your models here.
@admin.register(Ticket)
class TurnoverDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','description', 'created_by',
                    'assigned_to','screenshot',
                    'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'created_by', 'updated_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['created_by']
    ordering = ['status', 'created_at', 'updated_at']