from django.db import models

class Aisle(models.Model):
    name = models.CharField(max_length=50) # e.g., Dairy, Produce, Bakery

    def __str__(self):
        return self.name

class MarketProduct(models.Model):
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('un', 'Unit'),
        ('lt', 'Liter'),
    )
    
    name = models.CharField(max_length=150)
    aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, blank=True)
    net_content = models.DecimalField(max_digits=6, decimal_places=2)
    unit_measure = models.CharField(max_length=2, choices=UNIT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_organic = models.BooleanField(default=False)
    image = models.ImageField(upload_to='market/products/')

    def __str__(self):
        return f"{self.name} - {self.brand}"