from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Ticket
from .forms import TicketForm, MakePaymentForm, CommentForm
import stripe, datetime, calendar, re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView
import json
from django.http import HttpResponse
from dateutil.relativedelta import *
from django.db.models import Count

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
    
    
    return render(request, "tickets.html", {'issue_tickets': tickets, 'test': the_ticket})
    
@login_required(login_url="/login/") 
def the_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
        
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.ticket = ticket
            comment.save()
            return redirect('the-ticket', pk=ticket.pk)
    else:
        form = CommentForm()
        
    return render(request, "the-ticket.html", {'ticket': ticket, 'form': form})

def upvote(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    user = request.user
    
    if user.is_authenticated():
        if user in ticket.upvotes.all():
            ticket.upvotes.remove(user)
        else:
            if ticket.issue_status.lower() == 'feature':
                request.session['upvote_ticket_pk'] = pk
                messages.warning(request, "To upvote the feature ticket, you have to pay a minimum amount of your choice.")
                return redirect("payment")
            ticket.upvotes.add(user)
    
    return redirect("the-ticket", pk=pk)
        
@login_required(login_url="/login/")    
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form['issue_status'].value() == 'feature' and form.is_valid():
            # request.session['fn'] = form.cleaned_data
            feature_issue = form.save(commit=False)
            feature_issue.author = request.user
            feature_issue.save()
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
def payment(request):
    if request.method == "POST":
        payment_form = MakePaymentForm(request.POST)
        if payment_form.is_valid():
            try:
                transaction = stripe.Charge.create(
                    amount = 2000,
                    currency = "EUR",
                    description = "Issue Ticket",
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                
            if transaction.paid:
                if request.session.get('upvote_ticket_pk', None):
                    pk = request.session['upvote_ticket_pk']
                    user = request.user
                    ticket = Ticket.objects.get(pk=pk)
                    ticket.upvotes.add(user)
                    del request.session['upvote_ticket_pk']
                
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
        bug_tickets_qty = Ticket.objects.filter(issue_status='bug')
        feature_ticket_qty = Ticket.objects.filter(issue_status='feature')
        
        labels = ["Bugs", "Features"]
        
        data = {
            'labels': labels,
            'days': self.last_week_dates_name(),
            'months': self.months_of_the_year(),
            'bug_tickets_qty': self.tickets_qty_by_type(bug_tickets_qty),
            'feature_ticket_qty': self.tickets_qty_by_type(feature_ticket_qty),
            'bugs_per_week': self.tickets_per_week(bug_tickets_qty),
            'features_per_week': self.tickets_per_week(feature_ticket_qty),
            'bugs_per_month': self.tickets_qty_by_type_and_month(bug_tickets_qty),
            'feature_per_month': self.tickets_qty_by_type_and_month(feature_ticket_qty),
            'bugs_top_five_title': self.highes_voted_title(bug_tickets_qty),
            'bugs_top_five_upvotes_count': self.highes_voted_upvotes_count(bug_tickets_qty),
            'features_top_five_title': self.highes_voted_title(feature_ticket_qty),
            'features_top_five_upvotes_count': self.highes_voted_upvotes_count(feature_ticket_qty)
        }
        return Response(data)
        
    def last_week_dates_name(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        week_days_name = []
        
        for i in range(7):
            one_day = yesterday - datetime.timedelta(days=i)
            week_days_name.append(one_day.strftime("%A"))
            
        return week_days_name
    
    def months_of_the_year(self):
        one_month = datetime.datetime.now()
        now = one_month
        months = []
        for i in range(1,13):
            months.append(one_month.strftime('%B'))
            one_month = now - relativedelta(months=i)
        return months
        
    def tickets_qty_by_type(self, type):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        
        created_tickets_prev_week = []
        
        for i in range(7):
            one_day = yesterday - datetime.timedelta(days=i)
            
            tickets_per_day = 0
            
            for ticket in type:
                if ticket.created_at.date() == one_day:
                    tickets_per_day += 1
                else: 
                    tickets_per_day
            created_tickets_prev_week.append(tickets_per_day)
        return created_tickets_prev_week
        
    def tickets_qty_by_type_and_month(self, type):
        one_month = datetime.datetime.now()
        now = one_month
        
        created_tickets_by_months = []
        
        for i in range(12):
            one_month = now - relativedelta(months=i)
            
            tickets_per_month = 0
            
            for ticket in type:
                if ticket.created_at.strftime('%B') == one_month.strftime('%B'):
                    tickets_per_month += 1
                else: 
                    tickets_per_month
            created_tickets_by_months.append(tickets_per_month)
        return created_tickets_by_months
        
    def tickets_per_week(self, type):
        today = datetime.date.today() - datetime.timedelta(days=1)
        
        tickets_per_week = []
        count = 0
        
        for i in range(29):
            if i == 7 or i == 14 or i == 21 or i == 28:
                tickets_per_week.append(count)
                count = 0
                
            day = today - datetime.timedelta(days=i)
            
            for ticket in type: 
                if ticket.created_at.date() == day:
                    count += 1
                else:
                    count
            
        return tickets_per_week

    def highes_voted_title(self, type):
        type = type.annotate(like_count=Count('upvotes')).order_by('-like_count', 'created_at')
        top_five_title = []
        for ticket in type[:5]:
            if ticket.upvotes.count() >= 1:
                top_five_title.append(ticket.title)
        return top_five_title
        
    def highes_voted_upvotes_count(self, type):
        type = type.annotate(like_count=Count('upvotes')).order_by('-like_count', 'created_at')
        top_five_title = []
        for ticket in type[:5]:
            if ticket.upvotes.count() >= 1:
                top_five_title.append(ticket.upvotes.count())
        return top_five_title