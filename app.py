import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Project Alpha", layout="wide")

st.title("📊 Project Alpha Dashboard")
st.markdown("---")

# Generate clean sample data
dates = pd.date_range(start="2026-01-01", periods=50)
df = pd.DataFrame(
    {"Timeline": dates, "Performance Metric": np.random.randn(50).cumsum()}
)

# Display data smoothly on both laptop and mobile
st.subheader("📈 Core Operational Trends")
st.line_chart(df.set_index("Timeline"))

st.subheader("📋 Raw Data Breakdown")
st.dataframe(df, use_container_width=True)
