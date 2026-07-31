import requests
from datetime import datetime

# Free NASA FIRMS API — no key needed for basic access!
NASA_FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
NASA_KEY = "your_nasa_key_here"  # We will add this later

def get_pakistan_wildfires():
    """Get wildfire hotspots in Pakistan using NASA FIRMS"""
    try:
        # Pakistan bounding box
        # Using the public endpoint — no key needed!
        url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/your_key/VIIRS_SNPP_NRT/PKstan/1"
        
        # Alternative: use public FIRMS data
        # This gives us Pakistan wildfire data for last 24 hours
        response = requests.get(
            "https://firms.modaps.eosdis.nasa.gov/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_SouthAsia_24h.csv",
            timeout=15
        )

        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            headers = lines[0].split(',')
            
            wildfires = []
            for line in lines[1:]:
                values = line.split(',')
                if len(values) >= 5:
                    try:
                        lat = float(values[0])
                        lon = float(values[1])
                        brightness = float(values[2])
                        
                        # Filter for Pakistan region
                        if 23.0 <= lat <= 37.5 and 60.0 <= lon <= 77.5:
                            wildfires.append({
                                "latitude": lat,
                                "longitude": lon,
                                "brightness": brightness,
                                "severity": get_fire_severity(brightness),
                                "disaster_type": "wildfire",
                                "source": "NASA FIRMS"
                            })
                    except:
                        continue
            
            return {
                "source": "NASA FIRMS",
                "region": "Pakistan",
                "total": len(wildfires),
                "wildfires": wildfires
            }
        else:
            return {
                "source": "NASA FIRMS",
                "total": 0,
                "wildfires": [],
                "message": "No active wildfire data available"
            }
    except Exception as e:
        return {"error": str(e), "source": "NASA FIRMS"}

def get_fire_severity(brightness):
    """Convert brightness temperature to severity"""
    if brightness > 400:
        return "emergency"
    elif brightness > 350:
        return "warning"
    else:
        return "watch"