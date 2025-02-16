
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

@login_required
def ticket_list(request):
    user = request.user  # Получаем текущего пользователя

    if user.is_authenticated:  # Проверяем, авторизован ли пользователь
        tickets = Ticket.objects.filter(
            department=user.department,
            position=user.position
        )
    else:
        tickets = Ticket.objects.none()  # Если пользователь не авторизован, не показываем тикеты

    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


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
    # Получаем задачу по ID
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Проверяем, может ли пользователь принять задачу
    if ticket.status != 'open':
        messages.error(request, "Эта задача уже занята или завершена.")
        return redirect('tickets:ticket_list')

    if ticket.department != request.user.department or ticket.position != request.user.position:
        messages.error(request, "У вас нет прав на принятие этой задачи.")
        raise PermissionDenied("Вы не можете принять эту задачу.")

    # Назначаем задачу текущему пользователю и обновляем статус
    ticket.accepted_by = request.user
    ticket.status = 'in_progress'
    ticket.save()

    messages.success(request, "Задача успешно принята в работу!")
    return redirect('tickets:ticket_detail', ticket_id=ticket.id)