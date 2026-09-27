"""Terminal weather checker using the free Open-Meteo API (no API key needed)."""

import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 10


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


def get_weather(latitude, longitude):
    """Fetch current temperature, wind speed and today's high/low."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",  # "today" in the city's own timezone
        "forecast_days": 1,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()

    return {
        "temperature": data["current"]["temperature_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "high": data["daily"]["temperature_2m_max"][0],
        "low": data["daily"]["temperature_2m_min"][0],
    }


def format_report(location, weather):
    """Build the text shown to the user."""
    place = location["name"]
    if location["country"]:
        place += f", {location['country']}"

    return (
        f"Weather for {place}\n"
        f"  Temperature:  {weather['temperature']:.1f} °C\n"
        f"  Wind speed:   {weather['wind_speed']:.1f} km/h\n"
        f"  Today:        high {weather['high']:.1f} °C"
        f" / low {weather['low']:.1f} °C"
    )


def main():
    city = input("Enter a city: ").strip()
    if not city:
        print("Please enter a city name.")
        sys.exit(1)

    try:
        location = find_location(city)
        if location is None:
            print(f"City not found: {city}")
            sys.exit(1)
        weather = get_weather(location["latitude"], location["longitude"])
    except requests.RequestException as error:
        print(f"Could not reach the weather service: {error}")
        sys.exit(1)

    print(format_report(location, weather))


if __name__ == "__main__":
    main()
