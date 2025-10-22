from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from routers import auth_router, user_router, chatbots, sources, chat, analytics, plans, advanced_analytics, public_chat, lemonsqueezy
import auth
from services.plan_service import plan_service


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

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

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