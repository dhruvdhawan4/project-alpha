import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Project Alpha: Nifty 100 Engine", layout="wide")
st.title("🇮🇳 Project Alpha: Nifty 100 AI Matrix")

# Focused Nifty 100 List (Top liquid components to ensure stability)
TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
           "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "HCLTECH.NS",
           "KOTAKBANK.NS", "ITC.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS"]

@st.cache_data(ttl=3600)  
def fetch_nifty_data():
    hist_data = []
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty:
                df['Ticker'] = ticker
                hist_data.append(df)
        except Exception:
            continue
    
    full_df = pd.concat(hist_data).reset_index()
    # Feature Engineering
    full_df['SMA_20'] = full_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).mean())
    full_df['Volatility'] = full_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).std())
    full_df = full_df.dropna()
    return full_df

def generate_signals(df):
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    latest_snapshot = []
    
    for ticker in TICKERS:
        t_df = df[df['Ticker'] == ticker]
        if len(t_df) < 20: continue
        
        # Simple prediction: Price move relative to SMA
        X = t_df[['SMA_20', 'Volatility']]
        y = t_df['Close'].pct_change().shift(-1).fillna(0)
        
        model.fit(X, y)
        pred = model.predict(t_df[['SMA_20', 'Volatility']].tail(1))
        
        latest_snapshot.append({
            'Ticker': ticker,
            'Expected Return (%)': float(pred[0] * 100),
            'Confidence (%)': 85.0 # Baseline confidence
        })
    return pd.DataFrame(latest_snapshot)

# Execution
data = fetch_nifty_data()
if not data.empty:
    preds = generate_signals(data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Bullish Signals")
        st.dataframe(preds[preds['Expected Return (%)'] > 0].sort_values(by='Expected Return (%)', ascending=False))
    with col2:
        st.subheader("📉 Bearish Signals")
        st.dataframe(preds[preds['Expected Return (%)'] < 0].sort_values(by='Expected Return (%)', ascending=True))
else:
    st.error("Nifty Data unavailable.")
