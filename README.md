# Sun Chaser ☀️

**Find the nearest reachable sunshine from Vienna.**

Is it raining where you are? Sun Chaser checks the weather at 32 points around Vienna — 8 compass directions × 4 distances (50 / 100 / 150 / 200 km) — and ranks them by a simple sun score. Pick a direction and drive.

## Tech stack

- Python 3.10+
- Streamlit (UI)
- Open-Meteo API (free, no key required)
- Folium + streamlit-folium (map)
- Pandas (data wrangling)

## Project structure

```
sun-chaser/
├── app.py                 # Streamlit entry point
├── src/
│   ├── geo_points.py      # Generate candidate lat/lon points around Vienna
│   ├── weather_api.py     # Open-Meteo API calls
│   ├── scoring.py         # Sun score calculation
│   └── map_view.py        # Folium map builder
├── requirements.txt
└── README.md
```

## Sun score formula

```
score = 100
      − cloud_cover × 0.5          (max −50)
      − precip_probability × 0.3   (max −30, averaged over next 6 hours)
      − min(precipitation × 10, 20) (max −20)
      + temperature bonus            (+10 if 18–26 °C, +5 if 12–30 °C)
```

Scores are clamped to [0, 110].

## Quick start

```bash
cd sun-chaser
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## Notes

- No API keys needed — Open-Meteo is fully free.
- Weather data is fetched live on each button press; results are not cached between sessions.
- Starting location is hard-coded to Vienna (48.2082°N, 16.3738°E).
