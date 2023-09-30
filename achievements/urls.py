from django.urls import path

from . import views

urlpatterns = [
    path("achievements", views.viewAchievementsAll, name="achievements/all"),
]
