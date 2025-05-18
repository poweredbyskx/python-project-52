from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthForm(AuthenticationForm):
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
        widget=forms.PasswordInput(attrs={
            "placeholder": "Пароль",
            "class": "form-control",
            "id": "id_password",
        }),
    )