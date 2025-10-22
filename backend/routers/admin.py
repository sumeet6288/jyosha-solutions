from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Any
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])
db_instance = None

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db


@router.get("/stats")
async def get_admin_stats() -> Dict[str, Any]:
    """
    Get admin dashboard statistics
    """
    try:
        if not db_instance:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        # Get total users count (unique user_ids from chatbots collection)
        chatbots_collection = db_instance['chatbots']
        users = await chatbots_collection.distinct('user_id')
        total_users = len(users)
        
        # Get total chatbots count
        total_chatbots = await chatbots_collection.count_documents({})
        
        # Get total messages count
        messages_collection = db_instance['messages']
        total_messages = await messages_collection.count_documents({})
        
        # Get active integrations count (chatbots with external integrations)
        # For now, count unique AI providers being used
        providers = await chatbots_collection.distinct('ai_provider')
        active_integrations = len(providers)
        
        return {
            "totalUsers": total_users,
            "activeChatbots": total_chatbots,
            "totalMessages": total_messages,
            "activeIntegrations": active_integrations
        }
    except Exception as e:
        print(f"Error in get_admin_stats: {str(e)}")
        return {
            "totalUsers": 0,
            "activeChatbots": 0,
            "totalMessages": 0,
            "activeIntegrations": 0
        }


@router.get("/users")
async def get_all_users():
    """
    Get all users in the system
    """
    try:
        if not db_instance:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        chatbots_collection = db_instance['chatbots']
        
        # Get all unique users from chatbots
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "chatbots_count": {"$sum": 1},
                    "created_at": {"$first": "$created_at"}
                }
            },
            {
                "$project": {
                    "user_id": "$_id",
                    "chatbots_count": 1,
                    "created_at": 1,
                    "_id": 0
                }
            },
            {"$sort": {"created_at": -1}}
        ]
        
        users = []
        async for user in chatbots_collection.aggregate(pipeline):
            users.append(user)
        
        return {
            "users": users,
            "total": len(users)
        }
    except Exception as e:
        print(f"Error in get_all_users: {str(e)}")
        return {
            "users": [],
            "total": 0
        }


@router.get("/chatbots")
async def get_all_chatbots():
    """
    Get all chatbots in the system
    """
    try:
        if not db_instance:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        chatbots_collection = db_instance['chatbots']
        
        chatbots = []
        cursor = chatbots_collection.find(
            {},
            {
                "_id": 0,
                "id": 1,
                "name": 1,
                "ai_provider": 1,
                "ai_model": 1,
                "user_id": 1,
                "created_at": 1,
                "updated_at": 1
            }
        ).sort("created_at", -1)
        
        async for chatbot in cursor:
            chatbots.append(chatbot)
        
        return {
            "chatbots": chatbots,
            "total": len(chatbots)
        }
    except Exception as e:
        print(f"Error in get_all_chatbots: {str(e)}")
        return {
            "chatbots": [],
            "total": 0
        }


@router.get("/activity-logs")
async def get_activity_logs(limit: int = 100):
    """
    Get recent activity logs
    """
    try:
        if not db_instance:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        conversations_collection = db_instance['conversations']
        
        # Get recent conversations as activity logs
        logs = []
        cursor = conversations_collection.find(
            {},
            {
                "_id": 0,
                "id": 1,
                "chatbot_id": 1,
                "user_id": 1,
                "status": 1,
                "created_at": 1,
                "message_count": 1
            }
        ).sort("created_at", -1).limit(limit)
        
        async for log in cursor:
            logs.append(log)
        
        return {
            "logs": logs,
            "total": len(logs)
        }
    except Exception as e:
        print(f"Error in get_activity_logs: {str(e)}")
        return {
            "logs": [],
            "total": 0
        }


@router.get("/analytics")
async def get_admin_analytics():
    """
    Get admin analytics data
    """
    try:
        conversations_collection = db['conversations']
        chatbots_collection = db['chatbots']
        
        # Get conversations over time (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Conversations by day
        pipeline = [
            {
                "$match": {
                    "created_at": {"$gte": thirty_days_ago.isoformat()}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {"$toDate": "$created_at"}
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        conversations_by_day = list(conversations_collection.aggregate(pipeline))
        
        # Most popular AI providers
        provider_stats = list(chatbots_collection.aggregate([
            {
                "$group": {
                    "_id": "$ai_provider",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}}
        ]))
        
        return {
            "conversationsByDay": conversations_by_day,
            "providerStats": provider_stats
        }
    except Exception as e:
        return {
            "conversationsByDay": [],
            "providerStats": []
        }
