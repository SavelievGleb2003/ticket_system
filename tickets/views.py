
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chat.models import Chat  # импорт модели чата
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm, TicketRedirectForm, TicketCloneForm
from account.models import CustomUser
from chat.models import Chat
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user), is_active=True
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
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user), is_active=True
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
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user), is_active=True
    ).first()

    chat_id = chat.ticket.id if chat else None

    return render(request, 'tickets/my_accepted_ticket_list.html', {
        'tickets': tickets,
        'chat_id': chat_id
    })


@login_required
def ticket_list_for_boss(request):
    user = request.user
    chat_id = None
    tickets = Ticket.objects.filter(
        Q(status="closed") | Q(status="in_progress"),
        department=user.department
    )
    users = CustomUser.objects.filter(department=user.department).exclude(id=user.department.boss.id)

    # Get the filter period from GET parameters (today, week, or month)
    time_filter_user = request.GET.get('time_filter_user', 'today')  # Default to 'today'

    # Filter tickets based on time period
    if time_filter_user == 'today':
        tickets = tickets.filter(created_at__date=timezone.now().date())
    elif time_filter_user == 'week':
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        tickets = tickets.filter(created_at__gte=start_of_week)
    elif time_filter_user == 'month':
        tickets = tickets.filter(created_at__year=timezone.now().year,
                                 created_at__month=timezone.now().month)

    specific_user = request.GET.get('specific_user', '')
    if specific_user:
        try:
            specific_user = int(specific_user)  # Convert to an integer
            tickets = tickets.filter(accepted_by=specific_user)
        except ValueError:
            pass  # If conversion fails, do nothing (avoid crashing)

    specific_status = request.GET.get('specific_status', '')
    if specific_status:
        tickets = tickets.filter(status=specific_status)

    # Retrieve chat info
    chat = Chat.objects.filter(
        Q(ticket__accepted_by=user) | Q(ticket__created_by=user), is_active=True
    ).first()

    chat_id = chat.ticket.id if chat else None

    return render(request, 'tickets/ticket_list_for_boss.html', {
        'tickets': tickets,
        'users': users,
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

    # Делаем чат неактивным, а не удаляем его
    if hasattr(ticket, 'chat'):
        ticket.chat.is_active = False
        ticket.chat.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{ticket.id}",
            {
                "type": "chat_closed",
                "ticket_id": ticket.id
            }
        )

    messages.success(request, "Задача успешно закрыта, чат удален.")
    return redirect('tickets:ticket_detail', ticket_id=ticket.id)



@login_required
def redirect_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status == 'in_progress' or ticket.status == 'closed':
        messages.error(request, "Тикет нельзя перенаправить, так как он в процессе выполнения или уже выполнен.")
        return redirect('tickets:ticket_list')

    if ticket.accepted_by == request.user or ticket.accepted_at is not None:
         messages.error(request, "Вы не можете перенаправить этот тикет, так как он уже был принят вами.")
         return redirect('tickets:ticket_list')

    if ticket.department != request.user.department or ticket.position != request.user.position:
        messages.error(request, "Вы не можете перенаправить этот тикет, так как он предназначен не для вашего отдела или позиции .")
        return redirect('tickets:ticket_list')

    if request.method == 'POST':
        ticket.old_position = ticket.position
        ticket.old_department = ticket.department
        form = TicketRedirectForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Очищаем текущее назначение, чтобы новый исполнитель мог принять тикет
            ticket.status = 'open'
            ticket.save()

            messages.success(request, "Задача успешно перенаправлена, теперь ее может принять другой сотрудник.")
            return redirect('tickets:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketRedirectForm(instance=ticket)

    return render(request, 'tickets/redirect_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def clone_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status != 'in_progress':
        messages.error(request, "Тикет нельзя клонировать, так как он не в процессе выполнения или уже выполнен.")
        return redirect('tickets:ticket_list')

    if ticket.accepted_by != request.user or ticket.accepted_at is None:
         messages.error(request, "Вы не можете клонировать этот тикет, так как он уже не был принят вами.")
         return redirect('tickets:ticket_list')

    if ticket.department != request.user.department or ticket.position != request.user.position:
        messages.error(request, "Вы не можете клонировать этот тикет, так как он предназначен не для вашего отдела или позиции .")
        return redirect('tickets:ticket_list')

    if request.method == 'POST':
        ticket.old_position = None
        ticket.old_department = None
        form = TicketCloneForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Очищаем текущее назначение, чтобы новый исполнитель мог принять тикет
            ticket.accepted_at = None
            ticket.accepted_by = None
            ticket.status = 'open'
            ticket.save()

            messages.success(request, "Задача успешно клонировать, теперь ее может принять другой сотрудник.")
            return redirect('tickets:ticket_detail', ticket_id=ticket_id)
    else:
        form = TicketCloneForm(instance=ticket)

    return render(request, 'tickets/clone_ticket.html', {'form': form, 'ticket': ticket})



@login_required
def tickets_analytics_for_the_department(request):
    user = request.user
    tickets = Ticket.objects.filter(
        department=user.department
    )

    users = CustomUser.objects.filter(department=user.department).exclude(id=user.department.boss.id)
    # Get the filter period from GET parameters (today, week, or month)
    time_filter = request.GET.get('time_filter', 'today')  # Default to 'today'
    labels = [user.username for user in users]  # Extract usernames


    # Filter tickets based on time period
    if time_filter == 'today':
        tickets = tickets.filter(created_at__date=timezone.now().date())
        closed_tickets = [Ticket.objects.filter(accepted_by=u, status="closed", created_at__date=timezone.now().date()).count() for u in users]
        in_progress_tickets = [Ticket.objects.filter(accepted_by=u, status="in_progress", created_at__date=timezone.now().date()).count() for u in users]
    elif time_filter == 'week':
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        tickets = tickets.filter(created_at__gte=start_of_week)
        closed_tickets = [
            Ticket.objects.filter(accepted_by=u, status="closed", created_at__gte=start_of_week).count() for u in users]
        in_progress_tickets = [
            Ticket.objects.filter(accepted_by=u, status="in_progress", created_at__gte=start_of_week).count() for u in users]
    elif time_filter == 'month':
        tickets = tickets.filter(created_at__year=timezone.now().year, created_at__month=timezone.now().month)
        closed_tickets = [
            Ticket.objects.filter(accepted_by=u, status="closed", created_at__year=timezone.now().year, created_at__month=timezone.now().month).count() for u in users]
        in_progress_tickets = [
            Ticket.objects.filter(accepted_by=u, status="in_progress", created_at__year=timezone.now().year, created_at__month=timezone.now().month).count() for u in
            users]

    ticket_counts = {
        "closed": tickets.filter(status="closed").count(),
        "in_progress": tickets.filter(status="in_progress").count(),
        "open": tickets.filter(status="open").count(),
    }

    position_counts = {
        user.position.title: tickets.filter(position=user.position).count()
        for user in users
    }

    return render(request, 'data_analytics/data_analytics_for_the_department.html', {
        'tickets': tickets,
        'users': users,
        "ticket_counts": ticket_counts,
        "position_counts": position_counts,
        'labels': labels,
        'closed_tickets': closed_tickets,
        'in_progress_tickets': in_progress_tickets

    })