"""
Twilio SMS Service
Handles SMS messaging via Twilio API
"""
import os
import logging
from typing import Optional, Dict, Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class TwilioService:
    """Service for handling Twilio SMS operations"""
    
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        """
        Initialize Twilio service
        
        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            phone_number: Twilio phone number (e.g., +1234567890)
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.client = None
        
        if account_sid and auth_token:
            try:
                self.client = Client(account_sid, auth_token)
                logger.info(f"Twilio client initialized for phone: {phone_number}")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {str(e)}")
    
    async def send_sms(self, to_number: str, message: str) -> Dict[str, Any]:
        """
        Send SMS message
        
        Args:
            to_number: Recipient phone number (E.164 format, e.g., +1234567890)
            message: Message text to send
            
        Returns:
            Dict with success status and message details or error
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "Twilio client not initialized"
                }
            
            # Send SMS
            sms = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            logger.info(f"SMS sent successfully. SID: {sms.sid}")
            
            return {
                "success": True,
                "message_sid": sms.sid,
                "status": sms.status,
                "to": to_number,
                "from": self.phone_number
            }
            
        except TwilioRestException as e:
            logger.error(f"Twilio API error: {e.msg}")
            return {
                "success": False,
                "error": f"Twilio error: {e.msg}",
                "error_code": e.code
            }
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def validate_credentials(self) -> Dict[str, Any]:
        """
        Validate Twilio credentials by fetching account details
        
        Returns:
            Dict with success status and account info or error
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "message": "Twilio client not initialized"
                }
            
            # Fetch account details to validate credentials
            account = self.client.api.accounts(self.account_sid).fetch()
            
            logger.info(f"Twilio credentials validated for account: {account.friendly_name}")
            
            return {
                "success": True,
                "message": f"Connected to Twilio account: {account.friendly_name}",
                "account_name": account.friendly_name,
                "status": account.status
            }
            
        except TwilioRestException as e:
            logger.error(f"Twilio validation error: {e.msg}")
            return {
                "success": False,
                "message": f"Invalid credentials: {e.msg}"
            }
        except Exception as e:
            logger.error(f"Error validating credentials: {str(e)}")
            return {
                "success": False,
                "message": f"Validation error: {str(e)}"
            }
    
    async def get_phone_number_info(self) -> Dict[str, Any]:
        """
        Get information about the configured phone number
        
        Returns:
            Dict with phone number details
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "Twilio client not initialized"
                }
            
            # Get phone numbers on the account
            incoming_phone_numbers = self.client.incoming_phone_numbers.list(
                phone_number=self.phone_number
            )
            
            if incoming_phone_numbers:
                number = incoming_phone_numbers[0]
                return {
                    "success": True,
                    "phone_number": number.phone_number,
                    "friendly_name": number.friendly_name,
                    "capabilities": {
                        "sms": number.capabilities.get('sms', False),
                        "mms": number.capabilities.get('mms', False),
                        "voice": number.capabilities.get('voice', False)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Phone number {self.phone_number} not found in account"
                }
                
        except Exception as e:
            logger.error(f"Error getting phone number info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
