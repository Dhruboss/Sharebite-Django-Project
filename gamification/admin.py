from django.contrib import admin
from .models import Badge, UserBadge, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'points_required']
    list_filter = ['badge_type']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    list_filter = ['awarded_at', 'badge']
    search_fields = ['user__username', 'badge__name']
    date_hierarchy = 'awarded_at'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'rank', 'total_points', 'total_food_saved', 'total_carbon_saved', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__username']
    ordering = ['rank']
