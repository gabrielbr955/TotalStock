from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Site(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    Site = models.ForeignKey(Site, on_delete=models.DO_NOTHING, related_name='locations')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Dimensions
    dimension_x = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_y = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_z = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Unit of Measure
    UNIT_CHOICES = [
        ('un', 'Units'),
        ('kg', 'Kilogram'),
        ('l', 'liters'),
        ('m3', 'Cubic Meters'),
        ('in', 'Inches'),
        ('cm', 'Centimeters'),
        ('m', 'Meters'),
    ]
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES, default='un')

    def __str__(self):
        return self.name


class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} - Location {self.location.name}"
