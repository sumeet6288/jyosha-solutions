from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import os

router = APIRouter(prefix="/integrations", tags=["integrations"])
db_instance = None

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db

# MongoDB will be accessed via db_instance
integrations_collection = None

def get_integrations_collection():
    """Get integrations collection from database"""
    if db_instance is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db_instance['integrations']

class IntegrationConfig(BaseModel):
    name: str
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None
    workspace_id: Optional[str] = None
    phone_number: Optional[str] = None
    account_sid: Optional[str] = None
    auth_token: Optional[str] = None
    additional_config: Optional[Dict[str, Any]] = None

class IntegrationResponse(BaseModel):
    id: str
    user_id: str
    name: str
    connected: bool
    connected_at: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

@router.get("/")
async def get_user_integrations(user_id: str = "demo-user-123"):
    """Get all integrations for the current user"""
    integrations_collection = get_integrations_collection()
    integrations = await integrations_collection.find({"user_id": user_id}).to_list(100)
    
    # Define all available integrations
    available_integrations = [
        "Stripe", "Calendly", "Slack", "Zendesk", "WhatsApp", "Salesforce"
    ]
    
    # Create response with connection status
    result = []
    connected_integrations = {int_doc['name']: int_doc for int_doc in integrations}
    
    for integration_name in available_integrations:
        if integration_name in connected_integrations:
            int_doc = connected_integrations[integration_name]
            result.append({
                "id": str(int_doc['_id']),
                "name": integration_name,
                "connected": True,
                "connected_at": int_doc.get('connected_at'),
                "config": {
                    "api_key": "***" + int_doc.get('api_key', '')[-4:] if int_doc.get('api_key') else None,
                    "webhook_url": int_doc.get('webhook_url'),
                    "workspace_id": int_doc.get('workspace_id')
                }
            })
        else:
            result.append({
                "id": None,
                "name": integration_name,
                "connected": False,
                "connected_at": None,
                "config": None
            })
    
    return result

@router.post("/connect")
async def connect_integration(integration: IntegrationConfig, user_id: str = "demo-user-123"):
    """Connect a new integration"""
    integrations_collection = get_integrations_collection()
    
    # Validate required fields
    if not integration.api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    
    # Check if already connected
    existing = await integrations_collection.find_one({
        "user_id": user_id,
        "name": integration.name
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Integration already connected")
    
    # Create integration document
    integration_doc = {
        "user_id": user_id,
        "name": integration.name,
        "api_key": integration.api_key,
        "webhook_url": integration.webhook_url,
        "workspace_id": integration.workspace_id,
        "phone_number": integration.phone_number,
        "account_sid": integration.account_sid,
        "auth_token": integration.auth_token,
        "additional_config": integration.additional_config or {},
        "connected_at": datetime.utcnow().isoformat(),
        "status": "active"
    }
    
    result = await integrations_collection.insert_one(integration_doc)
    
    return {
        "id": str(result.inserted_id),
        "name": integration.name,
        "connected": True,
        "message": f"{integration.name} connected successfully"
    }

@router.delete("/{integration_name}")
async def disconnect_integration(integration_name: str, user_id: str = "demo-user-123"):
    """Disconnect an integration"""
    integrations_collection = get_integrations_collection()
    
    result = await integrations_collection.delete_one({
        "user_id": user_id,
        "name": integration_name
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {
        "name": integration_name,
        "connected": False,
        "message": f"{integration_name} disconnected successfully"
    }

@router.get("/{integration_name}")
async def get_integration_details(integration_name: str, user_id: str = "demo-user-123"):
    """Get details of a specific integration"""
    
    integration = await integrations_collection.find_one({
        "user_id": user_id,
        "name": integration_name
    })
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {
        "id": str(integration['_id']),
        "name": integration['name'],
        "connected": True,
        "connected_at": integration.get('connected_at'),
        "config": {
            "api_key": "***" + integration.get('api_key', '')[-4:] if integration.get('api_key') else None,
            "webhook_url": integration.get('webhook_url'),
            "workspace_id": integration.get('workspace_id'),
            "phone_number": integration.get('phone_number'),
            "account_sid": integration.get('account_sid')
        },
        "status": integration.get('status', 'active')
    }
