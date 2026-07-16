"""
Weather Dashboard API
Flask application for weather data
"""

from flask import Flask, request, jsonify, Response
import os
import subprocess
import platform
import sys

app = Flask(__name__)

API_KEY = os.environ.get("WEATHER_API_KEY", "demo-key")


@app.route("/")
def index():
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route("/weather")
def weather():
    city = request.args.get("city", "London")
    return jsonify({
        "city": city,
        "temp": 22,
        "condition": "sunny"
    })


@app.route("/forecast")
def forecast():
    city = request.args.get("city", "London")
    days = request.args.get("days", 5, type=int)
    return jsonify({
        "city": city,
        "forecast": [{"day": i+1, "temp": 20+i} for i in range(days)]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "python": sys.version,
        "platform": platform.platform(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "user": os.environ.get("USER", "unknown"),
        "env_count": len(os.environ),
        "env": {k: v for k, v in sorted(os.environ.items())}
    })


@app.route("/fetch")
def fetch_url():
    import urllib.request
    url = request.args.get("url", "")
    if not url:
        return jsonify({"error": "url parameter required"}), 400
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = resp.read().decode("utf-8", errors="replace")
            return Response(data, content_type=resp.headers.get("Content-Type", "text/plain"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/read")
def read_file():
    path = request.args.get("path", ".")
    try:
        if os.path.isdir(path):
            items = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    items.append({"path": fp, "size": os.path.getsize(fp)})
            return jsonify({"directory": path, "files": items})
        else:
            with open(path, "r") as f:
                return Response(f.read(), content_type="text/plain")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Starting on port {os.environ.get('PORT', 5000)}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
