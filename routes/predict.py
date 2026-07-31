from fastapi import APIRouter
from pydantic import BaseModel
from services.alert_engine import (
    run_alert_engine,
    get_alerts_near_location,
    calculate_earthquake_probability,
    calculate_flood_probability,
    get_alert_level
)
from services.notification_service import notify_alert, get_notification_log

router = APIRouter()

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 100

class EarthquakeRequest(BaseModel):
    magnitude: float
    depth_km: float
    latitude: float
    longitude: float
    location: str = "Pakistan"

class FloodRequest(BaseModel):
    rainfall_mm: float
    city: str
    latitude: float
    longitude: float

@router.get("/run")
def run_predictions():
    """Run full AI alert engine — fetch data + generate alerts"""
    results = run_alert_engine()
    
    # Send notifications for warnings and emergencies
    notified = 0
    for alert in results.get("alerts", []):
        if alert["level"] in ["WARNING", "EMERGENCY"]:
            notify_alert(alert)
            notified += 1
    
    results["notifications_sent"] = notified
    return results

@router.post("/nearby")
def get_nearby_predictions(request: LocationRequest):
    """Get AI-predicted alerts near a specific location"""
    return get_alerts_near_location(
        request.latitude,
        request.longitude,
        request.radius_km
    )

@router.post("/earthquake")
def predict_earthquake(request: EarthquakeRequest):
    """Predict threat level for a specific earthquake"""
    probability = calculate_earthquake_probability(
        request.magnitude,
        request.depth_km,
        request.latitude,
        request.longitude
    )
    level, emoji = get_alert_level(probability)
    
    return {
        "disaster_type": "earthquake",
        "input": {
            "magnitude": request.magnitude,
            "depth_km": request.depth_km,
            "location": request.location
        },
        "prediction": {
            "probability": probability,
            "probability_percent": f"{probability*100:.1f}%",
            "alert_level": level,
            "emoji": emoji,
        },
        "action": f"Alert level {level}: {'EVACUATE immediately!' if level == 'EMERGENCY' else 'Stay alert and monitor updates.'}"
    }

@router.post("/flood")
def predict_flood(request: FloodRequest):
    """Predict flood risk for a city"""
    probability = calculate_flood_probability(
        request.rainfall_mm,
        request.city
    )
    level, emoji = get_alert_level(probability)
    
    return {
        "disaster_type": "flood",
        "input": {
            "city": request.city,
            "rainfall_mm": request.rainfall_mm,
        },
        "prediction": {
            "probability": probability,
            "probability_percent": f"{probability*100:.1f}%",
            "alert_level": level,
            "emoji": emoji,
        },
        "action": f"Flood {level} for {request.city}"
    }

@router.get("/notifications")
def get_notifications():
    """Get all sent notifications log"""
    return get_notification_log()