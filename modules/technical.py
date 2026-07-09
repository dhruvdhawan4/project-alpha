# modules/technical.py
import numpy as np
import pandas as pd

class TechnicalIntelligenceEngine:
    """
    Module 2: Technical Intelligence Engine
    Computes structural breakout boundaries, trend strength, and momentum filters.
    """

    def __init__(self):
        pass

    def compute_indicators(self, df):
        # Work on a copy to prevent warnings
        df = df.copy()

        # Double check column structure is flat (Safety catch)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 1. Base Moving Average (Trend Baseline)
        df["Ema_20"] = df["Close"].ewm(span=20, adjust=False).mean()

        # 2. RSI Matrix (Momentum)
        change = df["Close"].diff()
        gain = change.where(change > 0, 0.0)
        loss = -change.where(change < 0, 0.0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean().replace(0.0, 0.00001)
        df["Rsi_14"] = 100 - (100 / (1 + (avg_gain / avg_loss)))

        # 3. ATR Volatility Boundary (For Risk Management)
        high_low = df["High"] - df["Low"]
        high_close = np.abs(df["High"] - df["Close"].shift())
        low_close = np.abs(df["Low"] - df["Close"].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["Atr_14"] = true_range.rolling(14).mean()

        # 4. ADX Trend Strength Component (Is the trend actually strong?)
        up_move = df["High"] - df["High"].shift()
        down_move = df["Low"].shift() - df["Low"]
        pos_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        neg_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

        rolled_tr = true_range.rolling(window=14).sum().replace(0.0, 0.00001)
        smoothed_pos = pd.Series(pos_dm, index=df.index).rolling(14).sum()
        smoothed_neg = pd.Series(neg_dm, index=df.index).rolling(14).sum()

        plus_di = 100 * (smoothed_pos / rolled_tr)
        minus_di = 100 * (smoothed_neg / rolled_tr)
        dx = 100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di).replace(0.0, 0.00001))
        df["Adx_14"] = dx.rolling(window=14).mean()

        # 5. Structural Levels (20-Day High Resistance Floor)
        df["Peak_20"] = df["High"].shift(1).rolling(window=20).max()

        # Clean up warm-up NaN rows safely
        df = df.bfill()
        
        return df
