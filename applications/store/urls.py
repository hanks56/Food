from django.urls import path
from . import views

app_name = "store_app"

urlpatterns = [
    path("catalogo/", views.catalog_view, name="catalog"),
]