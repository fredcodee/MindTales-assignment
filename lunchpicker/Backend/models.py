from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# models.py

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    date = models.DateField()
    items = models.TextField()  #nb- Comma-separated list of menu items (,)

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    points = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} voted {self.points} for {self.menu.restaurant.name}"