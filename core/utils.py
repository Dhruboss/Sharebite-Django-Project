from django.utils import timezone
from datetime import timedelta
from food.models import FoodItem


def get_expiring_soon_items(user, days=3):
    """
    Get food items belonging to user that are expiring within specified days
    """
    alert_date = timezone.now() + timedelta(days=days)
    
    expiring_items = FoodItem.objects.filter(
        donor=user,
        status='available',
        expiry_date__lte=alert_date,
        expiry_date__gte=timezone.now()
    ).order_by('expiry_date')
    
    return expiring_items


def get_expiry_alert_context(user):
    """
    Get context data for expiry alerts to display in templates
    """
    expiring_today = get_expiring_soon_items(user, days=1).count()
    expiring_this_week = get_expiring_soon_items(user, days=7).count()
    
    return {
        'expiring_today': expiring_today,
        'expiring_this_week': expiring_this_week,
        'has_expiry_alerts': expiring_today > 0 or expiring_this_week > 0,
    }

