import requests
import os

API_KEY = "ccc82fb77c6517a759235fb55c48c04f"

# Major Pakistan cities to monitor
PAKISTAN_CITIES = [
    {"name": "Karachi", "lat": 24.8607, "lon": 67.0011},
    {"name": "Lahore", "lat": 31.5204, "lon": 74.3587},
    {"name": "Islamabad", "lat": 33.6844, "lon": 73.0479},
    {"name": "Peshawar", "lat": 34.0151, "lon": 71.5249},
    {"name": "Quetta", "lat": 30.1798, "lon": 66.9750},
    {"name": "Multan", "lat": 30.1575, "lon": 71.5249},
    {"name": "Hyderabad", "lat": 25.3960, "lon": 68.3578},
    {"name": "Faisalabad", "lat": 31.4504, "lon": 73.1350},
]

def get_weather(city_name, lat, lon):
    """Get current weather for a city"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        return {
            "city": city_name,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", 0),
            "pressure": data["main"]["pressure"],
            "latitude": lat,
            "longitude": lon,
        }
    except Exception as e:
        return {"error": str(e), "city": city_name}

def get_all_pakistan_weather():
    """Get weather for all major Pakistan cities"""
    results = []
    for city in PAKISTAN_CITIES:
        weather = get_weather(city["name"], city["lat"], city["lon"])
        results.append(weather)
    return {
        "source": "OpenWeatherMap",
        "total_cities": len(results),
        "cities": results
    }

def check_flood_risk(lat, lon, city_name):
    """Check flood risk based on rainfall data"""
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "cnt": 8
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        total_rain = 0
        for item in data["list"]:
            rain = item.get("rain", {}).get("3h", 0)
            total_rain += rain

        if total_rain > 50:
            risk = "emergency"
        elif total_rain > 25:
            risk = "warning"
        elif total_rain > 10:
            risk = "watch"
        else:
            risk = "safe"

        return {
            "city": city_name,
            "total_rainfall_24h_mm": total_rain,
            "flood_risk": risk,
            "latitude": lat,
            "longitude": lon,
            "disaster_type": "flood"
        }
    except Exception as e:
        return {"error": str(e)}

def get_pakistan_flood_risks():
    """Check flood risk for all Pakistan cities"""
    risks = []
    for city in PAKISTAN_CITIES:
        risk = check_flood_risk(city["lat"], city["lon"], city["name"])
        risks.append(risk)
    return {
        "source": "OpenWeatherMap",
        "disaster_type": "flood",
        "cities": risks
    }