import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

class TestHealthEndpoint:
    def test_health_status_ok(self):
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_response_time(self):
        start = time.time()
        response = requests.get(f"{BASE_URL}/health")
        elapsed = (time.time() - start) * 1000
        assert elapsed < 500, f"Health check took {elapsed}ms"

class TestAlertsEndpoints:
    def test_get_all_alerts(self):
        response = requests.get(f"{BASE_URL}/alerts/")
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data
        assert "total" in data

    def test_get_active_alerts(self):
        response = requests.get(f"{BASE_URL}/alerts/active")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["alerts"], list)

    def test_alerts_have_required_fields(self):
        response = requests.get(f"{BASE_URL}/alerts/active")
        data = response.json()
        if data["alerts"]:
            alert = data["alerts"][0]
            required_fields = ["id", "type", "level", "title",
                               "location", "latitude", "longitude"]
            for field in required_fields:
                assert field in alert

    def test_alerts_response_time(self):
        start = time.time()
        response = requests.get(f"{BASE_URL}/alerts/active")
        elapsed = (time.time() - start) * 1000
        assert elapsed < 500, f"Alerts endpoint took {elapsed}ms"

class TestPredictEndpoints:
    def test_predict_earthquake_valid(self):
        response = requests.post(
            f"{BASE_URL}/predict/earthquake",
            json={
                "magnitude": 6.5,
                "depth_km": 15,
                "latitude": 33.6844,
                "longitude": 73.0479,
                "location": "Islamabad"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert 0 <= data["prediction"]["probability"] <= 1

    def test_predict_earthquake_response_time(self):
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/predict/earthquake",
            json={
                "magnitude": 5.0,
                "depth_km": 20,
                "latitude": 33.6844,
                "longitude": 73.0479,
                "location": "Test"
            }
        )
        elapsed = (time.time() - start) * 1000
        assert elapsed < 500, f"Prediction took {elapsed}ms"

    def test_predict_flood_valid(self):
        response = requests.post(
            f"{BASE_URL}/predict/flood",
            json={
                "rainfall_mm": 45,
                "city": "Karachi",
                "latitude": 24.8607,
                "longitude": 67.0011
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data

class TestReportsEndpoints:
    def test_create_report(self):
        response = requests.post(
            f"{BASE_URL}/reports/",
            json={
                "disaster_type": "flood",
                "description": "Test report",
                "location": "Test location",
                "latitude": 33.6844,
                "longitude": 73.0479,
                "reporter_phone": "+923001234567"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data

    def test_get_all_reports(self):
        response = requests.get(f"{BASE_URL}/reports/")
        assert response.status_code == 200
        data = response.json()
        assert "reports" in data

class TestDatabaseIntegration:
    def test_database_status_in_health(self):
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        assert data["services"]["database"] == "sqlite"

    def test_alerts_persist_in_database(self):
        response1 = requests.get(f"{BASE_URL}/alerts/active")
        response2 = requests.get(f"{BASE_URL}/alerts/active")
        assert response1.json()["total"] == response2.json()["total"]

class TestErrorHandling:
    def test_invalid_earthquake_data(self):
        response = requests.post(
            f"{BASE_URL}/predict/earthquake",
            json={"magnitude": "invalid"}
        )
        assert response.status_code in [400, 422]

    def test_nonexistent_alert_id(self):
        response = requests.get(f"{BASE_URL}/alerts/99999")
        data = response.json()
        assert "error" in data or response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])