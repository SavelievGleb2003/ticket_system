from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatMessage
from tickets.models import Ticket
from django.http import HttpResponseForbidden
from django.db.models import Q

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
    chat = get_object_or_404(Chat, ticket=ticket)
    # Проходимся по тикетам и ищем "другого" участника чата


    # Retrieve all messages for the chat (ordered by timestamp)
    messages = ChatMessage.objects.filter(chat=chat).order_by('timestamp')
    chats = Chat.objects.filter(
        Q(ticket__accepted_by=request.user) | Q(ticket__created_by=request.user)
    )
    for ticket in chats:
        # Получаем чат
        other_user = ticket.participants.exclude(id=request.user.id).first()  # Исключаем текущего пользователя
        ticket.other_participant = other_user  # Добавляем в объект ticket

    return render(request, 'chat/chat_detail.html', {
        'ticket': ticket,
        'chat': chat,
        'messages': messages,  # pass messages to template
        'has_access': has_access,  # <-- передаем в шаблон
        'tickets': chats
    })