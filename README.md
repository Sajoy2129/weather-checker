# Weather Checker

A small terminal program that shows the current weather for any city, using
the free [Open-Meteo](https://open-meteo.com/) API. No sign-up or API key needed.

## Features

- Look up any city by name
- Current temperature (°C) and wind speed (km/h)
- Today's high and low, in the city's own timezone
- Friendly messages for empty input, unknown cities and network errors

## Example

```
$ python weather.py
Enter a city: Paris
Weather for Paris, France
  Temperature:  21.7 °C
  Wind speed:   9.7 km/h
  Today:        high 24.1 °C / low 17.6 °C
```

## Requirements

- Python 3
- [`requests`](https://pypi.org/project/requests/) for making web requests
- [`pytest`](https://pypi.org/project/pytest/) for running the tests

## Setup

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source .venv/bin/activate
python weather.py
```

Type a city name and press Enter.

## Running the tests

```bash
pytest -v
```

The tests replace real API calls with fake replies (using pytest's
`monkeypatch`), so they run quickly and work without an internet connection.

## How it works

The program makes two requests to Open-Meteo:

1. **Find the city**: `find_location()` sends the city name to the
   [geocoding API](https://open-meteo.com/en/docs/geocoding-api) and gets back
   its latitude and longitude.
2. **Get the weather**: `get_weather()` sends those coordinates to the
   [forecast API](https://open-meteo.com/en/docs) and gets back the current
   conditions and today's high and low.

`format_report()` then turns the results into the text you see.

```
"Paris" → geocoding API → (48.85, 2.35) → forecast API → weather report
```

## Project structure

```
weather_checker/
├── weather.py            # the program
├── tests/
│   └── test_weather.py   # pytest tests with faked API replies
├── requirements.txt      # Python dependencies
└── CLAUDE.md             # notes for Claude Code
```

## Credits

Weather data by [Open-Meteo.com](https://open-meteo.com/), licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
