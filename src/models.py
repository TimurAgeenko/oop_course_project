from abc import ABC, abstractmethod

import requests


class BaseAPIHandler(ABC):

    @abstractmethod
    def get_aeroplane(self, country: str) -> str:
        pass


class APIHandler(BaseAPIHandler):
    """Класс для обработки API запросов"""

    def __init__(self):
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search?"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_aeroplane(self, country: str) -> None:
        """Метод для получения информации о самолетах, находящихся в воздухе над определенной страной"""
        headers = {
            "User-Agent": "test-app",
        }

        params = {"q": country, "format": "json"}

        response = requests.get(self.openstreetmap_url, params=params, headers=headers)

        data = response.json()

        geo_coordinates = data[0].get("boundingbox")

        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

        response = requests.get(self.opensky_url, params=params)

        self.aeroplanes = response.json()["states"]
