import time

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from src.geocoding import geocode_city
from src.nearby_cities import find_nearby_cities
from src.weather_api import fetch_weather
from src.scoring import score_dataframe
from src.map_view import build_map

st.set_page_config(page_title="Sun Chaser", page_icon="☀️", layout="wide")

st.title("☀️ Sun Chaser")
st.caption("Find the nearest reachable sunshine from wherever you are.")

st.divider()

col_city, col_dist = st.columns([2, 2], gap="large")

with col_city:
    start_city = st.text_input(
        "Start city",
        value="Vienna",
        placeholder="e.g. Munich, Prague, Bratislava",
    )

with col_dist:
    max_distance = st.slider(
        "Search distance (km)",
        min_value=50,
        max_value=200,
        step=50,
        value=150,
        help="Only show cities within this radius of your start city.",
    )

fetch_btn = st.button("🔍 Find Sunshine", type="primary")

if fetch_btn:
    with st.spinner(f"Locating {start_city}…"):
        try:
            origin_lat, origin_lon, origin_name = geocode_city(start_city)
        except ValueError as e:
            st.error(str(e))
            st.stop()

    candidates = find_nearby_cities(origin_lat, origin_lon, max_km=max_distance)

    if not candidates:
        st.warning(
            f"No cities found in the database within {max_distance} km of {origin_name}. "
            "The database covers Central Europe (Austria, Germany, Czech Republic, Slovakia, "
            "Hungary, Slovenia, Croatia, Poland, Switzerland, northern Italy). "
            "Try increasing the search distance, or use a city in that region."
        )
        st.stop()

    st.session_state["origin"] = (origin_lat, origin_lon, origin_name)

    progress = st.progress(0, text="Fetching weather data…")
    results = []
    for i, city in enumerate(candidates):
        weather = fetch_weather(city["lat"], city["lon"])
        results.append({**city, **weather})
        time.sleep(0.05)
        progress.progress(
            (i + 1) / len(candidates),
            text=f"Checked {i + 1} / {len(candidates)} cities…",
        )
    progress.empty()

    df = pd.DataFrame(results)
    df = score_dataframe(df)
    st.session_state["df"] = df

if "df" in st.session_state:
    df = st.session_state["df"]
    origin_lat, origin_lon, origin_name = st.session_state.get(
        "origin", (48.2085, 16.3721, "Vienna")
    )
    best = df.iloc[0]

    def _fmt(val, suffix=""):
        return f"{val}{suffix}" if val is not None else "N/A"

    place_name  = best.get("name") or best["label"]
    direction   = best.get("direction", "?")
    distance    = best.get("distance_km", "?")
    band        = best.get("sun_band", "")
    cloud       = _fmt(best["cloud_cover"], "%")
    rain_prob   = _fmt(best["precipitation_probability"], "%")
    temp        = _fmt(best["temperature_2m"], "°C")

    st.success(
        f"**Best lead: {place_name}** ({band})  \n"
        f"Head **{direction}**, about **{distance} km** from {origin_name}.  \n"
        f"Why: {cloud} cloud · {rain_prob} rain risk · {temp}."
    )

    col_table, col_map = st.columns([1, 1], gap="large")

    with col_table:
        st.subheader("Ranked cities")

        cols = [
            "rank", "label", "country", "direction", "distance_km",
            "sun_score", "sun_band", "temperature_2m",
            "cloud_cover", "precipitation_probability",
        ]
        rename = {
            "rank":                      "#",
            "label":                     "City",
            "country":                   "Country",
            "direction":                 "Dir",
            "distance_km":               "Dist (km)",
            "sun_score":                 "Score",
            "sun_band":                  "Conditions",
            "temperature_2m":            "Temp (°C)",
            "cloud_cover":               "Cloud (%)",
            "precipitation_probability": "Rain Prob (%)",
        }
        st.dataframe(df[cols].rename(columns=rename), use_container_width=True, hide_index=True)
        st.caption(
            "Score = 100 − cloud penalty − rain-prob penalty − precip penalty + temp bonus.  "
            "Gold ≥ 85 · Green ≥ 70 · Cyan ≥ 55 · Amber ≥ 40 · Coral < 40."
        )

    with col_map:
        st.subheader("Weather map")
        m = build_map(df, origin_lat, origin_lon, origin_name)
        st_folium(m, use_container_width=True, height=520, returned_objects=[])

    st.caption(
        "ℹ️ Reachability is estimated by straight-line distance. "
        "Drive-time routing and isochrones are planned next."
    )
