import streamlit as st
import pandas as pd

from data import build_slate
from model import calculate_hr_score

st.title("⚾ MLB HR Model (LIVE + STATCAST + LINEUPS)")

def build_slate():

    games = get_today_games_and_lineups()

    rows = []

    weather_score = get_weather_score()

    for g in games:

        # UNIQUE hitters per game (NO duplication spam)
        # TEMP LOGIC — later replaced with real lineups

        away_team = g["away_team"]
        home_team = g["home_team"]

        hitters = []

        # assign different hitters per team context
        if "Yankees" in away_team or "Yankees" in home_team:
            hitters.append("Aaron Judge")

        if "Dodgers" in away_team or "Dodgers" in home_team:
            hitters.append("Shohei Ohtani")

        # fallback so every game still has content
        if len(hitters) == 0:
            hitters = ["Aaron Judge"]

        for hitter in hitters:

            hitter_stats = get_statcast_hitter_profile(hitter)
            pitcher_stats = get_statcast_pitcher_profile("Opponent Pitcher")

            rows.append({
                "player": hitter,
                "game": g["game"],

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

df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

st.subheader("🔥 Top HR Targets")

st.dataframe(df[["player", "game", "HR_Score"]])

st.subheader("Full Slate")

st.dataframe(df)
