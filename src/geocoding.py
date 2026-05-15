import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_city(city_name: str) -> tuple[float, float, str]:
    """
    Returns (latitude, longitude, display_name) for the best match.
    Raises ValueError with a human-readable message on failure.
    """
    params = {"name": city_name.strip(), "count": 1, "language": "en", "format": "json"}
    try:
        resp = requests.get(GEOCODING_URL, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results", [])
    except Exception as e:
        raise ValueError(f"Geocoding request failed: {e}")

    if not results:
        raise ValueError(
            f"No location found for \"{city_name}\". "
            "Try a larger nearby city or check the spelling."
        )

    r = results[0]
    name = r.get("name", city_name)
    country = r.get("country", "")
    display_name = f"{name}, {country}" if country else name
    return float(r["latitude"]), float(r["longitude"]), display_name
