from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from food.models import FoodItem
from donations.models import Donation
from gamification.models import Leaderboard


def home(request):
    recent_food = FoodItem.objects.filter(status='available')[:8]
    context = {
        'recent_food': recent_food,
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    user_donations = Donation.objects.filter(donor=request.user).order_by('-requested_at')[:5]
    user_received = Donation.objects.filter(receiver=request.user).order_by('-requested_at')[:5]

    # Leaderboard data
    leaderboard = Leaderboard.objects.all()[:10]

    context = {
        'user_donations': user_donations,
        'user_received': user_received,
        'leaderboard': leaderboard,
    }
    return render(request, 'core/dashboard.html', context)