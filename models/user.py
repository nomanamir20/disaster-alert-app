from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    phone: str
    city: str
    latitude: float
    longitude: float

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool = True
    fcm_token: Optional[str] = None  # Firebase push notification token

    class Config:
        from_attributes = True