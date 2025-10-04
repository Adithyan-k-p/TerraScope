# models/schemas.py
from pydantic import BaseModel
from datetime import datetime

class RainfallRecord(BaseModel):
    location: str
    timestamp: datetime
    rainfall_mm: float

class AnomalyRecord(BaseModel):
    location: str
    timestamp: datetime
    rainfall_mm: float
