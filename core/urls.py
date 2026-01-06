from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("games/", views.gameList, name="gameList"),
    path("games/<int:gameId>/", views.gameDetail, name="gameDetail")
]