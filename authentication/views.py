from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from tickets.views import tickets 
from .forms import LoginForm

# Create your views here.
def signup(request):
    return render(request, "signup.html")
    
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