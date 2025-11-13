"""Process LemonSqueezy webhook events."""
import logging
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class WebhookProcessor:
    """Process LemonSqueezy webhook events and update database."""
    
    @staticmethod
    async def process_webhook(payload: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Process an incoming webhook event.
        
        Args:
            payload: Webhook payload from LemonSqueezy
            db: Database connection
        """
        try:
            meta = payload.get("meta", {})
            event_name = meta.get("event_name")
            data = payload.get("data", {})
            
            logger.info(f"Processing webhook event: {event_name}")
            
            # Store webhook event for audit
            await db.webhook_events.insert_one({
                "event_type": event_name,
                "payload": payload,
                "processed_at": datetime.utcnow(),
                "created_at": datetime.utcnow()
            })
            
            # Route to appropriate handler
            if event_name == "order_created":
                await WebhookProcessor.handle_order_created(data, meta, db)
            
            elif event_name == "subscription_created":
                await WebhookProcessor.handle_subscription_created(data, meta, db)
            
            elif event_name == "subscription_updated":
                await WebhookProcessor.handle_subscription_updated(data, meta, db)
            
            elif event_name == "subscription_cancelled":
                await WebhookProcessor.handle_subscription_cancelled(data, meta, db)
            
            elif event_name == "subscription_payment_success":
                await WebhookProcessor.handle_subscription_payment_success(data, meta, db)
            
            elif event_name == "subscription_payment_failed":
                await WebhookProcessor.handle_subscription_payment_failed(data, meta, db)
            
            else:
                logger.warning(f"Unhandled webhook event: {event_name}")
        
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    async def handle_order_created(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle order_created event."""
        
        attributes = data.get("attributes", {})
        custom_data = meta.get("custom_data", {})
        
        order_data = {
            "lemon_squeezy_order_id": data.get("id"),
            "user_id": custom_data.get("user_id"),
            "user_email": attributes.get("user_email"),
            "total": attributes.get("total"),
            "subtotal": attributes.get("subtotal"),
            "tax": attributes.get("tax"),
            "currency": attributes.get("currency"),
            "status": attributes.get("status"),
            "created_at": datetime.utcnow(),
            "webhook_data": data
        }
        
        await db.orders.insert_one(order_data)
        logger.info(f"Created order record for order {data.get('id')}")
    
    @staticmethod
    async def handle_subscription_created(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle subscription_created event."""
        
        attributes = data.get("attributes", {})
        custom_data = meta.get("custom_data", {})
        user_id = custom_data.get("user_id")
        
        subscription_data = {
            "lemon_squeezy_subscription_id": data.get("id"),
            "user_id": user_id,
            "user_email": attributes.get("user_email"),
            "variant_id": str(attributes.get("variant_id")),
            "product_id": str(attributes.get("product_id")),
            "status": attributes.get("status"),
            "renews_at": attributes.get("renews_at"),
            "ends_at": attributes.get("ends_at"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "webhook_data": data
        }
        
        await db.lemon_squeezy_subscriptions.insert_one(subscription_data)
        logger.info(f"Created subscription record for subscription {data.get('id')}")
        
        # Update user's plan based on variant_id
        if user_id:
            variant_id = str(attributes.get("variant_id"))
            plan_id = None
            
            # Map variant_id to plan_id
            if variant_id == "1052931":
                plan_id = "starter"
            elif variant_id == "1052933":
                plan_id = "professional"
            
            if plan_id:
                # Get plan details
                plan = await db.plans.find_one({"name": plan_id.capitalize()})
                if plan:
                    # Update user subscription
                    await db.users.update_one(
                        {"user_id": user_id},
                        {
                            "$set": {
                                "plan_id": plan_id,
                                "subscription_status": "active",
                                "subscription_start_date": datetime.utcnow(),
                                "lemon_squeezy_subscription_id": data.get("id"),
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    logger.info(f"Updated user {user_id} to plan {plan_id}")
    
    @staticmethod
    async def handle_subscription_updated(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle subscription_updated event."""
        
        subscription_id = data.get("id")
        attributes = data.get("attributes", {})
        
        update_data = {
            "status": attributes.get("status"),
            "variant_id": str(attributes.get("variant_id")),
            "renews_at": attributes.get("renews_at"),
            "ends_at": attributes.get("ends_at"),
            "updated_at": datetime.utcnow(),
            "webhook_data": data
        }
        
        await db.lemon_squeezy_subscriptions.update_one(
            {"lemon_squeezy_subscription_id": subscription_id},
            {"$set": update_data}
        )
        logger.info(f"Updated subscription {subscription_id}")
    
    @staticmethod
    async def handle_subscription_cancelled(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle subscription_cancelled event."""
        
        subscription_id = data.get("id")
        attributes = data.get("attributes", {})
        
        # Update subscription status
        await db.lemon_squeezy_subscriptions.update_one(
            {"lemon_squeezy_subscription_id": subscription_id},
            {
                "$set": {
                    "status": "cancelled",
                    "ends_at": attributes.get("ends_at"),
                    "updated_at": datetime.utcnow(),
                    "webhook_data": data
                }
            }
        )
        
        # Find user and update their subscription status
        subscription = await db.lemon_squeezy_subscriptions.find_one(
            {"lemon_squeezy_subscription_id": subscription_id}
        )
        
        if subscription and subscription.get("user_id"):
            await db.users.update_one(
                {"user_id": subscription["user_id"]},
                {
                    "$set": {
                        "subscription_status": "cancelled",
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        logger.info(f"Cancelled subscription {subscription_id}")
    
    @staticmethod
    async def handle_subscription_payment_success(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle subscription_payment_success event."""
        
        attributes = data.get("attributes", {})
        subscription_id = attributes.get("subscription_id")
        
        # Update subscription
        await db.lemon_squeezy_subscriptions.update_one(
            {"lemon_squeezy_subscription_id": str(subscription_id)},
            {
                "$set": {
                    "status": "active",
                    "last_payment_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Payment successful for subscription {subscription_id}")
    
    @staticmethod
    async def handle_subscription_payment_failed(data: Dict[str, Any], meta: Dict[str, Any], db: AsyncIOMotorDatabase) -> None:
        """Handle subscription_payment_failed event."""
        
        attributes = data.get("attributes", {})
        subscription_id = attributes.get("subscription_id")
        
        # Update subscription
        await db.lemon_squeezy_subscriptions.update_one(
            {"lemon_squeezy_subscription_id": str(subscription_id)},
            {
                "$set": {
                    "payment_failed": True,
                    "last_payment_attempt": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.warning(f"Payment failed for subscription {subscription_id}")
