# modules/risk.py
import pandas as pd

class RiskManagementEngine:
    """
    Module 7: Risk Management Engine 
    Dynamically sizes positions and sets defensive volatility boundaries using an expanded ATR factor.
    """

    def __init__(self, total_capital=500000, max_risk_per_trade_pct=1.0):
        self.total_capital = total_capital
        self.max_risk_per_trade = total_capital * (max_risk_per_trade_pct / 100.0)
        # 3.5 multiplier to survive standard market noise waves
        self.atr_multiplier = 3.5

    def calculate_trade_parameters(self, entry_price, atr, direction="LONG"):
        if atr <= 0 or entry_price <= 0:
            return None

        # Determine structural distance to risk termination point
        risk_per_share = atr * self.atr_multiplier

        # Sizing math: Total Risk Capital / Risk Per Unit
        # Use safe division and floor it to nearest integer share
        suggested_shares = int(self.max_risk_per_trade // risk_per_share) if risk_per_share > 0 else 0

        # Prevent oversizing beyond total liquid account equity safely
        if (suggested_shares * entry_price) > self.total_capital:
            suggested_shares = int(self.total_capital // entry_price)

        if direction == "LONG":
            stop_loss = entry_price - risk_per_share
            profit_target = entry_price + (risk_per_share * 2.5)
        else:
            stop_loss = entry_price + risk_per_share
            profit_target = entry_price - (risk_per_share * 2.5)

        return {
            "Suggested_Shares": suggested_shares,
            "Entry_Price": round(entry_price, 2),
            "Stop_Loss": round(stop_loss, 2),
            "Profit_Target": round(profit_target, 2),
            "Account_Risk_Allocated": round(suggested_shares * risk_per_share, 2),
        }
