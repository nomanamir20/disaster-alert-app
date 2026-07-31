from datetime import datetime

# Store notifications in memory for now
# Firebase FCM integration comes Day 10
notification_log = []

def send_push_notification(title, message, alert_level, location, lat, lon):
    """
    Send push notification to users in affected area
    For now logs to memory — Firebase FCM integrated Day 10
    """
    notification = {
        "id": len(notification_log) + 1,
        "title": title,
        "message": message,
        "alert_level": alert_level,
        "location": location,
        "latitude": lat,
        "longitude": lon,
        "sent_at": str(datetime.now()),
        "status": "logged"  # Will be "sent" after FCM integration
    }
    
    notification_log.append(notification)
    
    print(f"📲 NOTIFICATION LOGGED:")
    print(f"   Title: {title}")
    print(f"   Level: {alert_level}")
    print(f"   Location: {location}")
    
    return notification

def send_sms_fallback(phone, message):
    """
    SMS fallback for 2G users
    Twilio integration comes Day 12
    """
    sms = {
        "to": phone,
        "message": message[:160],  # SMS limit
        "sent_at": str(datetime.now()),
        "status": "logged"
    }
    print(f"📱 SMS LOGGED to {phone}: {message[:50]}...")
    return sms

def notify_alert(alert):
    """Send notification for a disaster alert"""
    title = alert.get("title", "Disaster Alert")
    level = alert.get("level", "WATCH")
    location = alert.get("location", "Pakistan")
    action = alert.get("action", "Stay alert")
    probability = alert.get("probability_percent", "0%")
    lat = alert.get("latitude", 0)
    lon = alert.get("longitude", 0)
    
    message = f"{action} Probability: {probability}"
    
    return send_push_notification(
        title=title,
        message=message,
        alert_level=level,
        location=location,
        lat=lat,
        lon=lon
    )

def get_notification_log():
    return {
        "total": len(notification_log),
        "notifications": notification_log
    }