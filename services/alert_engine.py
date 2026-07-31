import numpy as np
import pickle
import os
from datetime import datetime
from services.usgs_service import get_pakistan_earthquakes
from services.openweather_service import get_pakistan_flood_risks
from services.nasa_firms_service import get_pakistan_wildfires
from services.pmd_service import get_pakistan_weather_warnings

# Alert level thresholds
WATCH_THRESHOLD     = 0.40   # 40%
WARNING_THRESHOLD   = 0.60   # 60%
EMERGENCY_THRESHOLD = 0.80   # 80%

def get_alert_level(probability):
    """Convert probability to alert level"""
    if probability >= EMERGENCY_THRESHOLD:
        return "EMERGENCY", "🔴"
    elif probability >= WARNING_THRESHOLD:
        return "WARNING", "🟠"
    elif probability >= WATCH_THRESHOLD:
        return "WATCH", "🟡"
    else:
        return "SAFE", "🟢"

def calculate_earthquake_probability(magnitude, depth, lat, lon):
    """Calculate earthquake threat probability"""
    # Base probability from magnitude
    if magnitude >= 7.0:
        base_prob = 0.95
    elif magnitude >= 6.0:
        base_prob = 0.80
    elif magnitude >= 5.0:
        base_prob = 0.65
    elif magnitude >= 4.0:
        base_prob = 0.45
    elif magnitude >= 3.0:
        base_prob = 0.25
    else:
        base_prob = 0.10
    
    # Depth factor — shallow earthquakes are more dangerous
    if depth < 10:
        depth_factor = 1.3
    elif depth < 30:
        depth_factor = 1.1
    elif depth < 70:
        depth_factor = 0.9
    else:
        depth_factor = 0.7
    
    probability = min(base_prob * depth_factor, 0.99)
    return round(probability, 2)

def calculate_flood_probability(rainfall_mm, city):
    """Calculate flood probability from rainfall"""
    if rainfall_mm > 100:
        return 0.97
    elif rainfall_mm > 75:
        return 0.90
    elif rainfall_mm > 50:
        return 0.80
    elif rainfall_mm > 30:
        return 0.65
    elif rainfall_mm > 20:
        return 0.50
    elif rainfall_mm > 10:
        return 0.35
    elif rainfall_mm > 5:
        return 0.20
    else:
        return 0.05

