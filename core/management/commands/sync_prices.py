from django.core.management.base import BaseCommand
from ...models import Game, Store, PriceHistory
from ...services.itad import ITADClient
from decimal import Decimal
from django.utils import timezone
from datetime import datetime


BATCH_SIZE = 200
DuplicateCheckHours = 1

class Command(BaseCommand):
    help = "Обновление цен из ITAD"

    def handle(self, *args, **options):
        games = Game.objects.exclude(itad_id__isnull=True)

        if not games.exists():
            self.stdout.write((self.style.WARNING("No games with itad_id found")))
            return

        game_map = {str(game.itad_id): game for game in games}
        gameIds = list(game_map.keys())

        self.stdout.write(f"Syncing prices for {len(gameIds)} games")

        for i in range(0, len(gameIds), BATCH_SIZE):
            batch = gameIds[i:i + BATCH_SIZE]
            self.sync_batch(batch, game_map)

        self.stdout.write(self.style.SUCCESS("Price sync completed"))
    
    def sync_batch(self, gameIds, game_map):
        client = ITADClient()
        data = client.get_prices(gameIds)
        for item in data:
            game = game_map.get(item["id"])
            if not game:
                continue
            self.save_price(game, item)
    
    def save_price(self, game, entry):
        deals = entry.get("deals", [])
        if not deals:
            return
        
        history_low = entry.get("historyLow")

        hL = None
        if isinstance(history_low, dict):
            all_low = history_low.get("all")
            if isinstance(all_low, dict):
                hL = all_low.get("amount")

        history_low = Decimal(str(hL)) if hL is not None else None

        new_prices = []

        for deal in deals:
            shop_data = deal["shop"]
            nameShop = shop_data["name"]
            website = ""
            if nameShop == "Steam":
                website = "https://store.steampowered.com/"
            elif nameShop == "GOG":
                website = "https://www.gog.com/"
            elif nameShop == "Epic Game Store":
                website = "https://store.epicgames.com/"
            price_data = deal["price"]
            regular_data = deal.get("regular")

            store, _ = Store.objects.get_or_create(
                itad_id = shop_data["id"],
                defaults={
                    "name": nameShop,
                    "website": website
                }
            )

            price = Decimal(price_data["amount"])
            regular_price = Decimal(regular_data["amount"] if regular_data else price)

            discount_percent = deal.get("cut", 0)

            recorded_at = self.normalize_time(deal["timestamp"])

            priceObj = PriceHistory(
                game=game,
                store=store,
                recorded_at=recorded_at,
                price=regular_price,
                discount_price= price,
                discount_percent= discount_percent,
                is_history_low= (price==history_low),
                currency= price_data["currency"]
            )
            new_prices.append(priceObj)
        
        PriceHistory.objects.bulk_create(
            new_prices, ignore_conflicts=True
        )

    @staticmethod
    def normalize_time(ts, hours=6):
        if ts is None:
            return timezone.now()
        
        if isinstance(ts, (int, float)) or (isinstance(ts, str) and ts.isdigit()):
            dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        elif isinstance(ts, str):
            dt = datetime.fromisoformat(ts)

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        else:
            return timezone.now()
        
        return dt.replace(
            minute=0,
            second=0,
            microsecond=0,
            hour=(dt.hour // hours) * hours
        )