# modules/sector.py
import pandas as pd

class SectorRotationEngine:
    """
    Module 4: Sector Rotation Engine 
    Calculates relative strength and momentum rankings for market sectors against a benchmark index.
    """

    def __init__(self, lookback_periods=[5, 21, 63]):
        # 5 days (1 week), 21 days (1 month), 63 days (3 months)
        self.lookback_periods = lookback_periods

    def calculate_sector_momentum(self, sector_data_dict, benchmark_df):
        if benchmark_df is None or benchmark_df.empty:
            print("❌ Error: Benchmark data is empty.")
            return None

        # Clean benchmark series
        bench_close = benchmark_df["Close"].astype(float)
        sector_rankings = []

        for sector_name, sector_df in sector_data_dict.items():
            if sector_df is None or sector_df.empty:
                continue

            sector_close = sector_df["Close"].astype(float)

            # Align sector and benchmark dates to prevent mismatched rows
            combined = pd.concat(
                [sector_close, bench_close], axis=1, keys=["Sector", "Bench"]
            ).dropna()

            if combined.empty or len(combined) < max(self.lookback_periods):
                continue

            metrics = {"Sector": sector_name}
            total_score = 0

            # Weightings: Prefer short-term momentum for trading (50% weekly, 30% monthly, 20% quarterly)
            weights = {5: 0.50, 21: 0.30, 63: 0.20}

            for period in self.lookback_periods:
                sec_ret = (combined["Sector"].iloc[-1] / combined["Sector"].iloc[-period - 1]) - 1
                bench_ret = (combined["Bench"].iloc[-1] / combined["Bench"].iloc[-period - 1]) - 1

                # Relative Strength Performance (Alpha)
                relative_return = (sec_ret - bench_ret) * 100
                metrics[f"Alpha_{period}D(%)"] = round(relative_return, 2)
                total_score += relative_return * weights[period]

            metrics["Momentum_Score"] = round(total_score, 2)
            metrics["Market_Stance"] = "Outperforming" if total_score > 0 else "Underperforming"
            sector_rankings.append(metrics)

        ranking_df = pd.DataFrame(sector_rankings)
        if not ranking_df.empty:
            ranking_df = ranking_df.sort_values(by="Momentum_Score", ascending=False).reset_index(drop=True)

        return ranking_df
