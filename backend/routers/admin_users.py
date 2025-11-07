from fastapi import APIRouter, HTTPException, Query, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from models import (
    User, AdminUserUpdate, PasswordReset, LoginHistory, LoginHistoryResponse,
    ActivityLog, ActivityLogResponse, BulkUserOperation
)
from passlib.context import CryptContext
import logging
import uuid
import json
import io
import csv

router = APIRouter(prefix="/admin/users", tags=["admin-users"])
db_instance = None
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db


# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/test-db")
async def test_database():
    """Test database connection and user count"""
    if db_instance is None:
        return {"error": "Database not initialized", "db_instance": None}
    
    try:
        users_collection = db_instance['users']
        count = await users_collection.count_documents({})
        all_users = await users_collection.find({}).to_list(length=10)
        
        return {
            "database_connected": True,
            "collection_name": users_collection.name,
            "total_users": count,
            "sample_users": [{"id": u.get("id"), "email": u.get("email")} for u in all_users]
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/enhanced")
async def get_enhanced_users(
    sortBy: str = Query("created_at", description="Field to sort by"),
    sortOrder: str = Query("desc", description="Sort order: asc or desc"),
    status: Optional[str] = Query(None, description="Filter by status"),
    role: Optional[str] = Query(None, description="Filter by role"),
    search: Optional[str] = Query(None, description="Search term")
):
    """
    Get enhanced user list with all details for admin panel
    """
    if db_instance is None:
        logger.error("Database not initialized in admin_users router")
        return {"success": False, "users": [], "total": 0, "error": "Database not initialized"}
    
    try:
        users_collection = db_instance['users']
        
        # Simple test: just count users
        total_users = await users_collection.count_documents({})
        
        if total_users == 0:
            return {"success": True, "users": [], "total": 0, "message": "No users in database", "debug": "count is zero"}
        
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        sources_collection = db_instance['sources']
        
        # Build query
        query = {}
        if status:
            query['status'] = status
        if role:
            query['role'] = role
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'email': {'$regex': search, '$options': 'i'}}
            ]
        
        # Get users
        sort_direction = -1 if sortOrder == "desc" else 1
        users = await users_collection.find(query).sort(sortBy, sort_direction).to_list(length=1000)
        
        # Enhance with statistics
        enhanced_users = []
        for user in users:
            user_id = user.get('id')
            
            # Count chatbots
            chatbots_count = await chatbots_collection.count_documents({'user_id': user_id})
            
            # Get all chatbot IDs for this user first
            user_chatbot_ids = []
            async for bot in chatbots_collection.find({'user_id': user_id}, {'id': 1}):
                user_chatbot_ids.append(bot['id'])
            
            # Count messages for all chatbots
            messages_count = 0
            if user_chatbot_ids:
                messages_count = await messages_collection.count_documents({
                    'chatbot_id': {'$in': user_chatbot_ids}
                })
            
            # Count sources for all chatbots
            sources_count = 0
            if user_chatbot_ids:
                sources_count = await sources_collection.count_documents({
                    'chatbot_id': {'$in': user_chatbot_ids}
                })
            
            enhanced_users.append({
                'user_id': user.get('id'),
                'name': user.get('name'),
                'email': user.get('email'),
                'role': user.get('role', 'user'),
                'status': user.get('status', 'active'),
                'phone': user.get('phone'),
                'avatar_url': user.get('avatar_url'),
                'company': user.get('company'),
                'job_title': user.get('job_title'),
                'tags': user.get('tags', []),
                'created_at': user.get('created_at'),
                'last_login': user.get('last_login'),
                'login_count': user.get('login_count', 0),
                'last_ip': user.get('last_ip'),
                'suspension_reason': user.get('suspension_reason'),
                'suspension_until': user.get('suspension_until'),
                'custom_max_chatbots': user.get('custom_max_chatbots'),
                'custom_max_messages': user.get('custom_max_messages'),
                'custom_max_file_uploads': user.get('custom_max_file_uploads'),
                'admin_notes': user.get('admin_notes'),
                'statistics': {
                    'chatbots_count': chatbots_count,
                    'messages_count': messages_count,
                    'sources_count': sources_count
                }
            })
        
        return {"success": True, "users": enhanced_users, "total": len(enhanced_users)}
    
    except Exception as e:
        logger.error(f"Error fetching enhanced users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/details")
