import requests
from django.conf import settings
from requests.exceptions import RequestException, Timeout
import time


class ITADClient:
    BASE_URL = "https://api.isthereanydeal.com"

    def __init__(self):
        self.api_key = settings.ITAD_API_KEY

    def search_games(self, title, limit=20):
        responce = requests.get(f"{self.BASE_URL}/games/search/v1", params={
            "key": self.api_key,
            "title": title,
            "results": limit
        }, timeout=10)
        responce.raise_for_status()
        return responce.json()
    
    def get_game_info(self, id, retries=3):
        for attempt in range(retries):
            try:
                responce = requests.get(f"{self.BASE_URL}/games/info/v2", params={
                    "key": self.api_key,
                    "id": id,
                }, timeout=10)
                responce.raise_for_status()
                return responce.json()
            except Timeout:
                time.sleep(2 ** attempt)
        return None
    
    def get_prices(self, gameIds, retries=3):
        for attempt in range(retries):
            try:
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
            except Timeout:
                time.sleep(2 ** attempt)
        return None
    
    