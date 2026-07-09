# modules/market.py
import sys
import os

# This allows the market module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing market code below this line ---
# Example:
import yfinance as yf
class MarketDataEngine:
    def __init__(self):
        self.cache_dir = DATA_CACHE_DIR
    # ... rest of your code
import sys
import os

# This block ensures Python can find the 'config' folder in the root directory
# even when the code is running from inside the 'modules' folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import pandas as pd
import yfinance as yf
from config.settings import DATA_CACHE_DIR

class MarketDataEngine:
    """
    Module: Market Data Engine
    Handles all OHLCV fetching and caching operations.
    """
    def __init__(self):
        # Ensure your data cache directory is defined in settings.py
        self.cache_dir = DATA_CACHE_DIR if 'DATA_CACHE_DIR' in globals() else "data_cache"

    def fetch_ohlcv(self, ticker, period="4mo"):
        try:
            df = yf.download(ticker, period=period, progress=False)
            if df.empty:
                return None
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
