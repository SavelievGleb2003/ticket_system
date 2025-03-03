
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chat.models import Chat  # импорт модели чата
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.utils import timezone
from chat.models import Chat
from django.db.models import Q
@login_required
def ticket_list(request):
    user = request.user  # Получаем текущего пользователя
    chat_id = None  # Объявляем заранее
    if user.is_authenticated:
        tickets = Ticket.objects.filter(
            department=user.department,
            position=user.position
        )

        chat = Chat.objects.filter(
            Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
        ).first()

        chat_id = chat.ticket.id if chat else None
    else:
        tickets = Ticket.objects.none()
    print(f'Передаем chat_id: {chat_id}')  # Для проверки
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
    })

@login_required
def ticket_list_created_by(request):
    user = request.user  # Получаем текущего пользователя

    if user.is_authenticated:  # Проверяем, авторизован ли пользователь
        tickets = Ticket.objects.filter(
            created_by=request.user
        )
        chat = Chat.objects.filter(
            Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
        ).first()

        chat_id = chat.ticket.id if chat else None
    else:
        tickets = Ticket.objects.none()
    print(f'Передаем chat_id: {chat_id}')  # Для проверки
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
    })


@login_required
def ticket_list_accepted_by(request):
    user = request.user  # Получаем текущего пользователя

    if user.is_authenticated:  # Проверяем, авторизован ли пользователь
        tickets = Ticket.objects.filter(
            accepted_by=request.user
        )
        chat = Chat.objects.filter(
            Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
        ).first()

        chat_id = chat.ticket.id if chat else None
    else:
        tickets = Ticket.objects.none()
    print(f'Передаем chat_id: {chat_id}')  # Для проверки
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('tickets:ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})



@login_required
def accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status != 'open':
        messages.error(request, "Эта задача уже занята или завершена.")
        return redirect('tickets:ticket_list')

    if ticket.department != request.user.department or ticket.position != request.user.position:
        messages.error(request, "У вас нет прав на принятие этой задачи.")
        raise PermissionDenied("Вы не можете принять эту задачу.")

    # Назначаем задачу текущему пользователю и обновляем статус
    ticket.accepted_by = request.user
    ticket.accepted_at = timezone.now()
    ticket.status = 'in_progress'
    ticket.save()

    # Создаем чат для тикета, если его еще нет
    chat, created = Chat.objects.get_or_create(ticket=ticket)
    if created:
        chat.participants.add(ticket.created_by, request.user)
        chat.save()

    messages.success(request, "Задача успешно принята в работу!")
    return redirect('tickets:ticket_detail', ticket_id=ticket.id)

# tickets/views.py
@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Здесь можно добавить проверки прав, например, только администратор или тот, кто принял задачу, может закрыть тикет
    if  ticket.status != 'in_progress':
        messages.error(request, "Эту задачу невозможно завершить, поскольку она либо не была принята в работу, либо уже завершена.")
        return redirect('tickets:ticket_list')

    if ticket.department != request.user.department or ticket.position != request.user.position or ticket.accepted_by != request.user:
        messages.error(request, "У вас нет прав на завершения этой задачи.")
        raise PermissionDenied("Вы не можете завершеть эту задачу.")

    ticket.status = 'closed'
    ticket.save()

    # Удаляем связанный чат, если он существует
    if hasattr(ticket, 'chat'):
        ticket.chat.delete()

    messages.success(request, "Задача успешно закрыта, чат удален.")
    return redirect('tickets:ticket_detail', ticket_id=ticket.id)
