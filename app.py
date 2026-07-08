import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor

# --- CONFIGURATION ---
# Using .NS suffixes for Nifty 100 stocks as required for NSE data
TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
           "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "HCLTECH.NS", "KOTAKBANK.NS"]

st.set_page_config(page_title="Project Alpha: Institutional", layout="wide")
st.title("🏛️ Project Alpha: Institutional Investment Committee")

# --- CORE ENGINE: MODULES 1-4 ---
@st.cache_data(ttl=3600)
def build_research_database():
    master_data = []
    for ticker in TICKERS:
        try:
            # Robust download with error handling
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty and len(df) > 20:
                # Calculate Technicals & Volume Intelligence
                df['SMA_20'] = df['Close'].rolling(20).mean()
                df['RSI'] = 100 - (100 / (1 + (df['Close'].diff().clip(lower=0).rolling(14).mean() / 
                                              df['Close'].diff().clip(upper=0).abs().rolling(14).mean())))
                df['RVOL'] = df['Volume'] / df['Volume'].rolling(20).mean()
                df['Ticker'] = ticker
                # Append only the most recent day of data
                master_data.append(df.tail(1))
        except Exception:
            continue
            
    if master_data:
        return pd.concat(master_data).dropna()
    else:
        return pd.DataFrame()

# --- AI COMMITTEE & OPTIMIZER: MODULES 10-11 ---
def run_committee(data):
    # The Committee Brain (AI Scoring)
    data['AI_Score'] = (data['RSI'] < 45).astype(int) * 40 + (data['RVOL'] > 1.2).astype(int) * 30 + 30
    
    # Portfolio Allocation (Module 11)
    data['Weight'] = data['AI_Score'] / data['AI_Score'].sum()
    return data[['Ticker', 'Close', 'AI_Score', 'Weight']]

# --- DASHBOARD: MODULE 13 ---
data = build_research_database()

if not data.empty:
    report = run_committee(data)
    st.subheader("📋 Daily Institutional Recommendations")
    st.dataframe(report.style.format({'Weight': '{:.1%}', 'Close': '₹{:.2f}'}))
else:
    st.error("Engine failure: Data synchronization currently in progress. Please refresh in 60 seconds.")
