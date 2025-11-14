from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Donation


@login_required
def donation_list(request):
    donations_made = Donation.objects.filter(donor=request.user)
    donations_received = Donation.objects.filter(receiver=request.user)

    context = {
        'donations_made': donations_made,
        'donations_received': donations_received,
    }
    return render(request, 'donations/donation_list.html', context)


@login_required
def donation_detail(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    # Check if user is authorized to view this donation
    if request.user != donation.donor and request.user != donation.receiver:
        return redirect('donation_list')

    context = {
        'donation': donation,
    }
    return render(request, 'donations/donation_detail.html', context)


@login_required
def accept_donation(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id, donor=request.user)

    if request.method == 'POST':
        donation.status = 'accepted'
        donation.accepted_at = timezone.now()
        donation.save()
        return redirect('donation_detail', donation_id=donation.pk)

    return redirect('donation_detail', donation_id=donation.pk)


@login_required
def complete_donation(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id, donor=request.user)

    if request.method == 'POST':
        donation.status = 'completed'
        donation.save()
        return redirect('donation_detail', donation_id=donation.pk)

    return redirect('donation_detail', donation_id=donation.pk)