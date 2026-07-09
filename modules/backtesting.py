# modules/backtesting.py
import sys
import os

# This allows the module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing backtesting code below this line ---
# Example:
class BacktestEngine:
    def __init__(self):
        self.data_dir = DATA_CACHE_DIR
    # ... rest of your code
import pandas as pd

class HistoricalBacktestEngine:
    """
    Institutional Regime-Aligned Backtester
    Simulates execution of the trading pipeline over historical bars.
    """

    def __init__(self, initial_capital=500000, risk_pct=1.0):
        self.initial_capital = initial_capital
        self.risk_pct = risk_pct

    def execute_backtest(self, processed_df, benchmark_df, tech_indicator_engine, risk_engine):
        df = processed_df.copy()

        # Ensure indicators are computed on both the asset and the benchmark index
        if "Peak_20" not in df.columns:
            df = tech_indicator_engine.compute_indicators(df)

        bench = benchmark_df.copy()
        if "Ema_20" not in bench.columns:
            bench = tech_indicator_engine.compute_indicators(bench)

        # Align time series indices exactly to prevent look-ahead bias
        df = df.dropna()
        bench = bench.dropna()

        in_position = False
        entry_price = 0.0
        stop_loss = 0.0
        shares = 0
        current_capital = self.initial_capital
        trade_records = []

        for i in range(25, len(df)):
            current_date = df.index[i]

            # Ensure the benchmark date exists to check index health safely
            if current_date not in bench.index:
                continue

            row = df.iloc[i]
            bench_row = bench.loc[current_date]

            close_p = float(row["Close"])
            low_p = float(row["Low"])

            if not in_position:
                # ENTRY LOGIC: ALPHA BREAKOUT + BETA MARKET ALIGNMENT
                is_structural_breakout = close_p > float(row.get("Peak_20", close_p + 1))
                is_trending = float(row.get("Adx_14", 0)) > 22.0
                is_rsi_healthy = 45 < float(row.get("Rsi_14", 0)) < 70
                is_market_healthy = float(bench_row["Close"]) > float(bench_row.get("Ema_20", 0))

                if is_structural_breakout and is_trending and is_rsi_healthy and is_market_healthy:
                    entry_price = close_p
                    atr_v = float(row["Atr_14"]) if "Atr_14" in row else (close_p * 0.02)

                    plan = risk_engine.calculate_trade_parameters(
                        entry_price=entry_price, atr=atr_v, direction="LONG"
                    )

                    if plan and plan["Suggested_Shares"] > 0:
                        stop_loss = plan["Stop_Loss"]
                        shares = plan["Suggested_Shares"]
                        cap_before = current_capital
                        in_position = True
            else:
                # POSITION PERFORMANCE MONITORING (3.5x ATR TRAILING STOP)
                atr_v = float(row["Atr_14"]) if "Atr_14" in row else (close_p * 0.02)
                new_potential_floor = close_p - (3.5 * atr_v)

                if new_potential_floor > stop_loss:
                    stop_loss = new_potential_floor

                if low_p <= stop_loss:
                    pnl = (stop_loss - entry_price) * shares
                    current_capital += pnl
                    reason = "TRAILING_PROFIT_CAPTURE" if stop_loss > entry_price else "STOP_LOSS"
                    
                    trade_records.append({
                        "Capital_Before": cap_before,
                        "PnL": pnl,
                        "Exit_Reason": reason,
                    })
                    in_position = False

        if len(trade_records) == 0:
            return pd.DataFrame(columns=["Capital_Before", "PnL", "Exit_Reason"])

        return pd.DataFrame(trade_records)
