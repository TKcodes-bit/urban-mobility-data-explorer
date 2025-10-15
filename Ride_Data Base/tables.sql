CREATE TABLE IF NOT EXISTS operators (
  operator_id VARCHAR(8) PRIMARY KEY,
  company_name VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS payment_modes (
  mode_code VARCHAR(8) PRIMARY KEY,
  description VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS journeys (
  journey_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  operator_id VARCHAR(8),
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  start_lat DECIMAL(9,6) NOT NULL,
  start_lng DECIMAL(9,6) NOT NULL,
  end_lat DECIMAL(9,6) NOT NULL,
  end_lng DECIMAL(9,6) NOT NULL,
  distance_km DECIMAL(10,3) NOT NULL,
  duration_min DECIMAL(10,3) NOT NULL,
  fare DECIMAL(10,2) NOT NULL,
  tip DECIMAL(10,2) DEFAULT 0,
  payment_mode VARCHAR(8),

  avg_speed_kmh DECIMAL(10,3) GENERATED ALWAYS AS (
    CASE WHEN duration_min > 0 THEN distance_km / (duration_min / 60) ELSE NULL END
  ) STORED,

  fare_per_km DECIMAL(10,3) GENERATED ALWAYS AS (
    CASE WHEN distance_km > 0 THEN fare / distance_km ELSE NULL END
  ) STORED,

  trip_hour TINYINT GENERATED ALWAYS AS (HOUR(start_time)) STORED,
  weekday_num TINYINT GENERATED ALWAYS AS ((DAYOFWEEK(start_time) + 5) % 7) STORED,
  rush_flag TINYINT GENERATED ALWAYS AS (
    CASE WHEN HOUR(start_time) IN (7,8,9,16,17,18,19) THEN 1 ELSE 0 END
  ) STORED,
  weekend_flag TINYINT GENERATED ALWAYS AS (
    CASE WHEN DAYOFWEEK(start_time) IN (1,7) THEN 1 ELSE 0 END
  ) STORED,

  CONSTRAINT fk_journey_operator FOREIGN KEY (operator_id) REFERENCES operators(operator_id),
  CONSTRAINT fk_journey_payment FOREIGN KEY (payment_mode) REFERENCES payment_modes(mode_code)
);
CREATE TABLE IF NOT EXISTS stations (
  station_id VARCHAR(16) PRIMARY KEY,
  name VARCHAR(64),
  lat DECIMAL(9,6),
  lng DECIMAL(9,6),
  capacity INT
);