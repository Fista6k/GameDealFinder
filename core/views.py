from django.shortcuts import render
from .models import Game

def gameList(request):
    games = Game.objects.all().prefetch_related("prices", "prices__store")
    for g in games:
        g.latest_price = g.get_current_price()
        g.lowest_price = g.get_lowest_price()
    return render(request, "gameList.html", {"games": games})