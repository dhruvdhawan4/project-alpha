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
    """
    BASE_URL = "https://api.twelvedata.com/time_series"

    def __init__(self):
        self.cache_dir = DATA_CACHE_DIR if 'DATA_CACHE_DIR' in globals() else "data_cache"
        self.api_key = st.secrets.get("TWELVEDATA_API_KEY", "")

    def fetch_ohlcv(self, ticker, period="4mo", interval="1day", outputsize=100):
        # TEMPORARY: no try/except swallowing — raise so the real reason
        # shows up on screen. Put the try/except back once confirmed working.

        if not self.api_key:
            raise ValueError("TWELVEDATA_API_KEY is missing or empty in Streamlit secrets.")

        params = {
            "symbol": ticker,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": self.api_key,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "error" or "values" not in data:
            raise ValueError(f"Twelve Data API response for {ticker}: {data}")

        df = pd.DataFrame(data["values"])
        if df.empty:
            raise ValueError(f"Twelve Data returned an empty values list for {ticker}")

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

        time.sleep(1)
        return df
