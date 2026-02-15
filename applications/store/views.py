from django.db.models import Prefetch
from django.shortcuts import render

from .models import Category, Product


def catalog_view(request):
    """Vista del catálogo de comida rápida."""
    products_active = Product.objects.filter(is_active=True).order_by("order", "name")
    categories = Category.objects.filter(is_active=True).prefetch_related(
        Prefetch("products", queryset=products_active)
    ).order_by("order", "name")
    return render(request, "store/catalog.html", {"categories": categories})
