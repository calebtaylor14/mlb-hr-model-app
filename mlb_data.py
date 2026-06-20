import requests

def get_team_rosters():

    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    teams = requests.get(url).json()["teams"]

    roster_map = {}

    for t in teams:
        team_id = t["id"]
        team_name = t["name"]

        r = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster").json()

        hitters = []

        for p in r.get("roster", []):
            person = p.get("person", {}).get("fullName")
            if person:
                hitters.append(person)

        roster_map[team_name] = hitters

    return roster_map


# -----------------------------
# GAMES + LINEUPS
# -----------------------------
def get_today_games_with_lineups():

    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=lineups,probablePitcher"
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

            away_pitcher = g["teams"]["away"].get("probablePitcher", {}).get("fullName")
            home_pitcher = g["teams"]["home"].get("probablePitcher", {}).get("fullName")

            games.append({
                "game": f"{away} @ {home}",
                "away_team": away,
                "home_team": home,
                "away_lineup": away_lineup,
                "home_lineup": home_lineup,
                "away_pitcher": away_pitcher,
                "home_pitcher": home_pitcher
            })

    return games


# -----------------------------
# HITTER PROFILE (PLACEHOLDER STABLE)
# -----------------------------
def get_statcast_hitter_profile(player_name):
    return {
        "barrel_pct": 8.5,
        "hardhit_pct": 45,
        "pull_air_pct": 22,
        "iso": 0.205
    }


# -----------------------------
# PITCHER PROFILE (THIS WAS MISSING — FIXED)
# -----------------------------
def get_statcast_pitcher_profile(pitcher_name):
    return {
        "hr9": 1.25,
        "barrel_allowed": 9,
        "flyball": 42,
        "xslg": 0.430,
        "suppression": 9
    }
