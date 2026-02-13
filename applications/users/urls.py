from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users_app'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]