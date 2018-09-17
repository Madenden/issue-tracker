from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Ticket, FeatureTicket
from .forms import TicketForm, FeatureTicketForm
from .forms import MakePaymentForm
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
def tickets(request):
    issue_tickets = Ticket.objects.all().order_by("created_at")
    
    paginator = Paginator(issue_tickets, 3)
    page = request.GET.get('page', 1)
    
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    
    
    return render(request, "tickets.html", {'issue_tickets': tickets})
    
@login_required(login_url="/login/") 
def the_ticket(request, pk):
    
    try:
        feature_tk = FeatureTicket.objects.get(pk=pk)
    except FeatureTicket.DoesNotExist:
        feature_tk = None
        
    try:
        bug_tk = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        bug_tk = None
        
    if feature_tk == None:
        ticket = bug_tk
        return render(request, "the-ticket.html", {'ticket': ticket})
    elif bug_tk == None:
        ticket = feature_tk
        return render(request, "the-ticket.html", {'ticket': ticket})
    
def upvote(request, pk):
    try:
        feature_tk = FeatureTicket.objects.get(pk=pk)
    except FeatureTicket.DoesNotExist:
        feature_tk = None
        
    try:
        bug_tk = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
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
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        
        if form['issue_status'].value() == 'feature' and form.is_valid():
            feature_issue = form
            
            return redirect(reverse('payment'))
            
        elif form.is_valid():
            bug_issue = form.save(commit=False)
            bug_issue.author = request.user
            bug_issue.save()
            
            return redirect(reverse('tickets'))
    else:
        form = TicketForm()
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
    
@login_required(login_url="/login/")
def payment(request):
    if request.method == "POST":
        payment_form = MakePaymentForm(request.POST)
        if payment_form.is_valid():
            try:
                transaction = stripe.Charge.create(
                    amount = int(payment_form['amount'].value()),
                    currency = "EUR",
                    description = "Issue Ticket",
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
        payment_form = MakePaymentForm()
    
    return render(request, "payment.html", {'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})

def graphs(request):
    return render(request, "graphs.html")


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        bug_tickets = Ticket.objects.all().count()
        feature_tickets = FeatureTicket.objects.all().count()
        
        labels = ["Bugs", "Features"]
        tickets_qty = [bug_tickets, feature_tickets]
        
        data = {
            'labels': labels,
            'tickets_qty': tickets_qty
        }
        return Response(data)