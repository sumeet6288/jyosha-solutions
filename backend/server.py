from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from routers import auth_router, user_router, chatbots, sources, chat, analytics, plans, advanced_analytics, public_chat, lemonsqueezy, admin, admin_users, admin_users_enhanced, notifications, integrations
import auth
from services.plan_service import plan_service
from typing import Dict
import json

# Import security middleware
from middleware.security import (
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    InputValidationMiddleware,
    APIKeyProtectionMiddleware
)


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize auth module with database
auth.init_auth(db)

# Initialize routers with database
auth_router.init_router(db)
user_router.init_router(db)
chatbots.init_router(db)
sources.init_router(db)
chat.init_router(db)
analytics.init_router(db)
advanced_analytics.init_router(db)
public_chat.init_router(db)
lemonsqueezy.init_router(db)
admin.init_router(db)
admin_users.init_router(db)
admin_users_enhanced.init_router(db)
notifications.init_router(db)

# WebSocket connection manager for real-time notifications
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket connected for user: {user_id}")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"WebSocket disconnected for user: {user_id}")
    
    async def send_notification(self, user_id: str, notification: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(notification))
            except Exception as e:
                logger.error(f"Error sending notification to {user_id}: {e}")
                self.disconnect(user_id)

manager = ConnectionManager()

# Create the main app without a prefix
# Set max upload size to 100MB
app = FastAPI(
    title="BotSmith API",
    description="AI-powered chatbot builder with multi-provider support",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add health check route
@api_router.get("/")
async def root():
    return {"message": "BotSmith API", "status": "running"}

# Include all routers
api_router.include_router(auth_router.router)
api_router.include_router(user_router.router)
api_router.include_router(chatbots.router)
api_router.include_router(sources.router)
api_router.include_router(chat.router)
api_router.include_router(analytics.router)
api_router.include_router(plans.router)
api_router.include_router(advanced_analytics.router)
api_router.include_router(public_chat.router)
api_router.include_router(lemonsqueezy.router, prefix="/lemonsqueezy", tags=["Lemon Squeezy"])
api_router.include_router(admin.router)
api_router.include_router(admin_users.router)
api_router.include_router(notifications.router)
api_router.include_router(integrations.router)

# Include the router in the main app
app.include_router(api_router)

# Add security middleware (order matters - last added runs first)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting middleware (200 requests/min, 5000 requests/hour)
app.add_middleware(RateLimitMiddleware, requests_per_minute=200, requests_per_hour=5000)

# Input validation middleware
app.add_middleware(InputValidationMiddleware)

# API key protection middleware
app.add_middleware(APIKeyProtectionMiddleware)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize plans on startup"""
    logger.info("Initializing plans...")
    await plan_service.initialize_plans()
    logger.info("Plans initialized successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


# WebSocket endpoint for real-time notifications
@app.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # Keep connection alive and listen for any messages
            data = await websocket.receive_text()
            # Echo back to confirm connection is alive
            await websocket.send_text(json.dumps({"type": "ping", "message": "Connection alive"}))
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(user_id)