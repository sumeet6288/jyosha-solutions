from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import httpx
import os
import hmac
import hashlib
import json
import logging
from datetime import datetime

from auth import get_current_user, get_mock_user
from models import User

router = APIRouter()
logger = logging.getLogger(__name__)
db_instance = None

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db

# Lemon Squeezy Configuration
LEMONSQUEEZY_API_KEY = os.getenv("LEMONSQUEEZY_API_KEY")
LEMONSQUEEZY_STORE_ID = os.getenv("LEMONSQUEEZY_STORE_ID")
LEMONSQUEEZY_SIGNING_SECRET = os.getenv("LEMONSQUEEZY_SIGNING_SECRET")
LEMONSQUEEZY_API_BASE = "https://api.lemonsqueezy.com/v1"

# Variant IDs for subscription plans
VARIANT_IDS = {
    "starter": "1052931",  # ₹150/month
    "professional": "1052933"  # ₹499 one-time
}

class CheckoutRequest(BaseModel):
    plan: str  # "starter" or "professional"
    user_id: str
    user_email: str

class CheckoutResponse(BaseModel):
    checkout_url: str
    message: str


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify Lemon Squeezy webhook signature using HMAC-SHA256"""
    if not LEMONSQUEEZY_SIGNING_SECRET:
        logger.error("LEMONSQUEEZY_SIGNING_SECRET not configured")
        return False
    
    try:
        # Compute expected signature
        expected_signature = hmac.new(
            LEMONSQUEEZY_SIGNING_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Timing-safe comparison
        return hmac.compare_digest(expected_signature, signature)
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {str(e)}")
        return False


async def process_webhook_event(event_data: Dict[str, Any]):
    """Process Lemon Squeezy webhook events"""
    try:
        global db_instance
        db = db_instance
        event_name = event_data.get("meta", {}).get("event_name")
        custom_data = event_data.get("meta", {}).get("custom_data", {})
        user_id = custom_data.get("user_id")
        
        logger.info(f"Processing webhook event: {event_name} for user: {user_id}")
        
        if not user_id:
            logger.warning("No user_id in webhook custom_data")
            return
        
        # Extract subscription/order data
        attributes = event_data.get("data", {}).get("attributes", {})
        subscription_id = event_data.get("data", {}).get("id")
        
        # Handle different event types
        if event_name == "subscription_created":
            # Map variant_id to plan_id
            variant_id = str(attributes.get("variant_id", ""))
            plan_id = "free"  # default
            if variant_id == VARIANT_IDS["starter"]:
                plan_id = "starter"
            elif variant_id == VARIANT_IDS["professional"]:
                plan_id = "professional"
            
            # New subscription created
            subscription_data = {
                "user_id": user_id,
                "plan_id": plan_id,  # Add plan_id for plan service compatibility
                "lemonsqueezy_subscription_id": subscription_id,
                "status": "active",  # Set as active when created
                "variant_id": variant_id,
                "product_id": attributes.get("product_id"),
                "plan_name": attributes.get("product_name", "Unknown"),
                "price": attributes.get("price", 0),
                "renews_at": attributes.get("renews_at"),
                "ends_at": attributes.get("ends_at"),
                "started_at": datetime.utcnow(),  # Add for plan service compatibility
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "auto_renew": True,  # Add for plan service compatibility
                "usage": {  # Initialize usage tracking
                    "chatbots_count": 0,
                    "messages_this_month": 0,
                    "file_uploads_count": 0,
                    "website_sources_count": 0,
                    "text_sources_count": 0,
                    "last_reset": datetime.utcnow()
                }
            }
            
            # Insert or update subscription
            await db.subscriptions.update_one(
                {"user_id": user_id},
                {"$set": subscription_data},
                upsert=True
            )
            logger.info(f"Subscription created for user {user_id} with plan {plan_id}")
            
        elif event_name == "subscription_updated":
            # Subscription updated
            update_data = {
                "status": attributes.get("status"),
                "renews_at": attributes.get("renews_at"),
                "ends_at": attributes.get("ends_at"),
                "updated_at": datetime.utcnow()
            }
            
            await db.subscriptions.update_one(
                {"lemonsqueezy_subscription_id": subscription_id},
                {"$set": update_data}
            )
            logger.info(f"Subscription updated: {subscription_id}")
            
        elif event_name == "subscription_payment_success":
            # Successful payment
            await db.subscriptions.update_one(
                {"lemonsqueezy_subscription_id": subscription_id},
                {"$set": {
                    "status": "active",
                    "last_payment_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }}
            )
            logger.info(f"Payment successful for subscription: {subscription_id}")
            
        elif event_name in ["subscription_cancelled", "subscription_expired"]:
            # Subscription cancelled or expired
            await db.subscriptions.update_one(
                {"lemonsqueezy_subscription_id": subscription_id},
                {"$set": {
                    "status": "cancelled" if event_name == "subscription_cancelled" else "expired",
                    "updated_at": datetime.utcnow()
                }}
            )
            logger.info(f"Subscription {event_name}: {subscription_id}")
            
        elif event_name == "order_created":
            # One-time purchase
            order_data = {
                "user_id": user_id,
                "lemonsqueezy_order_id": subscription_id,
                "status": attributes.get("status", "paid"),
                "total": attributes.get("total", 0),
                "product_name": attributes.get("first_order_item", {}).get("product_name", "Unknown"),
                "created_at": datetime.utcnow()
            }
            
            await db.orders.insert_one(order_data)
            logger.info(f"Order created for user {user_id}")
            
    except Exception as e:
        logger.error(f"Error processing webhook event: {str(e)}")
        raise


@router.post("/checkout/create", response_model=CheckoutResponse)
async def create_checkout(
    request: CheckoutRequest,
    current_user: User = Depends(get_mock_user)
):
    """Create a Lemon Squeezy checkout session"""
    try:
        # Get variant ID for the requested plan
        variant_id = VARIANT_IDS.get(request.plan.lower())
        if not variant_id:
            raise HTTPException(status_code=400, detail=f"Invalid plan: {request.plan}")
        
        # Prepare checkout data
        checkout_data = {
            "data": {
                "type": "checkouts",
                "attributes": {
                    "custom_price": None,
                    "product_options": {
                        "enabled_variants": [int(variant_id)],
                        "redirect_url": "https://install-preview-4.preview.emergentagent.com/subscription?success=true",
                        "receipt_button_text": "Go to Dashboard",
                        "receipt_link_url": "https://install-preview-4.preview.emergentagent.com/dashboard"
                    },
                    "checkout_data": {
                        "email": request.user_email,
                        "custom": {
                            "user_id": request.user_id
                        }
                    }
                },
                "relationships": {
                    "store": {
                        "data": {
                            "type": "stores",
                            "id": LEMONSQUEEZY_STORE_ID
                        }
                    },
                    "variant": {
                        "data": {
                            "type": "variants",
                            "id": variant_id
                        }
                    }
                }
            }
        }
        
        # Make API request to Lemon Squeezy
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LEMONSQUEEZY_API_BASE}/checkouts",
                json=checkout_data,
                headers={
                    "Accept": "application/vnd.api+json",
                    "Content-Type": "application/vnd.api+json",
                    "Authorization": f"Bearer {LEMONSQUEEZY_API_KEY}"
                },
                timeout=30.0
            )
            
            if response.status_code != 201:
                logger.error(f"Lemon Squeezy API error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to create checkout: {response.text}"
                )
            
            result = response.json()
            checkout_url = result.get("data", {}).get("attributes", {}).get("url")
            
            if not checkout_url:
                raise HTTPException(
                    status_code=500,
                    detail="Checkout URL not returned from Lemon Squeezy"
                )
            
            return CheckoutResponse(
                checkout_url=checkout_url,
                message="Checkout created successfully"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Handle Lemon Squeezy webhook events"""
    try:
        global db_instance
        db = db_instance
        # Get raw body for signature verification
        body = await request.body()
        
        # Get signature from header
        signature = request.headers.get("X-Signature")
        if not signature:
            logger.warning("Webhook received without signature")
            raise HTTPException(status_code=401, detail="Missing signature")
        
        # Verify webhook signature
        if not verify_webhook_signature(body, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse event data
        event_data = json.loads(body)
        
        # Store webhook event for audit
        webhook_log = {
            "event_name": event_data.get("meta", {}).get("event_name"),
            "event_id": event_data.get("meta", {}).get("event_id"),
            "data": event_data,
            "received_at": datetime.utcnow(),
            "processed": False
        }
        await db.webhook_logs.insert_one(webhook_log)
        
        # Process webhook in background
        background_tasks.add_task(process_webhook_event, event_data)
        
        # Return 200 immediately to acknowledge receipt
        return JSONResponse(
            status_code=200,
            content={"message": "Webhook received"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subscription/status")
async def get_subscription_status(
    current_user: User = Depends(get_mock_user)
):
    """Get current user's subscription status"""
    try:
        global db_instance
        db = db_instance
        user_id = current_user.id
        
        # Get subscription from database
        subscription = await db.subscriptions.find_one({"user_id": user_id})
        
        if not subscription:
            return {
                "has_subscription": False,
                "plan": "free",
                "status": "inactive"
            }
        
        return {
            "has_subscription": True,
            "plan": subscription.get("plan_name", "Unknown"),
            "status": subscription.get("status", "unknown"),
            "renews_at": subscription.get("renews_at"),
            "ends_at": subscription.get("ends_at"),
            "subscription_id": subscription.get("lemonsqueezy_subscription_id")
        }
        
    except Exception as e:
        logger.error(f"Error getting subscription status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plans")
async def get_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price": 150,
                "currency": "INR",
                "interval": "month",
                "variant_id": VARIANT_IDS["starter"],
                "features": [
                    "3 Chatbots",
                    "1,000 messages/month",
                    "File uploads",
                    "Website scraping",
                    "Basic analytics"
                ]
            },
            {
                "id": "professional",
                "name": "Professional",
                "price": 499,
                "currency": "INR",
                "interval": "one-time",
                "variant_id": VARIANT_IDS["professional"],
                "features": [
                    "Unlimited chatbots",
                    "10,000 messages/month",
                    "Priority support",
                    "Advanced analytics",
                    "Custom branding",
                    "API access"
                ]
            }
        ]
    }


