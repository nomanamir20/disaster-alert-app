import requests
from datetime import datetime

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
USGS_DAY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
USGS_WEEK_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson"

def get_recent_earthquakes():
    """Get earthquakes from last 1 hour worldwide"""
    try:
        response = requests.get(USGS_URL, timeout=10)
        data = response.json()
        
        earthquakes = []
        for feature in data["features"]:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            
            earthquake = {
                "id": feature["id"],
                "magnitude": props["mag"],
                "location": props["place"],
                "latitude": coords[1],
                "longitude": coords[0],
                "depth_km": coords[2],
                "time": datetime.fromtimestamp(props["time"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                "alert_level": props.get("alert", "green"),
                "url": props["url"],
                "disaster_type": "earthquake"
            }
            earthquakes.append(earthquake)
        
        return {
            "source": "USGS",
            "total": len(earthquakes),
            "earthquakes": earthquakes
        }
    except Exception as e:
        return {"error": str(e), "source": "USGS"}

def get_pakistan_earthquakes():
    """Filter earthquakes near Pakistan"""
    try:
        response = requests.get(USGS_DAY_URL, timeout=10)
        data = response.json()
        
        # Pakistan bounds
        PAK_LAT_MIN, PAK_LAT_MAX = 23.0, 37.5
        PAK_LON_MIN, PAK_LON_MAX = 60.0, 77.5
        
        pakistan_quakes = []
        for feature in data["features"]:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            lat, lon = coords[1], coords[0]
            
            # Check if within Pakistan region
            if PAK_LAT_MIN <= lat <= PAK_LAT_MAX and PAK_LON_MIN <= lon <= PAK_LON_MAX:
                quake = {
                    "id": feature["id"],
                    "magnitude": props["mag"],
                    "location": props["place"],
                    "latitude": lat,
                    "longitude": lon,
                    "depth_km": coords[2],
                    "time": datetime.fromtimestamp(props["time"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                    "disaster_type": "earthquake",
                    "severity": get_severity(props["mag"])
                }
                pakistan_quakes.append(quake)
        
        return {
            "source": "USGS",
            "region": "Pakistan",
            "total": len(pakistan_quakes),
            "earthquakes": pakistan_quakes
        }
    except Exception as e:
        return {"error": str(e)}
    
def get_severity(magnitude):
    """Convert magnitude to severity level"""
    if magnitude >= 7.0:
        return "emergency"
    elif magnitude >= 5.0:
        return "warning"
    elif magnitude >= 3.0:
        return "watch"
    else:
        return "info"