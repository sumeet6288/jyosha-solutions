from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime, timezone
from models import (
    Chatbot, ChatbotCreate, ChatbotUpdate, ChatbotResponse
)
from auth import get_current_user, get_current_user, User
from services.plan_service import plan_service
from services.cache_service import cache_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbots", tags=["chatbots"])
db_instance = None


def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db


@router.post("", response_model=ChatbotResponse, status_code=status.HTTP_201_CREATED)
async def create_chatbot(
    chatbot_data: ChatbotCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new chatbot"""
    try:
        # Check plan limits
        limit_check = await plan_service.check_limit(current_user.id, "chatbots")
        if limit_check["reached"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Chatbot limit reached for your plan",
                    "current": limit_check["current"],
                    "max": limit_check["max"],
                    "upgrade_required": True
                }
            )
        
        chatbot = Chatbot(
            user_id=current_user.id,
            name=chatbot_data.name,
            model=chatbot_data.model,
            provider=chatbot_data.provider,
            temperature=chatbot_data.temperature,
            instructions=chatbot_data.instructions,
            welcome_message=chatbot_data.welcome_message
        )
        
        result = await db_instance.chatbots.insert_one(chatbot.model_dump())
        
        # Increment usage count
        await plan_service.increment_usage(current_user.id, "chatbots")
        
        return ChatbotResponse(**chatbot.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create chatbot"
        )


@router.get("", response_model=List[ChatbotResponse])
async def get_chatbots(current_user: User = Depends(get_current_user)):
    """Get all chatbots for the current user"""
    try:
        chatbots = await db_instance.chatbots.find(
            {"user_id": current_user.id}
        ).to_list(length=None)
        
        # Ensure instructions field is populated from system_message if not present
        # and add conversations count
        for chatbot in chatbots:
            if "instructions" not in chatbot or chatbot["instructions"] is None:
                chatbot["instructions"] = chatbot.get("system_message", "You are a helpful assistant.")
            
            # Count conversations for this chatbot
            conversations_count = await db_instance.conversations.count_documents(
                {"chatbot_id": chatbot["id"]}
            )
            chatbot["conversations_count"] = conversations_count
        
        return [ChatbotResponse(**chatbot) for chatbot in chatbots]
    except Exception as e:
        logger.error(f"Error fetching chatbots: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch chatbots"
        )


@router.get("/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
    chatbot_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific chatbot"""
    try:
        chatbot = await db_instance.chatbots.find_one({
            "id": chatbot_id,
            "user_id": current_user.id
        })
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Ensure instructions field is populated from system_message if not present
        if "instructions" not in chatbot or chatbot["instructions"] is None:
            chatbot["instructions"] = chatbot.get("system_message", "You are a helpful assistant.")
        
        return ChatbotResponse(**chatbot)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch chatbot"
        )


@router.put("/{chatbot_id}", response_model=ChatbotResponse)
async def update_chatbot(
    chatbot_id: str,
    chatbot_data: ChatbotUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a chatbot"""
    try:
        # Check if chatbot exists and belongs to user
        chatbot = await db_instance.chatbots.find_one({
            "id": chatbot_id,
            "user_id": current_user.id
        })
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Update only provided fields
        # Note: exclude_unset=True only includes explicitly set fields
        # We need to keep False boolean values, so don't filter by "if v is not None"
        update_data = chatbot_data.model_dump(exclude_unset=True)
        
        # Handle instructions field - map it to both instructions and system_message
        if "instructions" in update_data and update_data["instructions"] is not None:
            update_data["system_message"] = update_data["instructions"]
        
        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            
            await db_instance.chatbots.update_one(
                {"id": chatbot_id},
                {"$set": update_data}
            )
            
            # Invalidate cache for this chatbot
            cache_service.delete(f"chatbot:{chatbot_id}")
            cache_service.delete(f"public_chatbot:{chatbot_id}")
        
        # Fetch updated chatbot
        updated_chatbot = await db_instance.chatbots.find_one({"id": chatbot_id})
        
        # Ensure instructions field is populated from system_message if not present
        if "instructions" not in updated_chatbot or updated_chatbot["instructions"] is None:
            updated_chatbot["instructions"] = updated_chatbot.get("system_message", "You are a helpful assistant.")
        
        return ChatbotResponse(**updated_chatbot)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chatbot"
        )


@router.patch("/{chatbot_id}/toggle", response_model=ChatbotResponse)
async def toggle_chatbot(
    chatbot_id: str,
    current_user: User = Depends(get_current_user)
):
    """Toggle chatbot active/inactive status"""
    try:
        # Check if chatbot exists and belongs to user
        chatbot = await db_instance.chatbots.find_one({
            "id": chatbot_id,
            "user_id": current_user.id
        })
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Toggle status
        new_status = "inactive" if chatbot.get("status") == "active" else "active"
        
        await db_instance.chatbots.update_one(
            {"id": chatbot_id},
            {"$set": {"status": new_status, "updated_at": datetime.now(timezone.utc)}}
        )
        
        # Fetch updated chatbot
        updated_chatbot = await db_instance.chatbots.find_one({"id": chatbot_id})
        return ChatbotResponse(**updated_chatbot)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle chatbot"
        )


@router.delete("/{chatbot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chatbot(
    chatbot_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a chatbot"""
    try:
        # Check if chatbot exists and belongs to user
        chatbot = await db_instance.chatbots.find_one({
            "id": chatbot_id,
            "user_id": current_user.id
        })
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Delete chatbot and related data
        await db_instance.chatbots.delete_one({"id": chatbot_id})
        await db_instance.sources.delete_many({"chatbot_id": chatbot_id})
        await db_instance.conversations.delete_many({"chatbot_id": chatbot_id})
        await db_instance.messages.delete_many({"chatbot_id": chatbot_id})
        
        # Decrement usage count
        await plan_service.decrement_usage(current_user.id, "chatbots")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chatbot"
        )
