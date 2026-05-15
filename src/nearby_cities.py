"""
Static database of ~80 Central European cities with lat/lon.
find_nearby_cities() computes distance + bearing from any origin on the fly.
No API needed.
"""

import math

# ---------------------------------------------------------------------------
# City database — Central Europe
# ---------------------------------------------------------------------------

CITY_DB = [
    # Austria
    {"name": "Vienna",               "country": "Austria",      "lat": 48.2085, "lon": 16.3721},
    {"name": "Graz",                 "country": "Austria",      "lat": 47.0707, "lon": 15.4395},
    {"name": "Linz",                 "country": "Austria",      "lat": 48.3064, "lon": 14.2858},
    {"name": "Salzburg",             "country": "Austria",      "lat": 47.8095, "lon": 13.0550},
    {"name": "Innsbruck",            "country": "Austria",      "lat": 47.2692, "lon": 11.4041},
    {"name": "Klagenfurt",           "country": "Austria",      "lat": 46.6228, "lon": 14.3050},
    {"name": "Wiener Neustadt",      "country": "Austria",      "lat": 47.8095, "lon": 16.2428},
    {"name": "St. Pölten",           "country": "Austria",      "lat": 48.2044, "lon": 15.6229},
    {"name": "Wels",                 "country": "Austria",      "lat": 48.1573, "lon": 14.0286},
    {"name": "Steyr",                "country": "Austria",      "lat": 48.0406, "lon": 14.4197},
    {"name": "Bregenz",              "country": "Austria",      "lat": 47.5031, "lon":  9.7471},
    {"name": "Feldkirch",            "country": "Austria",      "lat": 47.2359, "lon":  9.5996},
    {"name": "Krems an der Donau",   "country": "Austria",      "lat": 48.4097, "lon": 15.6056},
    {"name": "Eisenstadt",           "country": "Austria",      "lat": 47.8452, "lon": 16.5336},
    {"name": "Leoben",               "country": "Austria",      "lat": 47.3836, "lon": 15.0925},
    {"name": "Baden bei Wien",       "country": "Austria",      "lat": 48.0017, "lon": 16.2318},
    {"name": "Amstetten",            "country": "Austria",      "lat": 48.1223, "lon": 14.8712},
    {"name": "Bad Ischl",            "country": "Austria",      "lat": 47.7139, "lon": 13.6314},
    # Germany
    {"name": "Munich",               "country": "Germany",      "lat": 48.1351, "lon": 11.5820},
    {"name": "Nuremberg",            "country": "Germany",      "lat": 49.4521, "lon": 11.0767},
    {"name": "Augsburg",             "country": "Germany",      "lat": 48.3705, "lon": 10.8978},
    {"name": "Regensburg",           "country": "Germany",      "lat": 49.0134, "lon": 12.1016},
    {"name": "Ingolstadt",           "country": "Germany",      "lat": 48.7665, "lon": 11.4258},
    {"name": "Landshut",             "country": "Germany",      "lat": 48.5376, "lon": 12.1506},
    {"name": "Passau",               "country": "Germany",      "lat": 48.5748, "lon": 13.4647},
    {"name": "Rosenheim",            "country": "Germany",      "lat": 47.8560, "lon": 12.1284},
    {"name": "Kempten im Allgäu",    "country": "Germany",      "lat": 47.7267, "lon": 10.3167},
    {"name": "Memmingen",            "country": "Germany",      "lat": 47.9874, "lon": 10.1814},
    {"name": "Würzburg",             "country": "Germany",      "lat": 49.7913, "lon":  9.9534},
    {"name": "Garmisch-Partenkirchen","country": "Germany",     "lat": 47.4912, "lon": 11.0956},
    {"name": "Lindau am Bodensee",   "country": "Germany",      "lat": 47.5455, "lon":  9.6830},
    {"name": "Ulm",                  "country": "Germany",      "lat": 48.3984, "lon":  9.9908},
    {"name": "Friedrichshafen",      "country": "Germany",      "lat": 47.6553, "lon":  9.4772},
    {"name": "Straubing",            "country": "Germany",      "lat": 48.8819, "lon": 12.5795},
    {"name": "Traunstein",           "country": "Germany",      "lat": 47.8697, "lon": 12.6394},
    {"name": "Bayreuth",             "country": "Germany",      "lat": 49.9481, "lon": 11.5783},
    {"name": "Dresden",              "country": "Germany",      "lat": 51.0504, "lon": 13.7373},
    {"name": "Chemnitz",             "country": "Germany",      "lat": 50.8278, "lon": 12.9214},
    {"name": "Leipzig",              "country": "Germany",      "lat": 51.3397, "lon": 12.3731},
    {"name": "Erfurt",               "country": "Germany",      "lat": 50.9848, "lon": 11.0299},
    {"name": "Stuttgart",            "country": "Germany",      "lat": 48.7758, "lon":  9.1829},
    {"name": "Freiburg im Breisgau", "country": "Germany",      "lat": 47.9990, "lon":  7.8421},
    {"name": "Konstanz",             "country": "Germany",      "lat": 47.6779, "lon":  9.1743},
    # Czech Republic
    {"name": "Prague",               "country": "Czechia",      "lat": 50.0755, "lon": 14.4378},
    {"name": "Brno",                 "country": "Czechia",      "lat": 49.1951, "lon": 16.6068},
    {"name": "Plzeň",                "country": "Czechia",      "lat": 49.7384, "lon": 13.3736},
    {"name": "Ostrava",              "country": "Czechia",      "lat": 49.8209, "lon": 18.2625},
    {"name": "Liberec",              "country": "Czechia",      "lat": 50.7663, "lon": 15.0543},
    {"name": "Olomouc",              "country": "Czechia",      "lat": 49.5938, "lon": 17.2509},
    {"name": "České Budějovice",     "country": "Czechia",      "lat": 48.9745, "lon": 14.4745},
    {"name": "Jihlava",              "country": "Czechia",      "lat": 49.3961, "lon": 15.5907},
    {"name": "Znojmo",               "country": "Czechia",      "lat": 48.8555, "lon": 16.0488},
    {"name": "Karlovy Vary",         "country": "Czechia",      "lat": 50.2301, "lon": 12.8716},
    # Slovakia
    {"name": "Bratislava",           "country": "Slovakia",     "lat": 48.1486, "lon": 17.1077},
    {"name": "Nitra",                "country": "Slovakia",     "lat": 48.3069, "lon": 18.0840},
    {"name": "Trnava",               "country": "Slovakia",     "lat": 48.3774, "lon": 17.5859},
    {"name": "Trenčín",              "country": "Slovakia",     "lat": 48.8943, "lon": 18.0440},
    {"name": "Žilina",               "country": "Slovakia",     "lat": 49.2235, "lon": 18.7393},
    {"name": "Banská Bystrica",      "country": "Slovakia",     "lat": 48.7395, "lon": 19.1530},
    # Hungary
    {"name": "Budapest",             "country": "Hungary",      "lat": 47.4979, "lon": 19.0402},
    {"name": "Győr",                 "country": "Hungary",      "lat": 47.6875, "lon": 17.6504},
    {"name": "Miskolc",              "country": "Hungary",      "lat": 48.1039, "lon": 20.7784},
    {"name": "Pécs",                 "country": "Hungary",      "lat": 46.0727, "lon": 18.2330},
    {"name": "Kecskemét",            "country": "Hungary",      "lat": 46.8964, "lon": 19.6897},
    {"name": "Székesfehérvár",       "country": "Hungary",      "lat": 47.1864, "lon": 18.4086},
    {"name": "Sopron",               "country": "Hungary",      "lat": 47.6849, "lon": 16.5902},
    {"name": "Szombathely",          "country": "Hungary",      "lat": 47.2299, "lon": 16.6218},
    {"name": "Eger",                 "country": "Hungary",      "lat": 47.9025, "lon": 20.3772},
    {"name": "Veszprém",             "country": "Hungary",      "lat": 47.0878, "lon": 17.9089},
    # Slovenia
    {"name": "Ljubljana",            "country": "Slovenia",     "lat": 46.0569, "lon": 14.5058},
    {"name": "Maribor",              "country": "Slovenia",     "lat": 46.5547, "lon": 15.6467},
    {"name": "Celje",                "country": "Slovenia",     "lat": 46.2313, "lon": 15.2606},
    {"name": "Koper",                "country": "Slovenia",     "lat": 45.5481, "lon": 13.7300},
    # Croatia
    {"name": "Zagreb",               "country": "Croatia",      "lat": 45.8150, "lon": 15.9819},
    {"name": "Varaždin",             "country": "Croatia",      "lat": 46.3044, "lon": 16.3378},
    # Poland
    {"name": "Kraków",               "country": "Poland",       "lat": 50.0647, "lon": 19.9450},
    {"name": "Wrocław",              "country": "Poland",       "lat": 51.1079, "lon": 17.0385},
    {"name": "Katowice",             "country": "Poland",       "lat": 50.2649, "lon": 19.0238},
    {"name": "Bielsko-Biała",        "country": "Poland",       "lat": 49.8225, "lon": 19.0444},
    {"name": "Opole",                "country": "Poland",       "lat": 50.6667, "lon": 17.9254},
    # Switzerland
    {"name": "Zurich",               "country": "Switzerland",  "lat": 47.3769, "lon":  8.5417},
    {"name": "Basel",                "country": "Switzerland",  "lat": 47.5596, "lon":  7.5886},
    {"name": "Bern",                 "country": "Switzerland",  "lat": 46.9480, "lon":  7.4474},
    {"name": "St. Gallen",           "country": "Switzerland",  "lat": 47.4245, "lon":  9.3767},
    {"name": "Chur",                 "country": "Switzerland",  "lat": 46.8499, "lon":  9.5329},
    # Italy (northern)
    {"name": "Bolzano",              "country": "Italy",        "lat": 46.4983, "lon": 11.3548},
    {"name": "Trento",               "country": "Italy",        "lat": 46.0748, "lon": 11.1217},
    {"name": "Verona",               "country": "Italy",        "lat": 45.4384, "lon": 10.9916},
    {"name": "Udine",                "country": "Italy",        "lat": 46.0636, "lon": 13.2358},
    {"name": "Trieste",              "country": "Italy",        "lat": 45.6496, "lon": 13.7681},
    {"name": "Venice",               "country": "Italy",        "lat": 45.4408, "lon": 12.3155},
]


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Great-circle distance between two lat/lon points. R is the earth's
    # radius in km, so the result comes out in km too.
    R = 6371.0
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2 - lat1)
    dλ = math.radians(lon2 - lon1)
    a = math.sin(dφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(dλ / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Forward azimuth from point 1 to point 2, normalised to 0-360 degrees
    # where 0 is north and angles run clockwise.
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dλ = math.radians(lon2 - lon1)
    x = math.sin(dλ) * math.cos(φ2)
    y = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(dλ)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def _bearing_to_direction(bearing: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # Each label covers a 45 degree sector centred on its bearing, so shift
    # by 22.5 first to push sector boundaries between labels rather than on them.
    return dirs[int((bearing + 22.5) / 45) % 8]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_nearby_cities(
    origin_lat: float,
    origin_lon: float,
    max_km: float,
    min_km: float = 15.0,
) -> list[dict]:
    """
    Return all CITY_DB entries within [min_km, max_km] of the origin,
    each enriched with distance_km, direction, and label.
    min_km=15 filters out the start city itself if it appears in the database.
    """
    results = []
    for city in CITY_DB:
        dist = _haversine_km(origin_lat, origin_lon, city["lat"], city["lon"])
        if min_km <= dist <= max_km:
            bearing = _initial_bearing(origin_lat, origin_lon, city["lat"], city["lon"])
            results.append({
                "name":        city["name"],
                "country":     city["country"],
                "lat":         city["lat"],
                "lon":         city["lon"],
                "label":       city["name"],   # used downstream by scoring / map
                "direction":   _bearing_to_direction(bearing),
                "distance_km": round(dist),
            })
    results.sort(key=lambda c: c["distance_km"])
    return results
