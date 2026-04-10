import os
import django

# Configuramos el entorno de Django para poder usar los modelos fuera de manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from applications.store.models import Category, Product

def run():
    print("Limpiando catálogo actual...")
    # Opcional: elimina las categorías actuales (y sus productos debido a CASCADE)
    # Category.objects.all().delete()
    
    if Category.objects.exists():
        print("La base de datos ya tiene categorías. Si deseas reemplazarlas, por favor limpia la base de datos primero.")
        return

    print("Creando categorías...")
    cat_pizzas = Category.objects.create(name="Pizzas", slug="pizzas", emoji="🍕", order=10)
    cat_burgers = Category.objects.create(name="Hamburguesas", slug="burgers", emoji="🍔", order=20)
    cat_drinks = Category.objects.create(name="Bebidas", slug="bebidas", emoji="🥤", order=30)
    cat_desserts = Category.objects.create(name="Postres", slug="postres", emoji="🍰", order=40)
    
    print("Creando productos para las categorías...")
    
    # --- Pizzas ---
    Product.objects.create(
        category=cat_pizzas,
        name="Pizza Margarita",
        description="Clásica masa artesanal con salsa de tomate de la casa, queso mozzarella fundido y hojas de albahaca fresca.",
        price=10500,
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=80",
        is_promo=True,
    )
    Product.objects.create(
        category=cat_pizzas,
        name="Pizza Pepperoni",
        description="Deliciosa base de queso cubierta con doble porción de pepperoni crujiente.",
        price=12900,
        image_url="https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )
    Product.objects.create(
        category=cat_pizzas,
        name="Pizza Cuatro Quesos",
        description="Mezcla perfecta de mozzarella, gorgonzola, parmesano y provolone.",
        price=14500,
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )
    
    # --- Hamburguesas ---
    Product.objects.create(
        category=cat_burgers,
        name="Hamburguesa Clásica",
        description="Carne de res de 200g, queso cheddar fundido, lechuga romana, tomate y nuestra salsa especial.",
        price=8500,
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80",
        is_promo=True,
    )
    Product.objects.create(
        category=cat_burgers,
        name="Hamburguesa Doble Bacon",
        description="Para los más hambrientos: Doble carne, cuádruple tocino ahumado, extra queso y salsa BBQ.",
        price=11900,
        image_url="https://images.unsplash.com/photo-1594212265004-998bd86dbec8?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )
    
    # --- Bebidas ---
    Product.objects.create(
        category=cat_drinks,
        name="Gaseosa Cola 500ml",
        description="Refrescante bebida de cola helada.",
        price=2000,
        image_url="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )
    Product.objects.create(
        category=cat_drinks,
        name="Limonada Natural",
        description="Limonada recién exprimida endulzada al punto exacto, con toque de menta.",
        price=3500,
        image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )

    # --- Postres ---
    Product.objects.create(
        category=cat_desserts,
        name="Tiramisú Tradicional",
        description="Suave postre italiano casero con capas de bizcocho café y queso mascarpone.",
        price=4500,
        image_url="https://images.unsplash.com/photo-1571115177098-24ec42ed204d?auto=format&fit=crop&w=500&q=80",
        is_promo=False,
    )
    Product.objects.create(
        category=cat_desserts,
        name="Cheesecake de Frutos Rojos",
        description="Delicioso pastel de queso con base crujiente y mermelada de la casa.",
        price=4900,
        image_url="https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=500&q=80",
        is_promo=True,
    )
    
    print("¡Catálogo creado y guardado exitosamente en tu base de datos!")

if __name__ == '__main__':
    run()
