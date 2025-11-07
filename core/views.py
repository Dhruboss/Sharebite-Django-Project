from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from food.models import FoodItem
from donations.models import Donation
from gamification.models import Leaderboard
from .utils import get_expiring_soon_items, get_expiry_alert_context


def home(request):
    recent_food = FoodItem.objects.filter(status='available')[:8]
    
    # Session tracking data
    visit_count = request.session.get('visit_count', 0)
    pages_visited = len(request.session.get('pages_visited', []))
    
    context = {
        'recent_food': recent_food,
        'visit_count': visit_count,
        'pages_visited': pages_visited,
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    user_donations = Donation.objects.filter(donor=request.user).order_by('-requested_at')[:5]
    user_received = Donation.objects.filter(receiver=request.user).order_by('-requested_at')[:5]

    # Leaderboard data
    leaderboard = Leaderboard.objects.all()[:10]
    
    # Statistics for visualizations
    total_donations_made = Donation.objects.filter(donor=request.user).count()
    total_donations_received = Donation.objects.filter(receiver=request.user).count()
    completed_donations = Donation.objects.filter(donor=request.user, status='completed').count()
    
    # Food items statistics
    total_food_shared = FoodItem.objects.filter(donor=request.user).count()
    available_food = FoodItem.objects.filter(donor=request.user, status='available').count()
    claimed_food = FoodItem.objects.filter(donor=request.user, status='claimed').count()
    
    # Monthly impact data (last 6 months)
    from django.utils import timezone
    from datetime import timedelta
    
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_donations = Donation.objects.filter(
        donor=request.user,
        requested_at__gte=six_months_ago
    ).values('requested_at__month').annotate(count=Count('id'))
    
    # Session tracking
    visit_count = request.session.get('visit_count', 0)
    
    # Expiry alerts
    expiring_items = get_expiring_soon_items(request.user, days=3)
    expiry_context = get_expiry_alert_context(request.user)

    context = {
        'user_donations': user_donations,
        'user_received': user_received,
        'leaderboard': leaderboard,
        'total_donations_made': total_donations_made,
        'total_donations_received': total_donations_received,
        'completed_donations': completed_donations,
        'total_food_shared': total_food_shared,
        'available_food': available_food,
        'claimed_food': claimed_food,
        'visit_count': visit_count,
        'expiring_items': expiring_items,
        **expiry_context,
    }
    return render(request, 'core/dashboard.html', context)


def about_us(request):
    team_members = [
        {
            'name': 'Debalina Barua',
            'role': 'Database & Models',
            'responsibilities': 'Database design, model creation, migrations, and relationships'
        },
        {
            'name': 'Tanjina Hoque',
            'role': 'Authentication & User Management',
            'responsibilities': 'User registration, login/logout, password reset, and profile management'
        },
        {
            'name': 'Showvik Salman Dhrubo',
            'role': 'Core Features & Views',
            'responsibilities': 'Food listings, donation workflow, and session tracking'
        },
        {
            'name': 'Sadika Sayma',
            'role': 'Uploads, Search & Filter',
            'responsibilities': 'File uploads, search functionality, and advanced filtering'
        },
        {
            'name': 'Mohammad Arifur Rahman Bhuiyan',
            'role': 'Gamification & Integration',
            'responsibilities': 'Badges, leaderboard, impact visualization, and system integration'
        }
    ]
    
    context = {
        'team_members': team_members,
        'university': 'University of Windsor',
        'course': 'Internet Applications and Distributed Systems',
    }
    return render(request, 'core/about_us.html', context)


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In a real application, you would send an email here
        # For now, we'll just show a success message
        messages.success(request, f'Thank you {name}! Your message has been received. We will get back to you soon.')
        return redirect('contact_us')
    
    return render(request, 'core/contact_us.html')