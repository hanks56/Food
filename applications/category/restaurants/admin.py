from django.contrib import admin
from .models import RestaurantCategory, Restaurant, Dish

admin.site.register(RestaurantCategory)
admin.site.register(Restaurant)
admin.site.register(Dish)