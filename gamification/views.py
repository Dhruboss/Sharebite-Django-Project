from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Leaderboard, Badge


@login_required
def leaderboard(request):
    leaders = Leaderboard.objects.all()[:20]
    context = {
        'leaders': leaders,
    }
    return render(request, 'gamification/leaderboard.html', context)


@login_required
def badges(request):
    user_badges = request.user.badges.all()
    all_badges = Badge.objects.all()

    context = {
        'user_badges': user_badges,
        'all_badges': all_badges,
    }
    return render(request, 'gamification/badges.html', context)


from django.shortcuts import render

# Create your views here.
