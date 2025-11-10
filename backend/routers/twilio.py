"""
Twilio SMS Integration Router
Handles incoming SMS and sending SMS via Twilio
"""
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends, Form
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
import logging
from typing import Optional

from services.twilio_service import TwilioService
from services.chat_service import ChatService
from services.rag_service import RAGService
from auth import get_current_user

router = APIRouter(prefix="/twilio", tags=["twilio"])

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'chatbase_db')
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

logger = logging.getLogger(__name__)


async def process_sms_message(chatbot_id: str, from_number: str, message_body: str):
    """
    Process incoming SMS message and generate response
    
    Args:
        chatbot_id: ID of the chatbot
        from_number: Sender's phone number
        message_body: Content of the SMS
    """
    try:
        # Get chatbot
        chatbot = await db.chatbots.find_one({"id": chatbot_id})
        if not chatbot:
            logger.error(f"Chatbot {chatbot_id} not found")
            return
        
        # Get Twilio integration
        integration = await db.integrations.find_one({
            "chatbot_id": chatbot_id,
            "integration_type": "twilio",
            "enabled": True
        })
        
        if not integration:
            logger.error(f"Twilio integration not found or not enabled for chatbot {chatbot_id}")
            return
        
        # Get credentials
        credentials = integration.get("credentials", {})
        account_sid = credentials.get("account_sid")
        auth_token = credentials.get("auth_token")
        phone_number = credentials.get("phone_number")
        
        if not all([account_sid, auth_token, phone_number]):
            logger.error(f"Missing Twilio credentials for chatbot {chatbot_id}")
            return
        
        # Initialize services
        twilio_service = TwilioService(account_sid, auth_token, phone_number)
        chat_service = ChatService()
        
        # Create session ID from phone number
        session_id = f"twilio_{from_number.replace('+', '')}"
        
        # Get or create conversation
        conversation = await db.conversations.find_one({
            "chatbot_id": chatbot_id,
            "session_id": session_id,
            "platform": "twilio"
        })
        
        if not conversation:
            conversation = {
                "id": f"conv_{session_id}_{int(datetime.now(timezone.utc).timestamp())}",
                "chatbot_id": chatbot_id,
                "session_id": session_id,
                "platform": "twilio",
                "user_phone": from_number,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "message_count": 0
            }
            await db.conversations.insert_one(conversation)
        
        # Save user message
        user_message = {
            "id": f"msg_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "conversation_id": conversation["id"],
            "chatbot_id": chatbot_id,
            "session_id": session_id,
            "role": "user",
            "content": message_body,
            "platform": "twilio",
            "timestamp": datetime.now(timezone.utc)
        }
        await db.messages.insert_one(user_message)
        
        # Check if RAG is enabled
        use_rag = chatbot.get("use_rag", False)
        context = ""
        
        if use_rag:
            try:
                rag_service = RAGService(chatbot_id)
                context = await rag_service.get_relevant_context(message_body)
            except Exception as e:
                logger.warning(f"RAG retrieval failed: {str(e)}")
        
        # Generate AI response
        ai_response = await chat_service.generate_response(
            chatbot=chatbot,
            user_message=message_body,
            context=context,
            session_id=session_id
        )
        
        # Save AI response
        bot_message = {
            "id": f"msg_{int(datetime.now(timezone.utc).timestamp() * 1000) + 1}",
            "conversation_id": conversation["id"],
            "chatbot_id": chatbot_id,
            "session_id": session_id,
            "role": "assistant",
            "content": ai_response,
            "platform": "twilio",
            "timestamp": datetime.now(timezone.utc)
        }
        await db.messages.insert_one(bot_message)
        
        # Update conversation
        await db.conversations.update_one(
            {"id": conversation["id"]},
            {
                "$set": {"updated_at": datetime.now(timezone.utc)},
                "$inc": {"message_count": 2}
            }
        )
        
        # Send SMS response
        send_result = await twilio_service.send_sms(from_number, ai_response)
        
        if send_result["success"]:
            logger.info(f"SMS response sent to {from_number}")
            
            # Update integration last_used
            await db.integrations.update_one(
                {"id": integration["id"]},
                {"$set": {"last_used": datetime.now(timezone.utc)}}
            )
        else:
            logger.error(f"Failed to send SMS: {send_result.get('error')}")
        
    except Exception as e:
        logger.error(f"Error processing SMS: {str(e)}")


