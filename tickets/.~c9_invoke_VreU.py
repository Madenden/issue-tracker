from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket
fo

# Create your views here.
def tickets(request):
    tickets = Ticket.objects.all().order_by("created_date")
    return render(request, "tickets.html", {'tickets': tickets})

@login_required(login_url="/login/")    
def create_ticket(request):
    return render(request, "create-ticket.html")