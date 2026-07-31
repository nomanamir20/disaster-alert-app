import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

os.makedirs("ai_model/processed", exist_ok=True)

def prepare_earthquake_data():
    print("🌍 Preparing earthquake dataset...")
    
    df = pd.read_csv("ai_model/datasets/pakistan_earthquakes_20yr.csv")
    print(f"   Raw records: {len(df)}")
    
    # Keep only needed columns
    df = df[['time', 'latitude', 'longitude', 'depth', 'mag', 'place']].copy()
    
    # Handle missing values
    df = df.dropna(subset=['mag', 'latitude', 'longitude'])
    df['depth'] = df['depth'].fillna(df['depth'].median())
    
    # Parse time
    df['time'] = pd.to_datetime(df['time'])
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    
    # Feature engineering
    df = df.sort_values('time').reset_index(drop=True)
    
    # Rolling features — average magnitude of last 5 earthquakes
    df['mag_rolling_5'] = df['mag'].rolling(window=5, min_periods=1).mean()
    df['mag_rolling_10'] = df['mag'].rolling(window=10, min_periods=1).mean()
    
    # Lag features
    df['mag_lag_1'] = df['mag'].shift(1).fillna(0)
    df['mag_lag_2'] = df['mag'].shift(2).fillna(0)
    df['depth_lag_1'] = df['depth'].shift(1).fillna(0)
    
    # Severity encoding
    df['severity'] = df['mag'].apply(lambda x:
        3 if x >= 7.0 else
        2 if x >= 5.0 else
        1 if x >= 3.0 else 0
    )
    
    # Final features
    features = ['latitude', 'longitude', 'depth', 'month', 'hour',
                'mag_rolling_5', 'mag_rolling_10', 'mag_lag_1',
                'mag_lag_2', 'depth_lag_1']
    target = 'severity'
    
    X = df[features]
    y = df[target]
    
    # Normalize features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data 80/10/10
    train_end = int(len(X_scaled) * 0.8)
    val_end = int(len(X_scaled) * 0.9)
    
    X_train = X_scaled[:train_end]
    X_val = X_scaled[train_end:val_end]
    X_test = X_scaled[val_end:]
    
    y_train = y[:train_end]
    y_val = y[train_end:val_end]
    y_test = y[val_end:]
    
    # Save processed data
    with open("ai_model/processed/earthquake_data.pkl", "wb") as f:
        pickle.dump({
            "X_train": X_train, "X_val": X_val, "X_test": X_test,
            "y_train": y_train, "y_val": y_val, "y_test": y_test,
            "scaler": scaler, "features": features,
            "df": df
        }, f)
    
    print(f"   Clean records: {len(df)}")
    print(f"   Training set: {len(X_train)} records")
    print(f"   Validation set: {len(X_val)} records")
    print(f"   Test set: {len(X_test)} records")
    print(f"   Features: {len(features)}")
    print(f"   Severity distribution:\n{y.value_counts().sort_index()}")
    print(f"✅ Earthquake data saved to ai_model/processed/earthquake_data.pkl")
    return df

def prepare_flood_data():
    print("\n🌊 Preparing flood/rainfall dataset...")
    
    df = pd.read_csv("ai_model/datasets/pakistan_rainfall_2020_2023.csv")
    print(f"   Raw records: {len(df)}")
    
    # Handle missing values
    df['precipitation_mm'] = df['precipitation_mm'].fillna(0)
    df['temp_max'] = df['temp_max'].fillna(df['temp_max'].median())
    df['temp_min'] = df['temp_min'].fillna(df['temp_min'].median())
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Sort by city and date
    df = df.sort_values(['city', 'date']).reset_index(drop=True)
    
    # Feature engineering per city
    df['precip_rolling_3'] = df.groupby('city')['precipitation_mm'].transform(
        lambda x: x.rolling(3, min_periods=1).mean())
    df['precip_rolling_7'] = df.groupby('city')['precipitation_mm'].transform(
        lambda x: x.rolling(7, min_periods=1).mean())
    df['precip_rolling_30'] = df.groupby('city')['precipitation_mm'].transform(
        lambda x: x.rolling(30, min_periods=1).mean())
    
    # Lag features
    df['precip_lag_1'] = df.groupby('city')['precipitation_mm'].shift(1).fillna(0)
    df['precip_lag_3'] = df.groupby('city')['precipitation_mm'].shift(3).fillna(0)
    df['precip_lag_7'] = df.groupby('city')['precipitation_mm'].shift(7).fillna(0)
    
    # Flood risk label
    df['flood_risk'] = df['precipitation_mm'].apply(lambda x:
        3 if x > 50 else
        2 if x > 25 else
        1 if x > 10 else 0
    )
    
    # Final features
    features = ['latitude', 'longitude', 'month', 'day_of_year',
                'temp_max', 'temp_min',
                'precip_rolling_3', 'precip_rolling_7', 'precip_rolling_30',
                'precip_lag_1', 'precip_lag_3', 'precip_lag_7']
    target = 'flood_risk'
    
    X = df[features]
    y = df[target]
    
    # Normalize
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split 80/10/10
    train_end = int(len(X_scaled) * 0.8)
    val_end = int(len(X_scaled) * 0.9)
    
    X_train = X_scaled[:train_end]
    X_val = X_scaled[train_end:val_end]
    X_test = X_scaled[val_end:]
    
    y_train = y[:train_end]
    y_val = y[train_end:val_end]
    y_test = y[val_end:]
    
    # Save
    with open("ai_model/processed/flood_data.pkl", "wb") as f:
        pickle.dump({
            "X_train": X_train, "X_val": X_val, "X_test": X_test,
            "y_train": y_train, "y_val": y_val, "y_test": y_test,
            "scaler": scaler, "features": features,
            "df": df
        }, f)
    
    print(f"   Clean records: {len(df)}")
    print(f"   Training set: {len(X_train)} records")
    print(f"   Validation set: {len(X_val)} records")
    print(f"   Test set: {len(X_test)} records")
    print(f"   Features: {len(features)}")
    print(f"   Flood risk distribution:\n{y.value_counts().sort_index()}")
    print(f"✅ Flood data saved to ai_model/processed/flood_data.pkl")
    return df

if __name__ == "__main__":
    print("="*60)
    print("DATA CLEANING AND FEATURE ENGINEERING")
    print("="*60)
    
    eq_df = prepare_earthquake_data()
    flood_df = prepare_flood_data()
    
    print("\n" + "="*60)
    print("ALL DATASETS PREPARED AND SAVED!")
    print("Ready for AI model training on Day 5!")
    print("="*60)