from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Usaremos email como identificador principal
    email = models.EmailField(unique=True)
    
    # Roles
    is_client = models.BooleanField(default=True)
    is_business_owner = models.BooleanField(default=False, verbose_name="Is Business Owner")
    
    # Campos adicionales
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email