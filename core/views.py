from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, Q
from .models import Game, PriceHistory, WaitList
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, WaitlistForm


def gameList(request):
    query = request.GET.get("q", "")

    games = Game.objects.all()
    if query:
        games = games.filter(
            Q(title__icontains=query) | Q(developer__icontains=query) | Q(publisher__icontains=query)
        )

    latest_price = PriceHistory.objects.filter(
        game=OuterRef("pk")
    ).order_by("-recorded_at")

    lowest_price = PriceHistory.objects.filter(
        game=OuterRef("pk")
    ).order_by("discount_price")

    games = games.annotate(
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

    in_waitlist = False
    if request.user.is_authenticated:
        in_waitlist = WaitList.objects.filter(
            user = request.user,
            game=game
        ).exists()

    prices = PriceHistory.objects.filter(game=game).select_related("store").order_by("discount_price")

    return render(request, "gameInfo.html", {"game": game, "prices": prices, "game_in_waitlist": in_waitlist})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("gameList")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("gameList")
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect("gameList")

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def add_to_waitlist(request, gameid):
    game = get_object_or_404(Game, itad_id=gameid)

    if request.method == "POST":
        form = WaitlistForm(request.POST)

        if form.is_valid():
            target_price = form.cleaned_data["target_price"]

            WaitList.objects.get_or_create(
                user = request.user,
                game=game,
                defaults={"target_price": target_price}
            )

            return redirect("waitlist")
    else:
        form = WaitlistForm()

    return render(request, "add_to_waitlist.html", {"form": form, "game": game})

@login_required
def remove_from_waitlist(request, gameid):
    game = get_object_or_404(Game, itad_id=gameid)
    WaitList.objects.filter(
        user=request.user,
        game=game
    ).delete()

    return redirect("waitlist")

@login_required
def waitlist_view(request):
    waitlist = (
        WaitList.objects.filter(user=request.user).select_related("game").order_by("-created_at")
    )

    return render(request, "waitlist.html", {"waitlist": waitlist})