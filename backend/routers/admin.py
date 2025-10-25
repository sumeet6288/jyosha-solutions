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

router = APIRouter(prefix="/admin", tags=["admin"])
db_instance = None

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
        
        if format == "csv":
            # Create CSV
            output = io.StringIO()
            if export_data:
                fieldnames = ['conversation_id', 'chatbot_id', 'user_name', 'user_email', 'status', 'created_at', 'message_count']
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                for conv in export_data:
                    writer.writerow({
                        'conversation_id': conv['conversation_id'],
                        'chatbot_id': conv['chatbot_id'],
                        'user_name': conv['user_name'],
                        'user_email': conv['user_email'],
                        'status': conv['status'],
                        'created_at': conv['created_at'],
                        'message_count': len(conv['messages'])
                    })
            
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=conversations_{datetime.now().strftime('%Y%m%d')}.csv"}
            )
        else:
            # Return JSON
            return {
                "conversations": export_data,
                "total": len(export_data),
                "exported_at": datetime.now().isoformat()
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
        if db_instance:
            try:
                stats = await db_instance.command("dbStats")
                db_stats = {
                    "collections": stats.get('collections', 0),
                    "dataSize": stats.get('dataSize', 0),
                    "storageSize": stats.get('storageSize', 0),
                    "indexes": stats.get('indexes', 0)
                }
            except:
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
            except:
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
