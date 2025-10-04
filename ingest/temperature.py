# ingest/temperature.py
from db import get_db_connection
from datetime import datetime

def store_temperature(location: str, timestamp: datetime, temperature_c: float):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO temperature_data (location, timestamp, temperature_c)
        VALUES (%s, %s, %s)
    """, (location, timestamp, temperature_c))
    conn.commit()
    cur.close()
    conn.close()

def fetch_temperature():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT location, timestamp, temperature_c FROM temperature_data ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"location": r[0], "timestamp": r[1], "temperature_c": r[2]} for r in rows]
