import streamlit as st
import pandas as pd
from config.settings import DATA_CACHE_DIR

# Import all engine modules
from modules.market import MarketDataEngine
from modules.technical import TechnicalIntelligenceEngine
from modules.volume import VolumeParticipationEngine
from modules.sector import SectorEngine
from modules.fundamental import FundamentalEngine
from modules.sentiment import SentimentEngine
from modules.risk import RiskManagementEngine
from modules.orchestrator import CoreOrchestrationEngine, WatchlistScreener

st.set_page_config(page_title="Performance Analytics Dashboard", layout="wide")
st.title("📊 Performance Analytics Dashboard")

# --- TEMPORARY DIAGNOSTIC: confirms whether yfinance can actually fetch data on this cloud instance ---
# Delete this whole block once the dashboard is confirmed working.
with st.expander("🔧 Diagnostic: Test yfinance connection", expanded=True):
    if st.button("Run yfinance test"):
        import yfinance as yf
        try:
            test_df = yf.download("AAPL", period="5d", progress=False)
            if test_df is not None and not test_df.empty:
                st.success(f"yfinance is working. Got {len(test_df)} rows.")
                st.dataframe(test_df)
            else:
                st.error("yfinance returned an EMPTY dataframe — likely blocked/rate-limited by Yahoo on this cloud IP.")
        except Exception as e:
            st.error(f"yfinance raised an error: {e}")
# --- END DIAGNOSTIC BLOCK ---

# 1. Initialize Engines
try:
    data_eng = MarketDataEngine()
    tech_eng = TechnicalIntelligenceEngine()
    vol_eng = VolumeParticipationEngine()
    sector_eng = SectorEngine()
    fund_eng = FundamentalEngine()
    sent_eng = SentimentEngine()
    risk_eng = RiskManagementEngine()

    orchestrator = CoreOrchestrationEngine(
        data_eng, tech_eng, vol_eng, sector_eng, fund_eng, sent_eng, risk_eng
    )

    # Initialize the Screener
    screener = WatchlistScreener(orchestrator)
    st.success("All systems initialized successfully!")

except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# 2. Run Analysis UI
st.sidebar.header("Controls")
# Define your watchlist here
my_watchlist = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "MSFT": "Microsoft"}

if st.sidebar.button("Run Analysis"):
    with st.spinner("Scanning markets..."):
        try:
            # Execute the scan
            # We pass 'None' for unused benchmark/leaderboard data for now
            results_df = screener.scan_watchlist(my_watchlist, None, None)

            if results_df is not None and not results_df.empty:
                st.write("### Active Trade Ideas")
                st.dataframe(results_df, use_container_width=True)
                st.success(f"Scan complete! Found {len(results_df)} potential setups.")
            else:
                st.warning("No active trade signals found in your watchlist.")

        except Exception as e:
            st.error(f"Analysis Error: {e}")

st.write("System ready. Click 'Run Analysis' to begin the market scan.")
