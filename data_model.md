Here is a **detailed PostgreSQL (Supabase-compatible)** data model for the **Energy Grid Load Optimizer (EGLO)**, designed to support:

* Load forecasting
* Grid switching optimization
* Battery utilization strategy
* Integration with APIs and historical inputs (weather, price, etc.)

---

## 🗂️ Data Model: Supabase (PostgreSQL)

---

### 1. **`locations`**

Stores metadata about grid-connected locations or nodes.

```sql
CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  timezone TEXT DEFAULT 'UTC',
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 2. **`energy_loads`**

Stores historical and forecasted energy load data.

```sql
CREATE TABLE energy_loads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  load_kw DOUBLE PRECISION NOT NULL,
  is_forecast BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT now()
);
```

> 🔍 `is_forecast = true` marks predicted values vs. actuals.

---

### 3. **`energy_sources`**

Defines the types of energy sources available (grid, solar, battery, etc.)

```sql
CREATE TABLE energy_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,         -- e.g., "grid", "solar", "battery"
  cost_per_kwh DOUBLE PRECISION, -- in $ or pricing unit
  emission_factor DOUBLE PRECISION, -- CO2 per kWh
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 4. **`grid_switch_plans`**

Represents optimized source-switching schedules.

```sql
CREATE TABLE grid_switch_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  selected_source_id UUID REFERENCES energy_sources(id),
  created_by TEXT, -- "qnn" | "manual" | "fallback"
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 5. **`battery_states`**

Captures battery storage utilization and charge/discharge plans.

```sql
CREATE TABLE battery_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  battery_level_kwh DOUBLE PRECISION,
  action TEXT CHECK (action IN ('charge', 'discharge', 'idle')),
  amount_kwh DOUBLE PRECISION,
  created_by TEXT DEFAULT 'qnn',
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 6. **`weather_data`**

Weather inputs for forecasting models.

```sql
CREATE TABLE weather_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  temperature_c DOUBLE PRECISION,
  humidity_percent DOUBLE PRECISION,
  solar_irradiance DOUBLE PRECISION,
  wind_speed DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 7. **`energy_prices`**

Represents grid pricing data used in optimization logic.

```sql
CREATE TABLE energy_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  timestamp TIMESTAMPTZ NOT NULL,
  price_per_kwh DOUBLE PRECISION,
  source_id UUID REFERENCES energy_sources(id),
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 8. **`qnn_forecast_logs`**

Logs raw QNN forecast outputs and error metrics (for future tuning).

```sql
CREATE TABLE qnn_forecast_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  forecast_at TIMESTAMPTZ,
  target_timestamp TIMESTAMPTZ,
  predicted_load_kw DOUBLE PRECISION,
  actual_load_kw DOUBLE PRECISION,
  model_version TEXT,
  error_mape DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now()
);
```

---

### 9. **`users`** (optional, for multi-user prototype or dashboard)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT now()
);
```

---

## 🧩 Entity Relationship Overview

```text
[locations]---(1:M)---[energy_loads]
           └---(1:M)---[grid_switch_plans]
           └---(1:M)---[battery_states]
           └---(1:M)---[weather_data]
           └---(1:M)---[energy_prices]

[energy_sources]---(1:M)---[grid_switch_plans]
                └---(1:M)---[energy_prices]

[energy_loads] ←→ [qnn_forecast_logs] (via timestamps + location_id)
```

---

## 🧠 Supabase Considerations

* Enable **Row-Level Security (RLS)** only if adding auth/users.
* Use **Supabase Realtime** to stream new forecasts or switching plans to a frontend dashboard.
* You can seed the database with dummy data for load, weather, and price using Supabase’s SQL editor.

---

Would you like a SQL dump or `.supabase/schema.sql` file ready to paste into the Supabase SQL editor?
