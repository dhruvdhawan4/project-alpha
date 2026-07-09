import pandas as pd

def run_project_alpha():

    data = {
        "Rank": [1, 2, 3, 4, 5],
        "Stock": [
            "ICICIBANK",
            "RELIANCE",
            "LT",
            "INFY",
            "BHARTIARTL"
        ],
        "Score": [95, 93, 91, 89, 88]
    }

    return pd.DataFrame(data)
