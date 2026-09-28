"""Terminal weather checker using the free Open-Meteo API (no API key needed)."""

import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 10
FORECAST_DAYS = 3  # days to show after today

# Temperature units the user can pick: Open-Meteo's name and the display symbol.
UNITS = {
    "C": {"api_name": "celsius", "symbol": "°C"},
    "F": {"api_name": "fahrenheit", "symbol": "°F"},
}
DEFAULT_UNIT = "C"


def find_location(city):
    """Look up a city's coordinates. Return None if the city is not found."""
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    response = requests.get(GEOCODING_URL, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    # Open-Meteo leaves out the "results" key entirely when nothing matches.
    results = response.json().get("results")
    if not results:
        return None

    place = results[0]
    return {
        "name": place["name"],
        "country": place.get("country", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
    }


def parse_unit(answer):
    """Turn the user's answer into 'C' or 'F'. Return None if it isn't valid."""
    answer = answer.strip().upper()
    if answer == "":
        return DEFAULT_UNIT
    if answer in ("C", "CELSIUS"):
        return "C"
    if answer in ("F", "FAHRENHEIT"):
        return "F"
    return None


def get_weather(latitude, longitude, unit=DEFAULT_UNIT):
    """Fetch current conditions, today's high/low and the next days' forecast."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": UNITS[unit]["api_name"],  # the API converts for us
        "timezone": "auto",  # "today" in the city's own timezone
        "forecast_days": 1 + FORECAST_DAYS,  # today plus the days ahead
    }
    response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()
    daily = data["daily"]

    # Daily values are lists with one entry per day: index 0 is today.
    forecast = [
        {
            "date": daily["time"][day],
            "high": daily["temperature_2m_max"][day],
            "low": daily["temperature_2m_min"][day],
        }
        for day in range(1, 1 + FORECAST_DAYS)
    ]

    return {
        "temperature": data["current"]["temperature_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "high": daily["temperature_2m_max"][0],
        "low": daily["temperature_2m_min"][0],
        "forecast": forecast,
    }


def format_report(location, weather, unit=DEFAULT_UNIT):
    """Build the text shown to the user."""
    place = location["name"]
    if location["country"]:
        place += f", {location['country']}"
    symbol = UNITS[unit]["symbol"]

    return (
        f"Weather for {place}\n"
        f"  Temperature:  {weather['temperature']:.1f} {symbol}\n"
        f"  Wind speed:   {weather['wind_speed']:.1f} km/h\n"
        f"  Today:        high {weather['high']:.1f} {symbol}"
        f" / low {weather['low']:.1f} {symbol}"
    )


def main():
    city = input("Enter a city: ").strip()
    if not city:
        print("Please enter a city name.")
        sys.exit(1)

    unit = parse_unit(input("Celsius or Fahrenheit? [C/F, default C]: "))
    if unit is None:
        print("Please enter C or F.")
        sys.exit(1)

    try:
        location = find_location(city)
        if location is None:
            print(f"City not found: {city}")
            sys.exit(1)
        weather = get_weather(location["latitude"], location["longitude"], unit)
    except requests.RequestException as error:
        print(f"Could not reach the weather service: {error}")
        sys.exit(1)

    print(format_report(location, weather, unit))


if __name__ == "__main__":
    main()
