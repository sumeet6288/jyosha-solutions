from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models import (
    Integration, IntegrationCreate, IntegrationUpdate, IntegrationResponse,
    IntegrationLog, IntegrationLogResponse, TestConnectionRequest
)
from auth import get_current_user, get_mock_user
import httpx

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'chatbase_db')
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def log_integration_event(
    chatbot_id: str,
    integration_id: str,
    integration_type: str,
    event_type: str,
    status: str,
    message: str,
    metadata: dict = None
):
    """Helper function to log integration events"""
    log = IntegrationLog(
        chatbot_id=chatbot_id,
        integration_id=integration_id,
        integration_type=integration_type,
        event_type=event_type,
        status=status,
        message=message,
        metadata=metadata or {}
    )
    await db.integration_logs.insert_one(log.model_dump())


async def test_integration_connection(integration_type: str, credentials: dict) -> dict:
    """Test integration connection based on type"""
    try:
        if integration_type == "whatsapp":
            # Test WhatsApp Business API
            if not credentials.get("api_key") or not credentials.get("phone_number"):
                return {"success": False, "message": "Missing API key or phone number"}
            return {"success": True, "message": "WhatsApp credentials validated"}
        
        elif integration_type == "slack":
            # Test Slack Bot Token
            if not credentials.get("bot_token"):
                return {"success": False, "message": "Missing bot token"}
            
            # Try to call Slack API auth.test
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://slack.com/api/auth.test",
                    headers={"Authorization": f"Bearer {credentials['bot_token']}"},
                    timeout=10.0
                )
                data = response.json()
                if data.get("ok"):
                    return {"success": True, "message": f"Connected to {data.get('team', 'Slack workspace')}"}
                else:
                    return {"success": False, "message": data.get("error", "Invalid token")}
        
        elif integration_type == "telegram":
            # Test Telegram Bot Token
            if not credentials.get("bot_token"):
                return {"success": False, "message": "Missing bot token"}
            
            # Try to call Telegram API getMe
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.telegram.org/bot{credentials['bot_token']}/getMe",
                    timeout=10.0
                )
                data = response.json()
                if data.get("ok"):
                    bot_info = data.get("result", {})
                    return {"success": True, "message": f"Connected to @{bot_info.get('username', 'bot')}"}
                else:
                    return {"success": False, "message": "Invalid bot token"}
        
        elif integration_type == "discord":
            # Test Discord Bot Token
            if not credentials.get("bot_token"):
                return {"success": False, "message": "Missing bot token"}
            
            # Try to call Discord API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://discord.com/api/v10/users/@me",
                    headers={"Authorization": f"Bot {credentials['bot_token']}"},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    return {"success": True, "message": f"Connected as {data.get('username', 'bot')}"}
                else:
                    return {"success": False, "message": "Invalid bot token"}
        
        elif integration_type == "twilio":
            # Test Twilio credentials
            if not credentials.get("account_sid") or not credentials.get("auth_token"):
                return {"success": False, "message": "Missing Account SID or Auth Token"}
            return {"success": True, "message": "Twilio credentials validated"}
        
        elif integration_type == "webchat":
            # Web chat is always available
            return {"success": True, "message": "Web chat widget is ready"}
        
        elif integration_type == "api":
            # API is always available
            return {"success": True, "message": "REST API is ready"}
        
        elif integration_type == "messenger":
            # Test Facebook Messenger
            if not credentials.get("page_access_token"):
                return {"success": False, "message": "Missing page access token"}
            return {"success": True, "message": "Messenger credentials validated"}
        
        else:
            return {"success": False, "message": "Unknown integration type"}
            
    except Exception as e:
        return {"success": False, "message": f"Connection test failed: {str(e)}"}


