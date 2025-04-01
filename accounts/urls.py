from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("registration_page/", views.registration_page, name = "registration_page"),
    path("login_page/", views.login_page, name = "login_page"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_page, name="profile"),

]