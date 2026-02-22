from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CustomLoginForm, UserRegisterForm


class UserRegisterView(FormView):
    """
    Vista de registro de usuario.

    Hereda de FormView (no CreateView) porque usamos el User nativo de Django
    con un formulario personalizado, no un ModelForm. Esto nos da control
    total sobre el proceso de creación sin acoplar el formulario al modelo.

    Flujo completo:
        1. GET  → renderiza el formulario vacío
        2. POST → valida con UserRegisterForm
                → si válido: crea el usuario con create_user() y redirige al login
                → si inválido: re-renderiza el template con los errores

    Seguridad:
        - create_user() aplica hash a la contraseña con PBKDF2-SHA256
          (nunca guardamos la contraseña en texto plano)
        - La validación de email duplicado está en el formulario (clean_email)
        - strip().lower() normaliza el email para evitar duplicados por capitalización
    """

    template_name = "users/register.html"
    form_class    = UserRegisterForm
    success_url   = reverse_lazy("users_app:user-login")

    def dispatch(self, request, *args, **kwargs):
        """
        Si el usuario ya está autenticado, lo redirigimos al inicio.
        No tiene sentido mostrar el registro a alguien que ya inició sesión.
        """
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Se ejecuta solo cuando form.is_valid() es True.
        Aquí creamos el usuario en la base de datos de Django.

        ¿Por qué create_user() y no User(**data).save()?
        create_user() internamente llama a set_password() que convierte
        la contraseña en texto plano a un hash seguro usando el hasher
        configurado en PASSWORD_HASHERS de settings.py (PBKDF2 por defecto).
        Si usáramos User(password=raw_password).save(), la contraseña
        quedaría guardada en texto plano en la DB — vulnerabilidad crítica.
        """
        data = form.cleaned_data

        # Normalización defensiva: aunque clean_email() ya hace esto,
        # lo repetimos en la vista como segunda capa de seguridad.
        email      = data["email"].strip().lower()
        first_name = data["first_name"].strip()
        last_name  = data["last_name"].strip()

        # create_user(username, email, password) → hashea la contraseña,
        # guarda el usuario en auth_user y retorna la instancia creada.
        # Usamos email como username porque nuestro CustomLoginForm
        # autentica con email, no con un username separado.
        User.objects.create_user(
            username=email,        # campo único en la tabla auth_user
            email=email,
            password=data["password"],
            first_name=first_name,
            last_name=last_name,
        )

        messages.success(
            self.request,
            f"¡Cuenta creada exitosamente! Bienvenido, {first_name}. "
            "Inicia sesión con tu correo y contraseña."
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        """
        Se ejecuta cuando la validación falla.
        FormView por defecto re-renderiza el template con los errores.
        Solo añadimos un mensaje flash para contexto adicional.
        """
        messages.error(
            self.request,
            "Revisa los errores del formulario antes de continuar."
        )
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """
    Vista de inicio de sesión.

    Hereda de LoginView (vista de Django) que maneja todo el flujo:
        - Verificación de credenciales contra auth_user en la DB
        - Generación y almacenamiento de la sesión en django_session
        - Redirección post-login según LOGIN_REDIRECT_URL en settings.py

    Nosotros solo personalizamos:
        - template_name: nuestro diseño
        - form_class: CustomLoginForm que usa email en lugar de username
        - redirect_authenticated_user: evita que usuarios logueados
          vean la pantalla de login (UX y seguridad)
    """

    template_name            = "users/login.html"
    form_class               = CustomLoginForm
    redirect_authenticated_user = True