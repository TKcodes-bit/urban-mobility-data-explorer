import pandas as pd
import numpy as np

def add_derived_features(df):
    """
    Adds derived features such as trip_speed (km/h), fare_per_km, and trip_distance.
    """
    # Convert datetime columns
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    
    # Compute trip duration in hours if not already (some datasets use seconds)
    df['trip_duration_hr'] = df['trip_duration'] / 3600  # convert seconds → hours
    
    # Compute approximate distance using Haversine formula
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [
        df['pickup_latitude'], df['pickup_longitude'],
        df['dropoff_latitude'], df['dropoff_longitude']
    ])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    df['trip_distance_km'] = R * c

    # Derived features
    df['trip_speed_kmh'] = df['trip_distance_km'] / df['trip_duration_hr']
    if 'fare_amount' in df.columns:
        df['fare_per_km'] = df['fare_amount'] / df['trip_distance_km'].replace(0, np.nan)

    # Handle infinities or missing results
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=['trip_speed_kmh'], inplace=True)

    return df
