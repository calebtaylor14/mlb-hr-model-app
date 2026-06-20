import streamlit as st
import pandas as pd

from data import build_slate
from model import calculate_hr_score

# -----------------------------
# APP TITLE
# -----------------------------
st.title("⚾ MLB HR Model (LIVE)")

# -----------------------------
# LOAD DATA SAFELY
# -----------------------------
df = build_slate()

# safety guard (prevents crashes)
if df is None or df.empty:
    st.error("No data loaded from build_slate()")
    st.stop()

# -----------------------------
# RUN MODEL
# -----------------------------
df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

# -----------------------------
# DISPLAY TOP TARGETS
# -----------------------------
st.subheader("🔥 Top HR Targets")

# dynamically handle missing columns safely
display_cols = [
    "player",
    "team",
    "batting_order",
    "barrel_pct",
    "hardhit_pct",
    "pull_air_pct",
    "iso",
    "pitcher_hr9",
    "pitcher_barrel_allowed",
    "pitcher_flyball",
    "pitcher_xslg",
    "pitcher_suppression",
    "park_score",
    "weather_score",
    "order_multiplier"
]

if "batting_order" in df.columns:
    display_cols.insert(2, "batting_order")

st.dataframe(df[display_cols])

# -----------------------------
# FULL TABLE
# -----------------------------
st.subheader("📊 Full Slate")

st.dataframe(df)

# -----------------------------
# DEBUG SECTION (optional but helpful)
# -----------------------------
with st.expander("Debug Data Preview"):
    st.write("Columns:", list(df.columns))
    st.dataframe(df.head())
