from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['food_item', 'donor', 'receiver', 'status', 'requested_at', 'completed_at']
    list_filter = ['status', 'requested_at', 'completed_at']
    search_fields = ['food_item__title', 'donor__username', 'receiver__username']
    date_hierarchy = 'requested_at'
    readonly_fields = ['requested_at', 'accepted_at', 'completed_at']
