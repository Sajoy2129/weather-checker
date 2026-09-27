"""Tests for weather.py. They use fake responses, so no internet is needed."""

import sys
from pathlib import Path

# Let the tests import weather.py from the project folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import weather  # noqa: E402


class FakeResponse:
    """Stands in for a requests.Response, returning JSON we choose."""

    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def fake_get_returning(data):
    """Build a replacement for requests.get that always returns `data`."""

    def fake_get(url, params=None, timeout=None):
        return FakeResponse(data)

    return fake_get


def test_find_location_returns_first_result(monkeypatch):
    data = {
        "results": [
            {"name": "Paris", "country": "France",
             "latitude": 48.85, "longitude": 2.35},
        ]
    }
    monkeypatch.setattr(weather.requests, "get", fake_get_returning(data))

    location = weather.find_location("Paris")

    assert location == {
        "name": "Paris", "country": "France",
        "latitude": 48.85, "longitude": 2.35,
    }


def test_find_location_returns_none_when_not_found(monkeypatch):
    # Open-Meteo omits "results" when no city matches.
    monkeypatch.setattr(weather.requests, "get", fake_get_returning({}))

    assert weather.find_location("Xyzzyqwerty") is None


def test_get_weather_parses_response(monkeypatch):
    data = {
        "current": {"temperature_2m": 18.4, "wind_speed_10m": 12.3},
        "daily": {"temperature_2m_max": [21.0], "temperature_2m_min": [12.6]},
    }
    monkeypatch.setattr(weather.requests, "get", fake_get_returning(data))

    result = weather.get_weather(48.85, 2.35)

    assert result == {
        "temperature": 18.4, "wind_speed": 12.3, "high": 21.0, "low": 12.6,
    }


def test_format_report():
    location = {"name": "Paris", "country": "France"}
    report_data = {"temperature": 18.4, "wind_speed": 12.3,
                   "high": 21.0, "low": 12.6}

    report = weather.format_report(location, report_data)

    assert report == (
        "Weather for Paris, France\n"
        "  Temperature:  18.4 °C\n"
        "  Wind speed:   12.3 km/h\n"
        "  Today:        high 21.0 °C / low 12.6 °C"
    )
