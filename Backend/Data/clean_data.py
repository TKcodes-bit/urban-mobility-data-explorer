import pandas as pd
import os

def clean_data():
    """
    Loads raw NYC taxi data, cleans it, and saves the result.
    Returns the cleaned DataFrame.
    """

    raw_data_path = os.path.join('Backend', 'Data', 'train.csv')
    clean_data_path = os.path.join('Backend', 'Data', 'cleaned_train.csv')

    # Load dataset
    df = pd.read_csv(raw_data_path)
    print(f"Original dataset size: {len(df)} rows")

    # Drop rows with missing essential columns
    required_columns = [
        'pickup_datetime', 'dropoff_datetime',
        'pickup_longitude', 'pickup_latitude',
        'dropoff_longitude', 'dropoff_latitude',
        'trip_duration'
    ]
    df_clean = df.dropna(subset=required_columns)

    # Keep only valid durations and coordinates
    df_clean = df_clean[df_clean['trip_duration'] > 0]
    df_clean = df_clean[
        (df_clean['pickup_longitude'].between(-180, 180)) &
        (df_clean['pickup_latitude'].between(-90, 90)) &
        (df_clean['dropoff_longitude'].between(-180, 180)) &
        (df_clean['dropoff_latitude'].between(-90, 90))
    ]

    # Save cleaned dataset
    df_clean.to_csv(clean_data_path, index=False)
    print(f"Cleaned dataset saved to: {clean_data_path}")
    print(f"New dataset size: {len(df_clean)} rows (removed {len(df) - len(df_clean)} invalid rows)")

    return df_clean

# Allow running this file directly
if __name__ == "__main__":
    clean_data()
