# main.py
from fastapi import FastAPI
from ingest.rainfall import store_rainfall, fetch_rainfall
from ingest.temperature import store_temperature, fetch_temperature
from ingest.humidity import store_humidity, fetch_humidity
from utils.nasa_api import fetch_nasa_data
from datetime import datetime, UTC
from detect.pipeline import run_climate_anomaly_detection
from scheduler import start_scheduler

app = FastAPI()

# Start the hourly scheduler
start_scheduler()

@app.get("/")
def home():
    return {"message": "TerraScope is running with hourly anomaly detection"}

# 🌧️ Simulate Rainfall
@app.get("/simulate-rainfall")
def simulate_rainfall():
    timestamp = datetime.now(UTC)
    store_rainfall("Kerala", timestamp, 42.7)
    return {"message": "Rainfall data stored"}

# 🌡️ Simulate Temperature
@app.get("/simulate-temperature")
def simulate_temperature():
    timestamp = datetime.now(UTC)
    store_temperature("Kerala", timestamp, 33.2)
    return {"message": "Temperature data stored"}

# 💧 Simulate Humidity
@app.get("/simulate-humidity")
def simulate_humidity():
    timestamp = datetime.now(UTC)
    store_humidity("Kerala", timestamp, 68.5)
    return {"message": "Humidity data stored"}

# 🚀 Ingest NASA Climate Data
@app.get("/ingest-nasa")
def ingest_nasa():
    try:
        records = fetch_nasa_data()
        return {
            "message": "NASA data ingested successfully",
            "records_inserted": records
        }
    except Exception as e:
        return {"error": str(e)}

# 📊 Fetch Rainfall Records
@app.get("/rainfall")
def get_rainfall():
    return fetch_rainfall()

# 📊 Fetch Temperature Records
@app.get("/temperature")
def get_temperature():
    return fetch_temperature()

# 📊 Fetch Humidity Records
@app.get("/humidity")
def get_humidity():
    return fetch_humidity()

@app.get("/run-anomaly-detection")
def run_anomaly():
    run_climate_anomaly_detection()
    return {"message": "Anomaly detection completed and stored"}
