from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView


class UserRegisterView(TemplateView):
    """Vista de registro (placeholder; luego añadirás formulario y lógica)."""
    template_name = 'users/register.html'


class UserLoginView(LoginView):
    """Vista de inicio de sesión con la auth de Django."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
