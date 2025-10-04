# utils/nasa_api.py
import requests
import os
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from ingest.rainfall import store_rainfall
from ingest.temperature import store_temperature
from ingest.humidity import store_humidity

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
LATITUDE = 9.6
LONGITUDE = 76.8

def fetch_nasa_data():
    today = datetime.now(UTC).strftime("%Y%m%d")
    start = (datetime.now(UTC) - timedelta(days=4)).strftime("%Y%m%d")

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOTCORR,T2M,RH2M"
        f"&start={start}&end={today}"
        f"&latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&community=RE&format=JSON"
        f"&api_key={NASA_API_KEY}"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    fill_value = data["header"].get("fill_value", -999.0)
    location = "Kerala, India"
    inserted = {"rainfall": 0, "temperature": 0, "humidity": 0}

    # 🌧️ Rainfall
    rainfall_data = data["properties"]["parameter"].get("PRECTOTCORR", {})
    for date_str, value in rainfall_data.items():
        if value != fill_value:
            timestamp = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=UTC)
            store_rainfall(location, timestamp, value)
            inserted["rainfall"] += 1

    # 🌡️ Temperature
    temp_data = data["properties"]["parameter"].get("T2M", {})
    for date_str, value in temp_data.items():
        if value != fill_value:
            timestamp = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=UTC)
            store_temperature(location, timestamp, value)
            inserted["temperature"] += 1

    # 💧 Humidity
    humidity_data = data["properties"]["parameter"].get("RH2M", {})
    for date_str, value in humidity_data.items():
        if value != fill_value:
            timestamp = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=UTC)
            store_humidity(location, timestamp, value)
            inserted["humidity"] += 1

    return inserted
