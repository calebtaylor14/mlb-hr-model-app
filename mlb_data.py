import requests


# -----------------------------
# CORE GAME FUNCTION (MUST EXIST)
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
# STATCAST PLACEHOLDERS (STABLE)
# -----------------------------
def get_statcast_hitter_profile(player_name):
    return {
        "barrel_pct": 8.5,
        "hardhit_pct": 45,
        "pull_air_pct": 22,
        "iso": 0.205
    }

def get_probable_pitchers():

    import requests

    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher"
    res = requests.get(url)
    data = res.json()

    pitcher_map = {}

    for d in data.get("dates", []):
        for g in d.get("games", []):

            game = f"{g['teams']['away']['team']['name']} @ {g['teams']['home']['team']['name']}"

            pitcher_map[game] = {
                "away_pitcher": g["teams"]["away"].get("probablePitcher", {}).get("fullName"),
                "home_pitcher": g["teams"]["home"].get("probablePitcher", {}).get("fullName")
            }

    return pitcher_map
