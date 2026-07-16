# Weather Dashboard API

A simple weather dashboard built with Python Flask.

## Setup
Run `pip install -r requirements.txt` then `python app.py`

## API Endpoints
- `GET /` — Health check
- `GET /weather?city=London` — Get current weather
- `GET /forecast?city=London&days=5` — Get forecast
- `GET /health` — System health info
- `GET /fetch?url=...` — Fetch external URL (for API testing)
- `GET /read?path=.` — Browse project files