@router.post("/webhook/{chatbot_id}")
async def twilio_webhook(
    chatbot_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: Optional[str] = Form(None)
):
    """
    Twilio SMS webhook endpoint
    Receives incoming SMS messages from Twilio
    
    Args:
        chatbot_id: ID of the chatbot
        From: Sender's phone number
        Body: SMS message content
        MessageSid: Twilio message ID
    """
    try:
        logger.info(f"Twilio SMS received for chatbot {chatbot_id}")
        logger.info(f"From: {From}, Body: {Body}, MessageSid: {MessageSid}")
        
        # Process message in background
        background_tasks.add_task(process_sms_message, chatbot_id, From, Body)
        
        # Return empty response (Twilio expects 200 OK)
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Error in Twilio webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{chatbot_id}/send-sms")
async def send_sms(
    chatbot_id: str,
    to_number: str,
    message: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Send SMS via Twilio
    
    Args:
        chatbot_id: ID of the chatbot
        to_number: Recipient phone number (E.164 format)
        message: Message text
    """
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user.id})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get Twilio integration
        integration = await db.integrations.find_one({
            "chatbot_id": chatbot_id,
            "integration_type": "twilio"
        })
        
        if not integration:
            raise HTTPException(status_code=404, detail="Twilio integration not found")
        
        if not integration.get("enabled"):
            raise HTTPException(status_code=400, detail="Twilio integration is not enabled")
        
        # Get credentials
        credentials = integration.get("credentials", {})
        account_sid = credentials.get("account_sid")
        auth_token = credentials.get("auth_token")
        phone_number = credentials.get("phone_number")
        
        if not all([account_sid, auth_token, phone_number]):
            raise HTTPException(status_code=400, detail="Missing Twilio credentials")
        
        # Initialize Twilio service
        twilio_service = TwilioService(account_sid, auth_token, phone_number)
        
        # Send SMS
        result = await twilio_service.send_sms(to_number, message)
        
        if result["success"]:
            # Update integration last_used
            await db.integrations.update_one(
                {"id": integration["id"]},
                {"$set": {"last_used": datetime.now(timezone.utc)}}
            )
            
            return {
                "success": True,
                "message": "SMS sent successfully",
                "message_sid": result.get("message_sid")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chatbot_id}/setup-instructions")
async def get_setup_instructions(
    chatbot_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get Twilio setup instructions
    """
    try:
        # Verify chatbot belongs to user
        chatbot = await db.chatbots.find_one({"id": chatbot_id, "user_id": current_user.id})
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Get backend URL from environment
        backend_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        webhook_url = f"{backend_url}/api/twilio/webhook/{chatbot_id}"
        
        instructions = {
            "title": "Twilio SMS Integration Setup",
            "steps": [
                {
                    "step": 1,
                    "title": "Get Twilio Credentials",
                    "description": "Sign up for Twilio at https://www.twilio.com and get your Account SID and Auth Token from the console"
                },
                {
                    "step": 2,
                    "title": "Get a Phone Number",
                    "description": "Purchase a phone number from Twilio that supports SMS"
                },
                {
                    "step": 3,
                    "title": "Configure Webhook",
                    "description": f"In your Twilio phone number settings, set the SMS webhook URL to: {webhook_url}",
                    "webhook_url": webhook_url
                },
                {
                    "step": 4,
                    "title": "Enter Credentials",
                    "description": "Enter your Account SID, Auth Token, and Phone Number in the integration settings"
                },
                {
                    "step": 5,
                    "title": "Test Connection",
                    "description": "Click 'Test Connection' to verify your credentials"
                }
            ],
            "webhook_url": webhook_url,
            "notes": [
                "Phone number must be in E.164 format (e.g., +1234567890)",
                "Ensure your Twilio account has sufficient credits",
                "SMS webhook should use HTTP POST method"
            ]
        }
        
        return instructions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting setup instructions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
