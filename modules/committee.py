# modules/committee.py
import pandas as pd

class CommitteeRanker:
    """
    The 'Brain' of the UI. Synthesizes signals and scores to rank the Nifty 100 universe.
    Takes the performance data and isolates actionable extremes.
    """
    
    def __init__(self):
        pass

    def rank_stocks(self, portfolio_data):
        """
        Takes a list of dictionaries containing analysis results.
        Returns:
            Top 10 Potential Longs
            Bottom 10 Potential Shorts
        """
        if not portfolio_data:
            return pd.DataFrame(), pd.DataFrame()
            
        df = pd.DataFrame(portfolio_data)

        # Dynamically identify the scoring column (Total_PnL, Score, etc.)
        sort_col = "Total_PnL" if "Total_PnL" in df.columns else (
            "Score" if "Score" in df.columns else df.columns[-1]
        )

        # Isolate the extremes for the portfolio manager
        longs = df.sort_values(by=sort_col, ascending=False).head(10)
        shorts = df.sort_values(by=sort_col, ascending=True).head(10)

        return longs, shorts
