from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_phone: str, message: str):
    """Send real SMS via Twilio"""
    try:
        # Ensure phone number has country code
        if not to_phone.startswith('+'):
            to_phone = f'+92{to_phone.lstrip("0")}'

        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )

        print(f"✅ SMS sent! SID: {sms.sid}")
        return {
            "success": True,
            "sid": sms.sid,
            "status": sms.status,
            "to": to_phone
        }
    except Exception as e:
        print(f"❌ SMS error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def send_emergency_sos(
        lat: float, lon: float,
        phone_numbers: list):
    """Send SOS alert to multiple emergency contacts"""
    message = (
        f"🚨 SOS EMERGENCY! Someone needs help!\n"
        f"Location: https://maps.google.com/?q={lat},{lon}\n"
        f"Please contact rescue services immediately!\n"
        f"- Disaster Alert Pakistan"
    )

    results = []
    for phone in phone_numbers:
        result = send_sms(phone, message)
        results.append({
            "phone": phone,
            "result": result
        })

    return {
        "total_sent": len(
            [r for r in results
             if r["result"].get("success")]
        ),
        "total_attempted": len(phone_numbers),
        "details": results
    }

def send_disaster_alert_sms(
        phone: str, alert_title: str,
        alert_message: str):
    """Send disaster alert SMS to a user"""
    message = (
        f"🚨 {alert_title}\n"
        f"{alert_message}\n"
        f"- Disaster Alert Pakistan"
    )
    return send_sms(phone, message)