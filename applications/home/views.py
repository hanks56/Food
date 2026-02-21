from django.shortcuts import render


def landing(request):
    """Despliega la página de aterrizaje."""
    return render(request, 'home/landing.html')
