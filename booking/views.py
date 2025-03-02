from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Location


def home_view(request:HttpRequest) -> HttpResponse:
    return render(request, "booking/home_page.html")

def check_location_view(request:HttpRequest) -> HttpResponse:
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    locations = Location.objects.all()
    if start_date and end_date:
        pass #TODO фильтрация локаций по дате
    return render(request, "booking/check_location.html", {"locations":locations})