# modules/analytics.py
import numpy as np
import pandas as pd

class PerformanceAnalyticsEngine:
    """
    Module 8: Performance Analytics Engine
    Evaluates historical trade logs, calculating key metrics like win ratios, 
    profit factor, drawdown curves, and Sharpe ratios.
    """

    def __init__(self):
        pass

    def calculate_performance_metrics(self, trade_log_df):
        if trade_log_df is None or trade_log_df.empty:
            print("❌ Error: Trade log is empty.")
            return None

        pnl_val = trade_log_df["PnL"].astype(float)
        total_t = len(pnl_val)
        wins = pnl_val[pnl_val > 0]
        losses = pnl_val[pnl_val <= 0]

        # 1. Basic Stats
        w_count = len(wins)
        win_rate = (w_count / total_t) * 100 if total_t > 0 else 0.0

        # 2. Profit Factor
        g_prof = wins.sum()
        g_loss = abs(losses.sum())
        prof_fac = (g_prof / g_loss) if g_loss > 0 else (g_prof if g_prof > 0 else 1.0)

        # 3. Risk Reward Ratio
        avg_w = wins.mean() if len(wins) > 0 else 0.0
        avg_l = abs(losses.mean()) if len(losses) > 0 else 0.0
        rr_ratio = avg_w / avg_l if avg_l > 0 else 0.0

        # 4. Drawdown Curves
        capital_init = float(trade_log_df["Capital_Before"].iloc[0]) if "Capital_Before" in trade_log_df else 500000
        eq_curve = capital_init + pnl_val.cumsum()
        peaks = eq_curve.cummax()
        dd_curve = (eq_curve - peaks) / peaks
        max_dd = dd_curve.min() * 100 if not dd_curve.empty else 0.0

        # 5. Sharpe Performance Ratio
        rets = pnl_val / capital_init
        avg_r = rets.mean()
        std_r = rets.std()
        sharpe = (avg_r / std_r) * np.sqrt(252) if std_r > 0 else 0.0

        # Output Generation
        return {
            "Total_Trades": int(total_t),
            "Win_Rate_Pct": round(float(win_rate), 2),
            "Profit_Factor": round(float(prof_fac), 2),
            "Risk_Reward_Ratio": round(float(rr_ratio), 2),
            "Max_Drawdown_Pct": round(float(max_dd), 2),
            "Sharpe_Ratio": round(float(sharpe), 2),
            "Net_Profit": round(float(pnl_val.sum()), 2),
        }
