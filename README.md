# Weather Dashboard API

A weather aggregator that pulls from multiple free providers (WeatherStack, Open-Meteo).

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## Endpoints
- `GET /` — API info
- `GET /weather?city=London&provider=weatherstack` — Current weather
- `GET /forecast?city=London&days=5` — Multi-day forecast
- `GET /providers` — List configured providers
- `GET /refresh` — Refresh cached provider data

## Environment Variables
- `PORT` — Server port (default: 5000)
- `WEATHERSTACK_URL` — Override WeatherStack API base URL
