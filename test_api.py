import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_forecast():
    resp = client.post("/forecast", json={"location_id": "dummy", "hours_ahead": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert "forecasts" in data
    assert len(data["forecasts"]) == 3
    assert "forecast_load_kw" in data["forecasts"][0]

def test_optimize_switching():
    resp = client.post("/optimize-switching", json={"location_id": "dummy", "forecasted_loads": [100, 110, 120]})
    assert resp.status_code == 200
    data = resp.json()
    assert "schedule" in data
    assert len(data["schedule"]) == 3
    assert "source" in data["schedule"][0]

def test_optimize_battery():
    resp = client.post("/optimize-battery", json={"location_id": "dummy", "battery_level_kwh": 50, "forecasted_loads": [100, 110, 120]})
    assert resp.status_code == 200
    data = resp.json()
    assert "battery_plan" in data
    assert len(data["battery_plan"]) == 3
    assert "action" in data["battery_plan"][0]

def test_forecast_real_data():
    # Should not fail even if Supabase is empty
    resp = client.post("/forecast", json={"location_id": "dummy", "hours_ahead": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert "forecasts" in data
    assert len(data["forecasts"]) == 2

def test_optimize_switching_real_data():
    resp = client.post("/optimize-switching", json={"location_id": "dummy", "forecasted_loads": [100, 110]})
    assert resp.status_code == 200
    data = resp.json()
    assert "schedule" in data
    assert len(data["schedule"]) == 2
    assert "source" in data["schedule"][0]

def test_optimize_battery_real_data():
    resp = client.post("/optimize-battery", json={"location_id": "dummy", "battery_level_kwh": 50, "forecasted_loads": [100, 110]})
    assert resp.status_code == 200
    data = resp.json()
    assert "battery_plan" in data
    assert len(data["battery_plan"]) == 2
    assert "action" in data["battery_plan"][0]
