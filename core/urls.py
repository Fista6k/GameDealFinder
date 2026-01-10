from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.gameList, name="gameList"),
    path("games/<uuid:gameid>/", views.gameInfo, name="gameInfo")
]