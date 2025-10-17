-- Urban Mobility  Schema (SQLite)

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Create vendor table 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Create location table 
CREATE TABLE IF NOT EXISTS location(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_longitude REAL NOT NULL,
    pickup_latitude REAL NOT NULL,
    dropoff_longitude REAL NOT NULL,
    dropoff_latitude REAL NOT NULL
);

-- Create trip table 
CREATE TABLE IF NOT EXISTS trip(
    id TEXT PRIMARY KEY,
    vendor_id INTEGER,
    pickup_date TEXT NOT NULL,
    dropoff_date TEXT NOT NULL,
    passenger_count INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    store_and_fwd_flag TEXT NOT NULL CHECK (store_and_fwd_flag IN ('Y','N')),
    trip_duration INTEGER NOT NULL,
    -- Extra columns based on MySQL schema
    distance_km REAL,
    fare_amount REAL,
    tip_amount REAL,
    payment_type TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendor(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_pickup_date ON trip(pickup_date);
CREATE INDEX IF NOT EXISTS idx_dropoff_date ON trip(dropoff_date);
CREATE INDEX IF NOT EXISTS idx_vendor_id ON trip(vendor_id);
CREATE INDEX IF NOT EXISTS idx_location_id ON trip(location_id);
CREATE INDEX IF NOT EXISTS idx_trip_duration ON trip(trip_duration);

-- Insert initial vendor data 
INSERT OR IGNORE INTO vendor (id, name) VALUES
(1, 'GoTaxi'),
(2, 'Move');

-- View for trip summary with vendor and location details
CREATE VIEW IF NOT EXISTS trip_summary AS
SELECT 
    t.id,
    v.name as vendor_name,
    t.pickup_date,
    t.dropoff_date,
    t.passenger_count,
    t.trip_duration,
    l.pickup_longitude,
    l.pickup_latitude,
    l.dropoff_longitude,
    l.dropoff_latitude,
    t.store_and_fwd_flag
FROM trip t
LEFT JOIN vendor v ON t.vendor_id = v.id
LEFT JOIN location l ON t.location_id = l.id;

-- View for daily trip statistics
CREATE VIEW IF NOT EXISTS daily_stats AS
SELECT 
    DATE(pickup_date) as trip_date,
    COUNT(*) as total_trips,
    AVG(trip_duration) as avg_duration,
    SUM(passenger_count) as total_passengers,
    COUNT(DISTINCT vendor_id) as unique_vendors
FROM trip
GROUP BY DATE(pickup_date)
ORDER BY trip_date;

-- View for vendor performance
CREATE VIEW IF NOT EXISTS vendor_stats AS
SELECT 
    v.name as vendor_name,
    COUNT(t.id) as total_trips,
    AVG(t.trip_duration) as avg_duration,
    AVG(t.passenger_count) as avg_passengers
FROM vendor v
LEFT JOIN trip t ON v.id = t.vendor_id
GROUP BY v.id, v.name;