import streamlit as st

# Import configuration
from config.settings import DATA_CACHE_DIR

# Import your modules
from modules.market import MarketDataEngine
from modules.analytics import PerformanceAnalyticsEngine
from modules.orchestrator import CoreOrchestrationEngine
from modules.backtesting import BacktestEngine
from modules.risk import RiskManagementEngine

# Set up the dashboard page
st.set_page_config(page_title="Performance Analytics Dashboard", layout="wide")
st.title("📊 Performance Analytics Dashboard")

# Initialize engines directly (No caching to avoid TypeError)
try:
    market = MarketDataEngine()
    analytics = PerformanceAnalyticsEngine()
    orchestrator = CoreOrchestrationEngine()
    backtest = BacktestEngine()
    risk = RiskManagementEngine()
except Exception as e:
    st.error(f"Error initializing engines: {e}")
    st.stop()

# Example Dashboard UI
st.sidebar.header("Controls")
if st.sidebar.button("Run Full Analysis"):
    with st.spinner("Processing data..."):
        try:
            # Here you can now call your engine methods
            # Example: result = orchestrator.run_everything()
            st.success("Analysis Complete!")
            st.write(f"Using data from: {DATA_CACHE_DIR}")
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

st.write("System initialized and ready. Use the sidebar to trigger analysis.")
