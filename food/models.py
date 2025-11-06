from django.db import models
from django.utils import timezone
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('claimed', 'Claimed'),
        ('expired', 'Expired'),
    )

    DIETARY_TAGS = (
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('nut_free', 'Nut Free'),
    )

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donated_food')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()  # in kg
    expiry_date = models.DateTimeField()
    dietary_tags = models.CharField(max_length=50, choices=DIETARY_TAGS, blank=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_location = models.TextField()
    instructions = models.TextField(blank=True)

    def is_expired(self):
        return timezone.now() > self.expiry_date

    def days_until_expiry(self):
        delta = self.expiry_date - timezone.now()
        return delta.days

    def calculate_carbon_saving(self):
        # Approximate calculation: 1kg food waste = 2.5kg CO₂
        return self.quantity * 2.5

    def __str__(self):
        return f"{self.title} by {self.donor.username}"