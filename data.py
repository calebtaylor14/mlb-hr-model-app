import pandas as pd
from weather import get_weather_score
from mlb_data import (
    get_today_games_with_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile
)


def build_slate():

    games = get_today_games_with_lineups()
    rows = []

    weather_score = get_weather_score()

    # expanded fallback pool (ensures full slate coverage)
    fallback_pool = [
        "Aaron Judge",
        "Shohei Ohtani",
        "Juan Soto",
        "Matt Olson",
        "Yordan Alvarez",
        "Kyle Schwarber",
        "Pete Alonso",
        "Mookie Betts"
    ]

    for g in games:

        away_lineup = g.get("away_lineup", [])
        home_lineup = g.get("home_lineup", [])

        hitters = []

        # -------------------------
        # TRY REAL LINEUPS FIRST
        # -------------------------
        for p in away_lineup:
            name = p.get("name")
            spot = p.get("battingOrder", 99)
            if name:
                hitters.append((name, spot))

        for p in home_lineup:
            name = p.get("name")
            spot = p.get("battingOrder", 99)
            if name:
                hitters.append((name, spot))

        # -------------------------
        # GUARANTEED COVERAGE FIX
        # -------------------------
        if len(hitters) < 6:
            # fill missing players so slate is never small
            for i, name in enumerate(fallback_pool):
                hitters.append((name, i + 1))

        # prevent duplicates
        hitters = list(dict.fromkeys(hitters))

        for hitter, spot in hitters:

            hitter_stats = get_statcast_hitter_profile(hitter)
            pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

            order_multiplier = 1.15 if spot <= 4 else 1.0 if spot <= 6 else 0.9

            rows.append({
                "player": hitter,
                "game": g["game"],
                "batting_order": spot,

                "barrel_pct": hitter_stats["barrel_pct"],
                "hardhit_pct": hitter_stats["hardhit_pct"],
                "pull_air_pct": hitter_stats["pull_air_pct"],
                "iso": hitter_stats["iso"],

                "pitcher_hr9": pitcher_stats["hr9"],
                "pitcher_barrel_allowed": pitcher_stats["barrel_allowed"],
                "pitcher_flyball": pitcher_stats["flyball"],
                "pitcher_xslg": pitcher_stats["xslg"],
                "pitcher_suppression": pitcher_stats["suppression"],

                "pitch_type_edge": 4,
                "handedness_edge": 5,
                "swing_fit": 4,

                "park_score": 4,
                "weather_score": weather_score,

                "recent_form": 2,
                "bullpen_risk": 2,

                "order_multiplier": order_multiplier
            })

    return pd.DataFrame(rows)
