import streamlit as st
from config.settings import DATA_CACHE_DIR

# Import modules from your modules folder
from modules.market import MarketDataEngine
from modules.technical import TechnicalIntelligenceEngine
from modules.volume import VolumeParticipationEngine
from modules.sector import SectorEngine
from modules.fundamental import FundamentalEngine
from modules.sentiment import SentimentEngine
from modules.risk import RiskManagementEngine
from modules.orchestrator import CoreOrchestrationEngine

# Page configuration
st.set_page_config(page_title="Performance Analytics Dashboard", layout="wide")
st.title("📊 Performance Analytics Dashboard")

# Initialize engines
try:
    # 1. Create the base engines
    data_eng = MarketDataEngine()
    tech_eng = TechnicalIntelligenceEngine()
    vol_eng = VolumeParticipationEngine()
    sector_eng = SectorEngine()
    fund_eng = FundamentalEngine()
    sent_eng = SentimentEngine()
    risk_eng = RiskManagementEngine()

    # 2. Inject these engines into the Orchestrator
    orchestrator = CoreOrchestrationEngine(
        data_eng, tech_eng, vol_eng, sector_eng, fund_eng, sent_eng, risk_eng
    )

except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# --- Example UI Section ---
st.sidebar.header("Controls")
if st.sidebar.button("Run Full Analysis"):
    with st.spinner("Processing data..."):
        try:
            # You can now call methods from your orchestrator
            # e.g., orchestrator.execute_all()
            st.success("Analysis Complete!")
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.write("System ready.")
