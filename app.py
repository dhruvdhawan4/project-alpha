import streamlit as st
from config.settings import DATA_CACHE_DIR

# Import modules
from modules.market import MarketDataEngine
from modules.technical import TechnicalIntelligenceEngine
from modules.volume import VolumeParticipationEngine
from modules.sector import SectorEngine
from modules.fundamental import FundamentalEngine
from modules.sentiment import SentimentEngine
from modules.risk import RiskManagementEngine
from modules.orchestrator import CoreOrchestrationEngine

st.set_page_config(page_title="Performance Analytics Dashboard", layout="wide")
st.title("📊 Performance Analytics Dashboard")

# Initialize and inject engines
try:
    # 1. Create instances in the order expected by the Orchestrator
    data_eng = MarketDataEngine()
    tech_eng = TechnicalIntelligenceEngine()
    vol_eng = VolumeParticipationEngine()
    sector_eng = SectorEngine()
    fund_eng = FundamentalEngine()
    sent_eng = SentimentEngine()
    risk_eng = RiskManagementEngine()

    # 2. Pass them into the Orchestrator to satisfy the __init__ requirements
    orchestrator = CoreOrchestrationEngine(
        data_eng, tech_eng, vol_eng, sector_eng, fund_eng, sent_eng, risk_eng
    )

    st.success("All engines initialized successfully!")

except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# Example interaction
if st.sidebar.button("Run Analysis"):
    st.write("Orchestrator is ready to process data.")
