import pytest

from src.models import Aeroplane


@pytest.fixture
def aeroplane():
    return Aeroplane(callsign="CALLSIGN", country="COUNTRY", velocity=1.0, altitude=2.0)


@pytest.fixture
def aeroplanes():
    aeroplanes = [
        Aeroplane("CALLSIGN1", "COUNTRY1", 1.0, 2.0),
        Aeroplane("CALLSIGN2", "COUNTRY2", 3.0, 4.0),
        Aeroplane("CALLSIGN3", "COUNTRY3", 5.0, 6.0),
        Aeroplane("CALLSIGN4", "COUNTRY3", 7.0, 8.0),
    ]

    return aeroplanes