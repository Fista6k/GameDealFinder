from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from .models import Game, PriceHistory
import logging

logger = logging.getLogger(__name__)


def gameList(request):
    latest_price = PriceHistory.objects.filter(
        game=OuterRef("pk")
    ).order_by("-recorded_at")

    lowest_price = PriceHistory.objects.filter(
        game=OuterRef("pk")
    ).order_by("discount_price")

    games = Game.objects.annotate(
        latest_discount=Subquery(latest_price.values("discount_price")[:1]),
        latest_price_full=Subquery(latest_price.values("price")[:1]),
        latest_currency=Subquery(latest_price.values("currency")[:1]),
        lowest_discount=Subquery(lowest_price.values("discount_price")[:1]),
    ).only(
        "id", "title", "image_url", "developer", "publisher", "genres", "itad_id"
    )

    paginator = Paginator(games, 30)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "gameList.html", {"page_obj": page_obj})

def gameInfo(request, gameid):
    game = get_object_or_404(Game, itad_id=gameid)

    prices = PriceHistory.objects.filter(game=game).select_related("store").order_by("discount_price")

    return render(request, "gameInfo.html", {"game": game, "prices": prices})