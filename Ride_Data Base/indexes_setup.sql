USE `urban_transport`;

ALTER TABLE journeys
  ADD INDEX IF NOT EXISTS idx_start_time (start_time),
  ADD INDEX IF NOT EXISTS idx_end_time (end_time),
  ADD INDEX IF NOT EXISTS idx_payment_mode (payment_mode),
  ADD INDEX IF NOT EXISTS idx_time_group (weekday_num, trip_hour),
  ADD INDEX IF NOT EXISTS idx_start_coords (start_lat, start_lng),
  ADD INDEX IF NOT EXISTS idx_end_coords (end_lat, end_lng),
  ADD INDEX IF NOT EXISTS idx_operator_id (operator_id);

