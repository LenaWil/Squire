from django.urls import path

from boardgames.views import BoardGameView

app_name = "boardgames"

urlpatterns = [
    # Change Language helper view
    path("", BoardGameView.as_view(), name="home"),
]
