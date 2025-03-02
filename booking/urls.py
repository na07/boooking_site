from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home_view, name = "home"),
    path("check_locations/", views.check_location_view, name = "check_location"),

]