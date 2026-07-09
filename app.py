# app.py
import streamlit as st
import pandas as pd

# Import our custom modules
from modules.market import MarketDataEngine
from modules.technical import TechnicalIntelligenceEngine
from modules.volume import VolumeParticipationEngine
from modules.risk import RiskManagementEngine
from modules.orchestrator import CoreOrchestrationEngine, WatchlistScreener
from config.settings import NIFTY_100_UNIVERSAL_BASKET

# 1. Page Configuration
st.set_page_config(page_title="Project Alpha | Institutional Terminal", layout="wide")

# 2. Sidebar Navigation
st.sidebar.title("Project Alpha")
page = st.sidebar.radio("Navigation", ["Dashboard", "Screener", "Risk Management"])

# 3. Initialization
@st.cache_resource
def initialize_system():
    return {
        "market": MarketDataEngine(),
        "tech": TechnicalIntelligenceEngine(),
        "vol": VolumeParticipationEngine(),
        "risk": RiskManagementEngine()
    }

engines = initialize_system()

# 4. Main UI Logic
if page == "Dashboard":
    st.title("Market Intelligence Dashboard")
    st.info("System Status: Operational. Ready for daily scan.")
    st.metric("Universe Size", len(NIFTY_100_UNIVERSAL_BASKET))

elif page == "Screener":
    st.title("Alpha Screener")
    if st.button("Execute Daily Alpha Scan"):
        with st.spinner("Processing Nifty 100... Analyzing signals..."):
            # Setup Orchestrator
            orchestrator = CoreOrchestrationEngine(
                engines["market"], engines["tech"], engines["vol"], 
                None, None, None, engines["risk"]
            )
            screener = WatchlistScreener(orchestrator)
            
            # Execute logic
            results = screener.scan_watchlist({t: t for t in NIFTY_100_UNIVERSAL_BASKET}, None, None)
            
            # Display results
            st.dataframe(results, use_container_width=True)
            st.success("Analysis Complete.")

elif page == "Risk Management":
    st.title("Risk Dashboard")
    st.write("Risk parameters are currently managed by the RiskManagementEngine.")
    # Add manual override controls here later if needed
