# modules/volume.py
import sys
import os

# This allows the volume module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing volume code below this line ---
# Example:
class VolumeParticipationEngine:
    def __init__(self):
        self.data_dir = DATA_CACHE_DIR
    # ... rest of your code
import numpy as np
import pandas as pd

class VolumeParticipationEngine:
    """
    Module 3: Volume & Participation Engine
    Analyzes volume structures, liquidity shocks, and institutional money flow.
    """

    def __init__(self, baseline_window=20, cmf_window=21):
        self.baseline_window = baseline_window
        self.cmf_window = cmf_window

    def analyze_volume(self, df):
        df = df.copy()

        # 1. 20-Day Average Volume & Volume Surge Ratio
        # Shifted by 1 so we compare today's volume against the historical baseline
        df["Avg_Volume_20"] = df["Volume"].shift(1).rolling(window=self.baseline_window).mean().replace(0.0, 1.0)
        df["Volume_Surge_Ratio"] = df["Volume"] / df["Avg_Volume_20"]

        # 2. On-Balance Volume (OBV)
        price_change = df["Close"].diff()
        volume_direction = np.sign(price_change)
        volume_direction.iloc[0] = 0  # Initialize first row to 0
        df["OBV"] = (volume_direction * df["Volume"]).cumsum()

        # 3. Chaikin Money Flow (CMF)
        high_low_range = df["High"] - df["Low"]
        high_low_range = np.where(high_low_range == 0, 1e-10, high_low_range)

        mf_multiplier = ((df["Close"] - df["Low"]) - (df["High"] - df["Close"])) / high_low_range
        mf_volume = mf_multiplier * df["Volume"]

        sum_mf_volume = mf_volume.rolling(window=self.cmf_window).sum()
        sum_volume = df["Volume"].rolling(window=self.cmf_window).sum()
        df["CMF"] = sum_mf_volume / (sum_volume + 1e-10)

        # 4. Binary Institutional Buying Output
        df["Institutional_Buying"] = np.where(
            (df["Volume_Surge_Ratio"] > 1.5) & (df["CMF"] > 0.05), 1, 0
        )

        # Backfill initial NaN rows
        df = df.bfill()
        
        return df
