from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Recipe, RecipeFavorite
from .forms import RecipeForm, RecipeSearchForm


def recipe_list(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        difficulty = form.cleaned_data.get('difficulty')
        leftover_friendly = form.cleaned_data.get('leftover_friendly')
        
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        if leftover_friendly:
            recipes = recipes.filter(leftover_friendly=True)
    
    context = {
        'recipes': recipes,
        'form': form,
    }
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.views += 1
    recipe.save(update_fields=['views'])
    
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = RecipeFavorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    ingredients_list = recipe.ingredients.split('\n')
    instructions_list = recipe.instructions.split('\n')
    
    context = {
        'recipe': recipe,
        'is_favorited': is_favorited,
        'ingredients_list': ingredients_list,
        'instructions_list': instructions_list,
    }
    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': 'Share an Eco-Friendly Recipe'
    }
    return render(request, 'recipes/recipe_form.html', context)


@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    favorite, created = RecipeFavorite.objects.get_or_create(user=request.user, recipe=recipe)
    
    if not created:
        favorite.delete()
    
    return redirect('recipe_detail', pk=pk)


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    favorites = RecipeFavorite.objects.filter(user=request.user).select_related('recipe')
    
    context = {
        'recipes': recipes,
        'favorites': favorites,
    }
    return render(request, 'recipes/my_recipes.html', context)

