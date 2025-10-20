import pandas as pd

def detect_suspicious_trips(df):
    """
    Identifies trips that look abnormal (e.g., too high speed or distance).
    """
    suspicious = df[
        (df['trip_speed_kmh'] > 120) |  # unrealistic speed
        (df['trip_distance_km'] > 100) |  # too long trip
        (df['trip_duration_hr'] > 5)  # unusually long trip
    ]
    return suspicious

def summarize_data(df):
    """
    Returns quick summary statistics for dashboard overview.
    """
    return {
        'total_trips': len(df),
        'avg_distance_km': round(df['trip_distance_km'].mean(), 2),
        'avg_speed_kmh': round(df['trip_speed_kmh'].mean(), 2),
        'avg_fare': round(df['fare_amount'].mean(), 2) if 'fare_amount' in df.columns else None
    }
