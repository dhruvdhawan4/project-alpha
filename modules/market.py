# modules/market.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import yfinance as yf
import pandas as pd

from config.settings import DATA_CACHE_DIR


class MarketDataEngine:
    """
    Production Market Data Engine

    Downloads historical OHLCV data from Yahoo Finance.

    Supported:
    - Nifty 50
    - Nifty 100
    - Nifty 200
    - Nifty 500
    - Entire NSE

    Example symbol:
        RELIANCE.NS
        TCS.NS
        INFY.NS
    """

    def __init__(self):

        self.cache_dir = DATA_CACHE_DIR

        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_ohlcv(
        self,
        ticker,
        period="6mo",
        interval="1d"
    ):

        try:

            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False,
                threads=False,
            )

            if df.empty:
                raise ValueError(
                    f"No data returned for {ticker}"
                )

            df = df.rename(
                columns={
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume",
                }
            )

            required = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ]

            for column in required:

                if column not in df.columns:
                    raise ValueError(
                        f"{ticker} missing column {column}"
                    )

            df = df.dropna()

            return df

        except Exception as e:

            raise Exception(
                f"Failed downloading {ticker}\n\n{e}"
            )
