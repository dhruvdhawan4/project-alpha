# modules/fundamental.py
import sys
import os

# This allows the fundamental module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing fundamental code below this line ---
# Example:
class FundamentalEngine:
    def __init__(self):
        self.data_dir = DATA_CACHE_DIR
    # ... rest of your code
import yfinance as yf
import numpy as np

class FundamentalIntelligenceEngine:
    """
    Module 5: Fundamental Intelligence Engine
    Performs quick metric health checks and extracts corporate event risks.
    """
    def __init__(self):
        pass

    def check_company_health(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info

            # Extract metrics defensively with fallback defaults
            metrics = {
                "Ticker": ticker_symbol,
                "Company_Name": info.get("longName", "Unknown"),
                "PE_Trailing": info.get("trailingPE", None),
                "PE_Forward": info.get("forwardPE", None),
                "Price_To_Book": info.get("priceToBook", None),
                "ROE": info.get("returnOnEquity", None),
                "Profit_Margin": info.get("profitMargins", None),
                "Debt_To_Equity": info.get("debtToEquity", None),
                "Beta": info.get("beta", None)
            }

            if metrics["ROE"]: metrics["ROE"] = round(metrics["ROE"] * 100, 2)
            if metrics["Profit_Margin"]: metrics["Profit_Margin"] = round(metrics["Profit_Margin"] * 100, 2)
            if metrics["PE_Trailing"]: metrics["PE_Trailing"] = round(metrics["PE_Trailing"], 2)
            if metrics["PE_Forward"]: metrics["PE_Forward"] = round(metrics["PE_Forward"], 2)

            # Institutional safety check
            if metrics["Debt_To_Equity"] and metrics["Debt_To_Equity"] > 200:
                metrics["Risk_Flag"] = "HIGH_DEBT"
            elif metrics["PE_Trailing"] and metrics["PE_Trailing"] > 80:
                metrics["Risk_Flag"] = "EXTREME_VALUATION"
            else:
                metrics["Risk_Flag"] = "HEALTHY"

            return metrics

        except Exception as e:
            print(f"⚠️ Warning: Could not parse fundamentals for {ticker_symbol}: {e}")
            return None

    def get_upcoming_events(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            calendar = ticker.calendar
            event_info = {"Upcoming_Earnings_Start": None, "Upcoming_Earnings_End": None}

            if calendar is not None and not calendar.empty:
                if 'Earnings Date' in calendar.index:
                    dates = calendar.loc['Earnings Date'].values[0]
                    if isinstance(dates, (list, np.ndarray)):
                        event_info["Upcoming_Earnings_Start"] = str(dates[0]).split("T")[0]
                        if len(dates) > 1:
                            event_info["Upcoming_Earnings_End"] = str(dates[1]).split("T")[0]
                    else:
                        event_info["Upcoming_Earnings_Start"] = str(dates).split("T")[0]
            return event_info

        except Exception:
            return {"Upcoming_Earnings_Start": "None Scheduled", "Upcoming_Earnings_End": "None Scheduled"}
