from django.db import models


class Category(models.Model):
    """Categoría del menú (Pizza, Hamburguesas, etc.)"""
    name = models.CharField("Nombre", max_length=100)
    slug = models.SlugField("Slug", max_length=50, unique=True, help_text="Para el enlace #pizza, #hamburguesas, etc.")
    emoji = models.CharField("Emoji", max_length=10, blank=True, help_text="Ej: 🍕 🍔")
    order = models.PositiveIntegerField("Orden", default=0, help_text="Orden de aparición en el menú")
    is_active = models.BooleanField("Activa", default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Producto del catálogo (pizza, hamburguesa, etc.)"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Categoría",
    )
    name = models.CharField("Nombre", max_length=150)
    description = models.TextField("Descripción", blank=True)
    price = models.PositiveIntegerField("Precio", help_text="En pesos sin puntos ni coma")
    image_url = models.URLField(
        "URL de imagen",
        blank=True,
        help_text="Enlace a la imagen del producto (ej: Unsplash, tu CDN)",
    )
    is_promo = models.BooleanField("Es promoción", default=False)
    is_active = models.BooleanField("Activo", default=True)
    order = models.PositiveIntegerField("Orden", default=0, help_text="Orden dentro de la categoría")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} (${self.price:,})"
