import datetime as dt
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
    def get_aeroplanes_by_country(aeroplanes: list, countries: list) -> list:
        """Метод для получения списка самолётов, отфильтрованных по стране регистрации"""
        return [aeroplane for aeroplane in aeroplanes if aeroplane.country in countries]

    @staticmethod
    def get_aeroplanes_by_altitude(aeroplanes: list, altitude: str) -> list:
        """Метод для получения списка самолётов, отфильтрованных по высоте,
        высота задается в виде строки, например: "10000-20000" """
        altitude_range = altitude.split("-")
        if len(altitude_range) != 2:
            raise ValueError("Высота должна быть задана в виде строки, например: '10000-20000'")

        try:
            min_altitude = float(altitude_range[0])
            max_altitude = float(altitude_range[1])
        except ValueError:
            raise ValueError("Высота должна быть задана в виде строки, например: '10000-20000'")

        return [aeroplane for aeroplane in aeroplanes if min_altitude <= aeroplane.altitude <= max_altitude]


class BaseJSONHandler(ABC):

    @abstractmethod
    def add_aeroplanes(self, aeroplanes_list: list[Aeroplane], country: str) -> str:
        pass

    @abstractmethod
    def get_aeroplane(self, callsign: str) -> dict | str:
        pass

    @abstractmethod
    def delete_aeroplane(self, callsign: str) -> str:
        pass


class JSONHandler(BaseJSONHandler):
    """Класс для работы с файлами в формате json."""

    def __init__(self, path: str = "./data/aeroplanes.json"):
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def get_aeroplanes_list(self, country: str = None, date: str = None) -> list[dict]:
        """Метод для получения списка словарей с данными о самолетах."""
        if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
            with open(self.path, "r") as f:
                data = json.load(f)
            if country and date:
                data = [item["aeroplanes"] for item in data if item["country"] == country and item["date"] == date][0]
        else:
            data = []

        return data

    def add_aeroplanes(self, aeroplanes_list: list[Aeroplane], country: str) -> str:
        """Метод для добавления информации о самолетах в файл."""
        data = self.get_aeroplanes_list()
        date = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        aeroplanes_info = []

        for aeroplane in aeroplanes_list:
            if not isinstance(aeroplane, Aeroplane):
                raise ValueError("Добавлять в файл можно только объекты класса Aeroplane.")

            aeroplane_dict = {
                "callsign": aeroplane.callsign,
                "country": aeroplane.country,
                "velocity": aeroplane.velocity,
                "altitude": aeroplane.altitude,
            }

            aeroplanes_info.append(aeroplane_dict)

        result = {"country": country, "date": date, "aeroplanes": aeroplanes_info}

        data.append(result)

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

        return "Информация о самолете добавлена в файл."

    def get_aeroplane(self, callsign: str) -> dict | str:
        """Метод для получения информации о самолете по его позывному."""
        data = self.get_aeroplanes_list()

        if data:
            aeroplane = [
                aeroplane for item in data for aeroplane in item["aeroplanes"] if aeroplane["callsign"].replace(" ", "") == callsign
            ]
            if aeroplane:
                return aeroplane[0]

        return "Самолет с указанным позывным отсутствует в файле."

    def delete_aeroplane(self, callsign: str) -> str:
        """Метод для удаления информации о самолете по его позывному"""
        data = self.get_aeroplanes_list()
        aeroplane = self.get_aeroplane(callsign)

        if aeroplane == "Самолет с указанным позывным отсутствует в файле.":
            return aeroplane

        item_index = [
            data.index(item) for item in data for aeroplane in item["aeroplanes"] if aeroplane["callsign"].replace(" ", "") == callsign
        ][0]

        item = data.pop(item_index)
        item["aeroplanes"].remove(aeroplane)
        data.append(item)

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

        return "Самолет с указанным позывным успешно удален из файла."
