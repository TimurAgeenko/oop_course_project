import json
import os

import pytest

from src.file_handler import JSONHandler


def test_get_aeroplanes_list():
    handler = JSONHandler("./data/test.json")

    assert handler.get_aeroplanes_list() == []

    data = [
        {
            "country": "Canada",
            "date": "24-02-2026 21:10:45",
            "aeroplanes": [{"callsign": "CALLSIGN1", "country": "COUNTRY1", "velocity": 1.0, "altitude": 2.0}],
        },
        {
            "country": "Australia",
            "date": "24.02.2026 22:10:45",
            "aeroplanes": [{"callsign": "CALLSIGN2", "country": "COUNTRY2", "velocity": 2.0, "altitude": 4.0}],
        },
    ]

    with open(handler.path, "w") as f:
        json.dump(data, f, indent=4)

    assert handler.get_aeroplanes_list() == data
    assert handler.get_aeroplanes_list("Australia", "24.02.2026 22:10:45") == data[1]["aeroplanes"]

    os.remove(handler.path)


def test_add_aeroplane(aeroplanes):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplanes(aeroplanes, "Canada")
    data = handler.get_aeroplanes_list()

    assert len(data) == 1
    assert data[0]["country"] == "Canada"
    assert data[0]["aeroplanes"][0]["callsign"] == "CALLSIGN1"
    assert data[0]["aeroplanes"][1]["callsign"] == "CALLSIGN2"

    os.remove(handler.path)


def test_add_aeroplane_value_error():
    handler = JSONHandler("./data/test.json")

    with pytest.raises(ValueError, match="Добавлять в файл можно только объекты класса Aeroplane."):
        handler.add_aeroplanes("aeroplane", "Canada")


def test_get_aeroplane(aeroplanes):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplanes(aeroplanes, "Canada")

    airplane = handler.get_aeroplane("CALLSIGN")
    assert airplane == "Самолет с указанным позывным отсутствует в файле."

    airplane = handler.get_aeroplane("CALLSIGN1")
    assert airplane["callsign"] == "CALLSIGN1"

    os.remove(handler.path)


def test_delete_aeroplane(aeroplanes):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplanes(aeroplanes, "Canada")

    airplane = handler.delete_aeroplane("CALLSIGN")
    assert airplane == "Самолет с указанным позывным отсутствует в файле."

    airplane = handler.delete_aeroplane("CALLSIGN1")
    assert airplane == "Самолет с указанным позывным успешно удален из файла."

    os.remove(handler.path)
