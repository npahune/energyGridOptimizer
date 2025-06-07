from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from forecast_qnn_scaffold import forecast_energy_load
from supabase import create_client, Client
import os

app = FastAPI(title="EGLO API", description="Energy Grid Load Optimizer Prototype", version="0.1.0")

SUPABASE_URL = os.getenv("SUPABASE_URL", "<your-supabase-url>")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<your-supabase-key>")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Models ---
class ForecastRequest(BaseModel):
    location_id: str
    hours_ahead: int = 24

class ForecastResponse(BaseModel):
    forecasts: List[dict]

class OptimizeSwitchingRequest(BaseModel):
    location_id: str
    forecasted_loads: List[float]

class SwitchingPlanItem(BaseModel):
    time: datetime
    source: str

class SwitchingPlanResponse(BaseModel):
    schedule: List[SwitchingPlanItem]

class OptimizeBatteryRequest(BaseModel):
    location_id: str
    battery_level_kwh: float
    forecasted_loads: List[float]

class BatteryPlanItem(BaseModel):
    time: datetime
    action: str
    amount_kwh: float

class BatteryPlanResponse(BaseModel):
    battery_plan: List[BatteryPlanItem]

# --- Endpoints ---
@app.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    # Fetch historical loads for the location from Supabase
    history_resp = supabase.table("energy_loads").select("timestamp,load_kw").eq("location_id", req.location_id).order("timestamp", desc=True).limit(48).execute()
    history = [(datetime.fromisoformat(row["timestamp"]), row["load_kw"]) for row in history_resp.data] if history_resp.data else [(datetime.utcnow(), 100.0)] * 48
    # Fetch weather data (optional, fallback to empty)
    weather_resp = supabase.table("weather_data").select("timestamp,temperature_c").eq("location_id", req.location_id).order("timestamp", desc=True).limit(48).execute()
    weather = weather_resp.data if weather_resp.data else []
    forecasts = forecast_energy_load(history, weather, hours_ahead=req.hours_ahead)
    return {"forecasts": [{"timestamp": t.isoformat(), "forecast_load_kw": v} for t, v in forecasts]}

@app.post("/optimize-switching", response_model=SwitchingPlanResponse)
def optimize_switching(req: OptimizeSwitchingRequest):
    # Fetch available sources and prices for the location
    sources_resp = supabase.table("energy_sources").select("id,name,cost_per_kwh").execute()
    sources = sources_resp.data if sources_resp.data else []
    prices_resp = supabase.table("energy_prices").select("timestamp,price_per_kwh,source_id").eq("location_id", req.location_id).order("timestamp").limit(len(req.forecasted_loads)).execute()
    prices = prices_resp.data if prices_resp.data else []
    now = datetime.utcnow()
    # Simple greedy: pick the lowest cost source for each time slot
    schedule = []
    for i, load in enumerate(req.forecasted_loads):
        if prices:
            min_price = min(prices, key=lambda p: p["price_per_kwh"])
            source_id = min_price["source_id"]
            source = next((s["name"] for s in sources if s["id"] == source_id), "grid")
        else:
            source = "grid"
        schedule.append(SwitchingPlanItem(time=now.replace(hour=(now.hour+i)%24), source=source))
    return {"schedule": schedule}

@app.post("/optimize-battery", response_model=BatteryPlanResponse)
def optimize_battery(req: OptimizeBatteryRequest):
    # Fetch battery state for the location
    battery_resp = supabase.table("battery_states").select("timestamp,battery_level_kwh").eq("location_id", req.location_id).order("timestamp", desc=True).limit(1).execute()
    battery_level = battery_resp.data[0]["battery_level_kwh"] if battery_resp.data else req.battery_level_kwh
    now = datetime.utcnow()
    plan = []
    for i, load in enumerate(req.forecasted_loads):
        # Simple rule: charge if battery < 50, discharge if > 80
        if battery_level < 50:
            action = "charge"
            amount = min(10, 100 - battery_level)
            battery_level += amount
        elif battery_level > 80:
            action = "discharge"
            amount = min(10, battery_level)
            battery_level -= amount
        else:
            action = "idle"
            amount = 0
        plan.append(BatteryPlanItem(time=now.replace(hour=(now.hour+i)%24), action=action, amount_kwh=amount))
    return {"battery_plan": plan}
