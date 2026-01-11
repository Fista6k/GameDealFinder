from django.core.management.base import BaseCommand
from django.db.models import Count
from ...models import PriceHistory

class Command(BaseCommand):
    help = "Чистка дубликатов цен"

    def handle(self, *args, **options):  
        dupes = (
            PriceHistory.objects
            .values(
                "game",
                "store",
                "discount_price",
                "currency"
            )
            .annotate(cnt=Count("id"))
            .filter(cnt__gt=1)
        )

        for d in dupes:
            ids = (
                PriceHistory.objects.filter(game=d["game"],
                                            store=d["store"],
                                            discount_price=d["discount_price"],
                                            currency=d["currency"]).order_by("recorded_at").values_list("id", flat=True)
            )

        PriceHistory.objects.exclude(id__in=[ids[0]]).delete()