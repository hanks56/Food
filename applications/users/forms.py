from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    """
    Formulario de registro de usuario.

    Usa el modelo estándar de Django (auth.User) sin extenderlo,
    lo que mantiene compatibilidad con el sistema de autenticación
    nativo y evita migraciones innecesarias en esta etapa del proyecto.

    Campos:
        first_name       -- Nombre del usuario
        last_name        -- Apellido del usuario
        email            -- Correo (se usa como username en el sistema)
        password         -- Contraseña elegida por el usuario
        confirm_password -- Repetición para verificar que no haya typo
        terms            -- Aceptación de términos y condiciones (requerida)
    """

    first_name = forms.CharField(
        label="Nombre",
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Tu nombre",
            "class": "w-full p-4 bg-humo border border-gray-100 rounded-xl "
                     "transition-all focus:outline-none focus:border-rappi "
                     "focus:bg-white focus:ring-2 focus:ring-rappi/20",
        }),
    )

    last_name = forms.CharField(
        label="Apellido",
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Tu apellido",
            "class": "w-full p-4 bg-humo border border-gray-100 rounded-xl "
                     "transition-all focus:outline-none focus:border-rappi "
                     "focus:bg-white focus:ring-2 focus:ring-rappi/20",
        }),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "correo@ejemplo.com",
            "class": "w-full p-4 bg-humo border border-gray-100 rounded-xl "
                     "transition-all focus:outline-none focus:border-rappi "
                     "focus:bg-white focus:ring-2 focus:ring-rappi/20",
        }),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mínimo 8 caracteres",
            "class": "w-full p-4 bg-humo border border-gray-100 rounded-xl "
                     "transition-all focus:outline-none focus:border-rappi "
                     "focus:bg-white focus:ring-2 focus:ring-rappi/20",
        }),
    )

    # ─────────────────────────────────────────────────────────────────────
    # BUG CORREGIDO: el campo se llamaba "password_confirm" en forms.py
    # pero el template lo referenciaba como "confirm_password".
    # Unificamos el nombre a "confirm_password" (más legible en el template).
    # ─────────────────────────────────────────────────────────────────────
    confirm_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repite tu contraseña",
            "class": "w-full p-4 bg-humo border border-gray-100 rounded-xl "
                     "transition-all focus:outline-none focus:border-rappi "
                     "focus:bg-white focus:ring-2 focus:ring-rappi/20",
        }),
    )

    # ─────────────────────────────────────────────────────────────────────
    # BUG CORREGIDO: el template usaba {{ form.terms }} pero el campo
    # no existía en el formulario. Lo declaramos aquí con required=True
    # para que la validación falle si no se acepta.
    # ─────────────────────────────────────────────────────────────────────
    terms = forms.BooleanField(
        label="Acepto los Términos y Condiciones",
        required=True,
        error_messages={
            "required": "Debes aceptar los Términos y Condiciones para continuar."
        },
        widget=forms.CheckboxInput(attrs={
            "class": "w-4 h-4 rounded border-gray-300 text-rappi focus:ring-rappi",
        }),
    )

    # ── Validaciones de campo individual ─────────────────────────────────

    def clean_email(self):
        """
        Normaliza el email (minúsculas, sin espacios) y verifica que no
        esté registrado. Usamos username=email como estrategia de autenticación
        para no requerir campo username separado.
        """
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean_password(self):
        """
        Validación mínima de contraseña.
        Django ya aplica los validators de AUTH_PASSWORD_VALIDATORS en
        create_user(), pero validamos longitud aquí para dar feedback
        inmediato en el formulario antes de llegar a la vista.
        """
        password = self.cleaned_data.get("password", "")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password

    def clean(self):
        """
        Validación cruzada: compara password y confirm_password.
        Se ejecuta después de clean_password() y clean_confirm_password(),
        por eso usamos .get() de forma segura.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm  = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            # Asociamos el error al campo confirm_password para que
            # Django lo muestre al lado del campo correcto en el template.
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    """
    Extiende AuthenticationForm para usar email en lugar de username.

    AuthenticationForm ya maneja:
        - Validación de credenciales contra la DB
        - Bloqueo de cuentas inactivas
        - Mensajes de error genéricos (no revela si el email existe)

    Solo sobreescribimos los widgets para adaptar la UX.
    """

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "correo@ejemplo.com",
            "autofocus": True,
        }),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
        }),
    )