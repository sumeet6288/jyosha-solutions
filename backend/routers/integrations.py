from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import qrcode
import io
import base64
from datetime import datetime
import secrets

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

# In-memory storage for demo (in production, use MongoDB)
whatsapp_sessions = {}

class WhatsAppConnect(BaseModel):
    chatbot_id: str

class WhatsAppStatus(BaseModel):
    connected: bool
    phone_number: Optional[str] = None
    connected_at: Optional[str] = None
    device_name: Optional[str] = None

class IntegrationCredentials(BaseModel):
    chatbot_id: str
    integration_type: str
    credentials: Dict[str, Any]

@router.post("/whatsapp/generate-qr")
async def generate_whatsapp_qr(data: WhatsAppConnect):
    """Generate QR code for WhatsApp Web linking"""
    try:
        # Generate a unique session token
        session_token = secrets.token_urlsafe(32)
        
        # In a real implementation, this would be a WebSocket connection URL
        # For demo, we'll create a QR code with session info
        qr_data = f"whatsapp://link?token={session_token}&chatbot={data.chatbot_id}&timestamp={datetime.utcnow().isoformat()}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Store session info
        whatsapp_sessions[data.chatbot_id] = {
            "session_token": session_token,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "connected": False
        }
        
        return {
            "qr_code": f"data:image/png;base64,{qr_base64}",
            "session_token": session_token,
            "expires_in": 60  # QR code expires in 60 seconds
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@router.post("/whatsapp/check-status")
async def check_whatsapp_status(data: WhatsAppConnect):
    """Check if WhatsApp is connected"""
    session = whatsapp_sessions.get(data.chatbot_id)
    
    if not session:
        return {
            "connected": False,
            "status": "not_initiated"
        }
    
    # In a real implementation, this would check the actual WhatsApp Web session
    # For demo purposes, we'll simulate a connection after QR is generated
    return {
        "connected": session.get("connected", False),
        "status": session.get("status", "pending"),
        "phone_number": session.get("phone_number"),
        "connected_at": session.get("connected_at"),
        "device_name": session.get("device_name", "WhatsApp Web")
    }

@router.post("/whatsapp/simulate-connect")
async def simulate_whatsapp_connect(data: WhatsAppConnect):
    """Simulate WhatsApp connection (for demo purposes)"""
    session = whatsapp_sessions.get(data.chatbot_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Please generate QR code first.")
    
    # Simulate successful connection
    whatsapp_sessions[data.chatbot_id].update({
        "connected": True,
        "status": "connected",
        "phone_number": "+1234567890",
        "connected_at": datetime.utcnow().isoformat(),
        "device_name": "WhatsApp Web"
    })
    
    return {
        "success": True,
        "message": "WhatsApp connected successfully"
    }

@router.post("/whatsapp/disconnect")
async def disconnect_whatsapp(data: WhatsAppConnect):
    """Disconnect WhatsApp session"""
    if data.chatbot_id in whatsapp_sessions:
        del whatsapp_sessions[data.chatbot_id]
    
    return {
        "success": True,
        "message": "WhatsApp disconnected successfully"
    }

@router.post("/save-credentials")
async def save_integration_credentials(data: IntegrationCredentials):
    """Save integration credentials (Slack, Telegram, Discord, etc.)"""
    # In production, save to MongoDB
    # For now, return success
    return {
        "success": True,
        "message": f"{data.integration_type} credentials saved successfully",
        "integration_id": secrets.token_urlsafe(16)
    }

@router.get("/status/{chatbot_id}/{integration_type}")
async def get_integration_status(chatbot_id: str, integration_type: str):
    """Get integration status for a specific chatbot"""
    
    if integration_type == "whatsapp":
        session = whatsapp_sessions.get(chatbot_id)
        if session and session.get("connected"):
            return {
                "connected": True,
                "integration_type": "whatsapp",
                "details": {
                    "phone_number": session.get("phone_number"),
                    "device_name": session.get("device_name"),
                    "connected_at": session.get("connected_at")
                }
            }
    
    return {
        "connected": False,
        "integration_type": integration_type
    }
