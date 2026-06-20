import pandas as pd
from weather import get_weather_score
from mlb_data import (
    get_today_games_with_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile
)

from mlb_data import (
    get_today_games_with_lineups,
    get_statcast_hitter_profile,
    get_statcast_pitcher_profile
)


import requests

def get_all_teams():

    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    res = requests.get(url)
    data = res.json()

    return [t["name"] for t in data.get("teams", [])]


def get_team_roster(team_id):

    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    res = requests.get(url)
    data = res.json()

    players = []

    for p in data.get("roster", []):
        if p.get("position", {}).get("type") == "Hitter":
            players.append(p["person"]["fullName"])

    return players


def build_slate():
    pitcher_map = get_probable_pitchers()
    
    from mlb_data import get_probable_pitchers
    pitcher_map = get_probable_pitchers()

    rows = []

    weather_score = get_weather_score()

    teams_url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    teams = requests.get(teams_url).json()["teams"]

    fallback_pool = [
        "Aaron Judge", "Shohei Ohtani", "Juan Soto",
        "Matt Olson", "Yordan Alvarez", "Pete Alonso"
    ]

    all_hitters = []

    # -----------------------------
    # BUILD FULL MLB PLAYER POOL
    # -----------------------------
    for t in teams:

        team_id = t["id"]
        roster = get_team_roster(team_id)

        for player in roster:
            all_hitters.append(player)

    # fallback safety
    if len(all_hitters) < 50:
        all_hitters += fallback_pool

    # remove duplicates
    all_hitters = list(set(all_hitters))

    # -----------------------------
    # BUILD MODEL ROWS
    # -----------------------------
    for hitter in all_hitters:

        hitter_stats = get_statcast_hitter_profile(hitter)
        pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

        rows.append({
            "player": hitter,
            "game": "ALL MLB SLATE",

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
            "bullpen_risk": 2
        })

    return pd.DataFrame(rows)
