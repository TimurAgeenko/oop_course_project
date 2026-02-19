import json
import os
from abc import ABC, abstractmethod

import requests


class BaseAPIHandler(ABC):

    @abstractmethod
    def get_aeroplanes(self, country: str) -> str:
        pass


class APIHandler(BaseAPIHandler):
    """Класс для обработки API запросов"""

    def __init__(self):
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search?"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> None:
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


class Aeroplane:
    """Класс для представления самолета"""

    def __init__(self, callsign: str, country: str, velocity: float, altitude: float):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    @classmethod
    def cast_to_object_list(cls, aeroplanes: list) -> list:
        """Метод для преобразования списка данных о самолетах в список объектов класса Aeroplane"""
        return [
            cls(callsign=aeroplane[1], country=aeroplane[2], velocity=aeroplane[9], altitude=aeroplane[13])
            for aeroplane in aeroplanes
        ]

    @staticmethod
    def get_top_altitude_aeroplanes(aeroplanes: list, top_n: int) -> list:
        """Метод для получения топ N самолетов по высоте"""
        sorted_aeroplanes = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
        return sorted_aeroplanes[:top_n]

    @staticmethod
    def get_aeroplanes_by_country(aeroplanes: list, country: str) -> list:
        """Метод для получения списка самолётов, отфильтрованных по стране регистрации"""
        return [aeroplane for aeroplane in aeroplanes if aeroplane.country == country]


class BaseJSONHandler(ABC):

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> str:
        pass

    @abstractmethod
    def get_aeroplane(self, callsign: str) -> dict | str:
        pass

    @abstractmethod
    def delete_aeroplane(self, callsign: str) -> str:
        pass


class JSONHandler(BaseJSONHandler):
    """Класс для работы с файлами в формате json."""

    def __init__(self, path: str = "../data/aeroplanes.json"):
        self.path = path

    def get_aeroplanes_list(self) -> list[dict]:
        """Метод для получения списка словарей с данными о самолетах."""
        if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
            with open(self.path, "r") as f:
                data = json.load(f)
        else:
            data = []

        return data

    def add_aeroplane(self, aeroplane: Aeroplane) -> str:
        """Метод для добавления информации о самолете в файл."""
        if not isinstance(aeroplane, Aeroplane):
            raise ValueError("Добавлять в файл можно только объекты класса Aeroplane.")

        data = self.get_aeroplanes_list()

        aeroplane_dict = {
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
        }

        data.append(aeroplane_dict)

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

        return "Информация о самолете добавлена в файл."

    def get_aeroplane(self, callsign: str) -> dict | str:
        """Метод для получения информации о самолете по его позывному."""
        data = self.get_aeroplanes_list()

        if data:
            aeroplane = [aeroplane for aeroplane in data if aeroplane["callsign"] == callsign]
            if aeroplane:
                return aeroplane[0]

        return "Самолет с указанным позывным отсутствует в файле."

    def delete_aeroplane(self, callsign: str) -> str:
        """Метод для удаления информации о самолете по его позывному"""
        data = self.get_aeroplanes_list()
        aeroplane = self.get_aeroplane(callsign)

        if aeroplane == "Самолет с указанным позывным отсутствует в файле.":
            return aeroplane

        data.remove(aeroplane)

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

        return "Самолет с указанным позывным успешно удален из файла"
