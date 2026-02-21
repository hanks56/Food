from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        label="Nombre",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"}),
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Tu apellido"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Repite tu contraseña"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com", "autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )