from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tickets.views import tickets 
from .forms import LoginForm, RegistrationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("tickets"))
        
    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            
            user = auth.authenticate(username=request.POST["username"],
                                    password=request.POST["password1"])
            
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have been successfully registered!")
                return redirect(reverse("tickets"))
            else:
                messages.error(request, "Unable to register your account")
    else:
        reg_form = RegistrationForm()
    return render(request, "signup.html", {"reg_form": reg_form})
    
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("tickets"))
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            if user: 
                auth.login(user=user, request=request)
                messages.success(request, "You have been successfully logged in!")
                return redirect(reverse("tickets"))
            else:
                login_form.add_error(None, "Username or password is incorrect!")
    else:
        login_form = LoginForm()
    return render(request, "login.html", {"login_form": login_form})    

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out!")
    return redirect(reverse("tickets"))