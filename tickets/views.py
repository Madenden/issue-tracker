from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import BugTicket
from .forms import BugTicketForm, FeatureTicketForm
from .forms import MakePaymentForm
from django.contrib import messages
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
def tickets(request):
    tickets = BugTicket.objects.all().order_by("created_date")
    return render(request, "tickets.html", {'tickets': tickets})

@login_required(login_url="/login/")    
def create_ticket(request):
    if request.method == "POST":
        form = BugTicketForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(reverse('tickets'))
        form = BugTicketForm()
    return render(request, "create-ticket.html", {'form': form})
    
@login_required(login_url="/login/")
def create_feature(request):
    if request.method=="POST":
        feature_ticket_form = FeatureTicketForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if feature_ticket_form.is_valid() and payment_form.is_valid():
            feature_ticket = feature_ticket_form.save(commit=False)
            feature_ticket.author = request.user
            feature_ticket.save()
            
            try:
                transaction = stripe.Charge.create(
                    amount = int(feature_ticket.amount*100),
                    currency = "EUR",
                    description = "Feature Ticket",
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                
            if transaction.paid:
                messages.error(request, "You have successfully paid")
                return redirect(reverse('tickets'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        feature_ticket_form = FeatureTicketForm()
        payment_form = MakePaymentForm()
    return render(request, "create-feature.html", {'form': feature_ticket_form, 'payment_form': payment_form,  'publishable': settings.STRIPE_PUBLISHABLE})