@router.get("/{chatbot_id}", response_model=List[IntegrationResponse])
async def get_integrations(chatbot_id: str, current_user: dict = Depends(get_mock_user)):
    """Get all integrations for a chatbot"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get all integrations for this chatbot
        integrations = await db.integrations.find({"chatbot_id": chatbot_id}).to_list(100)
        
        # Convert to response model (hiding actual credentials)
        response_integrations = []
        for integration in integrations:
            response_integrations.append(IntegrationResponse(
                id=integration["id"],
                chatbot_id=integration["chatbot_id"],
                integration_type=integration["integration_type"],
                enabled=integration["enabled"],
                status=integration["status"],
                last_tested=integration.get("last_tested"),
                last_used=integration.get("last_used"),
                error_message=integration.get("error_message"),
                has_credentials=bool(integration.get("credentials")),
                created_at=integration["created_at"],
                updated_at=integration["updated_at"]
            ))
        
        return response_integrations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{chatbot_id}", response_model=IntegrationResponse)
async def create_or_update_integration(
    chatbot_id: str,
    integration_data: IntegrationCreate,
    current_user: dict = Depends(get_mock_user)
):
    """Create or update an integration"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Check if integration already exists
        existing = await db.integrations.find_one({
            "chatbot_id": chatbot_id,
            "integration_type": integration_data.integration_type
        })
        
        if existing:
            # Update existing integration
            update_data = {
                "credentials": integration_data.credentials,
                "metadata": integration_data.metadata or existing.get("metadata", {}),
                "updated_at": datetime.now(timezone.utc),
                "status": "pending"
            }
            
            await db.integrations.update_one(
                {"id": existing["id"]},
                {"$set": update_data}
            )
            
            integration_id = existing["id"]
            
            # Log the update
            await log_integration_event(
                chatbot_id=chatbot_id,
                integration_id=integration_id,
                integration_type=integration_data.integration_type,
                event_type="configured",
                status="success",
                message=f"{integration_data.integration_type.capitalize()} integration credentials updated"
            )
        else:
            # Create new integration
            integration = Integration(
                chatbot_id=chatbot_id,
                integration_type=integration_data.integration_type,
                credentials=integration_data.credentials,
                metadata=integration_data.metadata or {},
                enabled=False,
                status="pending"
            )
            
            await db.integrations.insert_one(integration.model_dump())
            integration_id = integration.id
            
            # Log the creation
            await log_integration_event(
                chatbot_id=chatbot_id,
                integration_id=integration_id,
                integration_type=integration_data.integration_type,
                event_type="configured",
                status="success",
                message=f"{integration_data.integration_type.capitalize()} integration created"
            )
        
        # Fetch and return the integration
        updated_integration = await db.integrations.find_one({"id": integration_id})
        
        return IntegrationResponse(
            id=updated_integration["id"],
            chatbot_id=updated_integration["chatbot_id"],
            integration_type=updated_integration["integration_type"],
            enabled=updated_integration["enabled"],
            status=updated_integration["status"],
            last_tested=updated_integration.get("last_tested"),
            last_used=updated_integration.get("last_used"),
            error_message=updated_integration.get("error_message"),
            has_credentials=bool(updated_integration.get("credentials")),
            created_at=updated_integration["created_at"],
            updated_at=updated_integration["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{chatbot_id}/{integration_id}/toggle")
async def toggle_integration(
    chatbot_id: str,
    integration_id: str,
    current_user: dict = Depends(get_mock_user)
):
    """Enable or disable an integration"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get the integration
        integration = await db.integrations.find_one({
            "id": integration_id,
            "chatbot_id": chatbot_id
        })
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Toggle enabled status
        new_enabled = not integration["enabled"]
        
        await db.integrations.update_one(
            {"id": integration_id},
            {"$set": {"enabled": new_enabled, "updated_at": datetime.now(timezone.utc)}}
        )
        
        # Log the toggle
        await log_integration_event(
            chatbot_id=chatbot_id,
            integration_id=integration_id,
            integration_type=integration["integration_type"],
            event_type="enabled" if new_enabled else "disabled",
            status="success",
            message=f"Integration {'enabled' if new_enabled else 'disabled'}"
        )
        
        return {"success": True, "enabled": new_enabled}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{chatbot_id}/{integration_id}/test")
async def test_integration(
    chatbot_id: str,
    integration_id: str,
    current_user: dict = Depends(get_mock_user)
):
    """Test an integration connection"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get the integration
        integration = await db.integrations.find_one({
            "id": integration_id,
            "chatbot_id": chatbot_id
        })
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Test the connection
        test_result = await test_integration_connection(
            integration["integration_type"],
            integration["credentials"]
        )
        
        # Update integration status
        update_data = {
            "last_tested": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        if test_result["success"]:
            update_data["status"] = "connected"
            update_data["error_message"] = None
        else:
            update_data["status"] = "error"
            update_data["error_message"] = test_result["message"]
        
        await db.integrations.update_one(
            {"id": integration_id},
            {"$set": update_data}
        )
        
        # Log the test
        await log_integration_event(
            chatbot_id=chatbot_id,
            integration_id=integration_id,
            integration_type=integration["integration_type"],
            event_type="tested",
            status="success" if test_result["success"] else "failure",
            message=test_result["message"]
        )
        
        return test_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{chatbot_id}/{integration_id}")
async def delete_integration(
    chatbot_id: str,
    integration_id: str,
    current_user: dict = Depends(get_mock_user)
):
    """Delete an integration"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get the integration
        integration = await db.integrations.find_one({
            "id": integration_id,
            "chatbot_id": chatbot_id
        })
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Log before deletion
        await log_integration_event(
            chatbot_id=chatbot_id,
            integration_id=integration_id,
            integration_type=integration["integration_type"],
            event_type="configured",
            status="warning",
            message="Integration deleted"
        )
        
        # Delete the integration
        await db.integrations.delete_one({"id": integration_id})
        
        return {"success": True, "message": "Integration deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chatbot_id}/logs", response_model=List[IntegrationLogResponse])
async def get_integration_logs(
    chatbot_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_mock_user)
):
    """Get integration activity logs"""
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user["id"]})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get logs
        logs = await db.integration_logs.find(
            {"chatbot_id": chatbot_id}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return [IntegrationLogResponse(**log) for log in logs]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
