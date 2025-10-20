from flask import Flask, jsonify, request
import pandas as pd
import os

from calculation import add_derived_features
from algorithm import detect_suspicious_trips, summarize_data
from logger import log_unclean  # updated logger

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Urban Mobility Data Explorer API is running!"})

@app.route('/process-data', methods=['GET'])
def process_data():
    raw_data_path = os.path.join('Data', 'train.csv')
    clean_data_path = os.path.join('Data', 'cleaned_train.csv')

    # Step 1: Load raw data
    df = pd.read_csv(raw_data_path)
    original_len = len(df)

    # Step 2: Identify and remove rows with missing/invalid data
    required_columns = [
        'pickup_datetime', 'dropoff_datetime',
        'pickup_longitude', 'pickup_latitude',
        'dropoff_longitude', 'dropoff_latitude',
        'trip_duration'
    ]
    df_excluded = df[df[required_columns].isnull().any(axis=1) | (df['trip_duration'] <= 0)]
    df_clean = df.drop(df_excluded.index)

    # Step 3: Log all excluded rows
    if not df_excluded.empty:
        log_unclean(df_excluded)

    # Step 4: Add derived features
    df_clean = add_derived_features(df_clean)

    # Step 5: Detect suspicious trips
    suspicious = detect_suspicious_trips(df_clean)
    if not suspicious.empty:
        log_unclean(suspicious)

    # Step 6: Save cleaned data
    df_clean.to_csv(clean_data_path, index=False)

    # Step 7: Summarize data
    summary = summarize_data(df_clean)
    return jsonify({
        "message": f"Data processed successfully and saved to {clean_data_path}",
        "summary": summary
    })

if __name__ == '__main__':
    app.run(debug=True)
