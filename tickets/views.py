
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chat.models import Chat  # импорт модели чата
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

from chat.models import Chat
from django.db.models import Q
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta


@login_required
def ticket_list(request):
    user = request.user
    chat_id = None
    tickets = Ticket.objects.filter(
        department=user.department,
        position=user.position
    )

    # Get the filter period from GET parameters (today, week, or month)
    time_filter = request.GET.get('time_filter', 'today')  # Default to 'today'

    # Filter tickets based on time period
    if time_filter == 'today':
        tickets = tickets.filter(created_at__date=timezone.now().date())
    elif time_filter == 'week':
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        tickets = tickets.filter(created_at__gte=start_of_week)
    elif time_filter == 'month':
        tickets = tickets.filter(created_at__year=timezone.now().year,
                                 created_at__month=timezone.now().month)

    # Retrieve chat info
    chat = Chat.objects.filter(
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
    ).first()

    chat_id = chat.ticket.id if chat else None

    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
    })


@login_required
def ticket_list_created_by(request):
    user = request.user
    time_filter = request.GET.get('time_filter', 'today')  # Default to 'today'
    tickets = Ticket.objects.filter(created_by=request.user)

    if time_filter == 'today':
        tickets = tickets.filter(created_at__date=timezone.now().date())
    elif time_filter == 'week':
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        tickets = tickets.filter(created_at__gte=start_of_week)
    elif time_filter == 'month':
        tickets = tickets.filter(created_at__year=timezone.now().year,
                                 created_at__month=timezone.now().month)

    chat = Chat.objects.filter(
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
    ).first()

    chat_id = chat.ticket.id if chat else None

    return render(request, 'tickets/my_created_ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
    })


@login_required
def ticket_list_accepted_by(request):
    user = request.user
    time_filter = request.GET.get('time_filter', 'today')  # Default to 'today'
    tickets = Ticket.objects.filter(accepted_by=request.user)

    if time_filter == 'today':
        tickets = tickets.filter(created_at__date=timezone.now().date())
    elif time_filter == 'week':
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        tickets = tickets.filter(created_at__gte=start_of_week)
    elif time_filter == 'month':
        tickets = tickets.filter(created_at__year=timezone.now().year,
                                 created_at__month=timezone.now().month)

    chat = Chat.objects.filter(
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user)
    ).first()

    chat_id = chat.ticket.id if chat else None

    return render(request, 'tickets/my_accepted_ticket_list.html', {
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
        form = TicketForm(request.POST, request.FILES)
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

    if ticket.department != request.user.department or ticket.position != request.user.position or ticket.created_by == request.user:
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
    if request.method == "POST":
        comment = request.POST.get("completion_comment")
        if not comment:
            messages.error(request, "Вы должны добавить комментарий перед закрытием задачи.")
            return redirect('tickets:ticket_detail', ticket_id=ticket.id)

    ticket.completion_comment = comment
    ticket.closed_at = timezone.now()
    ticket.status = 'closed'
    ticket.save()

    # Удаляем связанный чат, если он существует
    if hasattr(ticket, 'chat'):
        ticket.chat.delete()

    messages.success(request, "Задача успешно закрыта, чат удален.")
    return redirect('tickets:ticket_detail', ticket_id=ticket.id)



