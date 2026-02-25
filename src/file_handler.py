import datetime as dt
import json
import os
from abc import ABC, abstractmethod

from src.models import Aeroplane


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
                aeroplane
                for item in data
                for aeroplane in item["aeroplanes"]
                if aeroplane["callsign"].replace(" ", "") == callsign
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
            data.index(item)
            for item in data
            for aeroplane in item["aeroplanes"]
            if aeroplane["callsign"].replace(" ", "") == callsign
        ][0]

        item = data.pop(item_index)
        item["aeroplanes"].remove(aeroplane)
        data.append(item)

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

        return "Самолет с указанным позывным успешно удален из файла."
