# ingest/humidity.py
from db import get_db_connection
from datetime import datetime

def store_humidity(location: str, timestamp: datetime, humidity_percent: float):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO humidity_data (location, timestamp, humidity_percent)
        VALUES (%s, %s, %s)
    """, (location, timestamp, humidity_percent))
    conn.commit()
    cur.close()
    conn.close()

def fetch_humidity():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT location, timestamp, humidity_percent FROM humidity_data ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"location": r[0], "timestamp": r[1], "humidity_percent": r[2]} for r in rows]
