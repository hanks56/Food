from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CustomLoginForm, UserRegisterForm


class UserRegisterView(FormView):
    """Registro de usuario en Django."""
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users_app:user-login")

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"].strip().lower()
        first_name = data["first_name"].strip()
        last_name = data["last_name"].strip()

        User.objects.create_user(
            username=email,
            email=email,
            password=data["password"],
            first_name=first_name,
            last_name=last_name,
        )

        messages.success(self.request, "Cuenta creada. Inicia sesión con tu correo y contraseña.")
        return redirect(self.success_url)


class UserLoginView(LoginView):
    """Vista de inicio de sesión con la auth de Django."""
    template_name = "users/login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True