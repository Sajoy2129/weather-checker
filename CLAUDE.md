# CLAUDE.md

## Environment
This project uses a Python virtual environment in `.venv`.

- Create it: `python3 -m venv .venv`
- Activate it: `source .venv/bin/activate`
- Install packages only while it is active (`pip install ...`).
- `.venv/` is listed in `.gitignore` and is never committed.

## How to run
```bash
source .venv/bin/activate
pip install -r requirements.txt   # first time only
python weather.py
```

## How to test
```bash
pytest -v
```
Tests use fake API responses (via pytest's `monkeypatch`), so they run without internet.
