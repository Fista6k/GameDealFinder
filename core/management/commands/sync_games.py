from django.core.management.base import BaseCommand
from ...models import Game
from ...services.itad import ITADClient

class Command(BaseCommand):
    help = "Импорт игр из IsThereAnyDeal"

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Название игры")

    def handle(self, *args, **options):
        client = ITADClient()
        title = options["title"]

        results = client.search_games(title)

        if not results:
            self.stdout.write(self.style.WARNING("Игры не найдены"))
            return

        created = 0

        for game in results:
            slug = game.get("slug")

            obj, is_created = Game.objects.update_or_create(
                itad_plain=slug,
                defaults={
                    "title": game.get("title", ""),
                    "description": "",
                    "image_url": game.get("assets", {}).get("boxart", "")
                }
            )

            if is_created:
                created += 1
        
        self.stdout.write(self.style.SUCCESS(f"Готово. Добавлено игр: {created}"))
