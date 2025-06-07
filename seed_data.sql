-- Seed data for locations
INSERT INTO locations (name, latitude, longitude, timezone)
VALUES
  ('Grid Node Alpha', 37.7749, -122.4194, 'America/Los_Angeles'),
  ('Grid Node Beta', 40.7128, -74.0060, 'America/New_York'),
  ('Grid Node Gamma', 51.5074, -0.1278, 'Europe/London');

-- Seed data for energy sources
INSERT INTO energy_sources (name, cost_per_kwh, emission_factor)
VALUES
  ('grid', 0.20, 0.5),
  ('solar', 0.05, 0.0),
  ('battery', 0.10, 0.02);
