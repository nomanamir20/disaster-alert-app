from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.db_service import ReportService
from pydantic import BaseModel
from services.twilio_service import send_emergency_sos

router = APIRouter()

class ReportCreate(BaseModel):
    disaster_type: str
    description: str
    location: str
    latitude: float
    longitude: float
    reporter_phone: str
    photo_url: str = None

@router.post("/")
def create_report(
        report: ReportCreate,
        db: Session = Depends(get_db)):
    """Create new incident report"""
    report_data = {
        "disaster_type": report.disaster_type,
        "description": report.description,
        "location": report.location,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "reporter_phone": report.reporter_phone,
        "photo_url": report.photo_url,
        "status": "received"
    }
    new_report = ReportService.create_report(
        db, report_data)
    return {
        "message": "Report received successfully!",
        "report_id": new_report.id,
        "status": "received"
    }

@router.get("/")
def get_all_reports(db: Session = Depends(get_db)):
    """Get all reports from database"""
    reports = ReportService.get_all_reports(db)
    return {
        "total": len(reports),
        "reports": [
            {
                "id": r.id,
                "disaster_type": r.disaster_type,
                "description": r.description,
                "location": r.location,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "status": r.status,
                "created_at": str(r.created_at),
            }
            for r in reports
        ]
    }

class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    phone_numbers: list[str]

@router.post("/sos-sms")
def send_sos_sms(request: SOSRequest):
    """Send real SOS SMS to emergency contacts"""
    result = send_emergency_sos(
        request.latitude,
        request.longitude,
        request.phone_numbers
    )
    return result