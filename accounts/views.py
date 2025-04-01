from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from booking.models import Booking
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate

def registration_page(request:HttpRequest) -> HttpResponse:
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("booking:home")
    return render(request, "accounts/registration_page.html", {'form': form})


def login_page(request:HttpRequest) -> HttpResponse:
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data["remember_me"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(60*60*24*7)
                else:
                    request.session.set_expiry(0)
                return redirect("booking:home")
    return render(request, "accounts/login_page.html", {'form': form})


@login_required
def profile_page(request:HttpRequest) -> HttpResponse:
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "accounts/profile.html", {"bookings": bookings})

