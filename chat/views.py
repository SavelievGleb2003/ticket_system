from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatMessage
from tickets.models import Ticket
from django.http import HttpResponseForbidden

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                chat=chat,
                sender=request.user,
                message=message_text
            )
    return redirect('chats:chat_detail', ticket_id=chat.ticket.id)
# chat/views.py


def chat_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    has_access = request.user == ticket.created_by or request.user == ticket.accepted_by
    if not has_access:
        return HttpResponseForbidden("Доступ запрещен")

    chat, created = Chat.objects.get_or_create(ticket=ticket)

    return render(request, 'chat/chat_detail.html', {
        'ticket': ticket,
        'chat': chat,
        'has_access': has_access,  # <-- передаем в шаблон
    })