import pandas as pd
from weather import get_weather_score
from mlb_data import (
    get_today_games_and_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile
)


def build_slate():

    games = get_today_games_and_lineups()

    rows = []

    weather_score = get_weather_score()

    for g in games:

        # -------------------------
        # GET SAMPLE LINEUP (SAFE MVP)
        # -------------------------

        away_lineup = g["away_lineup"]
        home_lineup = g["home_lineup"]

        # fallback if MLB doesn't provide lineup yet
        hitters = ["Aaron Judge", "Shohei Ohtani"]

        for hitter in hitters:

            hitter_stats = get_statcast_hitter_profile(hitter)
            pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

            rows.append({
                "player": hitter,
                "game": g["game"],

                # ---------------- BATTER ----------------
                "barrel_pct": hitter_stats["barrel_pct"],
                "hardhit_pct": hitter_stats["hardhit_pct"],
                "pull_air_pct": hitter_stats["pull_air_pct"],
                "iso": hitter_stats["iso"],

                # ---------------- PITCHER ----------------
                "pitcher_hr9": pitcher_stats["hr9"],
                "pitcher_barrel_allowed": pitcher_stats["barrel_allowed"],
                "pitcher_flyball": pitcher_stats["flyball"],
                "pitcher_xslg": pitcher_stats["xslg"],
                "pitcher_suppression": pitcher_stats["suppression"],

                # ---------------- MATCHUP ----------------
                "pitch_type_edge": 4,
                "handedness_edge": 5,
                "swing_fit": 4,

                # ---------------- ENVIRONMENT ----------------
                "park_score": 4,
                "weather_score": weather_score,

                # ---------------- FORM ----------------
                "recent_form": 2,
                "bullpen_risk": 2
            })

    return pd.DataFrame(rows)
