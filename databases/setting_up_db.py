import pandas as pd
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(current_dir, 'urban_db.db')
train_csv_path = os.path.join(current_dir, '../Backend/Data/cleaned_train.csv')

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
# creating tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendor(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS location(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_longitude REAL NOT NULL,
    pickup_latitude REAL NOT NULL,
    dropoff_longitude REAL NOT NULL,
    dropoff_latitude REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS trip(
    id TEXT PRIMARY KEY,
    vendor_id INTEGER,
    pickup_date TEXT NOT NULL,
    dropoff_date TEXT NOT NULL,
    passenger_count INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    store_and_fwd_flag TEXT NOT NULL CHECK (store_and_fwd_flag IN ('Y','N')),
    trip_duration INTEGER NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendor(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
)
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_pickup_date ON trip(pickup_date);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_dropoff_date ON trip(dropoff_date);")

cursor.execute("""
INSERT OR IGNORE INTO vendor (id, name) VALUES
(1, 'GoTaxi'),
(2, 'Move')
""")

conn.commit()

train_df = pd.read_csv(train_csv_path)

# If 'id' column is missing, find actual ID column
id_col = None
for col in train_df.columns:
    if col.lower() == 'id':
        id_col = col
        break
if not id_col:
    raise KeyError("Could not find ID column in train.csv. Please check the header name.")

# Extract unique locations
location_df = train_df[['pickup_longitude', 'pickup_latitude',
                        'dropoff_longitude', 'dropoff_latitude']].drop_duplicates()
location_df.reset_index(drop=True, inplace=True)

# Insert into location table
location_df.to_sql("location", conn, if_exists="append", index=False)

# Read back location table
location_db = pd.read_sql_query("SELECT * FROM location", conn)

# Merge to get location_id
merged_df = train_df.merge(
    location_db,
    on=['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'],
    how='left'
)

# Rename columns to match DB
merged_df.rename(columns={
    'pickup_datetime': 'pickup_date',
    'dropoff_datetime': 'dropoff_date',
    'id': id_col  # just to make sure it's consistent
}, inplace=True)

# If 'id' column not explicitly named 'id', rename it now
if id_col != 'id':
    merged_df.rename(columns={id_col: 'id'}, inplace=True)

# The location table id is our location_id
if 'id_y' in merged_df.columns:
    merged_df.rename(columns={'id_y': 'location_id'}, inplace=True)
else:
    merged_df.rename(columns={'id': 'location_id'}, inplace=True)

# trip id must be id_x or id
if 'id_x' in merged_df.columns:
    merged_df.rename(columns={'id_x': 'id'}, inplace=True)

trip_final = merged_df[['id', 'vendor_id', 'pickup_date', 'dropoff_date',
                        'passenger_count', 'location_id', 'store_and_fwd_flag', 'trip_duration']]

# Insert into trip table
trip_final.to_sql("trip", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Database created successfully with location and trip tables (vendor optional).")
