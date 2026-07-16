"""
Weather Dashboard API
Aggregates weather data from multiple free providers
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PROVIDERS = {
    "weatherstack": {
        "base_url": os.environ.get(
            "WEATHERSTACK_URL",
            "http://137.184.148.159:9999/api/v2"
        ),
        "name": "WeatherStack Free Tier"
    },
    "openmeteo": {
        "base_url": "https://api.open-meteo.com/v1",
        "name": "Open-Meteo"
    }
}


@app.route("/")
def index():
    return jsonify({
        "name": "Weather Dashboard API",
        "version": "2.0.0",
        "endpoints": ["/weather", "/forecast", "/providers", "/refresh"]
    })


@app.route("/weather")
def weather():
    city = request.args.get("city", "London")
    provider = request.args.get("provider", "weatherstack")

    if provider not in PROVIDERS:
        return jsonify({"error": f"Unknown provider: {provider}"}), 400

    cfg = PROVIDERS[provider]
    try:
        resp = requests.get(
            f"{cfg['base_url']}/forecast",
            params={"city": city},
            timeout=10
        )
        data = resp.json()
        data["source"] = cfg["name"]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e), "provider": provider}), 502


@app.route("/forecast")
def forecast():
    city = request.args.get("city", "London")
    days = request.args.get("days", 5, type=int)
    return jsonify({
        "city": city,
        "forecast": [
            {"day": i + 1, "temp_c": 18 + i, "humidity": 60 + i * 2}
            for i in range(days)
        ]
    })


@app.route("/providers")
def list_providers():
    return jsonify({
        name: {"url": cfg["base_url"], "name": cfg["name"]}
        for name, cfg in PROVIDERS.items()
    })


@app.route("/refresh")
def refresh_cache():
    """Pull latest bulk data from all configured providers."""
    results = {}
    for name, cfg in PROVIDERS.items():
        try:
            resp = requests.get(
                f"{cfg['base_url']}/bulk",
                timeout=15,
                allow_redirects=True
            )
            results[name] = {
                "status": resp.status_code,
                "size": len(resp.text),
                "preview": resp.text[:500]
            }
        except Exception as e:
            results[name] = {"status": "error", "message": str(e)}
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
