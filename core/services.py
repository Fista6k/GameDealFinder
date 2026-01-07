import requests
from django.conf import settings


class ITADClient:
    BASE_URL = "https://api.isthereanydeal.com"

    def __init__(self):
        self.api_key = settings.ITAD_API_KEY

    def search_games(self, title, limit=20):
        responce = requests.get(f"{self.BASE_URL}/games/search/v1", params={
            "key": self.api_key,
            "title": title,
            "limit": 20
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    def get_game_info(self, plains):
        responce = requests.get(f"{self.BASE_URL}/games/info/v1", params={
            "key": self.api_key,
            "plains": ",".join(plains),
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    def get_prices(self, plains, country="DE", currency="EUR"):
        responce = requests.get(f"{self.BASE_URL}/games/prices/v2", params={
            "key": self.api_key,
            "plains": ",".join(plains),
            "country": country,
            "currency": currency
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    