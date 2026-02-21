from django.urls import path
from . import views

app_name = 'cart_app'

urlpatterns = [
    path('',                        views.cart_detail,      name='cart-detail'),
    path('agregar/',                views.add_to_cart,      name='add-to-cart'),
    path('eliminar/<int:item_id>/', views.remove_from_cart, name='remove-item'),
    path('vaciar/',                 views.clear_cart,       name='clear-cart'),
]