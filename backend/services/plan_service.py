from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from datetime import datetime, timedelta
from models.plan import Plan, PlanLimits, UserSubscription, UsageStats
import os

class PlanService:
    """Service for managing plans and subscriptions"""
    
    def __init__(self):
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.chatbase
        self.plans_collection = self.db.plans
        self.subscriptions_collection = self.db.subscriptions
        self.users_collection = self.db.users
        
    async def initialize_plans(self):
        """Initialize default plans in database"""
        plans_data = [
            {
                "id": "free",
                "name": "Free",
                "price": 0.0,
                "description": "Perfect for trying out Chatbase",
                "limits": {
                    "max_chatbots": 1,
                    "max_messages_per_month": 100,
                    "max_file_uploads": 5,
                    "max_file_size_mb": 10,
                    "max_website_sources": 2,
                    "max_text_sources": 5,
                    "conversation_history_days": 7,
                    "allowed_ai_providers": ["openai"],
                    "api_access": False,
                    "custom_branding": False,
                    "analytics_level": "basic",
                    "support_level": "community"
                },
                "features": [
                    "1 chatbot",
                    "100 messages/month",
                    "Basic analytics",
                    "Community support",
                    "Standard AI models"
                ],
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "starter",
                "name": "Starter",
                "price": 150.0,
                "description": "For growing businesses",
                "limits": {
                    "max_chatbots": 5,
                    "max_messages_per_month": 10000,
                    "max_file_uploads": 20,
                    "max_file_size_mb": 50,
                    "max_website_sources": 10,
                    "max_text_sources": 20,
                    "conversation_history_days": 30,
                    "allowed_ai_providers": ["openai", "anthropic"],
                    "api_access": True,
                    "custom_branding": True,
                    "analytics_level": "advanced",
                    "support_level": "priority"
                },
                "features": [
                    "5 chatbots",
                    "10,000 messages/month",
                    "Advanced analytics",
                    "Priority support",
                    "Custom branding",
                    "API access",
                    "All AI models"
                ],
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "professional",
                "name": "Professional",
                "price": 499.0,
                "description": "For large teams & high volume",
                "limits": {
                    "max_chatbots": 25,
                    "max_messages_per_month": 100000,
                    "max_file_uploads": 100,
                    "max_file_size_mb": 100,
                    "max_website_sources": 50,
                    "max_text_sources": 100,
                    "conversation_history_days": 90,
                    "allowed_ai_providers": ["openai", "anthropic", "google"],
                    "api_access": True,
                    "custom_branding": True,
                    "analytics_level": "advanced",
                    "support_level": "24/7 priority"
                },
                "features": [
                    "25 chatbots",
                    "100,000 messages/month",
                    "Advanced analytics",
                    "24/7 priority support",
                    "Custom branding",
                    "Full API access",
                    "All AI models",
                    "Custom integrations",
                    "Dedicated account manager"
                ],
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price": -1.0,  # Custom pricing
                "description": "Tailored solutions for your needs",
                "limits": {
                    "max_chatbots": 999999,  # Unlimited
                    "max_messages_per_month": 999999999,  # Unlimited
                    "max_file_uploads": 999999,  # Unlimited
                    "max_file_size_mb": 100,
                    "max_website_sources": 999999,  # Unlimited
                    "max_text_sources": 999999,  # Unlimited
                    "conversation_history_days": 999999,  # Unlimited
                    "allowed_ai_providers": ["openai", "anthropic", "google"],
                    "api_access": True,
                    "custom_branding": True,
                    "analytics_level": "custom",
                    "support_level": "dedicated 24/7"
                },
                "features": [
                    "Unlimited chatbots",
                    "Unlimited messages",
                    "Custom analytics",
                    "Dedicated 24/7 support",
                    "White-label solution",
                    "Custom AI model training",
                    "On-premise deployment",
                    "SLA guarantee",
                    "Custom contracts",
                    "Enterprise security"
                ],
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        # Clear existing plans and insert new ones
        await self.plans_collection.delete_many({})
        await self.plans_collection.insert_many(plans_data)
        print("✅ Plans initialized successfully")
    
    async def get_all_plans(self) -> List[dict]:
        """Get all active plans"""
        plans = await self.plans_collection.find({"is_active": True}).to_list(length=100)
        return plans
    
    async def get_plan_by_id(self, plan_id: str) -> Optional[dict]:
        """Get plan by ID"""
        plan = await self.plans_collection.find_one({"id": plan_id})
        return plan
    
    async def get_user_subscription(self, user_id: str) -> Optional[dict]:
        """Get user's current subscription"""
        subscription = await self.subscriptions_collection.find_one({"user_id": user_id})
        if not subscription:
            # Create default free subscription
            await self.create_subscription(user_id, "free")
            subscription = await self.subscriptions_collection.find_one({"user_id": user_id})
        return subscription
    
    async def create_subscription(self, user_id: str, plan_id: str = "free") -> dict:
        """Create a new subscription for user"""
        subscription = {
            "user_id": user_id,
            "plan_id": plan_id,
            "status": "active",
            "started_at": datetime.utcnow(),
            "expires_at": None,  # Free plan never expires
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
        
        result = await self.subscriptions_collection.insert_one(subscription)
        subscription["_id"] = str(result.inserted_id)
        return subscription
    
    async def upgrade_plan(self, user_id: str, new_plan_id: str) -> dict:
        """Upgrade user to a new plan"""
        # Get current subscription
        subscription = await self.get_user_subscription(user_id)
        
        # Update plan
        update_data = {
            "plan_id": new_plan_id,
            "status": "active",
            "started_at": datetime.utcnow(),
            "expires_at": None  # For now, no expiration (manual management)
        }
        
        await self.subscriptions_collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        
        # Get updated subscription
        updated_subscription = await self.get_user_subscription(user_id)
        return updated_subscription
    
    async def check_limit(self, user_id: str, limit_type: str) -> dict:
        """Check if user has reached a specific limit"""
        subscription = await self.get_user_subscription(user_id)
        plan = await self.get_plan_by_id(subscription["plan_id"])
        
        usage = subscription.get("usage", {})
        limits = plan["limits"]
        
        limit_checks = {
            "chatbots": {
                "current": usage.get("chatbots_count", 0),
                "max": limits["max_chatbots"],
                "reached": usage.get("chatbots_count", 0) >= limits["max_chatbots"]
            },
            "messages": {
                "current": usage.get("messages_this_month", 0),
                "max": limits["max_messages_per_month"],
                "reached": usage.get("messages_this_month", 0) >= limits["max_messages_per_month"]
            },
            "file_uploads": {
                "current": usage.get("file_uploads_count", 0),
                "max": limits["max_file_uploads"],
                "reached": usage.get("file_uploads_count", 0) >= limits["max_file_uploads"]
            },
            "website_sources": {
                "current": usage.get("website_sources_count", 0),
                "max": limits["max_website_sources"],
                "reached": usage.get("website_sources_count", 0) >= limits["max_website_sources"]
            },
            "text_sources": {
                "current": usage.get("text_sources_count", 0),
                "max": limits["max_text_sources"],
                "reached": usage.get("text_sources_count", 0) >= limits["max_text_sources"]
            }
        }
        
        if limit_type in limit_checks:
            return limit_checks[limit_type]
        
        return {"error": "Invalid limit type"}
    
    async def increment_usage(self, user_id: str, usage_type: str, amount: int = 1):
        """Increment usage counter"""
        field_map = {
            "chatbots": "usage.chatbots_count",
            "messages": "usage.messages_this_month",
            "file_uploads": "usage.file_uploads_count",
            "website_sources": "usage.website_sources_count",
            "text_sources": "usage.text_sources_count"
        }
        
        if usage_type in field_map:
            await self.subscriptions_collection.update_one(
                {"user_id": user_id},
                {"$inc": {field_map[usage_type]: amount}}
            )
    
    async def decrement_usage(self, user_id: str, usage_type: str, amount: int = 1):
        """Decrement usage counter (when deleting resources)"""
        field_map = {
            "chatbots": "usage.chatbots_count",
            "file_uploads": "usage.file_uploads_count",
            "website_sources": "usage.website_sources_count",
            "text_sources": "usage.text_sources_count"
        }
        
        if usage_type in field_map:
            await self.subscriptions_collection.update_one(
                {"user_id": user_id},
                {"$inc": {field_map[usage_type]: -amount}}
            )
    
    async def reset_monthly_usage(self, user_id: str):
        """Reset monthly counters"""
        await self.subscriptions_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "usage.messages_this_month": 0,
                    "usage.last_reset": datetime.utcnow()
                }
            }
        )
    
    async def get_usage_stats(self, user_id: str) -> dict:
        """Get detailed usage statistics with limits"""
        subscription = await self.get_user_subscription(user_id)
        plan = await self.get_plan_by_id(subscription["plan_id"])
        
        usage = subscription.get("usage", {})
        limits = plan["limits"]
        
        return {
            "plan": {
                "id": plan["id"],
                "name": plan["name"],
                "price": plan["price"]
            },
            "usage": {
                "chatbots": {
                    "current": usage.get("chatbots_count", 0),
                    "limit": limits["max_chatbots"],
                    "percentage": round((usage.get("chatbots_count", 0) / limits["max_chatbots"]) * 100, 1) if limits["max_chatbots"] < 999999 else 0
                },
                "messages": {
                    "current": usage.get("messages_this_month", 0),
                    "limit": limits["max_messages_per_month"],
                    "percentage": round((usage.get("messages_this_month", 0) / limits["max_messages_per_month"]) * 100, 1) if limits["max_messages_per_month"] < 999999 else 0
                },
                "file_uploads": {
                    "current": usage.get("file_uploads_count", 0),
                    "limit": limits["max_file_uploads"],
                    "percentage": round((usage.get("file_uploads_count", 0) / limits["max_file_uploads"]) * 100, 1) if limits["max_file_uploads"] < 999999 else 0
                },
                "website_sources": {
                    "current": usage.get("website_sources_count", 0),
                    "limit": limits["max_website_sources"],
                    "percentage": round((usage.get("website_sources_count", 0) / limits["max_website_sources"]) * 100, 1) if limits["max_website_sources"] < 999999 else 0
                },
                "text_sources": {
                    "current": usage.get("text_sources_count", 0),
                    "limit": limits["max_text_sources"],
                    "percentage": round((usage.get("text_sources_count", 0) / limits["max_text_sources"]) * 100, 1) if limits["max_text_sources"] < 999999 else 0
                }
            },
            "last_reset": usage.get("last_reset", datetime.utcnow())
        }

# Global instance
plan_service = PlanService()
