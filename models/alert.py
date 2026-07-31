from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertBase(BaseModel):
    disaster_type: str    # earthquake, flood, cyclone, wildfire
    alert_level: str      # watch, warning, emergency
    title: str
    message: str
    location: str
    latitude: float
    longitude: float
    radius_km: float      # affected area radius

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    created_at: datetime
    is_active: bool = True
    affected_population: Optional[int] = None

    class Config:
        from_attributes = True