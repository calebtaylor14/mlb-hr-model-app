import requests


# -----------------------------
# GAMES + LINEUPS
# -----------------------------
def get_today_games_with_lineups():

    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=lineups"
    res = requests.get(url)
    data = res.json()

    games = []

    for d in data.get("dates", []):
        for g in d.get("games", []):

            away = g["teams"]["away"]["team"]["name"]
            home = g["teams"]["home"]["team"]["name"]

            lineups = g.get("lineups", {}) if "lineups" in g else {}

            away_lineup = lineups.get("away", []) if isinstance(lineups, dict) else []
            home_lineup = lineups.get("home", []) if isinstance(lineups, dict) else []

            games.append({
                "game": f"{away} @ {home}",
                "away_team": away,
                "home_team": home,
                "away_lineup": away_lineup,
                "home_lineup": home_lineup
            })

    return games


# -----------------------------
# STATCAST (SAFE PLACEHOLDERS)
# -----------------------------
def get_statcast_hitter_profile(player_name):

    # later we replace with real Baseball Savant data
    return {
        "barrel_pct": 8.5,
        "hardhit_pct": 45,
        "pull_air_pct": 22,
        "iso": 0.205
    }


def get_statcast_pitcher_profile(pitcher_name):

    return {
        "hr9": 1.25,
        "barrel_allowed": 9,
        "flyball": 42,
        "xslg": 0.430,
        "suppression": 9
    }
