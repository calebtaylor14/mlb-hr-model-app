import pandas as pd
from weather import get_weather_score


# -----------------------------
# SAFE BASE STAT FUNCTIONS
# (placeholders until Statcast upgrade)
# -----------------------------

def get_hitter_stats(player_name):

    return {
        "barrel_pct": 8,
        "hardhit_pct": 45,
        "pull_air_pct": 22,
        "iso": 0.200
    }


def get_pitcher_stats(pitcher_name):

    return {
        "hr9": 1.3,
        "barrel_allowed": 9,
        "flyball": 42,
        "xslg": 0.430,
        "suppression": 9
    }


# -----------------------------
# DAILY SLATE BUILDER
# -----------------------------

def get_today_games():

    hitter = get_hitter_stats("Aaron Judge")
    pitcher = get_pitcher_stats("Opposing Pitcher")

    # weather is intentionally global for MVP
    weather_score = get_weather_score()

    df = pd.DataFrame([
        {
            "player": "Aaron Judge",
            "game": "Yankees @ Red Sox",

            # ---------------- BATTER ----------------
            "barrel_pct": hitter["barrel_pct"],
            "hardhit_pct": hitter["hardhit_pct"],
            "pull_air_pct": hitter["pull_air_pct"],
            "iso": hitter["iso"],

            # ---------------- PITCHER ----------------
            "pitcher_hr9": pitcher["hr9"],
            "pitcher_barrel_allowed": pitcher["barrel_allowed"],
            "pitcher_flyball": pitcher["flyball"],
            "pitcher_xslg": pitcher["xslg"],

            # ---------------- MATCHUP ----------------
            "pitch_type_edge": 4,
            "handedness_edge": 5,
            "swing_fit": 4,

            # ---------------- SUPPRESSION ----------------
            "pitcher_suppression": pitcher["suppression"],

            # ---------------- ENVIRONMENT ----------------
            "park_score": 4,
            "weather_score": weather_score,

            # ---------------- FORM ----------------
            "recent_form": 2,
            "bullpen_risk": 2
        }
    ])

    return df
