from django.contrib import admin
from .models import Chat, ChatMessage
# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'created_at', 'is_active']



@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender','message', 'timestamp']