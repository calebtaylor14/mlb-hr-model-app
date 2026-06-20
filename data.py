import pandas as pd

def load_data():

    data = [
        {
            "player": "Aaron Judge",
            "barrel_pct": 8,
            "hardhit_pct": 52,
            "pull_air_pct": 28,
            "iso": 0.280,
            "pitcher_hr9": 1.4,
            "pitcher_barrel_allowed": 9,
            "pitcher_flyball": 42,
            "pitcher_xslg": 0.450,
            "pitch_type_edge": 4,
            "handedness_edge": 5,
            "swing_fit": 4,
            "pitcher_suppression": 10,
            "park_score": 4,
            "weather_score": 3,
            "recent_form": 2,
            "bullpen_risk": 2
        }
    ]

    return pd.DataFrame(data)
