from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("registration_page/", views.registration_page, name = "registration_page"),
    path("login_page/", views.login_page, name = "login_page"),

]