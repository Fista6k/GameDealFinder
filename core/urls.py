from django.urls import path
from . import views

urlpatterns = [
    path("", views.gameList, name="gameList"),
    path("games/<uuid:gameid>/", views.gameInfo, name="gameInfo")
]