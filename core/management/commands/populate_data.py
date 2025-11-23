from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from food.models import Category, FoodItem
from recipes.models import Recipe
from gamification.models import Badge, Leaderboard
from donations.models import Donation

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database...')
        
        # Create sample users
        self.stdout.write('Creating users...')
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'Pass123!', 
             'user_type': 'individual', 'phone_number': '519-123-4567', 
             'address': '401 Sunset Ave, Windsor, ON', 'bio': 'Food enthusiast helping reduce waste'},
            {'username': 'green_restaurant', 'email': 'info@greenrest.com', 'password': 'Pass123!', 
             'user_type': 'restaurant', 'phone_number': '519-234-5678', 
             'address': '123 University Ave, Windsor, ON', 'bio': 'Eco-friendly restaurant sharing surplus'},
            {'username': 'windsor_ngo', 'email': 'contact@windsorngo.org', 'password': 'Pass123!', 
             'user_type': 'ngo', 'phone_number': '519-345-6789', 
             'address': '456 Wyandotte St, Windsor, ON', 'bio': 'Helping feed the community'},
            {'username': 'sarah_green', 'email': 'sarah@example.com', 'password': 'Pass123!', 
             'user_type': 'individual', 'phone_number': '519-456-7890', 
             'address': '789 Ouellette Ave, Windsor, ON', 'bio': 'Love cooking and sharing'},
            {'username': 'mike_chef', 'email': 'mike@example.com', 'password': 'Pass123!', 
             'user_type': 'restaurant', 'phone_number': '519-567-8901', 
             'address': '321 Erie St, Windsor, ON', 'bio': 'Chef passionate about sustainability'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'user_type': user_data['user_type'],
                    'phone_number': user_data['phone_number'],
                    'address': user_data['address'],
                    'bio': user_data['bio'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
            users.append(user)
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Fresh Vegetables', 'description': 'Fresh and organic vegetables'},
            {'name': 'Fresh Fruits', 'description': 'Seasonal fresh fruits'},
            {'name': 'Prepared Meals', 'description': 'Ready-to-eat meals'},
            {'name': 'Baked Goods', 'description': 'Bread, pastries, and baked items'},
            {'name': 'Dairy Products', 'description': 'Milk, cheese, yogurt'},
            {'name': 'Canned Goods', 'description': 'Non-perishable canned items'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            categories.append(category)
        
        # Create food items
        self.stdout.write('Creating food items...')
        food_items_data = [
            {
                'title': 'Fresh Organic Tomatoes',
                'description': 'Locally grown organic tomatoes, perfect for salads or cooking. Still fresh and delicious!',
                'category': categories[0],
                'quantity': 3.5,
                'expiry_date': timezone.now() + timedelta(days=3),
                'dietary_tags': 'vegan',
                'pickup_location': '401 Sunset Ave, Windsor, ON',
                'instructions': 'Available for pickup after 5 PM on weekdays',
                'donor': users[0],
            },
            {
                'title': 'Homemade Vegetable Soup',
                'description': 'Freshly made vegetable soup with carrots, celery, and herbs. Warm and nutritious!',
                'category': categories[2],
                'quantity': 2.0,
                'expiry_date': timezone.now() + timedelta(days=2),
                'dietary_tags': 'vegetarian',
                'pickup_location': '123 University Ave, Windsor, ON',
                'instructions': 'Please bring your own container',
                'donor': users[1],
            },
            {
                'title': 'Surplus Bread Loaves',
                'description': 'Fresh whole wheat bread from today. Great for sandwiches or toast.',
                'category': categories[3],
                'quantity': 1.5,
                'expiry_date': timezone.now() + timedelta(days=4),
                'dietary_tags': 'vegetarian',
                'pickup_location': '321 Erie St, Windsor, ON',
                'instructions': 'Available all day, ring the doorbell',
                'donor': users[4],
            },
            {
                'title': 'Fresh Apples',
                'description': 'Crispy red apples from local farm. Excellent for snacking or baking.',
                'category': categories[1],
                'quantity': 5.0,
                'expiry_date': timezone.now() + timedelta(days=7),
                'dietary_tags': 'vegan',
                'pickup_location': '789 Ouellette Ave, Windsor, ON',
                'instructions': 'Pickup anytime, leave note if not home',
                'donor': users[3],
            },
            {
                'title': 'Canned Vegetables Mix',
                'description': 'Assorted canned vegetables - corn, peas, carrots. Long shelf life.',
                'category': categories[5],
                'quantity': 4.0,
                'expiry_date': timezone.now() + timedelta(days=365),
                'dietary_tags': 'vegan',
                'pickup_location': '456 Wyandotte St, Windsor, ON',
                'instructions': 'Contact before pickup',
                'donor': users[2],
            },
            {
                'title': 'Greek Yogurt Containers',
                'description': 'Unopened Greek yogurt, excellent source of protein.',
                'category': categories[4],
                'quantity': 1.0,
                'expiry_date': timezone.now() + timedelta(days=5),
                'dietary_tags': 'vegetarian',
                'pickup_location': '401 Sunset Ave, Windsor, ON',
                'instructions': 'Keep refrigerated',
                'donor': users[0],
            },
        ]
        
        food_items = []
        for food_data in food_items_data:
            food_item, created = FoodItem.objects.get_or_create(
                title=food_data['title'],
                donor=food_data['donor'],
                defaults=food_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created food item: {food_item.title}'))
            food_items.append(food_item)
        
        # Create recipes
        self.stdout.write('Creating recipes...')
        recipes_data = [
            {
                'title': 'Bread Pudding from Stale Bread',
                'description': 'Transform leftover bread into a delicious dessert. Perfect way to use stale bread!',
                'ingredients': '''4 cups stale bread, cubed
2 cups milk
3 eggs
1/2 cup sugar
1 tsp vanilla extract
1/2 tsp cinnamon
1/4 cup raisins (optional)''',
                'instructions': '''Preheat oven to 350°F (175°C)
Grease a baking dish
Place bread cubes in the dish
Mix milk, eggs, sugar, vanilla, and cinnamon
Pour mixture over bread
Let soak for 10 minutes
Sprinkle raisins on top
Bake for 45 minutes until golden
Serve warm with caramel sauce''',
                'prep_time': 15,
                'cook_time': 45,
                'servings': 6,
                'difficulty': 'easy',
                'leftover_friendly': True,
                'waste_reduction_tip': 'Use any stale bread - white, whole wheat, or even croissants work great!',
                'author': users[0],
            },
            {
                'title': 'Vegetable Scrap Broth',
                'description': 'Make nutritious broth from vegetable scraps. Zero waste cooking at its best!',
                'ingredients': '''Vegetable scraps (peels, ends, stems)
8 cups water
2 bay leaves
1 tsp peppercorns
Salt to taste
Optional: garlic skins, herb stems''',
                'instructions': '''Save vegetable scraps in freezer until you have enough
Place scraps in large pot
Add water, bay leaves, peppercorns
Bring to boil, then simmer for 1 hour
Strain and discard solids
Season with salt
Use immediately or freeze for later''',
                'prep_time': 10,
                'cook_time': 60,
                'servings': 8,
                'difficulty': 'easy',
                'leftover_friendly': True,
                'waste_reduction_tip': 'Save carrot peels, onion ends, celery leaves, and herb stems for this recipe!',
                'author': users[3],
            },
            {
                'title': 'Overripe Banana Muffins',
                'description': 'Delicious muffins made from bananas that are too ripe to eat. Moist and flavorful!',
                'ingredients': '''3 overripe bananas, mashed
1/3 cup melted butter
3/4 cup sugar
1 egg
1 tsp vanilla
1 tsp baking soda
Pinch of salt
1 1/2 cups flour
Optional: chocolate chips, nuts''',
                'instructions': '''Preheat oven to 375°F (190°C)
Line muffin tin with paper cups
Mash bananas in bowl
Mix in melted butter
Add sugar, egg, vanilla
Sprinkle baking soda and salt, mix
Add flour, stir until just combined
Fill muffin cups 2/3 full
Bake 18-20 minutes
Cool before serving''',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 12,
                'difficulty': 'easy',
                'leftover_friendly': True,
                'waste_reduction_tip': 'Perfect way to use brown bananas instead of throwing them away!',
                'author': users[4],
            },
        ]
        
        for recipe_data in recipes_data:
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                author=recipe_data['author'],
                defaults=recipe_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.title}'))
        
        # Create badges
        self.stdout.write('Creating badges...')
        badges_data = [
            {
                'name': 'First Share',
                'badge_type': 'food_saver',
                'description': 'Shared your first food item with the community',
                'points_required': 0,
            },
            {
                'name': 'Food Saver',
                'badge_type': 'food_saver',
                'description': 'Saved 10kg of food from waste',
                'points_required': 100,
            },
            {
                'name': 'Top Donor',
                'badge_type': 'top_donor',
                'description': 'Completed 10 successful donations',
                'points_required': 150,
            },
            {
                'name': 'Eco Warrior',
                'badge_type': 'eco_warrior',
                'description': 'Prevented 25kg of CO2 emissions',
                'points_required': 250,
            },
            {
                'name': 'Community Hero',
                'badge_type': 'community_hero',
                'description': 'Made 50+ successful donations',
                'points_required': 500,
            },
        ]
        
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created badge: {badge.name}'))
        
        # Update user points and create leaderboard
        self.stdout.write('Creating leaderboard data...')
        user_stats = [
            {'user': users[0], 'points': 150, 'food_saved': 15.0, 'carbon_saved': 37.5},
            {'user': users[1], 'points': 230, 'food_saved': 23.0, 'carbon_saved': 57.5},
            {'user': users[2], 'points': 180, 'food_saved': 18.0, 'carbon_saved': 45.0},
            {'user': users[3], 'points': 95, 'food_saved': 9.5, 'carbon_saved': 23.75},
            {'user': users[4], 'points': 320, 'food_saved': 32.0, 'carbon_saved': 80.0},
        ]
        
        for idx, stat in enumerate(user_stats, 1):
            stat['user'].points = stat['points']
            stat['user'].food_saved = stat['food_saved']
            stat['user'].carbon_saved = stat['carbon_saved']
            stat['user'].save()
            
            leaderboard, created = Leaderboard.objects.get_or_create(
                user=stat['user'],
                defaults={
                    'total_points': stat['points'],
                    'total_food_saved': stat['food_saved'],
                    'total_carbon_saved': stat['carbon_saved'],
                    'rank': idx,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created leaderboard entry for: {stat["user"].username}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('\nSample Login Credentials:'))
        self.stdout.write(self.style.SUCCESS('Username: john_doe | Password: Pass123!'))
        self.stdout.write(self.style.SUCCESS('Username: green_restaurant | Password: Pass123!'))
        self.stdout.write(self.style.SUCCESS('Username: windsor_ngo | Password: Pass123!'))
        self.stdout.write(self.style.SUCCESS('Username: sarah_green | Password: Pass123!'))
        self.stdout.write(self.style.SUCCESS('Username: mike_chef | Password: Pass123!'))
        self.stdout.write(self.style.SUCCESS('='*50))

