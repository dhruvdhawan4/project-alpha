# config/settings.py

# Your Nifty 100 Universal Basket
# You can update this list as needed; the platform will automatically scale
NIFTY_100_UNIVERSAL_BASKET = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "SBIN.NS", "BHARTIARTL.NS", "LICI.NS", "KOTAKBANK.NS", "ITC.NS",
    "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "AXISBANK.NS", "TITAN.NS", "ULTRACEMCO.NS", "TATAMOTORS.NS"
    # Add the remaining Nifty 100 tickers here as you scale
]

# Global System Defaults
INITIAL_CAPITAL = 500000
DEFAULT_RISK_PER_TRADE = 0.01  # 1% risk per trade
BENCHMARK_TICKER = "^NSEI"     # Nifty 50 Index
