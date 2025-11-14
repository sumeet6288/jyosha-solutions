"""LemonSqueezy checkout and subscription management routes."""
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from services.lemonsqueezy_service import LemonSqueezyService
from services.webhook_processor import WebhookProcessor
from utils.signature_verification import verify_lemon_squeezy_signature

logger = logging.getLogger(__name__)
router = APIRouter(tags=["lemonsqueezy"])

# Database instance
_db = None

def init_router(db):
    """Initialize router with database instance."""
    global _db
    _db = db


class CreateCheckoutRequest(BaseModel):
    """Request model for creating a checkout."""
    plan_id: str  # starter, professional, etc.
    user_id: str
    user_email: str
    user_name: Optional[str] = None


class SubscriptionActionRequest(BaseModel):
    """Request model for subscription actions."""
    subscription_id: str


class UpdateSubscriptionRequest(BaseModel):
    """Request model for updating subscription."""
    subscription_id: str
    new_plan_id: Optional[str] = None
    pause: Optional[bool] = None


@router.post("/create-checkout")
async def create_checkout(request: CreateCheckoutRequest):
    """
    Create a LemonSqueezy checkout for a subscription plan.
    
    Returns the checkout URL that the user should be redirected to.
    """
    try:
        # Get payment settings from database
        payment_settings = await _db.payment_settings.find_one({})
        
        if not payment_settings or not payment_settings.get('lemonsqueezy', {}).get('enabled'):
            raise HTTPException(
                status_code=400,
                detail="LemonSqueezy payment gateway is not enabled. Please contact administrator."
            )
        
        # Get variant ID from payment settings
        plans_mapping = payment_settings.get('lemonsqueezy', {}).get('plans', {})
        variant_id = plans_mapping.get(request.plan_id.lower())
        
        if not variant_id:
            raise HTTPException(
                status_code=400,
                detail=f"Plan {request.plan_id} does not have a LemonSqueezy variant ID configured in Payment Gateway settings. Please contact administrator."
            )
        
        # Create checkout with custom data
        service = LemonSqueezyService()
        
        checkout_data = {
            "email": request.user_email,
            "name": request.user_name or request.user_email.split('@')[0],
            "custom": {
                "user_id": request.user_id,
                "plan_id": request.plan_id
            }
        }
        
        result = await service.create_checkout(
            variant_id=variant_id,
            checkout_data=checkout_data
        )
        
        checkout_url = result.get("data", {}).get("attributes", {}).get("url")
        
        if not checkout_url:
            raise HTTPException(status_code=500, detail="Failed to get checkout URL")
        
        return {
            "success": True,
            "checkout_url": checkout_url,
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Handle incoming LemonSqueezy webhook events.
    
    This endpoint receives webhook events from LemonSqueezy, verifies
    the signature, and processes the event asynchronously.
    """
    
    # Get raw body for signature verification
    body = await request.body()
    
    # Get signature from header
    signature = request.headers.get("X-Signature")
    
    if not signature:
        raise HTTPException(status_code=401, detail="Missing X-Signature header")
    
    # Verify signature
    if not verify_lemon_squeezy_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse payload
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    
    # Process webhook in background
    background_tasks.add_task(WebhookProcessor.process_webhook, payload, _db)
    
    # Return 200 OK immediately
    return {"success": True}


@router.get("/subscription/{user_id}")
async def get_user_subscription(user_id: str):
    """
    Get the current subscription for a user.
    """
    try:
        subscription = await _db.lemon_squeezy_subscriptions.find_one(
            {"user_id": user_id, "status": {"$in": ["active", "on_trial", "past_due"]}}
        )
        
        if not subscription:
            return {
                "success": True,
                "subscription": None,
                "has_subscription": False
            }
        
        # Get plan details
        variant_id = subscription.get("variant_id")
        plan_name = "Unknown"
        
        if variant_id == "1052931":
            plan_name = "Starter"
        elif variant_id == "1052933":
            plan_name = "Professional"
        
        return {
            "success": True,
            "has_subscription": True,
            "subscription": {
                "id": subscription.get("lemon_squeezy_subscription_id"),
                "plan_name": plan_name,
                "status": subscription.get("status"),
                "renews_at": subscription.get("renews_at"),
                "ends_at": subscription.get("ends_at"),
                "variant_id": variant_id
            }
        }
    
    except Exception as e:
        logger.error(f"Error fetching subscription: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscription/cancel")
async def cancel_subscription(
    request: SubscriptionActionRequest
):
    """
    Cancel a subscription.
    """
    try:
        service = LemonSqueezyService()
        result = await service.cancel_subscription(request.subscription_id)
        
        return {
            "success": True,
            "message": "Subscription cancelled successfully",
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Error cancelling subscription: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscription/update")
async def update_subscription(
    request: UpdateSubscriptionRequest
):
    """
    Update a subscription (upgrade/downgrade or pause/resume).
    """
    try:
        service = LemonSqueezyService()
        
        # Get new variant ID if upgrading/downgrading
        new_variant_id = None
        if request.new_plan_id:
            plan = await _db.plans.find_one({"name": request.new_plan_id.capitalize()})
            if not plan:
                raise HTTPException(status_code=404, detail="Plan not found")
            
            new_variant_id = plan.get("lemon_squeezy_variant_id")
            if not new_variant_id:
                raise HTTPException(
                    status_code=400,
                    detail="Plan does not have a LemonSqueezy variant ID"
                )
        
        result = await service.update_subscription(
            subscription_id=request.subscription_id,
            variant_id=new_variant_id,
            pause=request.pause
        )
        
        return {
            "success": True,
            "message": "Subscription updated successfully",
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating subscription: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
