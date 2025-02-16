from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatMessage
from tickets.models import Ticket

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
    chat = getattr(ticket, 'chat', None)
    if not chat:
        # Если чат ещё не создан, можно его создать или показать сообщение об отсутствии чата.
        # Например:
        chat = None
    return render(request, 'chat/chat_detail.html', {'ticket': ticket, 'chat': chat})
