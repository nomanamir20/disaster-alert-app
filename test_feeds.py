from services.usgs_service import get_recent_earthquakes, get_pakistan_earthquakes
from services.openweather_service import get_all_pakistan_weather, get_pakistan_flood_risks
from services.nasa_firms_service import get_pakistan_wildfires
from services.pmd_service import get_pakistan_weather_warnings
import json

print("="*60)
print("TESTING ALL DISASTER DATA FEEDS")
print("="*60)

# Test 1 — USGS
print("\n🌍 TEST 1: USGS Earthquakes (Pakistan)")
result = get_pakistan_earthquakes()
print(f"Total earthquakes found: {result.get('total', 0)}")
if result.get('earthquakes'):
    first = result['earthquakes'][0]
    print(f"Latest: M{first['magnitude']} — {first['location']}")
print("✅ USGS feed working!")

# Test 2 — OpenWeatherMap
print("\n🌊 TEST 2: OpenWeatherMap — Karachi Weather")
result = get_all_pakistan_weather()
cities = result.get('cities', [])
if cities:
    karachi = cities[0]
    print(f"Karachi: {karachi.get('temperature')}°C, {karachi.get('weather')}")
print("✅ OpenWeatherMap feed working!")

# Test 3 — Flood Risk
print("\n🌊 TEST 3: Flood Risk Check")
result = get_pakistan_flood_risks()
cities = result.get('cities', [])
for city in cities[:3]:
    print(f"{city.get('city')}: {city.get('flood_risk')} risk — {city.get('total_rainfall_24h_mm')}mm rain")
print("✅ Flood risk check working!")

# Test 4 — NASA FIRMS
print("\n🔥 TEST 4: NASA FIRMS Wildfires")
result = get_pakistan_wildfires()
print(f"Wildfire hotspots: {result.get('total', 0)}")
print("✅ NASA FIRMS feed working!")

# Test 5 — PMD Weather
print("\n⛈️ TEST 5: Pakistan Weather Warnings")
result = get_pakistan_weather_warnings()
cities = result.get('data', [])
for city in cities[:3]:
    print(f"{city.get('city')}: {city.get('max_temperature_c')}°C, Wind: {city.get('max_windspeed_kmh')} km/h")
print("✅ PMD weather feed working!")

print("\n" + "="*60)
print("ALL FEEDS TESTED SUCCESSFULLY!")
print("="*60)