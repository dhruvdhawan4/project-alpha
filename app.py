import streamlit as st

# Import configuration
from config.settings import DATA_CACHE_DIR

# Import your modules
# Ensure these match the filenames in your 'modules' folder
from modules.market import MarketDataEngine
from modules.analytics import PerformanceAnalyticsEngine
from modules.orchestrator import CoreOrchestrationEngine
from modules.backtesting import BacktestEngine
from modules.risk import RiskManagementEngine

# Initialize the Streamlit app
st.set_page_config(page_title="Performance Analytics Dashboard", layout="wide")
st.title("📊 Performance Analytics Dashboard")

# Initialize your engines
@st.cache_resource
def load_engines():
    return {
        "market": MarketDataEngine(),
        "analytics": PerformanceAnalyticsEngine(),
        "orchestrator": CoreOrchestrationEngine(),
        "backtest": BacktestEngine(),
        "risk": RiskManagementEngine()
    }

engines = load_engines()

# Example Dashboard Logic
st.sidebar.header("Controls")
if st.sidebar.button("Run Full Analysis"):
    with st.spinner("Processing data..."):
        try:
            # Example flow: 
            # 1. Fetch data
            # 2. Run Analytics
            # 3. Check Risk
            st.success("Analysis Complete!")
            st.write(f"Data directory: {DATA_CACHE_DIR}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.write("Welcome to your dashboard. Select an option from the sidebar to begin.")
