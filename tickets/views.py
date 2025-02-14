
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
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
