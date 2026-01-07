from home.views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
]