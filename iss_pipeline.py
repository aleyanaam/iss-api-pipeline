import requests
import pandas as pd
from sqlalchemy import create_engine
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# --- UPDATE THESE ---
DB_USER = "postgres"
DB_PASSWORD = "livandmaddie"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "space_data"
# --------------------

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def extract():
    """Fetch current ISS position from the API."""
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    return data

def transform(data):
    """Parse the API response into a clean DataFrame."""
    df = pd.DataFrame([{
        "timestamp": datetime.utcfromtimestamp(data["timestamp"]),
        "latitude": float(data["iss_position"]["latitude"]),
        "longitude": float(data["iss_position"]["longitude"]),
        "fetched_at": datetime.utcnow()
    }])
    return df

def load(df):
    """Append the new row into PostgreSQL."""
    df.to_sql("iss_location", engine, if_exists="append", index=False)

def run_pipeline():
    """Run the full ETL pipeline."""
    print(f"[{datetime.utcnow()}] Fetching ISS position...")
    raw = extract()
    df = transform(raw)
    load(df)
    print(f"  → Lat: {df['latitude'][0]}, Lon: {df['longitude'][0]}")

# Run immediately on start, then every 5 minutes
run_pipeline()

scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, "interval", minutes=5)
print("Scheduler started — running every 5 minutes. Press Ctrl+C to stop.")
scheduler.start()