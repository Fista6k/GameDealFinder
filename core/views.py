from django.shortcuts import render, get_object_or_404
from .models import Game, PriceHistory

def gameList(request):
    games = Game.objects.all().prefetch_related("prices", "prices__store")
    for g in games:
        g.latest_price = g.get_current_price()
        g.lowest_price = g.get_lowest_price()
    return render(request, "gameList.html", {"games": games})

def gameInfo(request, gameid):
    game = get_object_or_404(Game, itad_id=gameid)

    prices = PriceHistory.objects.filter(game=game).select_related("store").order_by("discount_price")

    return render(request, "gameInfo.html", {"game": game, "prices": prices})