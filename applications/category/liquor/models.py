from django.db import models

class LiquorType(models.Model):
    name = models.CharField(max_length=50) # e.g., Beer, Wine, Whiskey, Rum

    def __str__(self):
        return self.name

class Bottle(models.Model):
    name = models.CharField(max_length=150)
    liquor_type = models.ForeignKey(LiquorType, on_delete=models.CASCADE)
    alcohol_percentage = models.DecimalField(max_digits=4, decimal_places=1)
    volume_ml = models.PositiveIntegerField(help_text="Volume in milliliters")
    origin = models.CharField(max_length=50, blank=True) # e.g., Scotland, France
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='liquor/bottles/')

    def __str__(self):
        return f"{self.name} ({self.volume_ml}ml)"