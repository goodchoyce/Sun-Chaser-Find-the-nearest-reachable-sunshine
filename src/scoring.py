import pandas as pd


def sun_band(score: float) -> str:
    if score >= 85:
        return "Sun hit"
    elif score >= 70:
        return "Promising"
    elif score >= 55:
        return "Maybe"
    elif score >= 40:
        return "Weak"
    else:
        return "Rain trap"


def calculate_sun_score(row):
    score = 100.0

    cloud_cover = row.get("cloud_cover") or 0
    precip_prob = row.get("precipitation_probability") or 0
    precipitation = row.get("precipitation") or 0
    temp = row.get("temperature_2m")

    # Cloud cover penalty: 100% cloud = -50 points
    score -= cloud_cover * 0.5

    # Precipitation probability penalty: 100% = -30 points
    score -= precip_prob * 0.3

    # Precipitation amount penalty: capped at -20
    score -= min(precipitation * 10, 20)

    # Temperature bonus for comfortable weather
    if temp is not None:
        if 18 <= temp <= 26:
            score += 10
        elif 12 <= temp <= 30:
            score += 5

    return round(max(0.0, min(110.0, score)), 1)


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sun_score"] = df.apply(calculate_sun_score, axis=1)
    df["sun_band"] = df["sun_score"].apply(sun_band)
    df = df.sort_values("sun_score", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df
