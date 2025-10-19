import pandas as pd 
import os

raw_data_path = os.path.join('data', 'train.csv')
clean_data_path = os.path.join('data', 'cleaned_train.csv')


df = pd.read_csv(raw_data_path)
print(f"Original database size: {len(df)} rows")

df_clean = df.dropna(subset=[
    'pickup_datetime', 'dropoff_datatime',
    'pickup_longitude', 'pickup_latitude',
    'dropoff_longitude', 'dropoff_latitude',
    'trip_duration'


])

df_clean = df_clean[df_clean['tip_duration'] > 0] 

df_clean.to_csv(clean_data_path,index=False)
print(f"Cleaned data save to {clean_data_path}")