@router.post("/subscription/sync")
async def sync_subscription(
    current_user: User = Depends(get_mock_user)
):
    """
    Manually sync subscription from Lemon Squeezy after successful payment.
    This is useful when webhooks are not configured yet.
    """
    try:
        if not LEMONSQUEEZY_API_KEY:
            raise HTTPException(status_code=500, detail="Lemon Squeezy API key not configured")
        
        global db_instance
        db = db_instance
        user_id = current_user.id
        
        # Fetch subscriptions from Lemon Squeezy API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{LEMONSQUEEZY_API_BASE}/subscriptions",
                headers={
                    "Accept": "application/vnd.api+json",
                    "Authorization": f"Bearer {LEMONSQUEEZY_API_KEY}"
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch subscriptions: {response.text}")
                # If no subscription found in Lemon Squeezy, return free plan
                return {
                    "success": True,
                    "plan": "free",
                    "message": "No active subscription found, using free plan"
                }
            
            result = response.json()
            subscriptions = result.get("data", [])
            
            # Find subscription for this user (by matching custom data or email)
            user_subscription = None
            for sub in subscriptions:
                attributes = sub.get("attributes", {})
                # Check if subscription is active
                if attributes.get("status") in ["active", "on_trial"]:
                    user_subscription = sub
                    break
            
            if not user_subscription:
                return {
                    "success": True,
                    "plan": "free",
                    "message": "No active subscription found"
                }
            
            # Extract subscription data
            sub_id = user_subscription.get("id")
            attributes = user_subscription.get("attributes", {})
            variant_id = str(attributes.get("variant_id", ""))
            
            # Map variant_id to plan_id
            plan_id = "free"
            if variant_id == VARIANT_IDS["starter"]:
                plan_id = "starter"
            elif variant_id == VARIANT_IDS["professional"]:
                plan_id = "professional"
            
            # Update subscription in database
            subscription_data = {
                "user_id": user_id,
                "plan_id": plan_id,
                "lemonsqueezy_subscription_id": sub_id,
                "status": "active",
                "variant_id": variant_id,
                "product_id": attributes.get("product_id"),
                "plan_name": attributes.get("product_name", plan_id.title()),
                "price": attributes.get("first_subscription_item", {}).get("price", 0),
                "renews_at": attributes.get("renews_at"),
                "ends_at": attributes.get("ends_at"),
                "started_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "auto_renew": True,
                "usage": {
                    "chatbots_count": 0,
                    "messages_this_month": 0,
                    "file_uploads_count": 0,
                    "website_sources_count": 0,
                    "text_sources_count": 0,
                    "last_reset": datetime.utcnow()
                }
            }
            
            await db.subscriptions.update_one(
                {"user_id": user_id},
                {"$set": subscription_data},
                upsert=True
            )
            
            logger.info(f"Subscription synced for user {user_id}: {plan_id}")
            
            return {
                "success": True,
                "plan": plan_id,
                "plan_name": subscription_data["plan_name"],
                "status": "active",
                "message": f"Successfully synced {plan_id} subscription"
            }
            
    except Exception as e:
        logger.error(f"Error syncing subscription: {str(e)}")
        # Don't raise error, just return free plan
        return {
            "success": False,
            "plan": "free",
            "message": f"Failed to sync subscription: {str(e)}"
        }

