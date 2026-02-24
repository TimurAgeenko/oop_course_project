import json
import os
from unittest.mock import Mock, patch

import pytest

from src.models import Aeroplane, APIHandler, JSONHandler


def make_osm_response(bbox):
    resp = Mock()
    resp.json.return_value = [{"boundingbox": bbox}]
    return resp


def make_opensky_response(states):
    resp = Mock()
    resp.json.return_value = {"states": states}
    return resp


@patch("src.models.requests.get")
def test_get_aeroplanes(mock_get):
    bbox = ["-44.0", "-10.0", "112.0", "154.0"]
    osm_resp = make_osm_response(bbox)

    sample_state = ["abc123", "CALLSIGN", "", 0.0, 0.0, 1.0, 2.0, 3.0]
    opensky_resp = make_opensky_response([sample_state])

    mock_get.side_effect = [osm_resp, opensky_resp]

    api = APIHandler()
    api.get_aeroplanes("australia")

    assert api.aeroplanes == [sample_state]

    assert mock_get.call_count == 2

    calls = mock_get.call_args_list

    first_call = calls[0]
    assert first_call[0][0] == api.openstreetmap_url
    assert first_call[1]["params"]["q"] == "australia"

    second_call = calls[1]
    assert second_call[0][0] == api.opensky_url
    assert second_call[1]["params"]["lamin"] == bbox[0]
    assert second_call[1]["params"]["lamax"] == bbox[1]
    assert second_call[1]["params"]["lomin"] == bbox[2]
    assert second_call[1]["params"]["lomax"] == bbox[3]


def test_aeroplane_initialization(aeroplane):
    assert aeroplane.callsign == "CALLSIGN"
    assert aeroplane.country == "COUNTRY"
    assert aeroplane.velocity == 1.0
    assert aeroplane.altitude == 2.0


def test_cast_to_object_list():
    aeroplanes = [[None, "CALLSIGN", "COUNTRY", None, None, None, None, None, None, 1.0, None, None, None, 2.0]]
    objects = Aeroplane.cast_to_object_list(aeroplanes)

    assert len(objects) == 1
    assert objects[0].callsign == "CALLSIGN"
    assert objects[0].country == "COUNTRY"
    assert objects[0].velocity == 1.0
    assert objects[0].altitude == 2.0


def test_get_top_altitude_aeroplanes(aeroplanes):
    top_aeroplanes = Aeroplane.get_top_altitude_aeroplanes(aeroplanes, top_n=2)

    assert len(top_aeroplanes) == 2
    assert top_aeroplanes[0].callsign == "CALLSIGN4"
    assert top_aeroplanes[1].callsign == "CALLSIGN3"


def test_get_aeroplanes_by_country(aeroplanes):
    sorted_aeroplanes = Aeroplane.get_aeroplanes_by_country(aeroplanes, ["COUNTRY1", "COUNTRY3"])

    assert len(sorted_aeroplanes) == 3
    assert sorted_aeroplanes[0].callsign == "CALLSIGN1"
    assert sorted_aeroplanes[1].callsign == "CALLSIGN3"
    assert sorted_aeroplanes[2].callsign == "CALLSIGN4"


def test_get_aeroplanes_by_altitude(aeroplanes):
    sorted_aeroplanes = Aeroplane.get_aeroplanes_by_altitude(aeroplanes, "3-7")

    assert len(sorted_aeroplanes) == 2
    assert sorted_aeroplanes[0].callsign == "CALLSIGN2"
    assert sorted_aeroplanes[1].callsign == "CALLSIGN3"


def test_get_aeroplanes_by_altitude_invalid_format(aeroplanes):
    with pytest.raises(ValueError, match="Высота должна быть задана в виде строки, например: '10000-20000'"):
        Aeroplane.get_aeroplanes_by_altitude(aeroplanes, "invalid_format")


def test_get_aeroplanes_list():
    handler = JSONHandler("./data/test.json")

    assert handler.get_aeroplanes_list() == []

    data = [{"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}]

    with open(handler.path, "w") as f:
        json.dump(data, f, indent=4)

    assert handler.get_aeroplanes_list() == [
        {"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}
    ]

    os.remove(handler.path)


def test_add_aeroplane(aeroplane):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplane(aeroplane)

    assert handler.get_aeroplanes_list() == [
        {"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}
    ]

    os.remove(handler.path)


def test_add_aeroplane_value_error():
    handler = JSONHandler("./data/test.json")

    with pytest.raises(ValueError, match="Добавлять в файл можно только объекты класса Aeroplane."):
        handler.add_aeroplane("aeroplane")


def test_get_aeroplane(aeroplane):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplane(aeroplane)

    airplane = handler.get_aeroplane("CALLSIG")
    assert airplane == "Самолет с указанным позывным отсутствует в файле."

    airplane = handler.get_aeroplane("CALLSIGN")
    assert airplane.get("callsign") == "CALLSIGN"

    os.remove(handler.path)


def test_delete_aeroplane(aeroplane):
    handler = JSONHandler("./data/test.json")

    handler.add_aeroplane(aeroplane)

    airplane = handler.delete_aeroplane("CALLSIG")
    assert airplane == "Самолет с указанным позывным отсутствует в файле."

    airplane = handler.delete_aeroplane("CALLSIGN")
    assert airplane == "Самолет с указанным позывным успешно удален из файла."

    os.remove(handler.path)
