import math

VIENNA_LAT = 48.2082
VIENNA_LON = 16.3738
EARTH_RADIUS_KM = 6371.0

DIRECTIONS = {
    "N":  0,
    "NE": 45,
    "E":  90,
    "SE": 135,
    "S":  180,
    "SW": 225,
    "W":  270,
    "NW": 315,
}

DISTANCES_KM = [50, 100, 150, 200]


def destination_point(lat, lon, bearing_deg, distance_km):
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    bearing_r = math.radians(bearing_deg)
    d_r = distance_km / EARTH_RADIUS_KM

    new_lat_r = math.asin(
        math.sin(lat_r) * math.cos(d_r)
        + math.cos(lat_r) * math.sin(d_r) * math.cos(bearing_r)
    )
    new_lon_r = lon_r + math.atan2(
        math.sin(bearing_r) * math.sin(d_r) * math.cos(lat_r),
        math.cos(d_r) - math.sin(lat_r) * math.sin(new_lat_r),
    )
    return math.degrees(new_lat_r), math.degrees(new_lon_r)


def generate_candidate_points(origin_lat: float = VIENNA_LAT, origin_lon: float = VIENNA_LON):
    points = []
    for direction, bearing in DIRECTIONS.items():
        for distance in DISTANCES_KM:
            lat, lon = destination_point(origin_lat, origin_lon, bearing, distance)
            points.append({
                "direction": direction,
                "distance_km": distance,
                "lat": round(lat, 4),
                "lon": round(lon, 4),
                "label": f"{direction} {distance}km",
            })
    return points
