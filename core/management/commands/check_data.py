from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from food.models import Category, FoodItem
from recipes.models import Recipe
from gamification.models import Badge, Leaderboard

User = get_user_model()


class Command(BaseCommand):
    help = 'Check what data exists in the database'

    def handle(self, *args, **options):
        self.stdout.write('='*50)
        self.stdout.write('DATABASE STATUS CHECK')
        self.stdout.write('='*50)
        
        users_count = User.objects.count()
        categories_count = Category.objects.count()
        food_count = FoodItem.objects.count()
        recipes_count = Recipe.objects.count()
        badges_count = Badge.objects.count()
        leaderboard_count = Leaderboard.objects.count()
        
        self.stdout.write(f'\nUsers: {users_count}')
        if users_count > 0:
            for user in User.objects.all()[:5]:
                self.stdout.write(f'  - {user.username} ({user.user_type})')
        
        self.stdout.write(f'\nCategories: {categories_count}')
        if categories_count > 0:
            for cat in Category.objects.all():
                self.stdout.write(f'  - {cat.name}')
        
        self.stdout.write(f'\nFood Items: {food_count}')
        if food_count > 0:
            for food in FoodItem.objects.all():
                self.stdout.write(f'  - {food.title} (Status: {food.status}, Donor: {food.donor.username})')
        
        self.stdout.write(f'\nRecipes: {recipes_count}')
        if recipes_count > 0:
            for recipe in Recipe.objects.all():
                self.stdout.write(f'  - {recipe.title} by {recipe.author.username}')
        
        self.stdout.write(f'\nBadges: {badges_count}')
        self.stdout.write(f'Leaderboard Entries: {leaderboard_count}')
        
        self.stdout.write('\n' + '='*50)

