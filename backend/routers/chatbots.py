from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime, timezone
from models import (
    Chatbot, ChatbotCreate, ChatbotUpdate, ChatbotResponse
)
from auth import get_current_user, User
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
        
        return ChatbotResponse(**chatbot.model_dump())
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
        update_data = {
            k: v for k, v in chatbot_data.model_dump(exclude_unset=True).items()
            if v is not None
        }
        
        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            
            await db_instance.chatbots.update_one(
                {"id": chatbot_id},
                {"$set": update_data}
            )
        
        # Fetch updated chatbot
        updated_chatbot = await db_instance.chatbots.find_one({"id": chatbot_id})
        return ChatbotResponse(**updated_chatbot)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chatbot"
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
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chatbot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chatbot"
        )
