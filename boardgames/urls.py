from django.urls import include, path

from boardgames.views import *

app_name = "boardgames"

urlpatterns = [
    # Change Language helper view
    path("", BoardGameView.as_view(), name="home"),
]
