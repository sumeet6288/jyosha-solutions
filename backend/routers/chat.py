from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime, timezone
from models import (
    ChatRequest, ChatResponse, Conversation, Message,
    ConversationResponse, MessageResponse
)
from services.chat_service import ChatService
from services.rag_service import RAGService
from services.plan_service import plan_service
from services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])
db_instance = None
chat_service = None
rag_service = None
notification_service = None


def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance, chat_service, rag_service, notification_service
    db_instance = db
    chat_service = ChatService()
    rag_service = RAGService()
    notification_service = NotificationService(db)


@router.post("", response_model=ChatResponse)
async def send_message(chat_request: ChatRequest):
    """Send a message to a chatbot (public endpoint)"""
    try:
        # Get chatbot
        chatbot = await db_instance.chatbots.find_one({"id": chat_request.chatbot_id})
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        if chatbot.get("status") != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chatbot is not active"
            )
        
        # Check message limit for chatbot owner
        user_id = chatbot.get("user_id")
        limit_check = await plan_service.check_limit(user_id, "messages")
        if limit_check["reached"]:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Monthly message limit reached. Please upgrade your plan to continue."
            )
        
        # Get or create conversation
        conversation = await db_instance.conversations.find_one({
            "chatbot_id": chat_request.chatbot_id,
            "session_id": chat_request.session_id
        })
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(
                chatbot_id=chat_request.chatbot_id,
                session_id=chat_request.session_id,
                user_name=chat_request.user_name,
                user_email=chat_request.user_email
            )
            await db_instance.conversations.insert_one(conversation.model_dump())
            
            # Send notification for new conversation
            try:
                await notification_service.create_notification(
                    user_id=user_id,
                    notification_type="new_conversation",
                    title="New Conversation Started",
                    message=f"A new conversation was started with your chatbot '{chatbot.get('name', 'Unknown')}'",
                    priority="medium",
                    metadata={
                        "chatbot_id": chat_request.chatbot_id,
                        "chatbot_name": chatbot.get("name"),
                        "conversation_id": conversation.id,
                        "user_name": chat_request.user_name,
                        "user_email": chat_request.user_email
                    },
                    action_url=f"/chatbot-builder/{chat_request.chatbot_id}?tab=analytics"
                )
            except Exception as notif_error:
                logger.error(f"Failed to create notification: {notif_error}")
        else:
            conversation = Conversation(**conversation)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            chatbot_id=chat_request.chatbot_id,
            role="user",
            content=chat_request.message
        )
        await db_instance.messages.insert_one(user_message.model_dump())
        
        # Get training data context
        sources = await db_instance.sources.find({
            "chatbot_id": chat_request.chatbot_id,
            "status": "processed"
        }).to_list(length=None)
        
        # Combine all source content
        context = "\n\n".join([source.get("content", "") for source in sources])
        
        # Generate AI response
        try:
            ai_response = await chat_service.generate_response(
                message=chat_request.message,
                session_id=chat_request.session_id,
                system_message=chatbot.get("instructions", "You are a helpful assistant."),
                model=chatbot.get("model", "gpt-4o-mini"),
                provider=chatbot.get("provider", "openai"),
                context=context if context else None
            )
        except Exception as e:
            logger.error(f"AI response error: {str(e)}")
            ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
        
        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            chatbot_id=chat_request.chatbot_id,
            role="assistant",
            content=ai_response
        )
        await db_instance.messages.insert_one(assistant_message.model_dump())
        
        # Update conversation
        await db_instance.conversations.update_one(
            {"id": conversation.id},
            {
                "$set": {"updated_at": datetime.now(timezone.utc)},
                "$inc": {"messages_count": 2}
            }
        )
        
        # Update chatbot stats
        await db_instance.chatbots.update_one(
            {"id": chat_request.chatbot_id},
            {
                "$inc": {
                    "messages_count": 2,
                    "conversations_count": 1 if not conversation else 0
                }
            }
        )
        
        # Increment message usage for chatbot owner
        await plan_service.increment_usage(user_id, "messages", amount=1)
        
        return ChatResponse(
            message=ai_response,
            conversation_id=conversation.id,
            session_id=chat_request.session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )


@router.get("/conversations/{chatbot_id}", response_model=List[ConversationResponse])
async def get_conversations(chatbot_id: str):
    """Get all conversations for a chatbot"""
    try:
        conversations = await db_instance.conversations.find(
            {"chatbot_id": chatbot_id}
        ).sort("updated_at", -1).to_list(length=100)
        
        return [ConversationResponse(**conv) for conv in conversations]
    except Exception as e:
        logger.error(f"Error fetching conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch conversations"
        )


@router.get("/messages/{conversation_id}", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    """Get all messages in a conversation"""
    try:
        messages = await db_instance.messages.find(
            {"conversation_id": conversation_id}
        ).sort("timestamp", 1).to_list(length=None)
        
        return [MessageResponse(**msg) for msg in messages]
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch messages"
        )
