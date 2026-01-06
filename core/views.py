from django.shortcuts import render
from .models import Game, PriceHistory, Store
from django.http import HttpResponse
from django.db.models import Min, Avg


def home(request):
    totalGames = Game.objects.count()

    bestDeals = PriceHistory.objects.filter(discountPercent__gte=50).order_by("-discountPercent")[:5]
    avgDiscount = PriceHistory.objects.aggregate(avg=Avg("discountPercent"))["avg"] or 0

    context = {
        "totalGames": totalGames,
        "bestDeals": bestDeals,
        "avgDiscount": round(avgDiscount, 1),
        "title": "Главная страница"
    }

    return render(request, "home.html", context)

def gameList(request):
    games = Game.objects.all().order_by("title")

    gameData = []
    for game in games:
        currentPrice = game.getCurrentPrice()
        gameData.append({
            "game": game,
            "currentPrice": currentPrice
        })

    context = {
        "gameData": gameData,
        "title": "Все игры"
    }

    return render(request, "gameList.html", context)

def gameDetail(request, gameId):
    game = Game.objects.get(id=gameId)

    prices = PriceHistory.objects.filter(game=game).order_by("-recordedAt")

    historicalLow = PriceHistory.objects.filter(game=game, isLowest=True).first()

    currentPrices = {}
    stores = ["steam", "epic", "gog"]
    for storeName in stores:
        latest = PriceHistory.objects.filter(game=game, store__name=storeName).order_by("-recordedAt").first()
        if latest:
            currentPrices[storeName] = latest
    
    context = {
        "game": game,
        "prices": prices,
        "historicalLow": historicalLow,
        "currentPrices": currentPrices,
        "title": game.title      
    }

    return render(request, "gameDetail.html", context)
