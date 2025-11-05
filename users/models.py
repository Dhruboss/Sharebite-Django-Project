from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPES = (
        ('individual', 'Individual'),
        ('restaurant', 'Restaurant'),
        ('ngo', 'NGO'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='individual')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    points = models.IntegerField(default=0)
    carbon_saved = models.FloatField(default=0.0)  # in kg CO₂
    food_saved = models.FloatField(default=0.0)  # in kg

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"