async def get_user_details(user_id: str):
    """
    Get detailed information about a specific user
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        user = await users_collection.find_one({'id': user_id})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Remove sensitive data
        user.pop('password_hash', None)
        user.pop('_id', None)
        
        return {"success": True, "user": user}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/update")
async def update_user(user_id: str, update_data: AdminUserUpdate):
    """
    Update user information (admin only)
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        
        # Build update document
        update_doc = {}
        for field, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                update_doc[field] = value
        
        if not update_doc:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_doc['updated_at'] = datetime.now(timezone.utc)
        
        result = await users_collection.update_one(
            {'id': user_id},
            {'$set': update_doc}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Log activity
        await log_activity(
            user_id="admin",
            action="updated_user",
            resource_type="user",
            resource_id=user_id,
            details=f"Updated fields: {', '.join(update_doc.keys())}"
        )
        
        return {"success": True, "message": "User updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """
    Delete a user and all associated data
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        chatbots_collection = db_instance['chatbots']
        sources_collection = db_instance['sources']
        conversations_collection = db_instance['conversations']
        messages_collection = db_instance['messages']
        
        # Get user's chatbots
        chatbots = await chatbots_collection.find({'user_id': user_id}).to_list(length=1000)
        chatbot_ids = [bot['id'] for bot in chatbots]
        
        # Delete all related data
        if chatbot_ids:
            await sources_collection.delete_many({'chatbot_id': {'$in': chatbot_ids}})
            await messages_collection.delete_many({'chatbot_id': {'$in': chatbot_ids}})
            await conversations_collection.delete_many({'chatbot_id': {'$in': chatbot_ids}})
            await chatbots_collection.delete_many({'user_id': user_id})
        
        # Delete user
        result = await users_collection.delete_one({'id': user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Log activity
        await log_activity(
            user_id="admin",
            action="deleted_user",
            resource_type="user",
            resource_id=user_id,
            details=f"Deleted user and {len(chatbot_ids)} chatbots"
        )
        
        return {"success": True, "message": "User and all associated data deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/reset-password")
async def reset_user_password(user_id: str, password_data: PasswordReset):
    """
    Reset user password (admin only)
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        
        # Hash new password
        hashed_password = pwd_context.hash(password_data.new_password)
        
        result = await users_collection.update_one(
            {'id': user_id},
            {'$set': {
                'password_hash': hashed_password,
                'updated_at': datetime.now(timezone.utc)
            }}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Log activity
        await log_activity(
            user_id="admin",
            action="reset_password",
            resource_type="user",
            resource_id=user_id,
            details="Admin reset user password"
        )
        
        return {"success": True, "message": "Password reset successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ACTIVITY TRACKING ENDPOINTS
# ============================================================================

@router.get("/{user_id}/activity")
async def get_user_activity(
    user_id: str,
    limit: int = Query(50, description="Number of activities to return"),
    skip: int = Query(0, description="Number of activities to skip")
):
    """
    Get user activity logs
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        activity_logs_collection = db_instance['activity_logs']
        
        activities = await activity_logs_collection.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).skip(skip).limit(limit).to_list(length=limit)
        
        # Remove MongoDB _id
        for activity in activities:
            activity.pop('_id', None)
        
        return {"success": True, "activities": activities, "total": len(activities)}
    
    except Exception as e:
        logger.error(f"Error fetching user activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/login-history")
async def get_login_history(
    user_id: str,
    limit: int = Query(20, description="Number of logins to return")
):
    """
    Get user login history
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        login_history_collection = db_instance['login_history']
        
        logins = await login_history_collection.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).limit(limit).to_list(length=limit)
        
        # Remove MongoDB _id
        for login in logins:
            login.pop('_id', None)
        
        return {"success": True, "logins": logins, "total": len(logins)}
    
    except Exception as e:
        logger.error(f"Error fetching login history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/stats")
async def get_user_stats(user_id: str):
    """
    Get comprehensive user statistics
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        chatbots_collection = db_instance['chatbots']
        messages_collection = db_instance['messages']
        sources_collection = db_instance['sources']
        conversations_collection = db_instance['conversations']
        activity_logs_collection = db_instance['activity_logs']
        
        # Get user
        user = await users_collection.find_one({'id': user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's chatbots
        chatbots = await chatbots_collection.find({'user_id': user_id}).to_list(length=1000)
        chatbot_ids = [bot['id'] for bot in chatbots]
        
        # Count statistics
        total_chatbots = len(chatbots)
        active_chatbots = len([bot for bot in chatbots if bot.get('status') == 'active'])
        
        total_messages = 0
        total_conversations = 0
        total_sources = 0
        
        if chatbot_ids:
            total_messages = await messages_collection.count_documents({'chatbot_id': {'$in': chatbot_ids}})
            total_conversations = await conversations_collection.count_documents({'chatbot_id': {'$in': chatbot_ids}})
            total_sources = await sources_collection.count_documents({'chatbot_id': {'$in': chatbot_ids}})
        
        # Activity in last 30 days
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        recent_activities = await activity_logs_collection.count_documents({
            'user_id': user_id,
            'timestamp': {'$gte': thirty_days_ago}
        })
        
        # Messages trend (last 7 days)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_messages = await messages_collection.count_documents({
            'chatbot_id': {'$in': chatbot_ids} if chatbot_ids else {'$in': []},
            'timestamp': {'$gte': seven_days_ago}
        })
        
        return {
            "success": True,
            "stats": {
                "user_info": {
                    "name": user.get('name'),
                    "email": user.get('email'),
                    "role": user.get('role', 'user'),
                    "status": user.get('status', 'active'),
                    "created_at": user.get('created_at'),
                    "last_login": user.get('last_login'),
                    "login_count": user.get('login_count', 0)
                },
                "usage": {
                    "total_chatbots": total_chatbots,
                    "active_chatbots": active_chatbots,
                    "total_messages": total_messages,
                    "total_conversations": total_conversations,
                    "total_sources": total_sources
                },
                "activity": {
                    "recent_activities_30d": recent_activities,
                    "recent_messages_7d": recent_messages
                },
                "limits": {
                    "custom_max_chatbots": user.get('custom_max_chatbots'),
                    "custom_max_messages": user.get('custom_max_messages'),
                    "custom_max_file_uploads": user.get('custom_max_file_uploads')
                }
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BULK OPERATIONS ENDPOINTS
# ============================================================================

@router.post("/bulk-operation")
async def bulk_user_operation(operation: BulkUserOperation):
    """
    Perform bulk operations on multiple users
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        results = {
            "success": True,
            "operation": operation.operation,
            "processed": 0,
            "failed": 0,
            "details": []
        }
        
        if operation.operation == "delete":
            for user_id in operation.user_ids:
                try:
                    await delete_user(user_id)
                    results["processed"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["details"].append(f"Failed to delete user {user_id}: {str(e)}")
        
        elif operation.operation == "change_role":
            if not operation.role:
                raise HTTPException(status_code=400, detail="Role is required for change_role operation")
            
            result = await users_collection.update_many(
                {'id': {'$in': operation.user_ids}},
                {'$set': {
                    'role': operation.role,
                    'updated_at': datetime.now(timezone.utc)
                }}
            )
            results["processed"] = result.modified_count
            
            # Log activity
            await log_activity(
                user_id="admin",
                action="bulk_role_change",
                resource_type="user",
                details=f"Changed role to {operation.role} for {result.modified_count} users"
            )
        
        elif operation.operation == "change_status":
            if not operation.status:
                raise HTTPException(status_code=400, detail="Status is required for change_status operation")
            
            result = await users_collection.update_many(
                {'id': {'$in': operation.user_ids}},
                {'$set': {
                    'status': operation.status,
                    'updated_at': datetime.now(timezone.utc)
                }}
            )
            results["processed"] = result.modified_count
            
            # Log activity
            await log_activity(
                user_id="admin",
                action="bulk_status_change",
                resource_type="user",
                details=f"Changed status to {operation.status} for {result.modified_count} users"
            )
        
        elif operation.operation == "add_tags":
            if not operation.tags:
                raise HTTPException(status_code=400, detail="Tags are required for add_tags operation")
            
            result = await users_collection.update_many(
                {'id': {'$in': operation.user_ids}},
                {'$addToSet': {'tags': {'$each': operation.tags}}}
            )
            results["processed"] = result.modified_count
        
        elif operation.operation == "export":
            # Get users data
            users = await users_collection.find({'id': {'$in': operation.user_ids}}).to_list(length=1000)
            for user in users:
                user.pop('_id', None)
                user.pop('password_hash', None)
            
            return {"success": True, "users": users, "count": len(users)}
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation.operation}")
        
        return results
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing bulk operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# NOTES ENDPOINTS
# ============================================================================

@router.get("/{user_id}/notes")
async def get_user_notes(user_id: str):
    """
    Get admin notes for a user
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        user = await users_collection.find_one({'id': user_id})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # For now, return admin_notes as a single note
        # In a more advanced system, you could have a separate notes collection
        notes = []
        if user.get('admin_notes'):
            notes.append({
                "id": "1",
                "content": user.get('admin_notes'),
                "created_at": user.get('updated_at'),
                "created_by": "admin"
            })
        
        return {"success": True, "notes": notes}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/notes")
async def add_user_note(user_id: str, note: dict):
    """
    Add an admin note for a user
    """
    try:
        if db_instance is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        users_collection = db_instance['users']
        
        note_content = note.get('content', '')
        if not note_content:
            raise HTTPException(status_code=400, detail="Note content is required")
        
        result = await users_collection.update_one(
            {'id': user_id},
            {'$set': {
                'admin_notes': note_content,
                'updated_at': datetime.now(timezone.utc)
            }}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"success": True, "message": "Note added successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding user note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def log_activity(user_id: str, action: str, resource_type: str = None, 
                       resource_id: str = None, details: str = None, ip_address: str = None):
    """
    Log user activity
    """
    try:
        if db_instance is None:
            return
        
        activity_logs_collection = db_instance['activity_logs']
        
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
        
        await activity_logs_collection.insert_one(activity.dict())
    
    except Exception as e:
        logger.error(f"Error logging activity: {str(e)}")
        # Don't raise exception, just log it
