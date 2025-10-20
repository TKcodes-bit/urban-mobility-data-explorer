import pandas as pd
import os

# Path to unclean file
UNCLEAN_FILE = os.path.join(os.path.dirname(__file__), 'Data', 'unclean.csv')

def log_unclean(df):
    """
    Append unclean or suspicious rows to unclean.csv
    """
    if df is None or df.empty:
        return  # nothing to log

    # If the file exists, read it and append new rows
    if os.path.exists(UNCLEAN_FILE):
        existing = pd.read_csv(UNCLEAN_FILE)
        df = pd.concat([existing, df], ignore_index=True)

    # Save to CSV
    df.to_csv(UNCLEAN_FILE, index=False)
    print(f"Logged {len(df)} unclean rows to {UNCLEAN_FILE}")
