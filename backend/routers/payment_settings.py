from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import os
import httpx
import logging

router = APIRouter(prefix="/admin/payment-settings", tags=["Admin Payment Settings"])

logger = logging.getLogger(__name__)

# MongoDB collection
from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'chatbase_db')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]
payment_settings_collection = db['payment_settings']


# Models
class LemonSqueezyPlans(BaseModel):
    free: str = ""
    starter: str = ""
    professional: str = ""
    enterprise: str = ""


class LemonSqueezySettings(BaseModel):
    enabled: bool = False
    api_key: str = ""
    store_id: str = ""
    webhook_url: str = ""
    webhook_secret: str = ""
    plans: LemonSqueezyPlans = Field(default_factory=LemonSqueezyPlans)


class PaymentSettings(BaseModel):
    lemonsqueezy: LemonSqueezySettings = Field(default_factory=LemonSqueezySettings)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None


class TestConnectionRequest(BaseModel):
    api_key: str
    store_id: str


class TestConnectionResponse(BaseModel):
    success: bool
    message: str
    store_name: Optional[str] = None


# Helper function to get current user (mock for now)
def get_mock_user():
    return {"id": "admin-001", "email": "admin@botsmith.com", "role": "admin"}


# Endpoints
@router.get("", response_model=PaymentSettings)
async def get_payment_settings():
    """
    Get current payment gateway settings
    """
    try:
        settings = await payment_settings_collection.find_one({})
        
        if not settings:
            # Return default settings
            default_settings = PaymentSettings()
            return default_settings
        
        # Remove MongoDB _id field
        settings.pop('_id', None)
        
        return PaymentSettings(**settings)
    except Exception as e:
        logger.error(f"Error fetching payment settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch payment settings: {str(e)}")


@router.put("", response_model=PaymentSettings)
async def update_payment_settings(settings: PaymentSettings):
    """
    Update payment gateway settings
    """
    try:
        user = get_mock_user()
        
        # Update timestamp and user
        settings.updated_at = datetime.utcnow()
        settings.updated_by = user['id']
        
        # Convert to dict
        settings_dict = settings.model_dump()
        
        # Upsert settings (update if exists, insert if not)
        await payment_settings_collection.delete_many({})  # Only keep one settings document
        await payment_settings_collection.insert_one(settings_dict)
        
        logger.info(f"Payment settings updated by user {user['id']}")
        
        # Remove MongoDB _id for response
        settings_dict.pop('_id', None)
        
        return PaymentSettings(**settings_dict)
    except Exception as e:
        logger.error(f"Error updating payment settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update payment settings: {str(e)}")


@router.post("/test", response_model=TestConnectionResponse)
async def test_lemonsqueezy_connection(request: TestConnectionRequest):
    """
    Test LemonSqueezy API connection
    """
    try:
        if not request.api_key or not request.store_id:
            raise HTTPException(
                status_code=400, 
                detail="API key and Store ID are required"
            )
        
        # Test LemonSqueezy API connection
        headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {request.api_key}"
        }
        
        async with httpx.AsyncClient() as client:
            # Try to fetch store details
            response = await client.get(
                f"https://api.lemonsqueezy.com/v1/stores/{request.store_id}",
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                store_name = data.get('data', {}).get('attributes', {}).get('name', 'Unknown Store')
                
                return TestConnectionResponse(
                    success=True,
                    message="Successfully connected to LemonSqueezy!",
                    store_name=store_name
                )
            elif response.status_code == 401:
                return TestConnectionResponse(
                    success=False,
                    message="Invalid API key. Please check your credentials."
                )
            elif response.status_code == 404:
                return TestConnectionResponse(
                    success=False,
                    message="Store not found. Please check your Store ID."
                )
            else:
                return TestConnectionResponse(
                    success=False,
                    message=f"Connection failed with status code: {response.status_code}"
                )
                
    except httpx.TimeoutException:
        return TestConnectionResponse(
            success=False,
            message="Connection timeout. Please check your network or try again."
        )
    except httpx.RequestError as e:
        logger.error(f"Network error testing LemonSqueezy connection: {str(e)}")
        return TestConnectionResponse(
            success=False,
            message=f"Network error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error testing LemonSqueezy connection: {str(e)}")
        return TestConnectionResponse(
            success=False,
            message=f"Error: {str(e)}"
        )


@router.delete("")
async def delete_payment_settings():
    """
    Reset payment gateway settings to default
    """
    try:
        user = get_mock_user()
        
        await payment_settings_collection.delete_many({})
        
        logger.info(f"Payment settings reset by user {user['id']}")
        
        return {"success": True, "message": "Payment settings reset to default"}
    except Exception as e:
        logger.error(f"Error resetting payment settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reset payment settings: {str(e)}")
