# app.py
import streamlit as st
import pandas as pd
from modules.market import MarketDataEngine
from modules.technical import TechnicalIntelligenceEngine
from modules.volume import VolumeParticipationEngine
from modules.orchestrator import CoreOrchestrationEngine, WatchlistScreener
from modules.risk import RiskManagementEngine
from config.settings import NIFTY_100_UNIVERSAL_BASKET

# Streamlit Page Config
st.set_page_config(page_title="Project Alpha Terminal", layout="wide")
st.title("Alpha Terminal | Institutional Research Platform")

# Sidebar for Navigation
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Screener", "Settings"])

# Initialization of Backend Engines
market_eng = MarketDataEngine()
tech_eng = TechnicalIntelligenceEngine()
vol_eng = VolumeParticipationEngine()
risk_eng = RiskManagementEngine()

# Orchestrator (Injecting engines)
orchestrator = CoreOrchestrationEngine(
    market_eng, tech_eng, vol_eng, None, None, None, risk_eng
)
screener = WatchlistScreener(orchestrator)

# UI Logic
if page == "Dashboard":
    st.subheader("Market Summary")
    st.write("Welcome to the Terminal. Select 'Screener' to run the analysis.")

elif page == "Screener":
    if st.button("Run Daily Scan"):
        with st.spinner("Analyzing Nifty 100... This may take a moment."):
            # Running the scanner (We pass empty/placeholder for now to keep it simple)
            results = screener.scan_watchlist({t: t for t in NIFTY_100_UNIVERSAL_BASKET[:20]}, None, None)
            st.dataframe(results)

elif page == "Settings":
    st.subheader("Configuration")
    st.write("Manage your Universe, Risk Limits, and Committee Weights here.")
