import mlflow
import pickle
import numpy as np
from datetime import datetime
import os

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlflow.db")

def log_earthquake_model():
    """Log earthquake model metrics to MLflow"""
    print("📊 Logging earthquake model to MLflow...")
    
    mlflow.set_experiment("Earthquake_LSTM_Model")
    
    with mlflow.start_run(run_name=f"earthquake_run_{datetime.now().strftime('%Y%m%d_%H%M')}"):
        
        # Log model parameters
        mlflow.log_param("model_type", "LSTM")
        mlflow.log_param("dataset", "USGS Pakistan 20-year")
        mlflow.log_param("training_records", 5147)
        mlflow.log_param("timesteps", 5)
        mlflow.log_param("lstm_units_1", 64)
        mlflow.log_param("lstm_units_2", 32)
        mlflow.log_param("dense_units", 16)
        mlflow.log_param("dropout_rate", 0.2)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("optimizer", "adam")
        mlflow.log_param("loss_function", "categorical_crossentropy")
        mlflow.log_param("epochs_trained", 30)
        mlflow.log_param("early_stopping_patience", 5)
        mlflow.log_param("num_classes", 4)
        mlflow.log_param("classes", "safe/watch/warning/emergency")
        
        # Log model metrics
        mlflow.log_metric("test_accuracy", 0.9255)
        mlflow.log_metric("test_loss", 0.2830)
        mlflow.log_metric("watch_precision", 0.93)
        mlflow.log_metric("watch_recall", 1.00)
        mlflow.log_metric("watch_f1_score", 0.96)
        mlflow.log_metric("training_samples", 4117)
        mlflow.log_metric("validation_samples", 514)
        mlflow.log_metric("test_samples", 510)
        
        # Log dataset info
        mlflow.log_param("features", 
            "latitude,longitude,depth,month,hour,"
            "mag_rolling_5,mag_rolling_10,"
            "mag_lag_1,mag_lag_2,depth_lag_1")
        mlflow.log_param("target", "severity_class")
        mlflow.log_param("train_split", "80%")
        mlflow.log_param("val_split", "10%")
        mlflow.log_param("test_split", "10%")
        
        # Log tags
        mlflow.set_tag("project", "Disaster Alert Pakistan")
        mlflow.set_tag("disaster_type", "earthquake")
        mlflow.set_tag("model_version", "1.0")
        mlflow.set_tag("status", "production_ready")
        mlflow.set_tag("target_achieved", "YES — 92.55% > 80% target")
        
        print("✅ Earthquake model logged to MLflow!")
        print(f"   Test Accuracy: 92.55%")
        print(f"   Test Loss: 0.2830")

def log_flood_model():
    """Log flood model metrics to MLflow"""
    print("\n📊 Logging flood model to MLflow...")
    
    mlflow.set_experiment("Flood_LSTM_Model")
    
    with mlflow.start_run(run_name=f"flood_run_{datetime.now().strftime('%Y%m%d_%H%M')}"):
        
        # Log model parameters
        mlflow.log_param("model_type", "LSTM")
        mlflow.log_param("dataset", "Pakistan Rainfall 2020-2023")
        mlflow.log_param("training_records", 8766)
        mlflow.log_param("timesteps", 7)
        mlflow.log_param("lstm_units_1", 128)
        mlflow.log_param("lstm_units_2", 64)
        mlflow.log_param("lstm_units_3", 32)
        mlflow.log_param("dropout_rate", 0.3)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("optimizer", "adam")
        mlflow.log_param("loss_function", "categorical_crossentropy")
        mlflow.log_param("epochs_trained", 30)
        mlflow.log_param("early_stopping_patience", 5)
        mlflow.log_param("num_classes", 4)
        mlflow.log_param("classes", "safe/watch/warning/emergency")
        
        # Log model metrics
        mlflow.log_metric("test_accuracy", 0.9667)
        mlflow.log_metric("val_accuracy", 0.9839)
        mlflow.log_metric("val_loss", 0.0817)
        mlflow.log_metric("training_samples", 7012)
        mlflow.log_metric("validation_samples", 876)
        mlflow.log_metric("test_samples", 876)
        
        # Flood risk distribution
        mlflow.log_metric("class_0_safe_samples", 8416)
        mlflow.log_metric("class_1_watch_samples", 268)
        mlflow.log_metric("class_2_warning_samples", 70)
        mlflow.log_metric("class_3_emergency_samples", 12)
        
        # Log dataset info
        mlflow.log_param("features",
            "latitude,longitude,month,day_of_year,"
            "temp_max,temp_min,"
            "precip_rolling_3,precip_rolling_7,precip_rolling_30,"
            "precip_lag_1,precip_lag_3,precip_lag_7")
        mlflow.log_param("target", "flood_risk_class")
        mlflow.log_param("cities_covered", 6)
        mlflow.log_param("cities",
            "Karachi,Lahore,Islamabad,Multan,Hyderabad,Sukkur")
        
        # Log tags
        mlflow.set_tag("project", "Disaster Alert Pakistan")
        mlflow.set_tag("disaster_type", "flood")
        mlflow.set_tag("model_version", "1.0")
        mlflow.set_tag("status", "production_ready")
        mlflow.set_tag("target_achieved", "YES — 96.67% > 85% target")
        
        print("✅ Flood model logged to MLflow!")
        print(f"   Test Accuracy: 96.67%")
        print(f"   Val Accuracy: 98.39%")

def log_data_pipeline():
    """Log data pipeline info to MLflow"""
    print("\n📊 Logging data pipeline to MLflow...")
    
    mlflow.set_experiment("Data_Pipeline")
    
    with mlflow.start_run(run_name=f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}"):
        
        mlflow.log_param("usgs_source", "earthquake.usgs.gov")
        mlflow.log_param("openweather_source", "api.openweathermap.org")
        mlflow.log_param("nasa_source", "firms.modaps.eosdis.nasa.gov")
        mlflow.log_param("pmd_source", "api.open-meteo.com")
        
        mlflow.log_metric("earthquake_records", 5147)
        mlflow.log_metric("global_earthquake_records", 17245)
        mlflow.log_metric("rainfall_records", 8766)
        mlflow.log_metric("total_records", 31158)
        mlflow.log_metric("cities_monitored", 6)
        mlflow.log_metric("years_of_data", 20)
        
        mlflow.set_tag("pipeline_status", "operational")
        mlflow.set_tag("update_frequency", "every_60_seconds")
        
        print("✅ Data pipeline logged to MLflow!")
        print(f"   Total records: 31,158")

if __name__ == "__main__":
    print("="*60)
    print("LOGGING ALL MODELS TO MLFLOW")
    print("="*60)
    
    log_earthquake_model()
    log_flood_model()
    log_data_pipeline()
    
    print("\n" + "="*60)
    print("ALL EXPERIMENTS LOGGED!")
    print("View dashboard: mlflow ui")
    print("Then open: http://127.0.0.1:5000")
    print("="*60)