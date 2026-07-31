from services.usgs_service import get_recent_earthquakes, get_pakistan_earthquakes
from services.openweather_service import get_all_pakistan_weather, get_pakistan_flood_risks
from services.nasa_firms_service import get_pakistan_wildfires
from services.pmd_service import get_pakistan_weather_warnings
from datetime import datetime

def run_all_feeds():
    """Run all disaster data feeds and combine results"""
    print(f"\n{'='*50}")
    print(f"Running disaster feeds at {datetime.now()}")
    print(f"{'='*50}")
    
    results = {}
    
    # Feed 1 — USGS Earthquakes
    print("\n🌍 Fetching USGS earthquake data...")
    results["earthquakes"] = get_pakistan_earthquakes()
    print(f"✅ Earthquakes: {results['earthquakes'].get('total', 0)} found")
    
    # Feed 2 — OpenWeatherMap Flood Risk
    print("\n🌊 Checking flood risks...")
    results["flood_risks"] = get_pakistan_flood_risks()
    print(f"✅ Flood data: {len(results['flood_risks'].get('cities', []))} cities checked")
    
    # Feed 3 — NASA FIRMS Wildfires
    print("\n🔥 Fetching NASA wildfire data...")
    results["wildfires"] = get_pakistan_wildfires()
    print(f"✅ Wildfires: {results['wildfires'].get('total', 0)} hotspots found")
    
    # Feed 4 — PMD Weather Warnings
    print("\n⛈️ Getting Pakistan weather warnings...")
    results["weather"] = get_pakistan_weather_warnings()
    print(f"✅ Weather: {results['weather'].get('total_cities', 0)} cities monitored")
    
    print(f"\n{'='*50}")
    print("All feeds completed!")
    print(f"{'='*50}\n")
    
    return results

def get_active_disaster_alerts():
    """Generate active alerts from all feeds"""
    all_data = run_all_feeds()
    active_alerts = []
    
    # Process earthquakes
    earthquakes = all_data.get("earthquakes", {}).get("earthquakes", [])
    for quake in earthquakes:
        if quake.get("magnitude", 0) >= 3.0:
            active_alerts.append({
                "type": "earthquake",
                "severity": quake.get("severity", "watch"),
                "title": f"Earthquake M{quake['magnitude']}",
                "location": quake.get("location", "Pakistan"),
                "latitude": quake.get("latitude", 0),
                "longitude": quake.get("longitude", 0),
                "message": f"Magnitude {quake['magnitude']} earthquake detected",
                "source": "USGS"
            })
    
    # Process flood risks
    flood_cities = all_data.get("flood_risks", {}).get("cities", [])
    for city in flood_cities:
        if city.get("flood_risk") in ["warning", "emergency"]:
            active_alerts.append({
                "type": "flood",
                "severity": city.get("flood_risk"),
                "title": f"Flood {city['flood_risk'].title()} — {city['city']}",
                "location": city.get("city", "Pakistan"),
                "latitude": city.get("latitude", 0),
                "longitude": city.get("longitude", 0),
                "message": city.get("message", "Flood risk detected"),
                "source": "OpenWeatherMap"
            })
    
    # Process wildfires
    wildfires = all_data.get("wildfires", {}).get("wildfires", [])
    for fire in wildfires:
        active_alerts.append({
            "type": "wildfire",
            "severity": fire.get("severity", "watch"),
            "title": "Wildfire Detected",
            "location": "Pakistan",
            "latitude": fire.get("latitude", 0),
            "longitude": fire.get("longitude", 0),
            "message": f"Active wildfire hotspot detected",
            "source": "NASA FIRMS"
        })
    
    return {
        "timestamp": str(datetime.now()),
        "total_alerts": len(active_alerts),
        "alerts": active_alerts
    }