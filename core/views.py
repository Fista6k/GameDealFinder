from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Game, PriceHistory

def gameList(request):
    games = Game.objects.all().prefetch_related("prices", "prices__store")
    for g in games:
        g.latest_price = g.get_current_price()
        g.lowest_price = g.get_lowest_price()

    paginator = Paginator(games, 30)
    page_number = request.GET.get("page")

    pageObj = paginator.get_page(page_number)
    
    return render(request, "gameList.html", {"page_obj": pageObj})

def gameInfo(request, gameid):
    game = get_object_or_404(Game, itad_id=gameid)

    prices = PriceHistory.objects.filter(game=game).select_related("store").order_by("discount_price")

    return render(request, "gameInfo.html", {"game": game, "prices": prices})