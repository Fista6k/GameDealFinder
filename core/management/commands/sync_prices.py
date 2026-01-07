from django.core.management.base import BaseCommand
from django.db import transaction
from models import Game, Store, PriceHistory
from GameDealFinder.core.services.itad import ITADClient


class Command(BaseCommand):
    help = "Обновление цен из ITAD"
    
    def handle(self, *args, **options):
        client = ITADClient()
        games = Game.objects.all()

        plains = [game.itad_plain for game in games]
        prices_data = client.get_prices(plains)

        with transaction.atomic():
            for plain, offers in prices_data.items():
                game = Game.objects.get(itad_plain=plain)

                for offer in offers:
                    shop = offer["shop"]

                    store, _ = Store.objects.get_or_create(
                        itad_id = shop["id"],
                        defaults={
                            "name":shop["name"],
                            "website": shop.get("url", "")
                        }
                    )

                    PriceHistory.objects.create(
                        game=game,
                        store=store,
                        price=offer["price"]["old"],
                        discount_price=offer["price"]["new"],
                        discount_percent=offer["price"]["cut"],
                        currency=offer["price"]["currency"],
                        store_url=offer.get("url", "")
                    )
        
        self.stdout.write(self.style.SUCCESS("Цены обновлены"))