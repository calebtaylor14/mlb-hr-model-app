import requests
import pandas as pd

def get_hitter_stats(player_name):

    url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&player_type=batter&year=2026"

    df = pd.read_csv(url)

    # filter player
    player_data = df[df["player_name"] == player_name]

    if len(player_data) == 0:
        return {
            "barrel_pct": 6,
            "hardhit_pct": 40,
            "iso": 0.180,
            "exit_velocity": 88,
            "pull_air_pct": 18
        }

    return {
        "barrel_pct": player_data["barrel"].mean(),
        "hardhit_pct": player_data["hard_hit_rate"].mean(),
        "iso": player_data["iso"].mean(),
        "exit_velocity": player_data["exit_velocity_avg"].mean(),
        "pull_air_pct": player_data["pull_air_rate"].mean()
    }
def get_pitcher_stats(player_name):

    url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&player_type=pitcher&year=2026"

    df = pd.read_csv(url)

    player_data = df[df["player_name"] == player_name]

    if len(player_data) == 0:
        return {
            "hr9": 1.2,
            "barrel_allowed": 8,
            "flyball": 40,
            "xslg": 0.420
        }

    return {
        "hr9": player_data["home_run"].mean(),
        "barrel_allowed": player_data["barrel"].mean(),
        "flyball": player_data["launch_angle"].mean(),
        "xslg": player_data["estimated_slg"].mean()
    }
