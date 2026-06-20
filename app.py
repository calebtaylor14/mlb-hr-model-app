import streamlit as st
import pandas as pd

from data import build_slate
from model import calculate_hr_score

st.title("⚾ MLB HR Model (LIVE)")

# -----------------------------
# LOAD DATA (THIS DEFINES df)
# -----------------------------
df = build_slate()

# -----------------------------
# SAFETY CHECK (prevents crash)
# -----------------------------
if df is None or df.empty:
    st.error("No data loaded")
    st.stop()

# -----------------------------
# MODEL RUN
# -----------------------------
df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

# -----------------------------
# OUTPUT
# -----------------------------
st.subheader("🔥 Top HR Targets")

st.dataframe(df[["player", "game", "batting_order", "HR_Score"]])

st.subheader("Full Slate")

st.dataframe(df)
