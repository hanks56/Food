from django.db import models

class PetType(models.Model):
    name = models.CharField(max_length=50) # e.g., Dog, Cat, Bird

    def __str__(self):
        return self.name

class PetProduct(models.Model):
    LIFE_STAGE_CHOICES = (
        ('puppy', 'Puppy/Kitten'),
        ('adult', 'Adult'),
        ('senior', 'Senior'),
        ('all', 'All Stages'),
    )

    name = models.CharField(max_length=150)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    life_stage = models.CharField(max_length=10, choices=LIFE_STAGE_CHOICES, default='all')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pets/products/')

    def __str__(self):
        return f"{self.name} for {self.pet_type.name}"