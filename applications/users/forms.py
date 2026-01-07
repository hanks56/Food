from django import forms
from django.contrib.auth import authenticate

# Formulario de Login
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'hola@ejemplo.com',
        'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:bg-white focus:border-[#FF441F] transition-colors'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:bg-white focus:border-[#FF441F] transition-colors'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Credenciales inválidas. Intenta de nuevo.")
        return cleaned_data

# Formulario de Registro
class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm w-full outline-none focus:border-[#00A373]'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm w-full outline-none focus:border-[#00A373]'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Correo electrónico', 'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-[#00A373]'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Crear contraseña', 'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-[#00A373]'}))
    
    # Checkbox para registrarse como negocio
    is_business = forms.BooleanField(required=False, label="Quiero registrar mi negocio", widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-[#00A373] focus:ring-[#00A373]'}))