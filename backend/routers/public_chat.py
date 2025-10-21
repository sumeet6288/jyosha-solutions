from fastapi import APIRouter, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime, timezone
from models import (
    PublicChatbotInfo, PublicChatRequest, ChatResponse,
    EmbedConfig, EmbedCodeResponse, ConversationResponse, MessageResponse
)
from services.chat_service import ChatService
import json

router = APIRouter(prefix="/public", tags=["public-chat"])
db_instance = None

def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db

@router.get("/chatbot/{chatbot_id}", response_model=PublicChatbotInfo)
async def get_public_chatbot(chatbot_id: str):
    """Get public chatbot information (no authentication required)"""
    chatbot = await db_instance.chatbots.find_one({"id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Check if public access is enabled
    if not chatbot.get("public_access", False):
        raise HTTPException(status_code=403, detail="This chatbot is not publicly accessible")
    
    return PublicChatbotInfo(
        id=chatbot["id"],
        name=chatbot["name"],
        welcome_message=chatbot.get("welcome_message", "Hello! How can I help you today?"),
        primary_color=chatbot.get("primary_color", "#7c3aed"),
        secondary_color=chatbot.get("secondary_color", "#a78bfa"),
        logo_url=chatbot.get("logo_url"),
        avatar_url=chatbot.get("avatar_url"),
        widget_theme=chatbot.get("widget_theme", "light")
    )


@router.post("/chat/{chatbot_id}", response_model=ChatResponse)
async def public_chat(chatbot_id: str, request: PublicChatRequest):
    """Send a message to a public chatbot (no authentication required)"""
    # Get chatbot
    chatbot = await db_instance.chatbots.find_one({"id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    if not chatbot.get("public_access", False):
        raise HTTPException(status_code=403, detail="This chatbot is not publicly accessible")
    
    # Find or create conversation
    conversation = await db_instance.conversations.find_one({
        "chatbot_id": chatbot_id,
        "session_id": request.session_id
    })
    
    if not conversation:
        conversation = {
            "id": str(__import__("uuid").uuid4()),
            "chatbot_id": chatbot_id,
            "session_id": request.session_id,
            "user_name": request.user_name,
            "user_email": request.user_email,
            "status": "active",
            "messages_count": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        await db_instance.conversations.insert_one(conversation)
    
    conversation_id = conversation["id"]
    
    # Save user message
    user_message = {
        "id": str(__import__("uuid").uuid4()),
        "conversation_id": conversation_id,
        "chatbot_id": chatbot_id,
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now(timezone.utc)
    }
    db.messages.insert_one(user_message)
    
    # Get AI response
    chat_service = ChatService()
    ai_response = await chat_service.get_chat_response(
        chatbot_id=chatbot_id,
        message=request.message,
        conversation_id=conversation_id
    )
    
    # Save AI message
    ai_message = {
        "id": str(__import__("uuid").uuid4()),
        "conversation_id": conversation_id,
        "chatbot_id": chatbot_id,
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now(timezone.utc)
    }
    db.messages.insert_one(ai_message)
    
    # Update conversation counts
    db.conversations.update_one(
        {"id": conversation_id},
        {
            "$inc": {"messages_count": 2},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
    )
    
    # Update chatbot counts
    db.chatbots.update_one(
        {"id": chatbot_id},
        {
            "$inc": {"messages_count": 2},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
    )
    
    # Send webhook notification if enabled
    if chatbot.get("webhook_enabled") and chatbot.get("webhook_url"):
        await send_webhook_notification(
            webhook_url=chatbot["webhook_url"],
            chatbot_id=chatbot_id,
            conversation_id=conversation_id,
            user_message=request.message,
            ai_response=ai_response
        )
    
    return ChatResponse(
        message=ai_response,
        conversation_id=conversation_id,
        session_id=request.session_id
    )


@router.get("/embed/{chatbot_id}")
async def get_embed_code(chatbot_id: str, theme: str = "light", position: str = "bottom-right"):
    """Get embed code for integrating chatbot into websites"""
    db = get_database()
    
    chatbot = db.chatbots.find_one({"id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Generate embed code
    embed_html = f"""
<!-- Chatbot Embed Code -->
<div id="chatbot-widget-{chatbot_id}"></div>
<script>
  (function() {{
    var chatbotConfig = {{
      chatbotId: '{chatbot_id}',
      theme: '{theme}',
      position: '{position}',
      apiUrl: '{chatbot.get("webhook_url", "https://api.example.com")}'
    }};
    
    var script = document.createElement('script');
    script.src = 'https://cdn.example.com/chatbot-widget.js';
    script.async = true;
    script.onload = function() {{
      if (window.ChatbotWidget) {{
        window.ChatbotWidget.init(chatbotConfig);
      }}
    }};
    document.head.appendChild(script);
  }})();
</script>
"""
    
    return EmbedCodeResponse(
        html_code=embed_html,
        script_url="https://cdn.example.com/chatbot-widget.js"
    )


@router.get("/conversations/{chatbot_id}/export")
async def export_conversations(chatbot_id: str, format: str = "json"):
    """Export all conversations for a chatbot"""
    db = get_database()
    
    chatbot = db.chatbots.find_one({"id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Get all conversations
    conversations = list(db.conversations.find({"chatbot_id": chatbot_id}))
    
    # Get messages for each conversation
    export_data = []
    for conv in conversations:
        messages = list(db.messages.find({"conversation_id": conv["id"]}).sort("timestamp", 1))
        
        conv_data = {
            "conversation_id": conv["id"],
            "session_id": conv["session_id"],
            "user_name": conv.get("user_name"),
            "user_email": conv.get("user_email"),
            "status": conv["status"],
            "created_at": conv["created_at"].isoformat(),
            "messages": [
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"].isoformat()
                }
                for msg in messages
            ]
        }
        export_data.append(conv_data)
    
    if format == "csv":
        # Convert to CSV format
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Conversation ID", "Session ID", "User Name", "User Email", "Status", "Created At", "Role", "Message", "Timestamp"])
        
        for conv in export_data:
            for msg in conv["messages"]:
                writer.writerow([
                    conv["conversation_id"],
                    conv["session_id"],
                    conv["user_name"] or "",
                    conv["user_email"] or "",
                    conv["status"],
                    conv["created_at"],
                    msg["role"],
                    msg["content"],
                    msg["timestamp"]
                ])
        
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=chatbot_{chatbot_id}_export.csv"}
        )
    else:
        # Return JSON
        return Response(
            content=json.dumps(export_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=chatbot_{chatbot_id}_export.json"}
        )


async def send_webhook_notification(webhook_url: str, chatbot_id: str, conversation_id: str, 
                                   user_message: str, ai_response: str):
    """Send webhook notification for new conversation"""
    import httpx
    
    payload = {
        "event": "new_message",
        "chatbot_id": chatbot_id,
        "conversation_id": conversation_id,
        "user_message": user_message,
        "ai_response": ai_response,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(webhook_url, json=payload, timeout=5.0)
    except Exception as e:
        # Log error but don't fail the request
        print(f"Webhook notification failed: {e}")
