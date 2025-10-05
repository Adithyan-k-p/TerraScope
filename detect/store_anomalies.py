from db import get_db_connection

def store_anomalies(df, column_name):
    conn = get_db_connection()
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO climate_anomalies (location, timestamp, parameter, value, deviation, severity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row["location"],
            row["timestamp"],
            column_name.split("_")[0],  # 'rainfall_mm' → 'rainfall'
            row[column_name],
            row["deviation"],
            row["severity"]
        ))
    conn.commit()
    cur.close()
    conn.close()
