import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Cart, CartItem

# Logger del módulo — los errores aparecerán en la consola de Django
# con el prefijo "applications.cart.views" para identificarlos fácilmente
logger = logging.getLogger(__name__)


def get_or_create_cart(user):
    """Obtiene el carrito activo del usuario o lo crea si no existe."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    """Vista principal del carrito — renderiza el template."""
    cart = get_or_create_cart(request.user)
    # select_related('product') evita el problema N+1:
    # en lugar de hacer 1 query por ítem, hace 1 sola query con JOIN
    items = cart.items.select_related('product').all()
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
    })


@login_required
@require_POST
def add_to_cart(request):
    """
    Recibe JSON del frontend y agrega o actualiza un producto en el carrito.

    Flujo:
        1. Parsear el JSON del body
        2. Buscar el producto por ID (solo activos — is_active=True)
        3. Obtener o crear el carrito del usuario
        4. Crear o actualizar el CartItem (update_or_create)
        5. Devolver JSON con el nuevo estado del carrito

    Errores posibles y sus causas:
        - json.JSONDecodeError  → el frontend envió body vacío o malformado
        - Http404               → product_id no existe o el producto está inactivo
        - ValueError            → quantity no es un número válido
    """
    # ── 1. Parsear body JSON ────────────────────────────────────────────────
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        logger.error("add_to_cart: JSON inválido recibido — %s", e)
        return JsonResponse(
            {'success': False, 'error': 'Datos inválidos enviados al servidor.'},
            status=400,
        )

    product_id = data.get('product_id')
    quantity   = data.get('quantity', 1)

    # ── 2. Validar product_id antes de consultar la DB ──────────────────────
    if not product_id:
        logger.warning("add_to_cart: product_id no fue enviado. Body recibido: %s", data)
        return JsonResponse(
            {'success': False, 'error': 'No se recibió el ID del producto.'},
            status=400,
        )

    # ── 3. Buscar producto activo ───────────────────────────────────────────
    # BUG CORREGIDO: el campo se llama is_active (no is_available)
    # is_available no existe en el modelo Product → FieldError → 400
    from applications.store.models import Product
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # ── 4. Validar cantidad ─────────────────────────────────────────────────
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("La cantidad debe ser al menos 1.")
        if quantity > 99:
            raise ValueError("La cantidad máxima por producto es 99.")
    except (TypeError, ValueError) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # ── 5. Obtener o crear carrito ──────────────────────────────────────────
    cart = get_or_create_cart(request.user)

    # ── 6. Crear o actualizar el ítem ───────────────────────────────────────
    # update_or_create devuelve (instancia, created:bool)
    # Si el producto ya existe en el carrito → actualiza la cantidad
    # Si es nuevo → lo crea con la cantidad indicada
    cart_item, created = CartItem.objects.update_or_create(
        cart=cart,
        product=product,
        defaults={
            'price': product.price,
            'needs_cutlery': data.get('needs_cutlery', False),
        },
    )

    if not created:
        # El producto ya estaba en el carrito → sumar la cantidad nueva
        cart_item.quantity += quantity
    else:
        # Producto nuevo en el carrito → asignar la cantidad
        cart_item.quantity = quantity

    cart_item.save()

    logger.info(
        "add_to_cart: usuario=%s agregó product_id=%s (qty=%s). "
        "Total carrito: %s items / $%s",
        request.user.username, product_id, quantity,
        cart.total_items, cart.total,
    )

    return JsonResponse({
        'success': True,
        'cart_total_items': cart.total_items,
        'cart_total': str(cart.total),
    })


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """
    Elimina un ítem específico del carrito.

    Seguridad: filtramos por cart=cart para asegurarnos de que el ítem
    pertenece al carrito del usuario autenticado. Sin este filtro, cualquier
    usuario podría eliminar ítems de otros usuarios conociendo el item_id.
    """
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return JsonResponse({'success': True, 'cart_total': str(cart.total)})


@login_required
@require_POST
def clear_cart(request):
    """Vacía completamente el carrito del usuario autenticado."""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return JsonResponse({'success': True})