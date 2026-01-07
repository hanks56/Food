from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from applications.home.views import index_view
from applications.users.views import login_view, register_view, logout_view, dashboard_view # Agregamos dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    
    # Auth
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard (Perfil, Pedidos, etc)
    path('dashboard/', dashboard_view, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)