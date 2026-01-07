from django.db import models

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=50) # e.g., Burgers, Sushi, Pizza
    image = models.ImageField(upload_to='restaurants/categories/')

    class Meta:
        verbose_name_plural = "Restaurant Categories"

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(RestaurantCategory, on_delete=models.CASCADE)
    delivery_time = models.CharField(max_length=20, default="30-45 min")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    cover_image = models.ImageField(upload_to='restaurants/covers/')
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='restaurants/dishes/')
    is_popular = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Dishes"

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"