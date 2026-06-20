import pandas as pd
import requests
from weather import get_weather_score
def get_park_score(park_name="default"):

    hr_parks = {
        "Yankee Stadium": 4,
        "Coors Field": 5,
        "Fenway Park": 4,
        "Dodger Stadium": 2,
        "Petco Park": 1
    }

    return hr_parks.get(park_name, 3)

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

            "park_score": get_park_score(),
            "weather_score": get_weather_score(),

            "recent_form": 2,
            "bullpen_risk": 2
        })

    return pd.DataFrame(rows)
