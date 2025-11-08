from django.db import models
from django.utils import timezone
from users.models import User


class Donation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # Use string reference instead of direct import
    food_item = models.ForeignKey('food.FoodItem', on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            # Import here to avoid circular import
            from food.models import FoodItem
            # Update user impact metrics
            carbon_saving = self.food_item.calculate_carbon_saving()
            self.donor.carbon_saved += carbon_saving
            self.donor.food_saved += self.food_item.quantity
            self.donor.points += int(self.food_item.quantity * 10)  # 10 points per kg
            self.donor.save()

            self.receiver.points += 5  # Points for receiving
            self.receiver.save()

            self.completed_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation: {self.food_item.title} -> {self.receiver.username}"