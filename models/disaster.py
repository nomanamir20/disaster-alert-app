from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DisasterBase(BaseModel):
    type: str           # earthquake, flood, cyclone, wildfire
    severity: str       # watch, warning, emergency
    location: str       # city/province name
    latitude: float
    longitude: float
    description: str
    probability: float  # AI prediction 0.0 to 1.0

class DisasterCreate(DisasterBase):
    pass

class Disaster(DisasterBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True