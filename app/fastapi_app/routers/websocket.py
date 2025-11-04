"""
WebSocket Router - FastAPI WebSocket support for real-time sensor data and live updates.
Implements WebSocket endpoints for live cultivation data streaming.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List, Dict, Any, Optional
import json
import asyncio
import logging
from datetime import datetime

# Import dependencies
from app.fastapi_app.jwt_utils import verify_jwt_token
from app.models_async.auth import User
from app.fastapi_app.dependencies import get_current_user

logger = logging.getLogger(__name__)
security = HTTPBearer()
router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    """WebSocket connection manager for cultivation data streaming."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """Accept WebSocket connection and store it."""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to specific user's connections."""
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    self.disconnect(connection, user_id)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                self.disconnect(connection)
    
    async def broadcast_sensor_data(self, sensor_data: dict):
        """Broadcast sensor data to all connected clients."""
        message = {
            "type": "sensor_data",
            "data": sensor_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_plant_update(self, plant_data: dict):
        """Broadcast plant update to all connected clients."""
        message = {
            "type": "plant_update",
            "data": plant_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast(message)

# Global connection manager
manager = ConnectionManager()

async def verify_token_for_websocket(
    credentials: Optional[HTTPAuthorizationCredentials] = Query(default=None)
) -> Optional[User]:
    """Verify JWT token for WebSocket connection."""
    if not credentials:
        return None
    
    try:
        payload = verify_jwt_token(credentials.credentials, "access")
        if payload is None:
            return None
        
        # You would typically fetch user from database here
        # For now, return a mock user object
        return User(id=payload.get("user_id"), username=payload.get("username"))
    except Exception:
        return None

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(default=None, description="JWT token for authentication")
):
    """Main WebSocket endpoint for real-time cultivation data."""
    user = None
    
    # Authenticate user if token provided
    if token:
        user = await verify_token_for_websocket(token)
    
    await manager.connect(websocket, user.id if user else None)
    
    try:
        # Send welcome message
        welcome_message = {
            "type": "welcome",
            "message": "Connected to Cultivar real-time updates",
            "authenticated": user is not None,
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Echo back for testing
            response = {
                "type": "echo",
                "data": message_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await websocket.send_text(json.dumps(response))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id if user else None)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user.id if user else None)

@router.websocket("/ws/sensors")
async def sensor_websocket_endpoint(
    websocket: WebSocket,
    sensor_id: Optional[str] = Query(default=None)
):
    """WebSocket endpoint specifically for sensor data."""
    await manager.connect(websocket)
    
    try:
        # Send sensor data stream notification
        message = {
            "type": "sensor_stream_started",
            "sensor_id": sensor_id,
            "message": "Subscribed to sensor data stream",
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(message))
        
        while True:
            # This would typically receive sensor data from a queue or database
            # For now, send mock data
            mock_sensor_data = {
                "sensor_id": sensor_id or "mock_sensor",
                "temperature": 22.5,
                "humidity": 65.0,
                "ph": 6.2,
                "ec": 1.8,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            sensor_message = {
                "type": "sensor_data",
                "data": mock_sensor_data
            }
            await websocket.send_text(json.dumps(sensor_message))
            
            # Wait 5 seconds before next data point
            await asyncio.sleep(5)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Sensor WebSocket error: {e}")
        manager.disconnect(websocket)

@router.get("/ws/status")
async def websocket_status():
    """Get WebSocket connection status."""
    return {
        "active_connections": len(manager.active_connections),
        "authenticated_connections": sum(len(conns) for conns in manager.user_connections.values()),
        "user_connections": len(manager.user_connections),
        "status": "operational"
    }

@router.post("/ws/broadcast")
async def broadcast_message(
    message: dict,
    current_user: User = Depends(get_current_user)
):
    """Admin endpoint to broadcast messages to all connected clients."""
    if not current_user.is_admin:
        return {"error": "Admin access required"}
    
    await manager.broadcast(message)
    return {"status": "broadcast_sent", "connections": len(manager.active_connections)}
