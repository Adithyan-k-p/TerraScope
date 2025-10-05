# db.py
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_db_engine():
    return engine

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print("❌ Database connection error:", e)
        return None
