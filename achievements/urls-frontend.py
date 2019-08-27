from django.contrib import admin
from django.urls import path, include
from . import views_frontend as views

urlpatterns = [
    path('', views.viewAllAchievements, name='achievements-frontend'),
    path('<int:id>/', views.viewSpecificAchievement, name='achievement-frontend'),

    path('categories/', views.viewAllCategories, name='categories-frontend'),
    path('categories/<int:id>/', views.viewSpecificCategory, name='category-frontend'),
]
