import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Cart, CartItem


def get_or_create_cart(user):
    """Obtiene el carrito activo del usuario o lo crea si no existe."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    """Vista principal del carrito — renderiza el template."""
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
    })


@login_required
@require_POST
def add_to_cart(request):
    """Recibe JSON del frontend y agrega o actualiza un producto en el carrito."""
    try:
        data = json.loads(request.body)
        from applications.store.models import Product

        product = get_object_or_404(Product, id=data.get('product_id'), is_available=True)
        cart = get_or_create_cart(request.user)
        quantity = int(data.get('quantity', 1))

        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.price, 'needs_cutlery': data.get('needs_cutlery', False)},
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_items,
            'cart_total': str(cart.total),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Elimina un ítem específico del carrito."""
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return JsonResponse({'success': True, 'cart_total': str(cart.total)})


@login_required
@require_POST
def clear_cart(request):
    """Vacía completamente el carrito."""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return JsonResponse({'success': True})