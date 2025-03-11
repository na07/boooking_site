from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Location
from datetime import datetime


def home_view(request:HttpRequest) -> HttpResponse:
    return render(request, "booking/home_page.html")

def check_location_view(request:HttpRequest) -> HttpResponse:
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    print(start_date, end_date)
    locations = Location.objects.all()
    filtered_locations = []
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        for location in locations:
            for booking in location.bookings.all():
                if not (end_date < booking.start_date or start_date > booking.end_date):
                    break
            else:
                filtered_locations.append(location)
    else:
        filtered_locations = locations
    return render(request, "booking/check_location.html", {"locations":filtered_locations})

def detail_location_view(request:HttpRequest, location_id:int) -> HttpResponse:
    try:
        location = Location.objects.get(pk=location_id)
    except Location.DoesNotExist:
        return redirect("booking:check_location")

    return render(request, "booking/detail_location.html", {"location":location})