from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
from db import get_db_connection
from ingest.rainfall import fetch_rainfall
from ingest.temperature import fetch_temperature
from ingest.humidity import fetch_humidity
from utils.nasa_api import fetch_nasa_data
from detect.pipeline import run_climate_anomaly_detection

app = Flask(__name__)
CORS(app)

# ✅ Home
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "TerraScope is running with NASA-powered anomaly detection"})

# ✅ User Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    district = data.get("district")
    panchayath = data.get("panchayath")

    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, email, password, district, panchayath)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (name, email, hashed_pw, district, panchayath))
        user_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"status": "success", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# ✅ User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password, district, panchayath FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and check_password_hash(user[1], password):
        return jsonify({
            "status": "success",
            "user_id": user[0],
            "district": user[2],
            "panchayath": user[3]
        })
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# 🚀 Ingest NASA Climate Data
@app.route("/ingest-nasa", methods=["GET"])
def ingest_nasa():
    try:
        inserted = fetch_nasa_data()
        return jsonify({
            "message": "NASA data ingested successfully",
            "records_inserted": inserted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🧠 Run Anomaly Detection
@app.route("/run-anomaly-detection", methods=["GET"])
def run_anomaly():
    run_climate_anomaly_detection()
    return jsonify({"message": "Anomaly detection completed and stored"})

# 📊 Fetch Rainfall Records
@app.route("/rainfall", methods=["GET"])
def get_rainfall():
    return jsonify(fetch_rainfall())

# 📊 Fetch Temperature Records
@app.route("/temperature", methods=["GET"])
def get_temperature():
    return jsonify(fetch_temperature())

# 📊 Fetch Humidity Records
@app.route("/humidity", methods=["GET"])
def get_humidity():
    return jsonify(fetch_humidity())

# 📍 Fetch Anomalies by District & Panchayath
@app.route("/anomalies", methods=["GET"])
def anomalies():
    district = request.args.get("district")
    panchayath = request.args.get("panchayath")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT parameter, value, deviation, severity, timestamp
        FROM climate_anomalies
        WHERE district=%s AND panchayath=%s
        ORDER BY timestamp DESC
        LIMIT 10
    """, (district, panchayath))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "parameter": r[0],
            "value": r[1],
            "deviation": r[2],
            "severity": r[3],
            "timestamp": r[4]
        } for r in rows
    ])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
