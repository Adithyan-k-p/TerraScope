import pandas as pd
from db import get_db_connection

def detect_anomalies(table, column, threshold, severity_levels):
    conn = get_db_connection()
    query = f"SELECT location, timestamp, {column} FROM {table} ORDER BY timestamp"
    df = pd.read_sql(query, conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    df["rolling_avg"] = df[column].rolling(window=7, min_periods=1).mean()
    df["deviation"] = df[column] - df["rolling_avg"]
    df["is_anomaly"] = abs(df["deviation"]) > threshold

    def classify_severity(dev):
        for label, bound in severity_levels.items():
            if abs(dev) >= bound:
                return label
        return "mild"

    df["severity"] = df["deviation"].apply(classify_severity)

    return df[df["is_anomaly"]][["location", column, "deviation", "severity"]].reset_index()
