from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database URL
DATABASE_URL = "sqlite:///./disaster_alert.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# ═══════════════════════════════════════
# DATABASE MODELS
# ═══════════════════════════════════════

class DisasterDB(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    severity = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(Text)
    probability = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class AlertDB(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    disaster_type = Column(String, index=True)
    alert_level = Column(String)
    title = Column(String)
    message = Column(Text)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    radius_km = Column(Float)
    probability = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    source = Column(String, default="System")

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)
    fcm_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class ReportDB(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    disaster_type = Column(String)
    description = Column(Text)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    reporter_phone = Column(String)
    photo_url = Column(String, nullable=True)
    status = Column(String, default="received")
    created_at = Column(DateTime, default=datetime.now)

class EarthquakeDB(Base):
    __tablename__ = "earthquakes"

    id = Column(Integer, primary_key=True, index=True)
    usgs_id = Column(String, unique=True)
    magnitude = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    depth_km = Column(Float)
    severity = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class FloodDB(Base):
    __tablename__ = "floods"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    rainfall_mm = Column(Float)
    flood_risk = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

# ═══════════════════════════════════════
# DATABASE FUNCTIONS
# ═══════════════════════════════════════

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

def init_db():
    """Initialize database with sample data"""
    create_tables()
    db = SessionLocal()

    try:
        # Check if data already exists
        existing = db.query(AlertDB).first()
        if existing:
            print("✅ Database already has data!")
            return

        # Add sample alerts
        sample_alerts = [
            AlertDB(
                disaster_type="flood",
                alert_level="warning",
                title="Flood Warning — Sindh Province",
                message="River levels rising critically.",
                location="Sindh, Pakistan",
                latitude=25.8943,
                longitude=68.5247,
                radius_km=50.0,
                probability=0.75,
                source="OpenWeatherMap"
            ),
            AlertDB(
                disaster_type="earthquake",
                alert_level="watch",
                title="Earthquake Watch — Balochistan",
                message="Magnitude 4.2 detected.",
                location="Balochistan, Pakistan",
                latitude=30.1798,
                longitude=66.9750,
                radius_km=100.0,
                probability=0.45,
                source="USGS"
            ),
            AlertDB(
                disaster_type="cyclone",
                alert_level="warning",
                title="Cyclone Warning — Karachi",
                message="Strong winds expected.",
                location="Karachi, Pakistan",
                latitude=24.8607,
                longitude=67.0011,
                radius_km=75.0,
                probability=0.65,
                source="PMD"
            ),
        ]

        for alert in sample_alerts:
            db.add(alert)

        db.commit()
        print(f"✅ Added {len(sample_alerts)} sample alerts!")

    except Exception as e:
        print(f"❌ Error initializing DB: {e}")
        db.rollback()
    finally:
        db.close()