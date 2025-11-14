from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('<int:donation_id>/', views.donation_detail, name='donation_detail'),
    path('<int:donation_id>/accept/', views.accept_donation, name='accept_donation'),
    path('<int:donation_id>/complete/', views.complete_donation, name='complete_donation'),
]