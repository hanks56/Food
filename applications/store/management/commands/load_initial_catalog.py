"""
Comando para cargar el catálogo inicial con categorías y productos de ejemplo.
Uso: python manage.py load_initial_catalog
"""
from django.core.management.base import BaseCommand

from applications.store.models import Category, Product


DATA = {
    "Pizza": {
        "slug": "pizza",
        "emoji": "🍕",
        "order": 1,
        "products": [
            ("Pizza Margherita", "Salsa de tomate, mozzarella y albahaca fresca.", 22000, "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&q=80&w=400"),
            ("Pizza Pepperoni", "Pepperoni, salsa y doble queso.", 24000, "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&q=80&w=400"),
            ("Pizza Hawaiana", "Jamón, piña y queso mozzarella.", 23000, "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Hamburguesas": {
        "slug": "hamburguesas",
        "emoji": "🍔",
        "order": 2,
        "products": [
            ("Classic Burger", "Carne, lechuga, tomate y salsa especial.", 18000, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&q=80&w=400"),
            ("Doble Carne", "Doble medallón, bacon y queso cheddar.", 24000, "https://images.unsplash.com/photo-1553979459-d2229ba7433b?auto=format&fit=crop&q=80&w=400"),
            ("Pollo Crispy", "Pechuga empanizada, coles y mayonesa.", 19000, "https://images.unsplash.com/photo-1571091718767-18b5b1457add?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Perros Calientes": {
        "slug": "perros",
        "emoji": "🌭",
        "order": 3,
        "products": [
            ("Perro Americano", "Salchicha, mostaza, salsa de tomate y cebolla.", 12000, "https://images.unsplash.com/photo-1612392062422-ef19b42f74df?auto=format&fit=crop&q=80&w=400"),
            ("Perro Ranchero", "Papa criolla, salsa ranchera y queso.", 14000, "https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Alitas y Pollo": {
        "slug": "alitas",
        "emoji": "🍗",
        "order": 4,
        "products": [
            ("Alitas BBQ", "8 piezas con salsa barbecue.", 18000, "https://images.unsplash.com/photo-1567620832903-0fc676de3866?auto=format&fit=crop&q=80&w=400"),
            ("Nuggets de Pollo", "10 unidades crujientes con salsa.", 15000, "https://images.unsplash.com/photo-1562967914-608f82629710?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Combos": {
        "slug": "combos",
        "emoji": "🎯",
        "order": 5,
        "products": [
            ("Combo Familiar", "2 hamburguesas + papas + 2 bebidas.", 38000, "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?auto=format&fit=crop&q=80&w=400", True),
        ],
    },
    "Bebidas": {
        "slug": "bebidas",
        "emoji": "🥤",
        "order": 6,
        "products": [
            ("Gaseosa 400ml", "Coca-Cola, Pepsi o Sprite.", 4000, "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&q=80&w=400"),
            ("Limonada Natural", "Limonada fresca 500ml.", 5000, "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Postres": {
        "slug": "postres",
        "emoji": "🍰",
        "order": 7,
        "products": [
            ("Brownie con Helado", "Brownie de chocolate y helado de vainilla.", 10000, "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?auto=format&fit=crop&q=80&w=400"),
        ],
    },
    "Opciones Saludables": {
        "slug": "saludables",
        "emoji": "🥗",
        "order": 8,
        "products": [
            ("Ensalada César", "Lechuga, pollo, parmesano y aderezo césar.", 16000, "https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&q=80&w=400"),
        ],
    },
}


class Command(BaseCommand):
    help = "Carga el catálogo inicial de categorías y productos"

    def handle(self, *args, **options):
        created = 0
        for cat_name, cat_data in DATA.items():
            cat, _ = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_name,
                    "emoji": cat_data["emoji"],
                    "order": cat_data["order"],
                },
            )
            for i, prod in enumerate(cat_data["products"]):
                is_promo = len(prod) > 4 and prod[4]
                Product.objects.get_or_create(
                    category=cat,
                    name=prod[0],
                    defaults={
                        "description": prod[1],
                        "price": prod[2],
                        "image_url": prod[3],
                        "is_promo": is_promo,
                        "order": i + 1,
                    },
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Catálogo cargado. Revisa en /admin/"))
