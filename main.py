from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes.alerts import router as alerts_router
from routes.reports import router as reports_router
from routes.predict import router as predict_router
import asyncio
import json

# Create app FIRST
app = FastAPI(
    title="Disaster Alert Pakistan API",
    description="AI-powered disaster early warning system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    alerts_router, prefix="/alerts", tags=["Alerts"])
app.include_router(
    reports_router, prefix="/reports", tags=["Reports"])
app.include_router(
    predict_router, prefix="/predict",
    tags=["AI Predictions"])

# Connected WebSocket clients
connected_clients = []

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    from database import init_db
    init_db()
    print("✅ Database initialized!")

@app.get("/")
def root():
    return {
        "app": "Disaster Alert Pakistan",
        "version": "1.0.0",
        "status": "running",
        "websocket": "ws://127.0.0.1:8000/ws/alerts"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Disaster Alert API is running!",
        "connected_clients": len(connected_clients),
        "services": {
            "api": "online",
            "websocket": "active",
            "ai_model": "ready",
            "database": "sqlite"
        }
    }

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """Real-time alert streaming via WebSocket"""
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"🔌 Client connected! Total: {len(connected_clients)}")

    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Disaster Alert real-time feed",
            "total_clients": len(connected_clients)
        })

        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                message = json.loads(data)

                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "message": "Server is alive"
                    })

                elif message.get("type") == "get_alerts":
                    from services.alert_engine import run_alert_engine
                    alerts = run_alert_engine()
                    await websocket.send_json({
                        "type": "alerts_update",
                        "data": alerts
                    })

            except asyncio.TimeoutError:
                await websocket.send_json({
                    "type": "heartbeat",
                    "message": "Server alive"
                })

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"🔌 Disconnected. Total: {len(connected_clients)}")

async def broadcast_alert(alert_data: dict):
    """Broadcast to all connected clients"""
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json({
                "type": "new_alert",
                "data": alert_data
            })
        except Exception:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)