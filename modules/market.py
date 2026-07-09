# modules/market.py
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import pandas as pd
import requests
import streamlit as st
from config.settings import DATA_CACHE_DIR


class MarketDataEngine:
    """
    Module: Market Data Engine
    Fetches OHLCV data via Twelve Data (free tier).
    Switched from yfinance because Yahoo Finance blocks/rate-limits
    requests coming from Streamlit Community Cloud's shared IPs.
    """
    BASE_URL = "https://api.twelvedata.com/time_series"

    def __init__(self):
        self.cache_dir = DATA_CACHE_DIR if 'DATA_CACHE_DIR' in globals() else "data_cache"
        self.api_key = st.secrets.get("TWELVEDATA_API_KEY", "")

    def fetch_ohlcv(self, ticker, period="4mo", interval="1day", outputsize=100):
        if not self.api_key:
            print("Missing TWELVEDATA_API_KEY in Streamlit secrets.")
            return None

        params = {
            "symbol": ticker,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": self.api_key,
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            data = resp.json()

            if data.get("status") == "error" or "values" not in data:
                print(f"Twelve Data error for {ticker}: {data.get('message', data)}")
                return None

            df = pd.DataFrame(data["values"])
            if df.empty:
                return None

            df = df.rename(columns={
                "datetime": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            })

            for col in ["Open", "High", "Low", "Close", "Volume"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date").set_index("Date")

            # Small pause to stay well under the free-tier per-minute limit
            # as your watchlist grows beyond a handful of tickers
            time.sleep(1)

            return df

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
