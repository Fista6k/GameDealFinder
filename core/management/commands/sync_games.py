from django.core.management.base import BaseCommand
from ...models import Game
from ...services.itad import ITADClient

class Command(BaseCommand):
    help = "Импорт игр из IsThereAnyDeal"

    def handle(self, *args, **options):
        client = ITADClient()
        all_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        totalAdded = 0

        for ch in all_chars:
            self.stdout.write(f"Fetching games starting with '{ch}'")
            results = client.search_games(ch, limit=1000)

            for game in results:
                gameInfo = client.get_game_info(game["id"])

                if gameInfo is None:
                    continue
                
                slug = gameInfo.get("slug", "")
                if not slug:
                    continue

                publishers = []
                for pub in gameInfo.get("publishers", []):
                    publishers.append(pub["name"])

                devs = []
                for dev in gameInfo.get("developers", []):
                    devs.append(dev["name"])

                obj, is_created = Game.objects.update_or_create(
                    itad_plain=slug,
                    defaults={
                        "itad_id": game.get("id", ""),
                        "title": game.get("title", ""),
                        "release_date": gameInfo.get("releaseDate", ""),
                        "developer": devs,
                        "publisher": publishers,
                        "genres": ", ".join(gameInfo.get("tags", {})),
                        "image_url": game.get("assets", {}).get("boxart", "")
                    }
                )
                totalAdded += 1
        
        self.stdout.write(self.style.SUCCESS(f"Готово. Добавлено игр: {totalAdded}"))
