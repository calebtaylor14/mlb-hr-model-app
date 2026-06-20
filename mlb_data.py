import requests


def get_probable_pitchers():

    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher"
    res = requests.get(url)
    data = res.json()

    pitcher_map = {}

    for d in data.get("dates", []):
        for g in d.get("games", []):

            game = f"{g['teams']['away']['team']['name']} @ {g['teams']['home']['team']['name']}"

            away_pitcher = g["teams"]["away"].get("probablePitcher", {}).get("fullName")
            home_pitcher = g["teams"]["home"].get("probablePitcher", {}).get("fullName")

            pitcher_map[game] = {
                "away_pitcher": away_pitcher,
                "home_pitcher": home_pitcher
            }

    return pitcher_map
