import sys
import os

# This allows the run_analysis module to reach the root 'config' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATA_CACHE_DIR

# --- Keep your existing run_analysis code below this line ---
# Example:
def execute_analysis():
    print(f"Running analysis using data from: {DATA_CACHE_DIR}")
    # ... rest of your code
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
