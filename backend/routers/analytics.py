from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import DashboardAnalytics, ChatbotAnalytics
from auth import get_current_user, get_current_user, User
from datetime import datetime, timedelta, date
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])
db_instance = None


def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db


@router.get("/dashboard", response_model=DashboardAnalytics)
async def get_dashboard_analytics(current_user: User = Depends(get_current_user)):
    """Get dashboard analytics for the current user"""
    try:
        # Get all user's chatbots
        chatbots = await db_instance.chatbots.find(
            {"user_id": current_user.id}
        ).to_list(length=None)
        
        chatbot_ids = [chatbot["id"] for chatbot in chatbots]
        
        # Count active chatbots
        active_chatbots = sum(1 for chatbot in chatbots if chatbot.get("status") == "active")
        
        # Count total conversations
        total_conversations = await db_instance.conversations.count_documents(
            {"chatbot_id": {"$in": chatbot_ids}}
        )
        
        # Count total messages
        total_messages = await db_instance.messages.count_documents(
            {"chatbot_id": {"$in": chatbot_ids}}
        )
        
        # Count total leads
        total_leads = await db_instance.leads.count_documents(
            {"user_id": current_user.id}
        )
        
        return DashboardAnalytics(
            total_conversations=total_conversations,
            total_messages=total_messages,
            active_chatbots=active_chatbots,
            total_chatbots=len(chatbots),
            total_leads=total_leads
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analytics"
        )


@router.get("/chatbot/{chatbot_id}", response_model=ChatbotAnalytics)
async def get_chatbot_analytics(
    chatbot_id: str,
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get analytics for a specific chatbot"""
    try:
        # Verify ownership
        chatbot = await db_instance.chatbots.find_one({
            "id": chatbot_id,
            "user_id": current_user.id
        })
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get conversations
        conversations = await db_instance.conversations.find({
            "chatbot_id": chatbot_id,
            "created_at": {"$gte": start_date, "$lte": end_date}
        }).to_list(length=None)
        
        # Get messages
        messages = await db_instance.messages.find({
            "chatbot_id": chatbot_id,
            "timestamp": {"$gte": start_date, "$lte": end_date}
        }).to_list(length=None)
        
        # Group by date
        conversations_by_date = defaultdict(int)
        messages_by_date = defaultdict(int)
        
        for conv in conversations:
            conv_date = conv["created_at"].date().isoformat()
            conversations_by_date[conv_date] += 1
        
        for msg in messages:
            msg_date = msg["timestamp"].date().isoformat()
            messages_by_date[msg_date] += 1
        
        # Generate date range
        date_range = []
        current_date = start_date.date()
        while current_date <= end_date.date():
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        # Fill in missing dates with 0
        for d in date_range:
            d_str = d.isoformat()
            if d_str not in conversations_by_date:
                conversations_by_date[d_str] = 0
            if d_str not in messages_by_date:
                messages_by_date[d_str] = 0
        
        return ChatbotAnalytics(
            chatbot_id=chatbot_id,
            total_conversations=len(conversations),
            total_messages=len(messages),
            date_range=date_range,
            conversations_by_date=dict(conversations_by_date),
            messages_by_date=dict(messages_by_date)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chatbot analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch chatbot analytics"
        )
