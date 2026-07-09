# modules/portfolio.py
import sys
import os

# This allows the portfolio module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing portfolio code below this line ---
# Example:
class PortfolioEngine:
    def __init__(self):
        self.data_dir = DATA_CACHE_DIR
    # ... rest of your code
import pandas as pd
from config.settings import DEFAULT_CAPITAL

class PortfolioManager:
    """
    Fund Allocation & Execution Module
    Safely distributes available capital across high-confidence committee recommendations.
    """
    
    def __init__(self, total_capital=DEFAULT_CAPITAL):
        self.total_capital = total_capital

    def calculate_allocations(self, longs, shorts):
        if longs.empty and shorts.empty:
            return pd.DataFrame()

        # Equal split for the top long positions (using half the capital for longs)
        num_longs = len(longs)
        allocation_per_stock = (self.total_capital / 2) / num_longs if num_longs > 0 else 0

        report = longs.copy()
        report["Capital_Allocation"] = allocation_per_stock
        return report

    def generate_execution_tickets(self, longs, shorts):
        tickets = []

        num_longs = len(longs)
        num_shorts = len(shorts)
        
        long_alloc = (self.total_capital / 2) / num_longs if num_longs > 0 else 0
        short_alloc = (self.total_capital / 2) / num_shorts if num_shorts > 0 else 0

        # Process Longs with synthetic confidence overlays for the dashboard
        for _, row in longs.iterrows():
            tickets.append({
                "Ticker": row.get("Ticker", "UNKNOWN"),
                "Trade_Type": "LONG",
                "Confidence": 0.85,  # Later can be dynamically linked to volume strength
                "Expected_Return": "2.5%",
                "Capital_Allocation": round(long_alloc, 2),
                "Entry_Strategy": "Market Open",
                "Stop_Loss": "Trailing ATR"
            })

        # Process Shorts
        for _, row in shorts.iterrows():
            tickets.append({
                "Ticker": row.get("Ticker", "UNKNOWN"),
                "Trade_Type": "SHORT",
                "Confidence": 0.78,
                "Expected_Return": "-2.0%",
                "Capital_Allocation": round(short_alloc, 2),
                "Entry_Strategy": "Market Open",
                "Stop_Loss": "Trailing ATR"
            })

        return pd.DataFrame(tickets)
