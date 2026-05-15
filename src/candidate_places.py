CANDIDATE_PLACES = [
    {"name": "St. Pölten",          "country": "Austria",  "direction": "W",  "distance_km": 55,  "lat": 48.2044, "lon": 15.6229},
    {"name": "Krems an der Donau",  "country": "Austria",  "direction": "NW", "distance_km": 60,  "lat": 48.4097, "lon": 15.6056},
    {"name": "Eisenstadt",          "country": "Austria",  "direction": "S",  "distance_km": 40,  "lat": 47.8452, "lon": 16.5336},
    {"name": "Wiener Neustadt",     "country": "Austria",  "direction": "S",  "distance_km": 45,  "lat": 47.8095, "lon": 16.2428},
    {"name": "Bratislava",          "country": "Slovakia", "direction": "E",  "distance_km": 55,  "lat": 48.1486, "lon": 17.1077},
    {"name": "Sopron",              "country": "Hungary",  "direction": "SE", "distance_km": 60,  "lat": 47.6849, "lon": 16.5902},
    {"name": "Znojmo",              "country": "Czechia",  "direction": "NW", "distance_km": 75,  "lat": 48.8555, "lon": 16.0488},
    {"name": "Győr",                "country": "Hungary",  "direction": "SE", "distance_km": 110, "lat": 47.6875, "lon": 17.6504},
    {"name": "Brno",                "country": "Czechia",  "direction": "N",  "distance_km": 110, "lat": 49.1951, "lon": 16.6068},
    {"name": "Graz",                "country": "Austria",  "direction": "SW", "distance_km": 145, "lat": 47.0707, "lon": 15.4395},
    {"name": "Linz",                "country": "Austria",  "direction": "W",  "distance_km": 155, "lat": 48.3064, "lon": 14.2858},
]


def get_candidate_places():
    return [
        {**p, "label": p["name"]}
        for p in CANDIDATE_PLACES
    ]
