import folium
import pandas as pd

# Calm cyber palette. Each colour is picked to read clearly on the dark map tile.
BAND_COLORS = {
    "Sun hit":   "#FFD700",  # gold
    "Promising": "#00E676",  # cyber green
    "Maybe":     "#00BCD4",  # cyan
    "Weak":      "#FFA726",  # amber
    "Rain trap": "#FF5252",  # coral
}


def score_to_color(score: float) -> str:
    # Thresholds mirror sun_band() in scoring.py. Keep the two in sync if
    # the bands ever change, otherwise the labels and colours will disagree.
    if score >= 85:
        return BAND_COLORS["Sun hit"]
    elif score >= 70:
        return BAND_COLORS["Promising"]
    elif score >= 55:
        return BAND_COLORS["Maybe"]
    elif score >= 40:
        return BAND_COLORS["Weak"]
    else:
        return BAND_COLORS["Rain trap"]


def _fmt(val, suffix=""):
    return f"{val}{suffix}" if val is not None else "N/A"


def build_map(
    df: pd.DataFrame,
    start_lat: float,
    start_lon: float,
    start_name: str = "Start",
) -> folium.Map:
    m = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=7,
        tiles="CartoDB dark_matter",
    )

    # Start location marker. Uses a DivIcon with a pin emoji so it stays
    # bright on the dark tile without needing a custom image asset.
    folium.Marker(
        location=[start_lat, start_lon],
        popup=folium.Popup(f"<b>{start_name}</b><br>Your start location", max_width=180),
        tooltip=start_name,
        icon=folium.DivIcon(
            html='<div style="font-size:26px;margin:-13px 0 0 -8px;">📍</div>',
            icon_size=(26, 26),
            icon_anchor=(13, 13),
        ),
    ).add_to(m)

    for _, row in df.iterrows():
        color = score_to_color(row["sun_score"])
        sun_band = row.get("sun_band", "")
        direction = row.get("direction", "")
        distance = row.get("distance_km", "")
        popup_html = (
            f"<b>{row['label']}</b><br>"
            f"{direction} &bull; {distance} km from {start_name}<br>"
            f"<hr style='margin:4px 0;border-color:#444'>"
            f"Score: <b>{row['sun_score']}</b> &mdash; {sun_band}<br>"
            f"Temp: {_fmt(row['temperature_2m'], ' °C')}<br>"
            f"Cloud Cover: {_fmt(row['cloud_cover'], ' %')}<br>"
            f"Rain Prob (6h): {_fmt(row['precipitation_probability'], ' %')}<br>"
            f"Precipitation: {_fmt(row['precipitation'], ' mm')}"
        )
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=230),
            tooltip=f"{row['label']} — {sun_band} ({row['sun_score']})",
        ).add_to(m)

    return m
