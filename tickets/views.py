from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import BugTicket, FeatureTicket
from .forms import BugTicketForm, FeatureTicketForm
from .forms import MakePaymentForm
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
def tickets(request):
    bug_tickets = BugTicket.objects.all().order_by("created_date")
    feature_tickets = FeatureTicket.objects.all().order_by("created_date")
    return render(request, "tickets.html", {'bug_tickets': bug_tickets, 'feature_tickets': feature_tickets})
    
@login_required(login_url="/login/") 
def the_ticket(request, pk):
    try:
        feature_tk = FeatureTicket.objects.get(pk=pk)
    except FeatureTicket.DoesNotExist:
        feature_tk = None
        
    try:
        bug_tk = BugTicket.objects.get(pk=pk)
    except BugTicket.DoesNotExist:
        bug_tk = None
        
    if feature_tk == None:
        ticket = bug_tk
    elif bug_tk == None:
        ticket = feature_tk
    
    return render(request, "the-ticket.html", {'ticket': ticket})
    
def upvote(request, pk):
    try:
        feature_tk = FeatureTicket.objects.get(pk=pk)
    except FeatureTicket.DoesNotExist:
        feature_tk = None
        
    try:
        bug_tk = BugTicket.objects.get(pk=pk)
    except BugTicket.DoesNotExist:
        bug_tk = None
        
    if feature_tk == None:
        ticket = bug_tk
    elif bug_tk == None:
        ticket = feature_tk
    
    user = request.user
    
    if user.is_authenticated():
        if user in ticket.upvotes.all():
            ticket.upvotes.remove(user)
        else:
            ticket.upvotes.add(user)
    
    return redirect("the-ticket", pk=pk)
        

@login_required(login_url="/login/")    
def create_bug_ticket(request):
    if request.method == "POST":
        form = BugTicketForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(reverse('tickets'))
    else:
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

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        bug_tickets = BugTicket.objects.all().count()
        feature_tickets = FeatureTicket.objects.all().count()
        
        labels = ["Bugs", "Features"]
        tickets_qty = [bug_tickets, feature_tickets]
        
        data = {
            'labels': labels,
            'tickets_qty': tickets_qty
        }
        return Response(data)