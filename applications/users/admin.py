from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('is_business_owner', 'phone_number', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)