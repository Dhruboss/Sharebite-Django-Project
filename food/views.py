from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import FoodItem, Category
from .forms import FoodItemForm, FoodSearchForm
from donations.models import Donation


def food_list(request):
    form = FoodSearchForm(request.GET or None)
    food_items = FoodItem.objects.filter(status='available')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        dietary_tags = form.cleaned_data.get('dietary_tags')

        if query:
            food_items = food_items.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        if category:
            food_items = food_items.filter(category=category)
        if dietary_tags:
            food_items = food_items.filter(dietary_tags=dietary_tags)

    context = {
        'food_items': food_items,
        'form': form,
    }
    return render(request, 'food/food_list.html', context)


def food_detail(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    context = {
        'food_item': food_item,
    }
    return render(request, 'food/food_detail.html', context)


@login_required
def food_create(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.donor = request.user
            food_item.save()
            return redirect('food_detail', pk=food_item.pk)
    else:
        form = FoodItemForm()

    context = {
        'form': form,
        'title': 'Share Food'
    }
    return render(request, 'food/food_form.html', context)


@login_required
def request_donation(request, food_id):
    food_item = get_object_or_404(FoodItem, pk=food_id, status='available')

    if request.method == 'POST':
        donation = Donation.objects.create(
            food_item=food_item,
            donor=food_item.donor,
            receiver=request.user
        )
        food_item.status = 'reserved'
        food_item.save()
        return redirect('donation_detail', donation_id=donation.pk)

    return render(request, 'food/request_donation.html', {'food_item': food_item})


from django.shortcuts import render

# Create your views here.