def run_alert_engine():
    """Main alert engine — fetches data and generates alerts"""
    print(f"\n{'='*60}")
    print(f"🚨 ALERT ENGINE RUNNING — {datetime.now()}")
    print(f"{'='*60}")
    
    active_alerts = []
    
    # ── EARTHQUAKE ALERTS ──────────────────────────────────────
    print("\n🌍 Checking earthquakes...")
    try:
        eq_data = get_pakistan_earthquakes()
        earthquakes = eq_data.get("earthquakes", [])
        
        for quake in earthquakes:
            mag = quake.get("magnitude", 0)
            depth = quake.get("depth_km", 30)
            lat = quake.get("latitude", 0)
            lon = quake.get("longitude", 0)
            location = quake.get("location", "Pakistan")
            
            if mag >= 3.0:
                probability = calculate_earthquake_probability(
                    mag, depth, lat, lon)
                level, emoji = get_alert_level(probability)
                
                alert = {
                    "id": f"EQ_{quake.get('id', 'unknown')}",
                    "type": "earthquake",
                    "title": f"{emoji} Earthquake M{mag} — {location}",
                    "level": level,
                    "probability": probability,
                    "probability_percent": f"{probability*100:.1f}%",
                    "location": location,
                    "latitude": lat,
                    "longitude": lon,
                    "details": {
                        "magnitude": mag,
                        "depth_km": depth,
                    },
                    "action": get_earthquake_action(level),
                    "timestamp": str(datetime.now()),
                    "source": "USGS"
                }
                active_alerts.append(alert)
                print(f"   {emoji} M{mag} at {location} — {level} ({probability*100:.1f}%)")
        
        if not earthquakes:
            print("   ✅ No significant earthquakes detected")
    except Exception as e:
        print(f"   ⚠️ Earthquake check error: {e}")
    
    # ── FLOOD ALERTS ────────────────────────────────────────────
    print("\n🌊 Checking flood risks...")
    try:
        flood_data = get_pakistan_flood_risks()
        cities = flood_data.get("cities", [])
        
        for city in cities:
            rainfall = city.get("total_rainfall_24h_mm", 0)
            city_name = city.get("city", "Unknown")
            lat = city.get("latitude", 0)
            lon = city.get("longitude", 0)
            
            if rainfall > 10:
                probability = calculate_flood_probability(
                    rainfall, city_name)
                level, emoji = get_alert_level(probability)
                
                alert = {
                    "id": f"FL_{city_name}_{datetime.now().strftime('%Y%m%d')}",
                    "type": "flood",
                    "title": f"{emoji} Flood {level} — {city_name}",
                    "level": level,
                    "probability": probability,
                    "probability_percent": f"{probability*100:.1f}%",
                    "location": city_name,
                    "latitude": lat,
                    "longitude": lon,
                    "details": {
                        "rainfall_mm": rainfall,
                        "risk_category": city.get("flood_risk")
                    },
                    "action": get_flood_action(level),
                    "timestamp": str(datetime.now()),
                    "source": "OpenWeatherMap"
                }
                active_alerts.append(alert)
                print(f"   {emoji} {city_name}: {rainfall}mm rain — {level} ({probability*100:.1f}%)")
        
        if not any(c.get("total_rainfall_24h_mm", 0) > 10 for c in cities):
            print("   ✅ No significant flood risk detected")
    except Exception as e:
        print(f"   ⚠️ Flood check error: {e}")
    
    # ── WILDFIRE ALERTS ─────────────────────────────────────────
    print("\n🔥 Checking wildfires...")
    try:
        fire_data = get_pakistan_wildfires()
        fires = fire_data.get("wildfires", [])
        
        for i, fire in enumerate(fires[:5]):  # Max 5 fire alerts
            severity = fire.get("severity", "watch")
            probability = 0.85 if severity == "emergency" else \
                         0.65 if severity == "warning" else 0.45
            level, emoji = get_alert_level(probability)
            
            alert = {
                "id": f"WF_{i}_{datetime.now().strftime('%Y%m%d')}",
                "type": "wildfire",
                "title": f"{emoji} Wildfire Detected — Pakistan",
                "level": level,
                "probability": probability,
                "probability_percent": f"{probability*100:.1f}%",
                "location": "Pakistan",
                "latitude": fire.get("latitude", 0),
                "longitude": fire.get("longitude", 0),
                "details": {
                    "brightness": fire.get("brightness", 0),
                    "severity": severity
                },
                "action": "Avoid the area. Alert local fire department.",
                "timestamp": str(datetime.now()),
                "source": "NASA FIRMS"
            }
            active_alerts.append(alert)
            print(f"   {emoji} Wildfire at {fire['latitude']}, {fire['longitude']} — {level}")
        
        if not fires:
            print("   ✅ No active wildfires detected")
    except Exception as e:
        print(f"   ⚠️ Wildfire check error: {e}")
    
    # ── SUMMARY ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"📊 ALERT SUMMARY:")
    print(f"   Total active alerts: {len(active_alerts)}")
    
    emergencies = [a for a in active_alerts if a['level'] == 'EMERGENCY']
    warnings = [a for a in active_alerts if a['level'] == 'WARNING']
    watches = [a for a in active_alerts if a['level'] == 'WATCH']
    
    print(f"   🔴 EMERGENCY: {len(emergencies)}")
    print(f"   🟠 WARNING:   {len(warnings)}")
    print(f"   🟡 WATCH:     {len(watches)}")
    print(f"{'='*60}\n")
    
    return {
        "timestamp": str(datetime.now()),
        "total_alerts": len(active_alerts),
        "summary": {
            "emergency": len(emergencies),
            "warning": len(warnings),
            "watch": len(watches),
            "safe": "All clear" if not active_alerts else "Alerts active"
        },
        "alerts": active_alerts
    }

def get_earthquake_action(level):
    actions = {
        "EMERGENCY": "EVACUATE immediately! Move to open areas away from buildings!",
        "WARNING": "Be prepared to evacuate. Stay away from tall buildings.",
        "WATCH": "Stay alert. Keep emergency kit ready. Monitor updates.",
        "SAFE": "No immediate action required. Stay informed."
    }
    return actions.get(level, "Stay alert.")

def get_flood_action(level):
    actions = {
        "EMERGENCY": "EVACUATE low-lying areas immediately! Move to higher ground!",
        "WARNING": "Prepare to evacuate. Move valuables to upper floors.",
        "WATCH": "Monitor water levels. Avoid crossing flooded roads.",
        "SAFE": "No immediate action required. Stay informed."
    }
    return actions.get(level, "Stay alert.")

def get_alerts_near_location(lat, lon, radius_km=100):
    """Get alerts within radius of a given location"""
    import math
    
    all_alerts = run_alert_engine()
    nearby = []
    
    for alert in all_alerts.get("alerts", []):
        alert_lat = alert.get("latitude", 0)
        alert_lon = alert.get("longitude", 0)
        
        # Haversine distance calculation
        R = 6371  # Earth radius in km
        dlat = math.radians(alert_lat - lat)
        dlon = math.radians(alert_lon - lon)
        a = math.sin(dlat/2)**2 + \
            math.cos(math.radians(lat)) * \
            math.cos(math.radians(alert_lat)) * \
            math.sin(dlon/2)**2
        distance = R * 2 * math.asin(math.sqrt(a))
        
        if distance <= radius_km:
            alert["distance_km"] = round(distance, 1)
            nearby.append(alert)
    
    return {
        "your_location": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "total_nearby": len(nearby),
        "alerts": sorted(nearby, key=lambda x: x["distance_km"])
    }