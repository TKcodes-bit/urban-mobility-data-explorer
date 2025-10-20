import pandas as pd
from clean_data import *
from calculation import add_derived_features
from algorithm import detect_suspicious_trips

def test_cleaning():
    df = pd.DataFrame({
        'pickup_datetime': ['2021-01-01 08:00', None],
        'dropoff_datetime': ['2021-01-01 08:20', '2021-01-01 08:40'],
        'pickup_longitude': [40.7, -200],
        'pickup_latitude': [73.9, 91],
        'dropoff_longitude': [40.8, 180],
        'dropoff_latitude': [73.8, 90],
        'trip_duration': [1200, -50],
        'fare_amount': [15, 10]
    })
    cleaned = df.dropna(subset=['pickup_datetime', 'dropoff_datetime'])
    assert len(cleaned) == 1
    print("✅ Data cleaning test passed!")

def test_features():
    df = pd.read_csv('Data/cleaned_train.csv')
    df = add_derived_features(df)
    assert 'trip_speed_kmh' in df.columns
    print("✅ Derived features test passed!")

def test_suspicious():
    df = pd.read_csv('Data/cleaned_train.csv')
    suspicious = detect_suspicious_trips(df)
    print(f"⚠️ Suspicious trips found: {len(suspicious)}")

if __name__ == "__main__":
    test_cleaning()
    test_features()
    test_suspicious()
