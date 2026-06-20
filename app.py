import streamlit as st
import pandas as pd

from data import load_data
from model import calculate_hr_score

st.title("⚾ MLB HR Model Dashboard (v1)")

df = load_data()

df["HR_Score"] = df.apply(calculate_hr_score, axis=1)

df = df.sort_values("HR_Score", ascending=False)

st.subheader("🔥 Top HR Targets")

st.dataframe(df[["player", "HR_Score"]])

st.subheader("Full Slate")

st.dataframe(df)
