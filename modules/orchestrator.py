# modules/orchestrator.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR
import pandas as pd


class CoreOrchestrationEngine:
    """
    Module 9: Central Orchestrator
    Synthesizes technical indicators, structural breakouts, volume spikes, and risk boundaries.
    """
    def __init__(self, data_eng, tech_eng, vol_eng, sector_eng, fund_eng, sent_eng, risk_eng):
        self.data_dir = DATA_CACHE_DIR
        self.data_eng = data_eng
        self.tech_eng = tech_eng
        self.vol_eng = vol_eng
        self.sector_eng = sector_eng
        self.fund_eng = fund_eng
        self.sent_eng = sent_eng
        self.risk_eng = risk_eng

    def process_ticker_pipeline(self, ticker_symbol, asset_name, benchmark_df, sector_leaderboard):
        # TEMPORARY: no try/except here — we WANT this to crash with a real
        # error message so we can see what's actually failing. Put the
        # try/except back once this is confirmed working.

        # 1. Fetch asset historical matrix
        df = self.data_eng.fetch_ohlcv(ticker_symbol, period="4mo")
        if df is None or df.empty or len(df) < 30:
            raise ValueError(f"{ticker_symbol}: fetch_ohlcv returned no usable data (df is None/empty/too short)")

        # 2. Extract technical intel and volume structures
        df = self.tech_eng.compute_indicators(df)
        df = self.vol_eng.analyze_volume(df)

        last_row = df.iloc[-1]
        close_p = float(last_row["Close"])
        rsi_v = round(float(last_row.get("Rsi_14", 50.0)), 2)

        avg_vol = float(last_row.get("Avg_Volume_20", 1.0))
        raw_vol = float(last_row.get("Volume", 1.0))
        vol_surge = round(raw_vol / avg_vol, 2) if avg_vol > 0 else 1.0

        # 3. Assess Entry Conditions
        is_breakout = close_p > float(last_row.get("Peak_20", close_p + 1))
        is_trending = float(last_row.get("Adx_14", 0)) > 22.0
        is_rsi_healthy = 45 < rsi_v < 70

        # 4. Synthesize Live Signal Decision
        if is_breakout and is_trending and is_rsi_healthy:
            decision = "🚀 STRUCTURAL BUY TRIGGERED"
            atr_v = float(last_row.get("Atr_14", close_p * 0.02))
            trade_plan = self.risk_eng.calculate_trade_parameters(
                entry_price=close_p, atr=atr_v, direction="LONG"
            )
        else:
            decision = "🔍 STANDBY (No Breakout)"
            trade_plan = None

        fund_data = self.fund_eng.check_company_health(ticker_symbol) if self.fund_eng else None
        sent_data = self.sent_eng.analyze_news_buzz(asset_name) if self.sent_eng else None

        return {
            "Ticker": ticker_symbol,
            "Close": round(close_p, 2),
            "RSI": rsi_v,
            "Vol_Surge_Ratio": vol_surge,
            "Fundamental_Risk": fund_data["Risk_Flag"] if fund_data else "Unknown",
            "Media_Sentiment": sent_data["Buzz_Stance"] if sent_data else "Neutral",
            "Sector_Stance": "Tracking",
            "Signal_Decision": decision,
            "Trade_Plan": trade_plan,
        }


class WatchlistScreener:
    """
    Wraps around the CoreOrchestrationEngine to scan batches of stocks
    and isolate active trade ideas.
    """
    def __init__(self, orchestrator_engine):
        self.orchestrator = orchestrator_engine

    def scan_watchlist(self, watchlist_dict, benchmark_df, sector_leaderboard):
        compiled_results = []

        for ticker, name in watchlist_dict.items():
            card = self.orchestrator.process_ticker_pipeline(
                ticker_symbol=ticker,
                asset_name=name,
                benchmark_df=benchmark_df,
                sector_leaderboard=sector_leaderboard,
            )

            if card is not None:
                row = {
                    "Ticker": card["Ticker"],
                    "Price": card["Close"],
                    "RSI": card["RSI"],
                    "Vol_Surge": card["Vol_Surge_Ratio"],
                    "Risk_Status": card["Fundamental_Risk"],
                    "Sentiment": card["Media_Sentiment"],
                    "Decision": card["Signal_Decision"],
                    "Shares_To_Buy": card["Trade_Plan"]["Suggested_Shares"] if card["Trade_Plan"] else 0,
                    "Stop_Loss": card["Trade_Plan"]["Stop_Loss"] if card["Trade_Plan"] else 0.0,
                    "Target": card["Trade_Plan"]["Profit_Target"] if card["Trade_Plan"] else 0.0,
                }
                compiled_results.append(row)

        screener_df = pd.DataFrame(compiled_results)
        if not screener_df.empty:
            screener_df = screener_df.sort_values(by=["Decision", "Vol_Surge"], ascending=[False, False])

        return screener_df
