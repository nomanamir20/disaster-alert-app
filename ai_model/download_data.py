import requests
import pandas as pd
import os

os.makedirs("ai_model/datasets", exist_ok=True)

def download_usgs_historical():
    """Download 20 years of significant earthquake data from USGS"""
    print("📥 Downloading USGS earthquake historical data...")
    
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "csv",
        "starttime": "2004-01-01",
        "endtime": "2024-01-01",
        "minmagnitude": "4.0",
        "minlatitude": "23.0",
        "maxlatitude": "37.5",
        "minlongitude": "60.0",
        "maxlongitude": "77.5",
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code == 200:
        filepath = "ai_model/datasets/pakistan_earthquakes_20yr.csv"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        df = pd.read_csv(filepath)
        print(f"✅ Downloaded {len(df)} earthquake records!")
        print(f"   Saved to: {filepath}")
        print(f"   Date range: {df['time'].min()} to {df['time'].max()}")
        return df
    else:
        print(f"❌ Failed to download. Status: {response.status_code}")
        return None

def download_global_significant_earthquakes():
    """Download global significant earthquakes for broader training data"""
    print("\n📥 Downloading global significant earthquakes...")
    
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "csv",
        "starttime": "2014-01-01",
        "endtime": "2024-01-01",
        "minmagnitude": "5.0",
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code == 200:
        filepath = "ai_model/datasets/global_earthquakes_10yr.csv"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        df = pd.read_csv(filepath)
        print(f"✅ Downloaded {len(df)} global earthquake records!")
        print(f"   Saved to: {filepath}")
        return df
    else:
        print(f"❌ Failed to download. Status: {response.status_code}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("DOWNLOADING HISTORICAL DISASTER DATASETS")
    print("="*60)
    
    pak_quakes = download_usgs_historical()
    global_quakes = download_global_significant_earthquakes()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE!")
    print("="*60)