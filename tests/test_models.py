import pytest

from src.models import Aeroplane


def test_aeroplane_initialization(aeroplane):
    assert aeroplane.callsign == "CALLSIGN"
    assert aeroplane.country == "COUNTRY"
    assert aeroplane.velocity == 1.0
    assert aeroplane.altitude == 2.0


def test_aeroplane_str(aeroplane):
    aeroplane_str = str(aeroplane)
    assert str(aeroplane) == aeroplane_str


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
