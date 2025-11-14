"""LemonSqueezy API service for checkout and subscription management."""
import httpx
import logging
from typing import Optional, Dict, Any
import os
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'chatbase_db')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]


class LemonSqueezyService:
    """Service for interacting with Lemon Squeezy API."""
    
    def __init__(self):
        self.base_url = "https://api.lemonsqueezy.com/v1"
        self.api_key = None
        self.store_id = None
    
    async def _load_settings(self):
        """Load payment settings from database."""
        if self.api_key and self.store_id:
            return  # Already loaded
        
        try:
            settings = await db.payment_settings.find_one({})
            if settings and settings.get('lemonsqueezy', {}).get('enabled'):
                self.api_key = settings['lemonsqueezy'].get('api_key')
                self.store_id = settings['lemonsqueezy'].get('store_id')
                logger.info("Payment settings loaded from database")
            else:
                # Fallback to environment variables
                self.api_key = os.environ.get('LEMON_SQUEEZY_API_KEY')
                self.store_id = os.environ.get('LEMON_SQUEEZY_STORE_ID', '234448')
                logger.warning("Using fallback environment variables for LemonSqueezy")
        except Exception as e:
            logger.error(f"Error loading payment settings: {e}")
            # Fallback to environment variables
            self.api_key = os.environ.get('LEMON_SQUEEZY_API_KEY')
            self.store_id = os.environ.get('LEMON_SQUEEZY_STORE_ID', '234448')
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers required for all Lemon Squeezy API requests."""
        return {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def create_checkout(
        self,
        variant_id: str,
        checkout_data: Optional[Dict[str, Any]] = None,
        custom_price: Optional[int] = None,
        redirect_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a checkout link for a product variant.
        
        Args:
            variant_id: LemonSqueezy variant ID
            checkout_data: Data to prefill in checkout (email, name, custom data)
            custom_price: Optional custom price in cents
            redirect_url: URL to redirect after successful checkout
        
        Returns:
            Checkout object with URL
        """
        # Load settings from database
        await self._load_settings()
        
        if not self.api_key or not self.store_id:
            raise ValueError("LemonSqueezy is not configured. Please configure it in Admin Panel > Payment Gateway Settings.")
        
        # Build attributes with only non-None values
        attributes = {}
        
        if custom_price is not None:
            attributes["custom_price"] = custom_price
        
        if redirect_url:
            attributes["product_options"] = {
                "redirect_url": redirect_url
            }
        
        if checkout_data:
            attributes["checkout_data"] = checkout_data
        
        payload = {
            "data": {
                "type": "checkouts",
                "attributes": attributes,
                "relationships": {
                    "store": {
                        "data": {
                            "type": "stores",
                            "id": str(self.store_id)
                        }
                    },
                    "variant": {
                        "data": {
                            "type": "variants",
                            "id": str(variant_id)
                        }
                    }
                }
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/checkouts",
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Created checkout for variant {variant_id}")
                return result
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to create checkout: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error creating checkout: {str(e)}")
            raise
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Retrieve subscription details.
        
        Args:
            subscription_id: LemonSqueezy subscription ID
        
        Returns:
            Subscription object
        """
        await self._load_settings()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching subscription {subscription_id}: {str(e)}")
            raise
    
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription.
        
        Args:
            subscription_id: LemonSqueezy subscription ID
        
        Returns:
            Updated subscription object
        """
        await self._load_settings()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                logger.info(f"Cancelled subscription {subscription_id}")
                return response.json()
        except Exception as e:
            logger.error(f"Error cancelling subscription {subscription_id}: {str(e)}")
            raise
    
    async def update_subscription(
        self,
        subscription_id: str,
        variant_id: Optional[str] = None,
        pause: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a subscription (upgrade/downgrade or pause/resume).
        
        Args:
            subscription_id: LemonSqueezy subscription ID
            variant_id: New variant ID for upgrade/downgrade
            pause: True to pause, False to resume, None to not change
        
        Returns:
            Updated subscription object
        """
        await self._load_settings()
        
        attributes = {}
        if variant_id:
            attributes["variant_id"] = int(variant_id)
        
        if pause is not None:
            attributes["pause"] = {"mode": "void"} if pause else None
        
        payload = {
            "data": {
                "type": "subscriptions",
                "id": str(subscription_id),
                "attributes": attributes
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.patch(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                logger.info(f"Updated subscription {subscription_id}")
                return response.json()
        except Exception as e:
            logger.error(f"Error updating subscription {subscription_id}: {str(e)}")
            raise
