import requests
from datetime import datetime

def get_pakistan_weather_warnings():
    """
    Pakistan Meteorological Department data
    PMD doesn't have a public API so we use
    Open-Meteo which is FREE and needs no key!
    """
    
    PAKISTAN_CITIES = [
        {"name": "Karachi", "lat": 24.8607, "lon": 67.0011},
        {"name": "Lahore", "lat": 31.5204, "lon": 74.3587},
        {"name": "Islamabad", "lat": 33.6844, "lon": 73.0479},
        {"name": "Peshawar", "lat": 34.0151, "lon": 71.5249},
        {"name": "Quetta", "lat": 30.1798, "lon": 66.9750},
        {"name": "Multan", "lat": 30.1575, "lon": 71.5249},
    ]
    
    warnings = []
    
    for city in PAKISTAN_CITIES:
        try:
            # Open-Meteo — completely FREE, no key needed!
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "hourly": "precipitation,windspeed_10m,temperature_2m",
                "forecast_days": 1,
                "timezone": "Asia/Karachi"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            hourly = data.get("hourly", {})
            precipitation = hourly.get("precipitation", [0])
            windspeed = hourly.get("windspeed_10m", [0])
            temperature = hourly.get("temperature_2m", [0])
            
            max_rain = max(precipitation) if precipitation else 0
            max_wind = max(windspeed) if windspeed else 0
            max_temp = max(temperature) if temperature else 0
            
            # Generate warnings based on conditions
            city_warnings = []
            
            if max_rain > 20:
                city_warnings.append({
                    "type": "heavy_rain",
                    "severity": "warning",
                    "message": f"Heavy rainfall expected in {city['name']}: {max_rain}mm"
                })
            
            if max_wind > 60:
                city_warnings.append({
                    "type": "storm",
                    "severity": "warning",
                    "message": f"Strong winds in {city['name']}: {max_wind} km/h"
                })
            
            if max_temp > 45:
                city_warnings.append({
                    "type": "heatwave",
                    "severity": "watch",
                    "message": f"Extreme heat in {city['name']}: {max_temp}°C"
                })
            
            warnings.append({
                "city": city["name"],
                "latitude": city["lat"],
                "longitude": city["lon"],
                "max_rainfall_mm": max_rain,
                "max_windspeed_kmh": max_wind,
                "max_temperature_c": max_temp,
                "warnings": city_warnings
            })
            
        except Exception as e:
            warnings.append({
                "city": city["name"],
                "error": str(e)
            })
    
    return {
        "source": "Open-Meteo (PMD Alternative)",
        "timestamp": str(datetime.now()),
        "total_cities": len(warnings),
        "data": warnings
    }