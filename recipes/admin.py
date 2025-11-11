from django.contrib import admin
from .models import Recipe, RecipeFavorite


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'difficulty', 'prep_time', 'cook_time', 'servings', 'leftover_friendly', 'created_at', 'views']
    list_filter = ['difficulty', 'leftover_friendly', 'created_at']
    search_fields = ['title', 'description', 'ingredients']
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'recipe__title']

