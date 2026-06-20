import requests


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
