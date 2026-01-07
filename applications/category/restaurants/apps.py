from django.apps import AppConfig

class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.category.restaurants'  # Full path is required
    verbose_name = 'Restaurants Manager'