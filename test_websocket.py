import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/alerts"
    print(f"Connecting to {uri}...")
    
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")
        
        # Receive welcome message
        response = await websocket.recv()
        print(f"📨 Received: {response}")
        
        # Send ping
        await websocket.send(json.dumps({"type": "ping"}))
        print("📤 Sent ping")
        
        # Receive pong
        response = await websocket.recv()
        print(f"📨 Received: {response}")
        
        # Request alerts
        await websocket.send(json.dumps({"type": "get_alerts"}))
        print("📤 Requested alerts")
        
        response = await websocket.recv()
        print(f"📨 Received alerts data!")
        data = json.loads(response)
        print(f"   Total alerts: {data.get('data', {}).get('total_alerts', 0)}")

if __name__ == "__main__":
    asyncio.run(test_websocket())