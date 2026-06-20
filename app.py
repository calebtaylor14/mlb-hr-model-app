import streamlit as st
import pandas as pd

from data import get_today_games
from model import calculate_hr_score

st.title("⚾ MLB HR Model Dashboard (LIVE)")

df = get_today_games()

df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

st.subheader("🔥 Top HR Targets Today")

st.dataframe(df[["game", "HR_Score"]])

st.subheader("Full Slate")

st.dataframe(df)
