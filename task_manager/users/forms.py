from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
                "autocomplete": "new-password",
                "class": "form-control",
                "aria-describedby": "id_password1_helptext",
                "id": "id_password1",
            }
        ),
        required=False,
        help_text="Оставьте пустым, если не хотите менять пароль.",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Подтверждение пароля",
                "autocomplete": "new-password",
                "class": "form-control",
                "aria-describedby": "id_password2_helptext",
                "id": "id_password2",
            }
        ),
        required=False,
        help_text="Введите тот же пароль для подтверждения.",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user
