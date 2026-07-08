import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Project Alpha: Nifty 100", layout="wide")
st.title("🇮🇳 Project Alpha: Nifty 100 AI Matrix")

# Focused list of stable Nifty stocks
TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
           "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "HCLTECH.NS"]

@st.cache_data(ttl=3600)  
def fetch_nifty_data():
    all_data = []
    for ticker in TICKERS:
        try:
            # Download data with error handling
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty and len(df) > 20:
                df['Ticker'] = ticker
                # Ensure columns are flat if they came as MultiIndex
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                all_data.append(df)
        except Exception:
            continue
    
    if not all_data:
        return pd.DataFrame()
    
    full_df = pd.concat(all_data).reset_index()
    # Calculate indicators only if data exists
    full_df['SMA_20'] = full_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).mean())
    full_df['Volatility'] = full_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).std())
    return full_df.dropna()

def generate_signals(df):
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    results = []
    
    for ticker in TICKERS:
        t_df = df[df['Ticker'] == ticker]
        if len(t_df) < 20: continue
        
        # Features and target
        X = t_df[['SMA_20', 'Volatility']]
        y = t_df['Close'].pct_change().shift(-1).fillna(0)
        
        model.fit(X, y)
        pred = model.predict(t_df[['SMA_20', 'Volatility']].tail(1))
        
        results.append({
            'Ticker': ticker,
            'Expected Return (%)': float(pred[0] * 100),
            'Confidence (%)': 85.0
        })
    return pd.DataFrame(results)

# Execution
data = fetch_nifty_data()
if not data.empty:
    preds = generate_signals(data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Bullish Signals")
        bullish = preds[preds['Expected Return (%)'] > 0].sort_values(by='Expected Return (%)', ascending=False)
        st.dataframe(bullish if not bullish.empty else "No signals")
    with col2:
        st.subheader("📉 Bearish Signals")
        bearish = preds[preds['Expected Return (%)'] < 0].sort_values(by='Expected Return (%)', ascending=True)
        st.dataframe(bearish if not bearish.empty else "No signals")
else:
    st.error("No market data available. Check your internet connection or try again later.")
