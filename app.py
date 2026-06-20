import streamlit as st
import pandas as pd

from data import build_slate
from model import calculate_hr_score

st.title("⚾ MLB HR Model (LIVE + STATCAST + LINEUPS)")

df = build_slate()

df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

st.subheader("🔥 Top HR Targets")

st.dataframe(df[["player", "game", "HR_Score"]])

st.subheader("Full Slate")

st.dataframe(df)
