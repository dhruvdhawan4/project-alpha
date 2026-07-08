import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor
import time

# --- CONFIGURATION ---
TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
           "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "HCLTECH.NS", "KOTAKBANK.NS"]

st.set_page_config(page_title="Project Alpha: Core", layout="wide")
st.title("🏛️ Project Alpha: Institutional Committee")

@st.cache_data(ttl=3600)
def fetch_safe_data():
    master_list = []
    # Fetching sequentially to avoid server timeouts
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, period="6mo", progress=False)
            if df is not None and not df.empty and len(df) > 20:
                # Standardize data structure
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                # Compute Indicators safely
                df = df.copy()
                df['SMA_20'] = df['Close'].rolling(20).mean()
                delta = df['Close'].diff()
                gain = delta.clip(lower=0).rolling(14).mean()
                loss = -delta.clip(upper=0).rolling(14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))
                df['RVOL'] = df['Volume'] / df['Volume'].rolling(20).mean()
                
                df['Ticker'] = ticker
                master_list.append(df.tail(1))
            time.sleep(0.5) # Rate limiting to prevent API blocks
        except Exception:
            continue
            
    return pd.concat(master_list) if master_list else pd.DataFrame()

# --- AI ENGINE ---
def run_committee_logic(df):
    # Committee scoring
    df['AI_Score'] = (df['RSI'] < 45).astype(int) * 40 + (df['RVOL'] > 1.2).astype(int) * 30 + 30
    df['Weight'] = df['AI_Score'] / df['AI_Score'].sum()
    return df[['Ticker', 'Close', 'AI_Score', 'Weight']]

# --- EXECUTION ---
data = fetch_safe_data()

if not data.empty:
    results = run_committee_logic(data)
    st.subheader("📋 Daily Institutional Recommendations")
    st.dataframe(results.style.format({'Weight': '{:.1%}', 'Close': '₹{:.2f}'}), use_container_width=True)
else:
    st.warning("Data sync in progress. Please refresh the page in 60 seconds.")
