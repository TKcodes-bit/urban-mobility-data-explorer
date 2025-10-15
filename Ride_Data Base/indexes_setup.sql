CREATE INDEX IF NOT EXISTS idx_start_time ON journeys (start_time);
CREATE INDEX IF NOT EXISTS idx_end_time ON journeys (end_time);
CREATE INDEX IF NOT EXISTS idx_payment_mode ON journeys (payment_mode);
CREATE INDEX IF NOT EXISTS idx_time_group ON journeys (weekday_num, trip_hour);
CREATE INDEX IF NOT EXISTS idx_start_coords ON journeys (start_lat, start_lng);
CREATE INDEX IF NOT EXISTS idx_end_coords ON journeys (end_lat, end_lng);

