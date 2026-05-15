import requests
import time

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,cloud_cover,precipitation,weather_code",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto",
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        hourly = data.get("hourly", {})

        # Average precipitation probability over next 6 hours
        precip_probs = hourly.get("precipitation_probability", [])
        precip_prob = round(sum(precip_probs[:6]) / 6, 1) if precip_probs else 0

        return {
            "temperature_2m": current.get("temperature_2m"),
            "cloud_cover": current.get("cloud_cover"),
            "precipitation": current.get("precipitation"),
            "precipitation_probability": precip_prob,
            "weather_code": current.get("weather_code"),
        }
    except Exception as e:
        return {
            "temperature_2m": None,
            "cloud_cover": None,
            "precipitation": None,
            "precipitation_probability": None,
            "weather_code": None,
            "error": str(e),
        }


def fetch_all_weather(points, delay=0.05):
    results = []
    for point in points:
        weather = fetch_weather(point["lat"], point["lon"])
        results.append({**point, **weather})
        time.sleep(delay)
    return results
