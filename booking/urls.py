from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home_view, name = "home"),
    path("check_locations/", views.check_location_view, name = "check_location"),
    path("detail_location/<int:location_id>", views.detail_location_view, name="detail_location"),
    path("activate_booking/<str:token>/<int:booking_id>", views.booking_activation_view, name="activate")

]