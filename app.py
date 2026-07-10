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
from modules.universe import UniverseManager

st.set_page_config(
    page_title="Project Alpha",
    layout="wide"
)

st.title("📈 Project Alpha")
st.caption("AI Powered Institutional Investment Research Platform")

# ----------------------------------------------------
# Initialise all engines
# ----------------------------------------------------

try:
    data_eng = MarketDataEngine()
    tech_eng = TechnicalIntelligenceEngine()
    vol_eng = VolumeParticipationEngine()
    sector_eng = SectorEngine()
    fund_eng = FundamentalEngine()
    sent_eng = SentimentEngine()
    risk_eng = RiskManagementEngine()

    orchestrator = CoreOrchestrationEngine(
        data_eng,
        tech_eng,
        vol_eng,
        sector_eng,
        fund_eng,
        sent_eng,
        risk_eng,
    )

    screener = WatchlistScreener(orchestrator)

    universe = UniverseManager()

    my_watchlist = universe.get_universe("nifty100")

    st.success(f"Loaded {len(my_watchlist)} stocks from Nifty 100 universe.")

except Exception as e:
    st.error(f"Initialization Error : {e}")
    st.stop()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.header("Controls")

st.sidebar.write(f"Universe : Nifty 100")

st.sidebar.write(f"Stocks : {len(my_watchlist)}")

# ----------------------------------------------------
# Run Analysis
# ----------------------------------------------------

if st.sidebar.button("Run Analysis", use_container_width=True):

    with st.spinner("Running Project Alpha Analysis..."):

        try:

            results_df = screener.scan_watchlist(
                my_watchlist,
                None,
                None,
            )

            if (
                results_df is not None
                and not results_df.empty
            ):

                st.subheader("Trade Ideas")

                st.dataframe(
                    results_df,
                    use_container_width=True,
                )

                st.success(
                    f"Analysis completed successfully.\n\n"
                    f"Stocks Analysed : {len(my_watchlist)}\n"
                    f"Signals Found : {len(results_df)}"
                )

            else:

                st.warning(
                    "Analysis completed successfully.\n\n"
                    "No active trade signals were generated."
                )

        except Exception as e:

            st.error(f"Analysis Error : {e}")

st.info(
    "System ready.\n\n"
    "Click 'Run Analysis' to analyse the Nifty 100 universe."
)
