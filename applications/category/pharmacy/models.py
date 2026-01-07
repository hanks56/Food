from django.db import models

class Lab(models.Model):
    name = models.CharField(max_length=100) # e.g., Pfizer, Bayer

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=150)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    presentation = models.CharField(max_length=100) # e.g., Box x 10 tablets
    active_component = models.CharField(max_length=150) # e.g., Acetaminophen
    requires_prescription = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='pharmacy/products/')

    def __str__(self):
        return f"{self.name} ({self.presentation})"