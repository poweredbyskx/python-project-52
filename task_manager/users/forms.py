from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users"""
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing users"""
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class CustomAuthForm(AuthenticationForm):
    """Authentication form with Russian placeholders"""
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "placeholder": "Имя пользователя",
            "class": "form-control",
            "id": "id_username",
        }),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Пароль",
            "class": "form-control",
            "id": "id_password",
        }),
    )