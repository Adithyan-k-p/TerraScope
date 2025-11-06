from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db import get_db_connection

app = FastAPI()

@app.get("/alerts")
def get_anomaly_alerts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT location, timestamp, parameter, value, deviation, severity
        FROM climate_anomalies
        WHERE timestamp >= CURRENT_DATE - INTERVAL '2 days'
        ORDER BY timestamp DESC
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    alerts = []
    for location, timestamp, parameter, value, deviation, severity in rows:
        emoji = "🌧️" if parameter == "rainfall" else "🌡️" if parameter == "temperature" else "💧"
        severity_tag = "⚠" if severity > 0.5 else "🔍"
        message = (
            f"{severity_tag} {emoji} {parameter.capitalize()} anomaly in {location} on "
            f"{timestamp.strftime('%d-%b')} ({value:.1f}, deviation: {deviation:.1f}, severity: {severity:.2f})"
        )
        alerts.append({"location": location, "parameter": parameter, "message": message})

    return JSONResponse(content={"alerts": alerts})
