from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
# ESTA ES LA LÍNEA QUE TE FALTABA:
from django.contrib.auth.decorators import login_required 
from .forms import LoginForm, RegisterForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear usuario manualmente para asignar campos extra
            user = User.objects.create_user(
                username=form.cleaned_data['email'], # Username es el email
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Asignar rol de negocio si se marcó el checkbox
            if form.cleaned_data['is_business']:
                user.is_business_owner = True
                user.save()
            
            # Loguear automáticamente
            login(request, user)
            return redirect('home')
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

# VISTA DEL DASHBOARD
@login_required(login_url='home') # Si no está logueado, lo manda al home
def dashboard_view(request):
    # Capturamos el parámetro 'section' de la URL (ej: /dashboard/?section=orders)
    # Si no hay parámetro, por defecto mostramos 'profile'
    section = request.GET.get('section', 'profile')
    
    context = {
        'section': section
    }
    return render(request, 'dashboard.html', context)