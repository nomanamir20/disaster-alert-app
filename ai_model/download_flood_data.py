import requests
import pandas as pd
import os

os.makedirs("ai_model/datasets", exist_ok=True)

def download_pakistan_rainfall_data():
    """
    Download historical rainfall data for Pakistan cities
    using Open-Meteo's free historical weather API
    """
    print("📥 Downloading Pakistan historical rainfall data...")
    
    cities = [
        {"name": "Karachi", "lat": 24.8607, "lon": 67.0011},
        {"name": "Lahore", "lat": 31.5204, "lon": 74.3587},
        {"name": "Islamabad", "lat": 33.6844, "lon": 73.0479},
        {"name": "Multan", "lat": 30.1575, "lon": 71.5249},
        {"name": "Hyderabad", "lat": 25.3960, "lon": 68.3578},
        {"name": "Sukkur", "lat": 27.7052, "lon": 68.8574},
    ]
    
    all_data = []
    
    for city in cities:
        print(f"   Fetching {city['name']}...")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "start_date": "2020-01-01",
            "end_date": "2023-12-31",
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
            "timezone": "Asia/Karachi"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precip = daily.get("precipitation_sum", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            
            for i in range(len(dates)):
                all_data.append({
                    "city": city["name"],
                    "date": dates[i],
                    "precipitation_mm": precip[i] if i < len(precip) else None,
                    "temp_max": temp_max[i] if i < len(temp_max) else None,
                    "temp_min": temp_min[i] if i < len(temp_min) else None,
                    "latitude": city["lat"],
                    "longitude": city["lon"],
                })
        except Exception as e:
            print(f"   ⚠️ Error fetching {city['name']}: {e}")
    
    df = pd.DataFrame(all_data)
    filepath = "ai_model/datasets/pakistan_rainfall_2020_2023.csv"
    df.to_csv(filepath, index=False)
    
    print(f"\n✅ Downloaded {len(df)} daily rainfall records!")
    print(f"   Saved to: {filepath}")
    print(f"   Cities covered: {df['city'].nunique()}")
    
    # Show flood-risk days (high rainfall)
    high_rain_days = df[df['precipitation_mm'] > 30]
    print(f"   High rainfall days (>30mm): {len(high_rain_days)}")
    
    return df

if __name__ == "__main__":
    print("="*60)
    print("DOWNLOADING PAKISTAN FLOOD/RAINFALL DATASET")
    print("="*60)
    
    rainfall_data = download_pakistan_rainfall_data()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE!")
    print("="*60)