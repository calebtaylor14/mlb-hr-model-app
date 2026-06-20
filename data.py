import pandas as pd

from mlb_data import get_team_rosters

from mlb_data import (
    get_today_games_with_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile
)

from weather import get_weather_score


# -----------------------------
# BUILD SLATE (STABLE VERSION)
# -----------------------------
def build_slate():

    games = get_today_games_with_lineups()
    rows = []

    weather_score = get_weather_score()

    fallback_pool = [
        "Aaron Judge",
        "Shohei Ohtani",
        "Juan Soto",
        "Matt Olson",
        "Yordan Alvarez",
        "Pete Alonso",
        "Kyle Schwarber",
        "Mookie Betts"
    ]

    all_hitters = []

    # -----------------------------
    # STEP 1: COLLECT PLAYERS
    # -----------------------------
    for g in games:

        away_lineup = g.get("away_lineup", [])
        home_lineup = g.get("home_lineup", [])

        for p in away_lineup:
            name = p.get("name")
            spot = p.get("battingOrder", 99)
            if name:
                all_hitters.append((name, spot, g["game"]))

        for p in home_lineup:
            name = p.get("name")
            spot = p.get("battingOrder", 99)
            if name:
                all_hitters.append((name, spot, g["game"]))

    # -----------------------------
    # STEP 2: FALLBACK SAFETY
    # -----------------------------
    if len(all_hitters) < 10:
        for i, name in enumerate(fallback_pool):
            all_hitters.append((name, i + 1, "FALLBACK"))

    # remove duplicates safely
    seen = set()
    unique_hitters = []

    for h in all_hitters:
        key = (h[0], h[2])
        if key not in seen:
            seen.add(key)
            unique_hitters.append(h)

    # -----------------------------
    # STEP 3: BUILD ROWS
    # -----------------------------
    for hitter, spot, game in unique_hitters:

        hitter_stats = get_statcast_hitter_profile(hitter)
        pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

        order_multiplier = 1.15 if spot <= 4 else 1.0 if spot <= 6 else 0.9

        rows.append({
            "player": hitter,
            "game": game,
            "batting_order": spot,

            # hitter metrics
            "barrel_pct": hitter_stats["barrel_pct"],
            "hardhit_pct": hitter_stats["hardhit_pct"],
            "pull_air_pct": hitter_stats["pull_air_pct"],
            "iso": hitter_stats["iso"],

            # pitcher metrics (placeholder model)
            "pitcher_hr9": pitcher_stats["hr9"],
            "pitcher_barrel_allowed": pitcher_stats["barrel_allowed"],
            "pitcher_flyball": pitcher_stats["flyball"],
            "pitcher_xslg": pitcher_stats["xslg"],
            "pitcher_suppression": pitcher_stats["suppression"],

            # matchup factors
            "pitch_type_edge": 4,
            "handedness_edge": 5,
            "swing_fit": 4,

            # environment
            "park_score": 4,
            "weather_score": weather_score,

            # form
            "recent_form": 2,
            "bullpen_risk": 2,

            # batting order impact
            "order_multiplier": order_multiplier
        })

    return pd.DataFrame(rows)
