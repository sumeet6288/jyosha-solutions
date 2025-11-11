from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from models import User, Lead, LeadResponse, LeadCreate, LeadUpdate, LeadStatsResponse
from services.plan_service import plan_service
from auth import get_current_user

router = APIRouter()

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'chatbase_db')
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
leads_collection = db.leads


@router.get("/leads", response_model=List[LeadResponse])
async def get_my_leads(current_user: User = Depends(get_current_user)):
    """Get all leads for the current user"""
    try:
        leads = await leads_collection.find({"user_id": current_user.id}).to_list(length=10000)
        
        # Convert to response format
        lead_responses = []
        for lead in leads:
            if '_id' in lead:
                lead.pop('_id')
            lead_responses.append(LeadResponse(**lead))
        
        return lead_responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leads/stats", response_model=LeadStatsResponse)
async def get_lead_stats(current_user: User = Depends(get_current_user)):
    """Get lead statistics for current user"""
    try:
        # Count current leads
        current_count = await leads_collection.count_documents({"user_id": current_user.id})
        
        # Get plan limits using plan service
        subscription = await plan_service.get_user_subscription(current_user.id)
        plan = await plan_service.get_plan_by_id(subscription["plan_id"])
        
        # Check if custom limits exist
        if hasattr(current_user, 'custom_limits') and current_user.custom_limits and 'max_leads' in current_user.custom_limits:
            max_leads = current_user.custom_limits['max_leads']
        else:
            max_leads = plan["limits"].get("max_leads", 50)
        
        # Calculate percentage
        percentage = (current_count / max_leads * 100) if max_leads > 0 else 0
        
        return LeadStatsResponse(
            current_leads=current_count,
            max_leads=max_leads,
            percentage_used=round(percentage, 2),
            can_add_more=current_count < max_leads,
            plan_name=plan["name"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/leads")
async def create_lead(lead_data: LeadCreate, current_user: dict = Depends(get_current_user)):
    """Create a new lead for the current user"""
    try:
        # Handle both dict and User object
        if hasattr(current_user, 'id'):
            user_id = current_user.id
        else:
            user_id = current_user.get('id')
        
        # Get user's plan info
        user = await db.users.find_one({"id": user_id})
        subscription = user.get('subscription', {}) if user else {}
        plan_name = subscription.get('plan_name', 'Free')
        
        plan_limits = {
            'Free': 0,
            'Starter': 100,
            'Professional': 500,
            'Enterprise': 10000
        }
        
        max_leads = plan_limits.get(plan_name, 0)
        current_count = await db.leads.count_documents({"user_id": user_id})
        
        # Check if user has reached their limit
        if current_count >= max_leads:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": f"You have reached your lead limit of {max_leads}. Upgrade your plan to add more leads.",
                    "current": current_count,
                    "max": max_leads,
                    "plan": plan_name
                }
            )
        
        # Create new lead
        lead = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "name": lead_data.name or "",
            "email": lead_data.email or "",
            "phone": lead_data.phone or "",
            "company": lead_data.company or "",
            "status": lead_data.status or "active",
            "notes": lead_data.notes or "",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "metadata": {}
        }
        
        await db.leads.insert_one(lead)
        
        return {
            "success": True,
            "lead": lead,
            "message": "Lead created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/leads/{lead_id}")
async def update_lead(lead_id: str, lead_data: LeadCreate, current_user: dict = Depends(get_current_user)):
    """Update a specific lead (user can only update their own leads)"""
    try:
        # Handle both dict and User object
        if hasattr(current_user, 'id'):
            user_id = current_user.id
        else:
            user_id = current_user.get('id')
        
        # Check if lead belongs to user
        lead = await db.leads.find_one({"id": lead_id, "user_id": user_id})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found or access denied")
        
        update_data = lead_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        result = await db.leads.update_one(
            {"id": lead_id, "user_id": user_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        updated_lead = await db.leads.find_one({"id": lead_id})
        return {"success": True, "lead": updated_lead, "message": "Lead updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a specific lead (user can only delete their own leads)"""
    try:
        # Handle both dict and User object
        if hasattr(current_user, 'id'):
            user_id = current_user.id
        else:
            user_id = current_user.get('id')
        
        # Check if lead belongs to user
        lead = await db.leads.find_one({"id": lead_id, "user_id": user_id})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found or access denied")
        
        result = await db.leads.delete_one({"id": lead_id, "user_id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {"success": True, "message": "Lead deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
