from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import CreateTicket

# Create your views here.
def tickets(request):
    tickets = Ticket.objects.all().order_by("created_date")
    return render(request, "tickets.html", {'tickets': tickets})

@login_required(login_url="/login/")    
def create_ticket(request):
    if request.method == "POST":
        form = CreateTicket(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(reverse('tickets'))
    else:
        form = CreateTicket()
    return render(request, "create-ticket.html", {'form': form})
    
@login_required(login_url="/login/")
def create_feature(request):
    form = CreateTicket()
    return render(request, "create-feature.html", {'form': form})