from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.db_service import AlertService
from typing import List

router = APIRouter()

@router.get("/")
def get_all_alerts(db: Session = Depends(get_db)):
    """Get all alerts from database"""
    alerts = AlertService.get_all_alerts(db)
    return {
        "total": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "disaster_type": a.disaster_type,
                "alert_level": a.alert_level,
                "title": a.title,
                "message": a.message,
                "location": a.location,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "radius_km": a.radius_km,
                "probability": a.probability,
                "probability_percent":
                    f"{a.probability * 100:.1f}%",
                "is_active": a.is_active,
                "created_at": str(a.created_at),
                "source": a.source,
                "type": a.disaster_type,
                "level": a.alert_level.upper(),
                "action": get_action(a.alert_level),
                "timestamp": str(a.created_at),
            }
            for a in alerts
        ]
    }

@router.get("/active")
def get_active_alerts(db: Session = Depends(get_db)):
    """Get active alerts from database"""
    alerts = AlertService.get_active_alerts(db)
    return {
        "total": len(alerts),
        "alerts": [
            {
                "id": str(a.id),
                "disaster_type": a.disaster_type,
                "alert_level": a.alert_level,
                "title": a.title,
                "message": a.message,
                "location": a.location,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "probability": a.probability,
                "probability_percent":
                    f"{a.probability * 100:.1f}%",
                "is_active": a.is_active,
                "created_at": str(a.created_at),
                "source": a.source,
                "type": a.disaster_type,
                "level": a.alert_level.upper(),
                "action": get_action(a.alert_level),
                "timestamp": str(a.created_at),
            }
            for a in alerts
        ]
    }

@router.get("/nearby")
def get_nearby_alerts(
        lat: float,
        lon: float,
        radius: float = 200,
        db: Session = Depends(get_db)):
    """Get alerts near location"""
    alerts = AlertService.get_active_alerts(db)
    return {
        "your_location": {"lat": lat, "lon": lon},
        "search_radius_km": radius,
        "alerts": [
            {
                "id": str(a.id),
                "type": a.disaster_type,
                "level": a.alert_level.upper(),
                "title": a.title,
                "location": a.location,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "probability": a.probability,
                "probability_percent":
                    f"{a.probability * 100:.1f}%",
                "action": get_action(a.alert_level),
                "timestamp": str(a.created_at),
                "source": a.source,
            }
            for a in alerts
        ]
    }

@router.get("/{alert_id}")
def get_alert(
        alert_id: int,
        db: Session = Depends(get_db)):
    """Get single alert by ID"""
    alert = AlertService.get_alert_by_id(db, alert_id)
    if not alert:
        return {"error": "Alert not found"}
    return {
        "id": alert.id,
        "type": alert.disaster_type,
        "level": alert.alert_level.upper(),
        "title": alert.title,
        "location": alert.location,
        "latitude": alert.latitude,
        "longitude": alert.longitude,
        "probability": alert.probability,
        "action": get_action(alert.alert_level),
        "timestamp": str(alert.created_at),
        "source": alert.source,
    }

def get_action(level: str) -> str:
    """Get action message based on alert level"""
    actions = {
        "emergency": "EVACUATE immediately! Move to open areas!",
        "warning": "Be prepared to evacuate. Stay alert.",
        "watch": "Monitor the situation. Keep emergency kit ready.",
        "safe": "No immediate action required.",
    }
    return actions.get(level.lower(),
                       "Stay alert and monitor updates.")