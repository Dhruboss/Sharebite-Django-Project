from django.db import models
from users.models import User


class Badge(models.Model):
    BADGE_TYPES = (
        ('food_saver', 'Food Saver'),
        ('top_donor', 'Top Donor'),
        ('eco_warrior', 'Eco Warrior'),
        ('community_hero', 'Community Hero'),
        ('quick_responder', 'Quick Responder'),
    )

    name = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPES)
    description = models.TextField()
    icon = models.ImageField(upload_to='badge_icons/')
    points_required = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    total_food_saved = models.FloatField(default=0.0)
    total_carbon_saved = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"