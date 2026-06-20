import pandas as pd

from mlb_data import (
    get_today_games_with_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile,
    get_team_rosters
)

from weather import get_weather_score


def build_slate():

    rosters = get_team_rosters()
    rows = []

    weather_score = get_weather_score()

    all_hitters = []

    # -----------------------------
    # BUILD PLAYER POOL
    # -----------------------------
    for team, players in rosters.items():

        for i, player in enumerate(players[:12]):

            spot = (i % 9) + 1

            all_hitters.append((player, spot, team))

    # -----------------------------
    # BUILD MODEL ROWS
    # -----------------------------
    for hitter, spot, team in all_hitters:

        hitter_stats = get_statcast_hitter_profile(hitter)
        pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

        order_multiplier = 1.15 if spot <= 4 else 1.0 if spot <= 6 else 0.9

        rows.append({
            "player": hitter,
            "team": team,
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
