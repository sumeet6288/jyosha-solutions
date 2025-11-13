"""Webhook signature verification for LemonSqueezy."""
import hmac
import hashlib
import os
import logging

logger = logging.getLogger(__name__)


def verify_lemon_squeezy_signature(body: bytes, signature: str) -> bool:
    """
    Verify that a webhook request came from Lemon Squeezy by checking
    the X-Signature header against a calculated HMAC-SHA256 hash.
    
    Args:
        body: The raw request body as bytes
        signature: The value of the X-Signature header
    
    Returns:
        True if the signature is valid, False otherwise
    """
    signing_secret = os.environ.get('LEMON_SQUEEZY_WEBHOOK_SECRET', '')
    
    if not signing_secret:
        logger.error("LEMON_SQUEEZY_WEBHOOK_SECRET not configured")
        return False
    
    # Calculate the expected signature
    expected_signature = hmac.new(
        signing_secret.encode('utf-8'),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Use constant-time comparison to prevent timing attacks
    is_valid = hmac.compare_digest(expected_signature, signature)
    
    if not is_valid:
        logger.warning("Invalid webhook signature received")
    
    return is_valid
