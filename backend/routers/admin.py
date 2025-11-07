from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import json
import csv
import io
from fastapi.responses import StreamingResponse
import psutil
import os
from uuid import uuid4
import logging

router = APIRouter(prefix="/admin", tags=["admin"])
db_instance = None
logger = logging.getLogger(__name__)

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db

# Pydantic models
class UserUpdate(BaseModel):
    plan: Optional[str] = None
    max_chatbots: Optional[int] = None
    max_messages: Optional[int] = None
    status: Optional[str] = None

class ChatbotUpdate(BaseModel):
    enabled: Optional[bool] = None
    status: Optional[str] = None

class BulkOperation(BaseModel):
    ids: List[str]
    operation: str  # 'delete', 'enable', 'disable', 'export'

class AIProviderConfig(BaseModel):
    provider: str
    api_key: Optional[str] = None
    enabled: bool = True
    rate_limit: Optional[int] = None

class UserEditData(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    plan: Optional[str] = None
    max_chatbots: Optional[int] = None
    max_messages: Optional[int] = None
    max_file_uploads: Optional[int] = None
    max_website_sources: Optional[int] = None
    max_text_sources: Optional[int] = None
    status: Optional[str] = None

class SystemSettings(BaseModel):
    maintenance_mode: Optional[bool] = None
    allow_registrations: Optional[bool] = None
    default_plan: Optional[str] = None
    max_chatbots_per_user: Optional[int] = None

class EmailTemplate(BaseModel):
    name: str
    subject: str
    body: str
    variables: Optional[List[str]] = None

class BulkEmail(BaseModel):
    subject: str
    body: str
    recipient_filter: Optional[str] = None  # 'all', 'free', 'paid'


@router.get("/stats")
async def get_admin_stats() -> Dict[str, Any]:
    """
    Get admin dashboard statistics
    """
    try:
        if db_instance is None:
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
        if db_instance is None:
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
        if db_instance is None:
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
        if db_instance is None:
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
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        conversations_collection = db_instance['conversations']
        chatbots_collection = db_instance['chatbots']
        
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
        
        conversations_by_day = []
        async for doc in conversations_collection.aggregate(pipeline):
            conversations_by_day.append(doc)
        
        # Most popular AI providers
        provider_stats = []
        async for doc in chatbots_collection.aggregate([
            {
                "$group": {
                    "_id": "$ai_provider",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}}
        ]):
            provider_stats.append(doc)
        
        return {
            "conversationsByDay": conversations_by_day,
            "providerStats": provider_stats
        }
    except Exception as e:
        print(f"Error in get_admin_analytics: {str(e)}")
        return {
            "conversationsByDay": [],
            "providerStats": []
        }


# ==================== USER MANAGEMENT ====================
@router.get("/users/detailed")
async def get_users_detailed():
    """Get detailed user information with usage stats"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        conversations_collection = db_instance['conversations']
        
        # Get all unique users
        user_ids = await chatbots_collection.distinct('user_id')
        
        users_data = []
        for user_id in user_ids:
            # Count chatbots
            chatbots_count = await chatbots_collection.count_documents({"user_id": user_id})
            
            # Get user's chatbots
            user_chatbots = []
            async for bot in chatbots_collection.find({"user_id": user_id}):
                user_chatbots.append(bot.get('id'))
            
            # Count messages for user's chatbots
            messages_count = 0
            conversations_count = 0
            if user_chatbots:
                messages_count = await messages_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
                conversations_count = await conversations_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
            
            # Get user's first chatbot creation date
            first_chatbot = await chatbots_collection.find_one(
                {"user_id": user_id},
                sort=[("created_at", 1)]
            )
            
            users_data.append({
                "user_id": user_id,
                "email": f"{user_id}@botsmith.co",  # Mock email
                "chatbots_count": chatbots_count,
                "messages_count": messages_count,
                "conversations_count": conversations_count,
                "created_at": first_chatbot.get('created_at') if first_chatbot else None,
                "plan": "Free",  # Default plan
                "status": "active",
                "max_chatbots": 1,
                "max_messages": 100
            })
        
        return {
            "users": users_data,
            "total": len(users_data)
        }
    except Exception as e:
        print(f"Error in get_users_detailed: {str(e)}")
        return {"users": [], "total": 0}


@router.put("/users/{user_id}")
async def update_user(user_id: str, update_data: UserUpdate):
    """Update user plan and limits"""
    try:
        # In a real app, you'd update a users collection
        # For now, we'll return success
        return {
            "success": True,
            "message": f"User {user_id} updated successfully",
            "user": {
                "user_id": user_id,
                **update_data.dict(exclude_unset=True)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete user and all their data"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        sources_collection = db_instance['sources']
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # Get user's chatbots
        user_chatbots = []
        async for bot in chatbots_collection.find({"user_id": user_id}):
            user_chatbots.append(bot.get('id'))
        
        # Delete all related data
        if user_chatbots:
            await messages_collection.delete_many({"chatbot_id": {"$in": user_chatbots}})
            await conversations_collection.delete_many({"chatbot_id": {"$in": user_chatbots}})
            await sources_collection.delete_many({"chatbot_id": {"$in": user_chatbots}})
        
        # Delete user's chatbots
        result = await chatbots_collection.delete_many({"user_id": user_id})
        
        return {
            "success": True,
            "message": f"User {user_id} and all related data deleted",
            "deleted_chatbots": result.deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CHATBOT MANAGEMENT ====================
@router.get("/chatbots/detailed")
async def get_chatbots_detailed():
    """Get detailed chatbot information"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
            
        chatbots_collection = db_instance['chatbots']
        sources_collection = db_instance['sources']
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        chatbots = []
        async for bot in chatbots_collection.find({}).sort("created_at", -1):
            chatbot_id = bot.get('id')
            
            # Count sources
            sources_count = await sources_collection.count_documents({"chatbot_id": chatbot_id})
            
            # Count conversations
            conversations_count = await conversations_collection.count_documents({"chatbot_id": chatbot_id})
            
            # Count messages
            messages_count = await messages_collection.count_documents({"chatbot_id": chatbot_id})
            
            chatbots.append({
                "id": bot.get('id'),
                "name": bot.get('name'),
                "ai_provider": bot.get('ai_provider'),
                "ai_model": bot.get('ai_model'),
                "user_id": bot.get('user_id'),
                "created_at": bot.get('created_at'),
                "updated_at": bot.get('updated_at'),
                "sources_count": sources_count,
                "conversations_count": conversations_count,
                "messages_count": messages_count,
                "enabled": bot.get('enabled', True),
                "status": bot.get('status', 'active'),
                "primary_color": bot.get('primary_color'),
                "welcome_message": bot.get('welcome_message')
            })
        
        return {
            "chatbots": chatbots,
            "total": len(chatbots)
        }
    except Exception as e:
        print(f"Error in get_chatbots_detailed: {str(e)}")
        return {"chatbots": [], "total": 0}


@router.put("/chatbots/{chatbot_id}/toggle")
async def toggle_chatbot(chatbot_id: str):
    """Enable/disable a chatbot"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Get current status
        chatbot = await chatbots_collection.find_one({"id": chatbot_id})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        current_enabled = chatbot.get('enabled', True)
        new_enabled = not current_enabled
        
        # Update
        await chatbots_collection.update_one(
            {"id": chatbot_id},
            {"$set": {"enabled": new_enabled, "updated_at": datetime.now().isoformat()}}
        )
        
        return {
            "success": True,
            "chatbot_id": chatbot_id,
            "enabled": new_enabled
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbots/bulk")
async def bulk_chatbot_operations(operation: BulkOperation):
    """Perform bulk operations on chatbots"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        if operation.operation == "delete":
            result = await chatbots_collection.delete_many({"id": {"$in": operation.ids}})
            return {
                "success": True,
                "operation": "delete",
                "affected": result.deleted_count
            }
        elif operation.operation == "enable":
            result = await chatbots_collection.update_many(
                {"id": {"$in": operation.ids}},
                {"$set": {"enabled": True}}
            )
            return {
                "success": True,
                "operation": "enable",
                "affected": result.modified_count
            }
        elif operation.operation == "disable":
            result = await chatbots_collection.update_many(
                {"id": {"$in": operation.ids}},
                {"$set": {"enabled": False}}
            )
            return {
                "success": True,
                "operation": "disable",
                "affected": result.modified_count
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONVERSATIONS MANAGEMENT ====================
@router.get("/conversations")
async def get_all_conversations(
    chatbot_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
):
    """Get all conversations with filters"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        conversations_collection = db_instance['conversations']
        
        # Build filter
        filter_dict = {}
        if chatbot_id:
            filter_dict["chatbot_id"] = chatbot_id
        if status:
            filter_dict["status"] = status
        if start_date:
            if "created_at" not in filter_dict:
                filter_dict["created_at"] = {}
            filter_dict["created_at"]["$gte"] = start_date
        if end_date:
            if "created_at" not in filter_dict:
                filter_dict["created_at"] = {}
            filter_dict["created_at"]["$lte"] = end_date
        
        # Get conversations
        conversations = []
        async for conv in conversations_collection.find(filter_dict).sort("created_at", -1).limit(limit):
            conversations.append({
                "id": conv.get('id'),
                "chatbot_id": conv.get('chatbot_id'),
                "user_name": conv.get('user_name'),
                "user_email": conv.get('user_email'),
                "status": conv.get('status'),
                "message_count": conv.get('message_count', 0),
                "created_at": conv.get('created_at'),
                "updated_at": conv.get('updated_at')
            })
        
        return {
            "conversations": conversations,
            "total": len(conversations)
        }
    except Exception as e:
        print(f"Error in get_all_conversations: {str(e)}")
        return {"conversations": [], "total": 0}


@router.get("/conversations/export")
async def export_conversations(
    format: str = "json",
    chatbot_id: Optional[str] = None
):
    """Export conversations to JSON or CSV"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # Get conversations
        filter_dict = {}
        if chatbot_id:
            filter_dict["chatbot_id"] = chatbot_id
        
        export_data = []
        async for conv in conversations_collection.find(filter_dict):
            # Get messages for this conversation
            messages = []
            async for msg in messages_collection.find({"conversation_id": conv.get('id')}):
                messages.append({
                    "role": msg.get('role'),
                    "content": msg.get('content'),
                    "timestamp": msg.get('timestamp')
                })
            
            export_data.append({
                "conversation_id": conv.get('id'),
                "chatbot_id": conv.get('chatbot_id'),
                "user_name": conv.get('user_name'),
                "user_email": conv.get('user_email'),
                "status": conv.get('status'),
                "created_at": conv.get('created_at'),
                "messages": messages
            })
        
        # Return based on format
        if format == "csv":
            # Convert to CSV format
            csv_data = []
            for conv in export_data:
                for msg in conv['messages']:
                    csv_data.append({
                        "conversation_id": conv['conversation_id'],
                        "chatbot_id": conv['chatbot_id'],
                        "user_name": conv['user_name'],
                        "user_email": conv['user_email'],
                        "status": conv['status'],
                        "created_at": conv['created_at'],
                        "role": msg['role'],
                        "content": msg['content'],
                        "timestamp": msg['timestamp']
                    })
            return csv_data
        else:
            return export_data
            
    except Exception as e:
        print(f"Error in export_conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== REVENUE & BILLING ====================
@router.get("/revenue/overview")
async def get_revenue_overview():
    """Get revenue overview and statistics"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Mock data for demo - replace with actual billing database
        return {
            "mrr": 15000,  # Monthly Recurring Revenue
            "arr": 180000,  # Annual Recurring Revenue
            "total_revenue": 45000,
            "active_subscriptions": 25,
            "churned_this_month": 2,
            "new_this_month": 8,
            "revenue_by_plan": {
                "Free": 0,
                "Starter": 7500,
                "Professional": 12000,
                "Enterprise": 25500
            },
            "revenue_growth": 15.5,  # percentage
            "payment_failures": 1,
            "pending_invoices": 3
        }
    except Exception as e:
        print(f"Error in get_revenue_overview: {str(e)}")
        return {
            "mrr": 0,
            "arr": 0,
            "total_revenue": 0,
            "active_subscriptions": 0
        }


@router.get("/revenue/history")
async def get_revenue_history(days: int = 30):
    """Get revenue history for charts"""
    try:
        # Mock data - replace with actual data
        history = []
        from datetime import datetime, timedelta
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
            history.append({
                "date": date,
                "revenue": 500 + (i * 50),  # Mock increasing revenue
                "subscriptions": 20 + i,
                "new_users": 2 + (i % 5)
            })
        return {
            "history": history,
            "total": len(history)
        }
    except Exception as e:
        print(f"Error in get_revenue_history: {str(e)}")
        return {"history": [], "total": 0}


@router.get("/users/{user_id}/activity")
async def get_user_activity(user_id: str):
    """Get detailed activity timeline for a user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        conversations_collection = db_instance['conversations']
        
        activities = []
        
        # Get user's chatbots
        async for bot in chatbots_collection.find({"user_id": user_id}).sort("created_at", -1):
            activities.append({
                "type": "chatbot_created",
                "title": f"Created chatbot: {bot.get('name')}",
                "timestamp": bot.get('created_at'),
                "details": {
                    "chatbot_id": bot.get('id'),
                    "provider": bot.get('ai_provider')
                }
            })
        
        # Get user's chatbot IDs
        user_chatbots = [bot.get('id') async for bot in chatbots_collection.find({"user_id": user_id})]
        
        # Get conversations
        if user_chatbots:
            async for conv in conversations_collection.find(
                {"chatbot_id": {"$in": user_chatbots}}
            ).sort("created_at", -1).limit(50):
                activities.append({
                    "type": "conversation",
                    "title": f"Conversation with {conv.get('user_name', 'Anonymous')}",
                    "timestamp": conv.get('created_at'),
                    "details": {
                        "conversation_id": conv.get('id'),
                        "status": conv.get('status')
                    }
                })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "activities": activities[:100],  # Limit to 100
            "total": len(activities)
        }
    except Exception as e:
        print(f"Error in get_user_activity: {str(e)}")
        return {"activities": [], "total": 0}


@router.put("/users/{user_id}/edit")
async def edit_user(user_id: str, data: UserEditData):
    """Edit user details and limits"""
    try:
        # In production, update users collection
        return {
            "success": True,
            "message": f"User {user_id} updated successfully",
            "user": {
                "user_id": user_id,
                **data.dict(exclude_unset=True)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/suspend")
async def suspend_user(user_id: str):
    """Suspend/block a user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Disable all user's chatbots
        result = await chatbots_collection.update_many(
            {"user_id": user_id},
            {"$set": {"enabled": False, "status": "suspended"}}
        )
        
        return {
            "success": True,
            "message": f"User {user_id} suspended",
            "chatbots_disabled": result.modified_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/activate")
async def activate_user(user_id: str):
    """Activate a suspended user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Enable all user's chatbots
        result = await chatbots_collection.update_many(
            {"user_id": user_id},
            {"$set": {"enabled": True, "status": "active"}}
        )
        
        return {
            "success": True,
            "message": f"User {user_id} activated",
            "chatbots_enabled": result.modified_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ADVANCED ANALYTICS ====================
@router.get("/analytics/users/growth")
async def get_user_growth(days: int = 30):
    """Get user growth analytics"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Get unique users by day
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "date": {"$substr": ["$created_at", 0, 10]},
                        "user_id": "$user_id"
                    }
                }
            },
            {
                "$group": {
                    "_id": "$_id.date",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        growth_data = []
        async for doc in chatbots_collection.aggregate(pipeline):
            growth_data.append({
                "date": doc['_id'],
                "users": doc['count']
            })
        
        return {
            "growth": growth_data,
            "total": len(growth_data)
        }
    except Exception as e:
        print(f"Error in get_user_growth: {str(e)}")
        return {"growth": [], "total": 0}


@router.get("/analytics/messages/volume")
async def get_message_volume(days: int = 30):
    """Get message volume over time"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        messages_collection = db_instance['messages']
        
        # Get messages by day
        thirty_days_ago = (datetime.now() - timedelta(days=days)).isoformat()
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": thirty_days_ago}
                }
            },
            {
                "$group": {
                    "_id": {"$substr": ["$timestamp", 0, 10]},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        volume_data = []
        async for doc in messages_collection.aggregate(pipeline):
            volume_data.append({
                "date": doc['_id'],
                "messages": doc['count']
            })
        
        return {
            "volume": volume_data,
            "total": len(volume_data)
        }
    except Exception as e:
        print(f"Error in get_message_volume: {str(e)}")
        return {"volume": [], "total": 0}


@router.get("/analytics/providers/distribution")
async def get_provider_distribution():
    """Get AI provider usage distribution"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        pipeline = [
            {
                "$group": {
                    "_id": "$ai_provider",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}}
        ]
        
        distribution = []
        async for doc in chatbots_collection.aggregate(pipeline):
            distribution.append({
                "provider": doc['_id'] or 'Unknown',
                "count": doc['count']
            })
        
        return {
            "distribution": distribution,
            "total": len(distribution)
        }
    except Exception as e:
        print(f"Error in get_provider_distribution: {str(e)}")
        return {"distribution": [], "total": 0}


# ==================== SYSTEM SETTINGS ====================
@router.get("/settings")
async def get_system_settings():
    """Get system settings"""
    try:
        # Mock settings - in production, fetch from database
        return {
            "maintenance_mode": False,
            "allow_registrations": True,
            "default_plan": "Free",
            "max_chatbots_per_user": 1,
            "ai_providers": {
                "openai": {"enabled": True, "rate_limit": 100},
                "claude": {"enabled": True, "rate_limit": 100},
                "gemini": {"enabled": True, "rate_limit": 100}
            },
            "email_notifications": True,
            "auto_moderation": False
        }
    except Exception as e:
        print(f"Error in get_system_settings: {str(e)}")
        return {}


@router.put("/settings")
async def update_system_settings(settings: SystemSettings):
    """Update system settings"""
    try:
        # In production, save to database
        return {
            "success": True,
            "message": "Settings updated successfully",
            "settings": settings.dict(exclude_unset=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ACTIVITY LOGS ====================
@router.get("/logs/activity")
async def get_detailed_activity_logs(
    limit: int = 100,
    action: Optional[str] = None,
    user_id: Optional[str] = None
):
    """Get detailed activity/audit logs"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Build comprehensive activity log from multiple collections
        logs = []
        
        chatbots_collection = db_instance['chatbots']
        sources_collection = db_instance['sources']
        
        # Get chatbot activities
        filter_dict = {}
        if user_id:
            filter_dict["user_id"] = user_id
        
        async for bot in chatbots_collection.find(filter_dict).sort("created_at", -1).limit(limit):
            logs.append({
                "id": bot.get('id'),
                "action": "chatbot_created",
                "user_id": bot.get('user_id'),
                "details": f"Created chatbot: {bot.get('name')}",
                "timestamp": bot.get('created_at'),
                "entity_type": "chatbot",
                "entity_id": bot.get('id')
            })
        
        # Get source activities
        async for source in sources_collection.find(filter_dict if user_id else {}).sort("created_at", -1).limit(limit):
            logs.append({
                "id": source.get('id'),
                "action": "source_added",
                "user_id": "system",
                "details": f"Added source: {source.get('name')}",
                "timestamp": source.get('created_at'),
                "entity_type": "source",
                "entity_id": source.get('id')
            })
        
        # Sort by timestamp
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {
            "logs": logs[:limit],
            "total": len(logs)
        }
    except Exception as e:
        print(f"Error in get_activity_logs: {str(e)}")
        return {"logs": [], "total": 0}


# ==================== EMAIL MANAGEMENT ====================
@router.post("/email/send-bulk")
async def send_bulk_email(email_data: BulkEmail):
    """Send bulk email to users"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Get recipients based on filter
        recipients = []
        if email_data.recipient_filter == 'all':
            user_ids = await chatbots_collection.distinct('user_id')
            recipients = [f"{uid}@botsmith.co" for uid in user_ids]
        
        # In production, integrate with email service (SendGrid, AWS SES, etc.)
        return {
            "success": True,
            "message": f"Email queued for {len(recipients)} recipients",
            "recipients_count": len(recipients)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email/templates")
async def get_email_templates():
    """Get email templates"""
    try:
        # Mock templates
        return {
            "templates": [
                {
                    "id": "welcome",
                    "name": "Welcome Email",
                    "subject": "Welcome to BotSmith!",
                    "body": "Hi {{name}}, welcome to BotSmith...",
                    "variables": ["name", "email"]
                },
                {
                    "id": "upgrade",
                    "name": "Upgrade Reminder",
                    "subject": "Upgrade your BotSmith plan",
                    "body": "You're using {{usage}}% of your plan...",
                    "variables": ["name", "usage", "plan"]
                }
            ],
            "total": 2
        }
    except Exception as e:
        print(f"Error in get_email_templates: {str(e)}")
        return {"templates": [], "total": 0}


# ==================== BACKUP & EXPORT ====================
@router.get("/backup/database")
async def backup_database():
    """Create database backup"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Get all data
        backup_data = {}
        
        for collection_name in ['chatbots', 'sources', 'conversations', 'messages']:
            collection = db_instance[collection_name]
            data = []
            async for doc in collection.find({}):
                # Remove _id field for JSON serialization
                doc.pop('_id', None)
                data.append(doc)
            backup_data[collection_name] = data
        
        backup_data['backup_timestamp'] = datetime.now().isoformat()
        backup_data['version'] = '1.0'
        
        return {
            "success": True,
            "backup": backup_data,
            "collections": len(backup_data) - 2,  # Minus timestamp and version
            "total_documents": sum(len(v) for k, v in backup_data.items() if isinstance(v, list))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CHATBOT ADVANCED MANAGEMENT ====================
@router.get("/chatbots/{chatbot_id}/details")
async def get_chatbot_details(chatbot_id: str):
    """Get comprehensive chatbot details"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        sources_collection = db_instance['sources']
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # Get chatbot
        chatbot = await chatbots_collection.find_one({"id": chatbot_id})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get sources
        sources = []
        async for source in sources_collection.find({"chatbot_id": chatbot_id}):
            sources.append({
                "id": source.get('id'),
                "name": source.get('name'),
                "type": source.get('type')
            })
        
        # Get conversations count
        conv_count = await conversations_collection.count_documents({"chatbot_id": chatbot_id})
        
        # Get messages count
        msg_count = await messages_collection.count_documents({"chatbot_id": chatbot_id})
        
        chatbot.pop('_id', None)
        
        return {
            "chatbot": chatbot,
            "sources": sources,
            "conversations_count": conv_count,
            "messages_count": msg_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbots/{chatbot_id}/clone")
async def clone_chatbot(chatbot_id: str, new_name: str, target_user_id: str):
    """Clone a chatbot"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        
        # Get original chatbot
        original = await chatbots_collection.find_one({"id": chatbot_id})
        if not original:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Create clone
        clone = original.copy()
        clone['id'] = str(uuid4())
        clone['name'] = new_name
        clone['user_id'] = target_user_id
        clone['created_at'] = datetime.now().isoformat()
        clone.pop('_id', None)
        
        await chatbots_collection.insert_one(clone)
        
        return {
            "success": True,
            "message": "Chatbot cloned successfully",
            "clone_id": clone['id']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SOURCES MANAGEMENT ====================
@router.get("/sources")
async def get_all_sources():
    """Get all sources across all chatbots"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        sources_collection = db_instance['sources']
        
        sources = []
        async for source in sources_collection.find({}).sort("created_at", -1):
            sources.append({
                "id": source.get('id'),
                "chatbot_id": source.get('chatbot_id'),
                "type": source.get('type'),
                "name": source.get('name'),
                "url": source.get('url'),
                "file_size": source.get('file_size', 0),
                "status": source.get('status', 'active'),
                "created_at": source.get('created_at')
            })
        
        return {
            "sources": sources,
            "total": len(sources)
        }
    except Exception as e:
        print(f"Error in get_all_sources: {str(e)}")
        return {"sources": [], "total": 0}


@router.delete("/sources/{source_id}")
async def delete_source(source_id: str):
    """Delete a source"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        sources_collection = db_instance['sources']
        result = await sources_collection.delete_one({"id": source_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Source not found")
        
        return {
            "success": True,
            "message": "Source deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SYSTEM MONITORING ====================
@router.get("/system/health")
async def get_system_health():
    """Get system health metrics"""
    try:
        # CPU and Memory usage
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database stats
        db_stats = {}
        if db_instance is not None:
            try:
                stats = await db_instance.command("dbStats")
                db_stats = {
                    "collections": stats.get('collections', 0),
                    "dataSize": stats.get('dataSize', 0),
                    "storageSize": stats.get('storageSize', 0),
                    "indexes": stats.get('indexes', 0)
                }
            except Exception as e:
                print(f"Error fetching DB stats: {str(e)}")
                db_stats = {"error": "Unable to fetch DB stats"}
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_usage": disk.percent,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024)
            },
            "database": db_stats
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/system/activity")
async def get_real_time_activity():
    """Get real-time system activity"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # Activity in last hour
        one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
        
        recent_conversations = await conversations_collection.count_documents({
            "created_at": {"$gte": one_hour_ago}
        })
        
        recent_messages = await messages_collection.count_documents({
            "timestamp": {"$gte": one_hour_ago}
        })
        
        # Get last 10 activities
        recent_activity = []
        async for conv in conversations_collection.find(
            {"created_at": {"$gte": one_hour_ago}}
        ).sort("created_at", -1).limit(10):
            recent_activity.append({
                "type": "conversation",
                "chatbot_id": conv.get('chatbot_id'),
                "user": conv.get('user_name', 'Anonymous'),
                "timestamp": conv.get('created_at')
            })
        
        return {
            "last_hour": {
                "conversations": recent_conversations,
                "messages": recent_messages
            },
            "recent_activity": recent_activity
        }
    except Exception as e:
        print(f"Error in get_real_time_activity: {str(e)}")
        return {
            "last_hour": {"conversations": 0, "messages": 0},
            "recent_activity": []
        }


# ==================== DATABASE MANAGEMENT ====================
@router.get("/database/stats")
async def get_database_stats():
    """Get detailed database statistics"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        stats = {
            "chatbots": await db_instance['chatbots'].count_documents({}),
            "sources": await db_instance['sources'].count_documents({}),
            "conversations": await db_instance['conversations'].count_documents({}),
            "messages": await db_instance['messages'].count_documents({}),
            "plans": await db_instance['plans'].count_documents({}) if 'plans' in await db_instance.list_collection_names() else 0
        }
        
        # Get collection sizes
        collections_info = []
        for collection_name in ['chatbots', 'sources', 'conversations', 'messages']:
            try:
                coll_stats = await db_instance.command("collStats", collection_name)
                collections_info.append({
                    "name": collection_name,
                    "count": coll_stats.get('count', 0),
                    "size": coll_stats.get('size', 0),
                    "avgObjSize": coll_stats.get('avgObjSize', 0)
                })
            except Exception as e:
                print(f"Error fetching stats for {collection_name}: {str(e)}")
                pass
        
        return {
            "counts": stats,
            "collections": collections_info,
            "total_documents": sum(stats.values())
        }
    except Exception as e:
        print(f"Error in get_database_stats: {str(e)}")
        return {
            "counts": {},
            "collections": [],
            "total_documents": 0
        }


# ==================== CONTENT MODERATION ====================
@router.get("/moderation/flagged")
async def get_flagged_content():
    """Get flagged conversations for moderation"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # For demo, get conversations with "escalated" status
        flagged = []
        async for conv in conversations_collection.find({"status": "escalated"}):
            # Get messages
            messages = []
            async for msg in messages_collection.find({"conversation_id": conv.get('id')}):
                messages.append({
                    "role": msg.get('role'),
                    "content": msg.get('content'),
                    "timestamp": msg.get('timestamp')
                })
            
            flagged.append({
                "conversation_id": conv.get('id'),
                "chatbot_id": conv.get('chatbot_id'),
                "user_name": conv.get('user_name'),
                "status": conv.get('status'),
                "created_at": conv.get('created_at'),
                "messages": messages,
                "flag_reason": "User escalated to human"
            })
        
        return {
            "flagged_conversations": flagged,
            "total": len(flagged)
        }
    except Exception as e:
        print(f"Error in get_flagged_content: {str(e)}")
        return {"flagged_conversations": [], "total": 0}


# ==================== ENHANCED USER MANAGEMENT ====================

@router.get("/users/enhanced")
async def get_users_enhanced(
    sortBy: str = "created_at",
    sortOrder: str = "desc"
):
    """Get enhanced user data with all metrics"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        conversations_collection = db_instance['conversations']
        sources_collection = db_instance['sources']
        
        # Get all users from the users collection
        all_users = await users_collection.find({}).to_list(length=1000)
        
        users_data = []
        for user in all_users:
            user_id = user.get('id')
            
            # Count chatbots for this user
            chatbots_count = await chatbots_collection.count_documents({"user_id": user_id})
            
            # Get user's chatbot IDs
            user_chatbots = []
            async for bot in chatbots_collection.find({"user_id": user_id}, {"id": 1}):
                user_chatbots.append(bot.get('id'))
            
            messages_count = 0
            conversations_count = 0
            sources_count = 0
            last_message_time = None
            
            if user_chatbots:
                messages_count = await messages_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
                conversations_count = await conversations_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
                sources_count = await sources_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
                
                # Get last message time
                last_message = await messages_collection.find_one(
                    {"chatbot_id": {"$in": user_chatbots}},
                    sort=[("timestamp", -1)]
                )
                if last_message:
                    last_message_time = last_message.get('timestamp')
            
            users_data.append({
                "user_id": user_id,
                "email": user.get('email', f"{user_id}@botsmith.com"),
                "name": user.get('name', f"User {user_id[:8]}"),
                "role": user.get('role', 'user'),
                "status": user.get('status', 'active'),
                "phone": user.get('phone'),
                "avatar_url": user.get('avatar_url'),
                "company": user.get('company'),
                "job_title": user.get('job_title'),
                "tags": user.get('tags', []),
                "chatbots_count": chatbots_count,
                "messages_count": messages_count,
                "conversations_count": conversations_count,
                "sources_count": sources_count,
                "created_at": user.get('created_at'),
                "last_login": user.get('last_login'),
                "login_count": user.get('login_count', 0),
                "last_ip": user.get('last_ip'),
                "last_active": last_message_time or user.get('last_login'),
                "suspension_reason": user.get('suspension_reason'),
                "suspension_until": user.get('suspension_until'),
                "custom_max_chatbots": user.get('custom_max_chatbots'),
                "custom_max_messages": user.get('custom_max_messages'),
                "custom_max_file_uploads": user.get('custom_max_file_uploads'),
                "admin_notes": user.get('admin_notes')
            })
        
        # Sort users - handle both string and datetime types for date fields
        if sortBy == "created_at" or sortBy == "last_login":
            def sort_key(x):
                val = x.get(sortBy)
                if val is None:
                    return datetime.min if sortOrder == 'desc' else datetime.max
                if isinstance(val, str):
                    try:
                        return datetime.fromisoformat(val.replace('Z', '+00:00'))
                    except:
                        return datetime.min if sortOrder == 'desc' else datetime.max
                return val
            users_data.sort(key=sort_key, reverse=(sortOrder == 'desc'))
        elif sortBy in ["messages_count", "chatbots_count", "login_count"]:
            users_data.sort(key=lambda x: x.get(sortBy, 0), reverse=(sortOrder == 'desc'))
        
        return {
            "users": users_data,
            "total": len(users_data)
        }
    except Exception as e:
        logger.error(f"Error in get_users_enhanced: {str(e)}")
        return {"users": [], "total": 0, "error": str(e)}


@router.get("/users/{user_id}/stats")
async def get_user_stats(user_id: str):
    """Get comprehensive statistics for a specific user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        conversations_collection = db_instance['conversations']
        sources_collection = db_instance['sources']
        
        # Get user's chatbots
        user_chatbots = []
        async for bot in chatbots_collection.find({"user_id": user_id}):
            user_chatbots.append(bot.get('id'))
        
        total_chatbots = len(user_chatbots)
        total_messages = 0
        total_conversations = 0
        total_sources = 0
        
        if user_chatbots:
            total_messages = await messages_collection.count_documents(
                {"chatbot_id": {"$in": user_chatbots}}
            )
            total_conversations = await conversations_collection.count_documents(
                {"chatbot_id": {"$in": user_chatbots}}
            )
            total_sources = await sources_collection.count_documents(
                {"chatbot_id": {"$in": user_chatbots}}
            )
        
        # Calculate average messages per day
        first_chatbot = await chatbots_collection.find_one(
            {"user_id": user_id},
            sort=[("created_at", 1)]
        )
        
        avg_messages_per_day = 0
        if first_chatbot and total_messages > 0:
            created_date = datetime.fromisoformat(first_chatbot.get('created_at', ''))
            days_active = max(1, (datetime.now() - created_date).days)
            avg_messages_per_day = round(total_messages / days_active, 2)
        
        return {
            "total_chatbots": total_chatbots,
            "total_messages": total_messages,
            "total_conversations": total_conversations,
            "total_sources": total_sources,
            "avg_messages_per_day": avg_messages_per_day,
            "engagement_score": min(100, total_messages + (total_chatbots * 10))
        }
    except Exception as e:
        print(f"Error in get_user_stats: {str(e)}")
        return {
            "total_chatbots": 0,
            "total_messages": 0,
            "total_conversations": 0,
            "total_sources": 0,
            "avg_messages_per_day": 0,
            "engagement_score": 0
        }


@router.get("/users/{user_id}/notes")
async def get_user_notes(user_id: str):
    """Get notes for a user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # In real app, you'd have a notes collection
        # For now, return empty
        return {"notes": []}
    except Exception as e:
        print(f"Error in get_user_notes: {str(e)}")
        return {"notes": []}


@router.post("/users/{user_id}/notes")
async def add_user_note(user_id: str, note_data: dict):
    """Add a note to user"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # In real app, you'd save to notes collection
        return {
            "success": True,
            "message": "Note added successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}/tags")
async def update_user_tags(user_id: str, tag_data: dict):
    """Update user tags"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # In real app, you'd update tags in users collection
        return {
            "success": True,
            "message": "Tags updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/send-email")
async def send_bulk_email(email_data: dict):
    """Send email to users"""
    try:
        user_ids = email_data.get('user_ids', [])
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        
        # In real app, you'd integrate with email service
        # For now, just log it
        print(f"Sending email to {len(user_ids)} users: {subject}")
        
        return {
            "success": True,
            "message": f"Email sent to {len(user_ids)} user(s)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/bulk-action")
async def bulk_user_action(action_data: dict):
    """Perform bulk actions on users"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        user_ids = action_data.get('user_ids', [])
        action = action_data.get('action', '')
        
        if action == 'suspend':
            # In real app, update user status to suspended
            print(f"Suspending {len(user_ids)} users")
        elif action == 'activate':
            # In real app, update user status to active
            print(f"Activating {len(user_ids)} users")
        elif action == 'delete':
            # In real app, delete users and their data
            chatbots_collection = db_instance['chatbots']
            for user_id in user_ids:
                await chatbots_collection.delete_many({"user_id": user_id})
        
        return {
            "success": True,
            "message": f"{action} applied to {len(user_ids)} user(s)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}/update")
async def update_user_enhanced(user_id: str, user_data: dict):
    """Update user with all fields"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # In real app, update users collection
        print(f"Updating user {user_id}: {user_data}")
        
        return {
            "success": True,
            "message": "User updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONTACT SALES MANAGEMENT ====================

@router.get("/contact-sales")
async def get_contact_sales_submissions(
    status: Optional[str] = None,
    limit: int = 100
):
    """Get all contact sales form submissions"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        contact_sales_collection = db_instance['contact_sales']
        
        # Build filter
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        
        # Get submissions
        submissions = []
        async for submission in contact_sales_collection.find(filter_dict).sort("created_at", -1).limit(limit):
            submissions.append({
                "id": submission.get('id'),
                "name": submission.get('name'),
                "email": submission.get('email'),
                "company": submission.get('company'),
                "message": submission.get('message'),
                "status": submission.get('status', 'new'),
                "created_at": submission.get('created_at'),
                "notes": submission.get('notes', '')
            })
        
        return {
            "submissions": submissions,
            "total": len(submissions)
        }
    except Exception as e:
        print(f"Error in get_contact_sales_submissions: {str(e)}")
        return {"submissions": [], "total": 0}


@router.put("/contact-sales/{submission_id}")
async def update_contact_sales_status(submission_id: str, update_data: dict):
    """Update contact sales submission status"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        contact_sales_collection = db_instance['contact_sales']
        
        # Update submission
        await contact_sales_collection.update_one(
            {"id": submission_id},
            {"$set": {
                "status": update_data.get('status', 'new'),
                "notes": update_data.get('notes', ''),
                "updated_at": datetime.now().isoformat()
            }}
        )
        
        return {
            "success": True,
            "message": "Submission updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/contact-sales/{submission_id}")
async def delete_contact_sales_submission(submission_id: str):
    """Delete a contact sales submission"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        contact_sales_collection = db_instance['contact_sales']
        result = await contact_sales_collection.delete_one({"id": submission_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        return {
            "success": True,
            "message": "Submission deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== USER SEGMENTATION & ANALYTICS ====================

@router.get("/users/segments")
async def get_user_segments():
    """Get user segments (power users, at-risk, new users, etc.)"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        
        user_ids = await chatbots_collection.distinct('user_id')
        
        segments = {
            "power_users": [],
            "at_risk": [],
            "new_users": [],
            "champions": []
        }
        
        for user_id in user_ids:
            chatbots_count = await chatbots_collection.count_documents({"user_id": user_id})
            
            user_chatbots = []
            async for bot in chatbots_collection.find({"user_id": user_id}):
                user_chatbots.append(bot.get('id'))
            
            messages_count = 0
            if user_chatbots:
                messages_count = await messages_collection.count_documents(
                    {"chatbot_id": {"$in": user_chatbots}}
                )
            
            # Segment logic
            if messages_count > 100 or chatbots_count > 3:
                segments["power_users"].append(user_id)
            elif chatbots_count <= 1 and messages_count < 10:
                segments["new_users"].append(user_id)
            elif messages_count > 500:
                segments["champions"].append(user_id)
        
        return {
            "segments": segments,
            "totals": {
                "power_users": len(segments["power_users"]),
                "at_risk": len(segments["at_risk"]),
                "new_users": len(segments["new_users"]),
                "champions": len(segments["champions"])
            }
        }
    except Exception as e:
        print(f"Error in get_user_segments: {str(e)}")
        return {"segments": {}, "totals": {}}


@router.get("/users/{user_id}/lifecycle")
async def get_user_lifecycle(user_id: str):
    """Get user lifecycle timeline"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        conversations_collection = db_instance['conversations']
        
        timeline = []
        
        # Get all chatbots created
        async for bot in chatbots_collection.find({"user_id": user_id}).sort("created_at", 1):
            timeline.append({
                "event": "chatbot_created",
                "description": f"Created chatbot: {bot.get('name')}",
                "timestamp": bot.get('created_at'),
                "details": {
                    "chatbot_id": bot.get('id'),
                    "chatbot_name": bot.get('name')
                }
            })
        
        return {
            "timeline": timeline,
            "total_events": len(timeline)
        }
    except Exception as e:
        print(f"Error in get_user_lifecycle: {str(e)}")
        return {"timeline": [], "total_events": 0}


@router.get("/users/retention")
async def get_user_retention():
    """Get user retention metrics"""
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        
        # Simple retention calculation
        user_ids = await chatbots_collection.distinct('user_id')
        total_users = len(user_ids)
        
        active_users = 0
        for user_id in user_ids:
            user_chatbots = []
            async for bot in chatbots_collection.find({"user_id": user_id}):
                user_chatbots.append(bot.get('id'))
            
            if user_chatbots:
                recent_messages = await messages_collection.count_documents({
                    "chatbot_id": {"$in": user_chatbots},
                    "timestamp": {"$gte": (datetime.now() - timedelta(days=30)).isoformat()}
                })
                if recent_messages > 0:
                    active_users += 1
        
        retention_rate = (active_users / total_users * 100) if total_users > 0 else 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "retention_rate": round(retention_rate, 2),
            "churn_risk": total_users - active_users
        }
    except Exception as e:
        print(f"Error in get_user_retention: {str(e)}")
        return {
            "total_users": 0,
            "active_users": 0,
            "retention_rate": 0,
            "churn_risk": 0
        }

