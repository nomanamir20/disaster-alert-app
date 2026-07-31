from sqlalchemy.orm import Session
from database import (
    AlertDB, DisasterDB, UserDB,
    ReportDB, EarthquakeDB, FloodDB
)
from datetime import datetime
from typing import List, Optional

class AlertService:
    """Service for alert database operations"""

    @staticmethod
    def get_all_alerts(db: Session) -> List[AlertDB]:
        return db.query(AlertDB)\
            .filter(AlertDB.is_active == True)\
            .order_by(AlertDB.created_at.desc())\
            .all()

    @staticmethod
    def get_active_alerts(db: Session) -> List[AlertDB]:
        return db.query(AlertDB)\
            .filter(AlertDB.is_active == True)\
            .order_by(AlertDB.created_at.desc())\
            .all()

    @staticmethod
    def get_alert_by_id(
            db: Session, alert_id: int
    ) -> Optional[AlertDB]:
        return db.query(AlertDB)\
            .filter(AlertDB.id == alert_id)\
            .first()

    @staticmethod
    def create_alert(
            db: Session, alert_data: dict
    ) -> AlertDB:
        alert = AlertDB(**alert_data)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def save_earthquake(
            db: Session, quake_data: dict
    ) -> EarthquakeDB:
        # Check if already exists
        existing = db.query(EarthquakeDB)\
            .filter(
                EarthquakeDB.usgs_id ==
                quake_data.get('id', '')
            ).first()

        if existing:
            return existing

        quake = EarthquakeDB(
            usgs_id=quake_data.get('id', ''),
            magnitude=quake_data.get('magnitude', 0),
            location=quake_data.get('location', ''),
            latitude=quake_data.get('latitude', 0),
            longitude=quake_data.get('longitude', 0),
            depth_km=quake_data.get('depth_km', 0),
            severity=quake_data.get('severity', 'watch'),
        )
        db.add(quake)
        db.commit()
        db.refresh(quake)
        return quake

    @staticmethod
    def save_flood_data(
            db: Session, flood_data: dict
    ) -> FloodDB:
        flood = FloodDB(
            city=flood_data.get('city', ''),
            rainfall_mm=flood_data.get(
                'total_rainfall_24h_mm', 0),
            flood_risk=flood_data.get('flood_risk', 'safe'),
            latitude=flood_data.get('latitude', 0),
            longitude=flood_data.get('longitude', 0),
        )
        db.add(flood)
        db.commit()
        db.refresh(flood)
        return flood

class ReportService:
    """Service for report database operations"""

    @staticmethod
    def create_report(
            db: Session, report_data: dict
    ) -> ReportDB:
        report = ReportDB(**report_data)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_all_reports(db: Session) -> List[ReportDB]:
        return db.query(ReportDB)\
            .order_by(ReportDB.created_at.desc())\
            .all()

class UserService:
    """Service for user database operations"""

    @staticmethod
    def create_user(
            db: Session, user_data: dict
    ) -> UserDB:
        user = UserDB(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_phone(
            db: Session, phone: str
    ) -> Optional[UserDB]:
        return db.query(UserDB)\
            .filter(UserDB.phone == phone)\
            .first()

    @staticmethod
    def update_fcm_token(
            db: Session, phone: str, token: str
    ) -> Optional[UserDB]:
        user = db.query(UserDB)\
            .filter(UserDB.phone == phone)\
            .first()
        if user:
            user.fcm_token = token
            db.commit()
            db.refresh(user)
        return user