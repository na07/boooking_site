from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import Location, Booking
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from config import settings


def home_view(request:HttpRequest) -> HttpResponse:
    return render(request, "booking/home_page.html")

def check_location_view(request:HttpRequest) -> HttpResponse:
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    max_cost = request.GET.get("max_cost", None)
    min_cost = request.GET.get("min_cost", None)
    min_capacity = request.GET.get("min_capacity", None)
    max_capacity = request.GET.get("max_capacity", None)
    print(start_date, end_date)
    locations = Location.objects.all()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        locations = locations.exclude(
            bookings__start_date__lte=end_date,
            bookings__end_date__gte=start_date
        )
    if max_cost:
        locations = locations.filter(
            cost__lte=max_cost
        )
    if min_cost:
        locations = locations.filter(
            cost__gte=min_cost
        )
    if max_capacity:
        locations = locations.filter(
            capacity__lte=max_capacity
        )
    if min_capacity:
        locations = locations.filter(
            capacity__gte=min_capacity
        )
    return render(request, "booking/check_location.html", {"locations":locations})

def detail_location_view(request:HttpRequest, location_id:int) -> HttpResponse:
    if request.method == "GET":
        try:
            location = Location.objects.get(pk=location_id)
        except Location.DoesNotExist:
            return redirect("booking:check_location")

        return render(request, "booking/detail_location.html", {"location":location})
    elif request.method == "POST":
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        email = request.POST.get("email", None)
        print(start_date, end_date, "ffff")
        try:
            booking = Booking.objects.create(location_id=location_id, user=request.user, start_date=start_date, end_date=end_date)
            token = get_random_string(length=16)
            booking.activation_token = token
            booking.save()
            url = f"{request.scheme}://{request.get_host()}" \
                  f"{reverse('booking:activate', args=[token, booking.id])}"
            send_mail(
                subject='Тест от Django',
                message='Для активации перейдите по сыллке' + url,
                from_email= settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except ValidationError as u:
            messages.error(request, u.message)
        return redirect("booking:detail_location", location_id)

def booking_activation_view(request:HttpRequest, token:str, booking_id:int):
    if request.method == "GET":
        try:
            booking = Booking.objects.get(pk=booking_id)
            if booking.activation_token == token:
                booking.confirmed = True
                booking.save()
                messages.success(request, "confirmed")
        except Booking.DoesNotExist:
            pass
    return redirect("booking:check_location")

