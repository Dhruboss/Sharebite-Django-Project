from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('new/', views.food_create, name='food_create'),
    path('<int:pk>/', views.food_detail, name='food_detail'),
    path('<int:food_id>/request/', views.request_donation, name='request_donation'),
]