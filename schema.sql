-- EGLO Supabase/PostgreSQL Schema
-- Generated for Task 1.1: Define Supabase schema

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  timezone TEXT DEFAULT 'UTC',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE energy_loads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  load_kw DOUBLE PRECISION NOT NULL,
  is_forecast BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (timestamp)
);

CREATE TABLE energy_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  cost_per_kwh DOUBLE PRECISION,
  emission_factor DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE grid_switch_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  selected_source_id UUID REFERENCES energy_sources(id),
  created_by TEXT,
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (timestamp)
);

CREATE TABLE battery_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  battery_level_kwh DOUBLE PRECISION,
  action TEXT CHECK (action IN ('charge', 'discharge', 'idle')),
  amount_kwh DOUBLE PRECISION,
  created_by TEXT DEFAULT 'qnn',
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (timestamp)
);

CREATE TABLE weather_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  temperature_c DOUBLE PRECISION,
  humidity_percent DOUBLE PRECISION,
  solar_irradiance DOUBLE PRECISION,
  wind_speed DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (timestamp)
);

CREATE TABLE energy_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  price_per_kwh DOUBLE PRECISION,
  source_id UUID REFERENCES energy_sources(id),
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (timestamp)
);

CREATE TABLE qnn_forecast_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  forecast_at TIMESTAMPTZ,
  target_timestamp TIMESTAMPTZ,
  predicted_load_kw DOUBLE PRECISION,
  actual_load_kw DOUBLE PRECISION,
  model_version TEXT,
  error_mape DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now(),
  INDEX (location_id),
  INDEX (target_timestamp)
);

-- Optional users table for dashboard/multi-user
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT now()
);
