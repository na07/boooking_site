from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput,
            "password1": forms.PasswordInput,
            "password2": forms.PasswordInput
        }

class LoginForm(forms.Form):
    username = forms.CharField(label="login")
    password = forms.CharField(label="password", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label="remember me", widget=forms.CheckboxInput(), initial=True)