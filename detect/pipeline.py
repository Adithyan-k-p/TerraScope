from detect.anomaly_engine import detect_anomalies
from detect.store_anomalies import store_anomalies

def run_climate_anomaly_detection():
    rainfall = detect_anomalies(
        table="rainfall_data",
        column="rainfall_mm",
        threshold=20.0,
        severity_levels={"critical": 50, "moderate": 30, "mild": 20}
    )
    store_anomalies(rainfall, "rainfall_mm")

    temperature = detect_anomalies(
        table="temperature_data",
        column="temperature_c",
        threshold=5.0,
        severity_levels={"critical": 8, "moderate": 6, "mild": 5}
    )
    store_anomalies(temperature, "temperature_c")

    humidity = detect_anomalies(
        table="humidity_data",
        column="humidity_percent",
        threshold=10.0,
        severity_levels={"critical": 20, "moderate": 15, "mild": 10}
    )
    store_anomalies(humidity, "humidity_percent")
