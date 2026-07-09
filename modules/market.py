# modules/market.py
import os
import pandas as pd
import yfinance as yf
from config.settings import DATA_CACHE_DIR

class MarketDataEngine:
    """
    Module 1: Market Data Engine
    Handles data acquisition, caching, and flattening for the pipeline.
    Status: Production Ready, Multi-Index Immune, Cache-Enabled
    """

    def __init__(self, data_folder=DATA_CACHE_DIR):
        self.data_folder = data_folder
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

    def fetch_ohlcv(self, ticker, period="4mo", interval="1d"):
        """
        Fetches, flattens using cross-sections, caches clean data, and returns a robust DataFrame.
        """
        file_path = f"{self.data_folder}/{ticker}_{period}_{interval}.csv"

        # 1. Check for cache to optimize batch processing speeds
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            # Ensure no corrupted text rows leaked into numeric columns
            if (
                df is not None
                and not df.empty
                and "Close" in df.columns
                and not isinstance(df["Close"].iloc[0], str)
            ):
                return df
            else:
                os.remove(file_path)  # Auto-delete corrupted cache file

        # 2. Download fresh data
        try:
            # Download with auto_adjust to handle modern yfinance standards cleanly
            df = yf.download(
                ticker, period=period, interval=interval, auto_adjust=True, progress=False
            )

            if df is None or df.empty:
                print(f"❌ No data retrieved for {ticker}")
                return None

            # 3. Institutional-grade fix: Strip Multi-Index if yfinance returns it
            if isinstance(df.columns, pd.MultiIndex):
                # We extract the 0th level which contains the actual OHLCV headers
                df.columns = df.columns.get_level_values(0)

            # Standardize column headers to clean strings and force upper case for first letter
            df.columns = [str(col).capitalize() for col in df.columns]
            df.index.name = "Date"
            
            # Ensure index is standard datetime
            df.index = pd.to_datetime(df.index)

            # Drop any accidental string rows or completely empty rows
            df = df.dropna(subset=["Close"])

            # 4. Save the clean dataframe to cache
            df.to_csv(file_path)
            return df
            
        except Exception as e:
            print(f"❌ Error fetching {ticker}: {e}")
            return None
