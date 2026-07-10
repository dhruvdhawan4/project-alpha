from pathlib import Path
import pandas as pd


class UniverseManager:
    """
    Central source of truth for all supported universes.

    Every module should obtain symbols through this class.
    No ticker should ever be hardcoded elsewhere.
    """

    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)

    def get_universe(self, name="nifty100"):
        """
        Returns a dictionary:

        {
            "RELIANCE.NS": "Reliance Industries",
            ...
        }
        """

        csv_path = self.config_dir / f"{name}.csv"

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Universe file not found: {csv_path}"
            )

        df = pd.read_csv(csv_path)

        required = {"YahooSymbol", "Company"}

        if not required.issubset(df.columns):
            raise ValueError(
                f"{csv_path} must contain columns: {required}"
            )

        df = df[df["Active"] == True]

        return dict(
            zip(df["YahooSymbol"], df["Company"])
        )

    def get_symbols(self, name="nifty100"):
        return list(self.get_universe(name).keys())

    def get_dataframe(self, name="nifty100"):
        return pd.read_csv(
            self.config_dir / f"{name}.csv"
        )
