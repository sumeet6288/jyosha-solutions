from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_db
from auth import get_current_user
from models import User
from models_notifications import (
    NotificationResponse,
    NotificationPreferences,
    NotificationPreferencesUpdate,
    PushSubscription
)
from services.notification_service import NotificationService
from pydantic import BaseModel

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class PushSubscriptionRequest(BaseModel):
    endpoint: str
    keys: dict
    browser: Optional[str] = None


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's notifications"""
    notification_service = NotificationService(db)
    notifications = await notification_service.get_user_notifications(
        user_id=current_user.id,
        limit=limit,
        skip=skip,
        unread_only=unread_only
    )
    return notifications


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get count of unread notifications"""
    notification_service = NotificationService(db)
    count = await notification_service.get_unread_count(current_user.id)
    return {"count": count}


@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Mark a notification as read"""
    notification_service = NotificationService(db)
    success = await notification_service.mark_as_read(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}


@router.put("/read-all")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Mark all notifications as read"""
    notification_service = NotificationService(db)
    count = await notification_service.mark_all_as_read(current_user.id)
    return {"message": f"Marked {count} notifications as read"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete a notification"""
    notification_service = NotificationService(db)
    success = await notification_service.delete_notification(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification deleted"}


@router.get("/preferences")
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's notification preferences"""
    notification_service = NotificationService(db)
    prefs = await notification_service.get_user_preferences(current_user.id)
    
    # Return default preferences if not set
    if not prefs:
        return {
            "user_id": current_user.id,
            "email_enabled": True,
            "email_new_conversation": True,
            "email_high_priority": True,
            "email_performance_alert": True,
            "email_usage_warning": True,
            "email_digest": "daily",
            "email_digest_time": "09:00",
            "push_enabled": True,
            "push_new_conversation": True,
            "push_high_priority": True,
            "push_performance_alert": True,
            "push_usage_warning": True,
            "inapp_enabled": True,
            "inapp_sound": True,
            "admin_new_user_signup": True,
            "admin_webhook_events": True
        }
    
    return prefs


@router.put("/preferences")
async def update_notification_preferences(
    preferences: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update user's notification preferences"""
    notification_service = NotificationService(db)
    
    # Convert to dict and remove None values
    prefs_dict = {k: v for k, v in preferences.dict().items() if v is not None}
    
    updated_prefs = await notification_service.update_user_preferences(
        user_id=current_user.id,
        preferences=prefs_dict
    )
    
    return updated_prefs


@router.post("/push-subscription")
async def save_push_subscription(
    subscription: PushSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Save browser push notification subscription"""
    notification_service = NotificationService(db)
    
    result = await notification_service.save_push_subscription(
        user_id=current_user.id,
        endpoint=subscription.endpoint,
        keys=subscription.keys,
        browser=subscription.browser
    )
    
    return {"message": "Push subscription saved", "subscription": result}


@router.post("/test")
async def create_test_notification(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a test notification (for development)"""
    notification_service = NotificationService(db)
    
    notification = await notification_service.create_notification(
        user_id=current_user.id,
        notification_type="new_conversation",
        title="Test Notification",
        message="This is a test notification to verify the system is working.",
        priority="medium",
        action_url="/chatbots"
    )
    
    return {"message": "Test notification created", "notification": notification}
