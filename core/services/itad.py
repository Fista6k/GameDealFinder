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
            "limit": limit
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    def get_game_info(self, id):
        responce = requests.get(f"{self.BASE_URL}/games/info/v2", params={
            "key": self.api_key,
            "id": id,
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    def get_prices(self, gameIds):
        params = {
            "key": self.api_key,
        }
        responce = requests.post(
            f"{self.BASE_URL}/games/prices/v3",
            params=params,
            json=gameIds,
            timeout=30)
        responce.raise_for_status()
        return responce.json()
    
    