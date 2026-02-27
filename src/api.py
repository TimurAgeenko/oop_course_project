from abc import ABC, abstractmethod

import requests


class BaseAPIHandler(ABC):

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list]:
        pass


class APIHandler(BaseAPIHandler):
    """Класс для обработки API запросов"""

    def __init__(self):
        self.__openstreetmap_url = "https://nominatim.openstreetmap.org/search?"
        self.__opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> list[list]:
        """Метод для получения информации о самолетах, находящихся в воздухе над определенной страной"""
        headers = {
            "User-Agent": "test-app",
        }

        params = {"q": country, "format": "json"}

        response = requests.get(self.__openstreetmap_url, params=params, headers=headers)

        data = response.json()

        geo_coordinates = data[0].get("boundingbox")

        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

        response = requests.get(self.__opensky_url, params=params)

        self.aeroplanes = response.json()["states"]

        return self.aeroplanes
