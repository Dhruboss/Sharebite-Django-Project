from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('new/', views.recipe_create, name='recipe_create'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]

