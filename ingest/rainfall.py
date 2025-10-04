# ingest/rainfall.py
from db import get_db_connection
from datetime import datetime

def store_rainfall(location: str, timestamp: datetime, rainfall_mm: float):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rainfall_data (location, timestamp, rainfall_mm)
        VALUES (%s, %s, %s)
    """, (location, timestamp, rainfall_mm))
    conn.commit()
    cur.close()
    conn.close()

def fetch_rainfall():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT location, timestamp, rainfall_mm FROM rainfall_data ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"location": r[0], "timestamp": r[1], "rainfall_mm": r[2]} for r in rows]
