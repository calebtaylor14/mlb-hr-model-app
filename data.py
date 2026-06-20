import pandas as pd
import requests
from weather import get_weather_score

def get_today_games():

    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
    response = requests.get(url)
    data = response.json()

    games = data["dates"][0]["games"]

    rows = []

    for g in games:

        away = g["teams"]["away"]["team"]["name"]
        home = g["teams"]["home"]["team"]["name"]

        rows.append({
            "player": "TBD",
            "game": f"{away} @ {home}",
            "barrel_pct": 8,
            "hardhit_pct": 45,
            "pull_air_pct": 20,
            "iso": 0.200,

            "pitcher_hr9": 1.2,
            "pitcher_barrel_allowed": 8,
            "pitcher_flyball": 40,
            "pitcher_xslg": 0.420,

            "pitch_type_edge": 3,
            "handedness_edge": 3,
            "swing_fit": 3,

            "pitcher_suppression": 8,

            "park_score": 3,
            "weather_score": 3,

            "recent_form": 2,
            "bullpen_risk": 2
        })

    return pd.DataFrame(rows)
