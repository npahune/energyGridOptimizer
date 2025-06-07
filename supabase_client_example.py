# Supabase Client Integration Example (Python)
# Task 1.3: Connect Supabase client to backend (FastAPI/Flask)

from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "<your-supabase-url>")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<your-supabase-key>")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Example: Fetch all locations
def get_locations():
    response = supabase.table("locations").select("*").execute()
    return response.data

# Example: Insert a new energy source
def add_energy_source(name: str, cost_per_kwh: float, emission_factor: float):
    response = supabase.table("energy_sources").insert({
        "name": name,
        "cost_per_kwh": cost_per_kwh,
        "emission_factor": emission_factor
    }).execute()
    return response.data
