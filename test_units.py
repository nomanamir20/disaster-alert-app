import pytest
import requests
from services.usgs_service import (
    get_recent_earthquakes,
    get_pakistan_earthquakes,
    get_severity
)
from services.openweather_service import (
    get_weather,
    check_flood_risk,
)
from services.alert_engine import (
    calculate_earthquake_probability,
    calculate_flood_probability,
    get_alert_level,
)
from services.pmd_service import get_pakistan_weather_warnings

# ═══════════════════════════════════════════
# UNIT TESTS — USGS SERVICE
# ═══════════════════════════════════════════

class TestUSGSService:

    def test_get_severity_emergency(self):
        """Magnitude 7+ should return emergency"""
        assert get_severity(7.5) == "emergency"
        assert get_severity(8.0) == "emergency"

    def test_get_severity_warning(self):
        """Magnitude 5-7 should return warning"""
        assert get_severity(5.0) == "warning"
        assert get_severity(6.9) == "warning"

    def test_get_severity_watch(self):
        """Magnitude 3-5 should return watch"""
        assert get_severity(3.0) == "watch"
        assert get_severity(4.9) == "watch"

    def test_get_severity_info(self):
        """Magnitude below 3 should return info"""
        assert get_severity(2.9) == "info"
        assert get_severity(1.0) == "info"

    def test_get_recent_earthquakes_returns_dict(self):
        """USGS API should return a dictionary"""
        result = get_recent_earthquakes()
        assert isinstance(result, dict)
        assert "source" in result
        assert result["source"] == "USGS"

    def test_get_pakistan_earthquakes_has_region(self):
        """Pakistan earthquakes should have region field"""
        result = get_pakistan_earthquakes()
        assert isinstance(result, dict)
        assert "region" in result
        assert result["region"] == "Pakistan"

    def test_pakistan_earthquakes_coordinates_in_bounds(self):
        """All Pakistan earthquakes should be within Pakistan bounds"""
        result = get_pakistan_earthquakes()
        earthquakes = result.get("earthquakes", [])
        for quake in earthquakes:
            assert 23.0 <= quake["latitude"] <= 37.5
            assert 60.0 <= quake["longitude"] <= 77.5


# ═══════════════════════════════════════════
# UNIT TESTS — ALERT ENGINE
# ═══════════════════════════════════════════

class TestAlertEngine:

    def test_earthquake_probability_high_magnitude(self):
        """High magnitude earthquake should have high probability"""
        prob = calculate_earthquake_probability(7.5, 10, 33.0, 73.0)
        assert prob >= 0.80

    def test_earthquake_probability_low_magnitude(self):
        """Low magnitude earthquake should have low probability"""
        prob = calculate_earthquake_probability(2.0, 30, 33.0, 73.0)
        assert prob < 0.50

    def test_earthquake_shallow_more_dangerous(self):
        """Shallow earthquake should be more dangerous than deep"""
        shallow = calculate_earthquake_probability(5.0, 5, 33.0, 73.0)
        deep = calculate_earthquake_probability(5.0, 100, 33.0, 73.0)
        assert shallow > deep

    def test_flood_probability_heavy_rain(self):
        """Heavy rainfall should give high flood probability"""
        prob = calculate_flood_probability(100, "Karachi")
        assert prob >= 0.80

    def test_flood_probability_no_rain(self):
        """No rainfall should give low flood probability"""
        prob = calculate_flood_probability(0, "Lahore")
        assert prob < 0.20

    def test_flood_probability_moderate_rain(self):
        """Moderate rainfall should give moderate probability"""
        prob = calculate_flood_probability(30, "Islamabad")
        assert 0.40 <= prob <= 0.80

    def test_alert_level_emergency(self):
        """Probability >= 0.80 should return EMERGENCY"""
        level, emoji = get_alert_level(0.85)
        assert level == "EMERGENCY"
        assert emoji == "🔴"

    def test_alert_level_warning(self):
        """Probability 0.60-0.80 should return WARNING"""
        level, emoji = get_alert_level(0.70)
        assert level == "WARNING"
        assert emoji == "🟠"

    def test_alert_level_watch(self):
        """Probability 0.40-0.60 should return WATCH"""
        level, emoji = get_alert_level(0.50)
        assert level == "WATCH"
        assert emoji == "🟡"

    def test_alert_level_safe(self):
        """Probability < 0.40 should return SAFE"""
        level, emoji = get_alert_level(0.20)
        assert level == "SAFE"
        assert emoji == "🟢"

    def test_probability_never_exceeds_one(self):
        """Probability should never exceed 1.0"""
        prob = calculate_earthquake_probability(9.9, 1, 33.0, 73.0)
        assert prob <= 1.0

    def test_probability_never_below_zero(self):
        """Probability should never be negative"""
        prob = calculate_flood_probability(0, "Karachi")
        assert prob >= 0.0


# ═══════════════════════════════════════════
# UNIT TESTS — API ENDPOINTS
# ═══════════════════════════════════════════

class TestAPIEndpoints:

    BASE_URL = "http://127.0.0.1:8000"

    def test_health_endpoint(self):
        """Health endpoint should return ok status"""
        try:
            response = requests.get(f"{self.BASE_URL}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

    def test_alerts_endpoint(self):
        """Alerts endpoint should return list"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/alerts/", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "alerts" in data
            assert isinstance(data["alerts"], list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

    def test_alerts_active_endpoint(self):
        """Active alerts endpoint should work"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/alerts/active", timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

    def test_predict_earthquake_endpoint(self):
        """Predict earthquake endpoint should return prediction"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/predict/earthquake",
                json={
                    "magnitude": 6.5,
                    "depth_km": 15,
                    "latitude": 33.6844,
                    "longitude": 73.0479,
                    "location": "Islamabad"
                },
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "prediction" in data
            assert "probability" in data["prediction"]
            assert "alert_level" in data["prediction"]
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

    def test_predict_flood_endpoint(self):
        """Predict flood endpoint should return prediction"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/predict/flood",
                json={
                    "rainfall_mm": 45,
                    "city": "Karachi",
                    "latitude": 24.8607,
                    "longitude": 67.0011
                },
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "prediction" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")


# ═══════════════════════════════════════════
# UNIT TESTS — DATA VALIDATION
# ═══════════════════════════════════════════

class TestDataValidation:

    def test_weather_data_has_required_fields(self):
        """Weather data should have all required fields"""
        from services.openweather_service import get_weather
        result = get_weather("Karachi", 24.8607, 67.0011)
        if "error" not in result:
            assert "city" in result
            assert "temperature" in result
            assert "humidity" in result

    def test_pmd_data_has_cities(self):
        """PMD service should return data for multiple cities"""
        result = get_pakistan_weather_warnings()
        assert "data" in result
        assert len(result["data"]) > 0

    def test_pmd_data_has_required_fields(self):
        """Each city in PMD data should have required fields"""
        result = get_pakistan_weather_warnings()
        for city in result["data"]:
            if "error" not in city:
                assert "city" in city
                assert "max_temperature_c" in city
                assert "max_windspeed_kmh" in city


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])