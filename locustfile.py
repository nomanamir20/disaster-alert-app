from locust import HttpUser, task, between
import random

class DisasterAlertUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"

    @task(5)
    def check_health(self):
        self.client.get("/health")

    @task(4)
    def get_active_alerts(self):
        self.client.get("/alerts/active")

    @task(3)
    def get_all_alerts(self):
        self.client.get("/alerts/")

    @task(2)
    def predict_earthquake(self):
        self.client.post(
            "/predict/earthquake",
            json={
                "magnitude": round(random.uniform(3.0, 8.0), 1),
                "depth_km": round(random.uniform(5, 100), 1),
                "latitude": 33.6844,
                "longitude": 73.0479,
                "location": "Test Location"
            }
        )

    @task(2)
    def predict_flood(self):
        self.client.post(
            "/predict/flood",
            json={
                "rainfall_mm": round(random.uniform(0, 100), 1),
                "city": random.choice(
                    ["Karachi", "Lahore", "Islamabad"]),
                "latitude": 24.8607,
                "longitude": 67.0011
            }
        )

    @task(1)
    def submit_report(self):
        self.client.post(
            "/reports/",
            json={
                "disaster_type": "flood",
                "description": "Load test report",
                "location": "Test",
                "latitude": 33.6844,
                "longitude": 73.0479,
                "reporter_phone": "+923001234567"
            }
        )