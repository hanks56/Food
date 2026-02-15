from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "emoji", "order", "product_count", "is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Productos"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price_formatted", "is_promo", "is_active", "order"]
    list_editable = ["order", "is_promo", "is_active"]
    list_filter = ["category", "is_promo", "is_active"]
    search_fields = ["name", "description"]
    list_per_page = 20

    def price_formatted(self, obj):
        return f"${obj.price:,}"

    price_formatted.short_description = "Precio"
