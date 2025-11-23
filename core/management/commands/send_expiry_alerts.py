from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from food.models import FoodItem


class Command(BaseCommand):
    help = 'Send expiry alerts for food items that are expiring soon'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=2,
            help='Number of days before expiry to send alert (default: 2)',
        )

    def handle(self, *args, **options):
        days_threshold = options['days']
        alert_date = timezone.now() + timedelta(days=days_threshold)
        
        # Get food items expiring within the threshold
        expiring_food = FoodItem.objects.filter(
            status='available',
            expiry_date__lte=alert_date,
            expiry_date__gte=timezone.now()
        )
        
        alert_count = 0
        for food_item in expiring_food:
            days_left = food_item.days_until_expiry()
            
            # Send email to donor
            subject = f'Expiry Alert: {food_item.title} expires in {days_left} day(s)'
            message = f'''
Hello {food_item.donor.username},

This is a reminder that your food item "{food_item.title}" will expire in {days_left} day(s).

Expiry Date: {food_item.expiry_date.strftime("%B %d, %Y at %I:%M %p")}
Quantity: {food_item.quantity} kg
Status: {food_item.get_status_display()}

If this food is still available, please ensure it is claimed soon to avoid waste.
You can view it here: /food/{food_item.pk}/

Thank you for helping reduce food waste!

- Sharebite Team
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@sharebite.com',
                    [food_item.donor.email],
                    fail_silently=False,
                )
                alert_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Alert sent for: {food_item.title} to {food_item.donor.email}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send alert for {food_item.title}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {alert_count} expiry alerts')
        )

