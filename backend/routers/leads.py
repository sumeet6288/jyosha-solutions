from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from models import Lead, LeadResponse, LeadCreate
from auth import get_current_user

router = APIRouter()

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client.chatbase_db


@router.get("/leads", response_model=dict)
async def get_my_leads(current_user: dict = Depends(get_current_user)):
    """Get all leads for the current user"""
    try:
        user_id = current_user.get('id')
        leads = await db.leads.find({"user_id": user_id}).to_list(length=None)
        
        # Get user's plan info
        user = await db.users.find_one({"id": user_id})
        subscription = user.get('subscription', {}) if user else {}
        plan_name = subscription.get('plan_name', 'Free')
        
        plan_limits = {
            'Free': 0,
            'Starter': 100,
            'Professional': 1000,
            'Enterprise': 10000
        }
        
        max_leads = plan_limits.get(plan_name, 0)
        current_count = len(leads)
        
        return {
            "leads": leads,
            "total": current_count,
            "max_leads": max_leads,
            "remaining": max(0, max_leads - current_count),
            "plan_name": plan_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leads/stats", response_model=dict)
async def get_lead_stats(current_user: dict = Depends(get_current_user)):
    """Get lead statistics for current user"""
    try:
        user_id = current_user.get('id')
        
        total_leads = await db.leads.count_documents({"user_id": user_id})
        active_leads = await db.leads.count_documents({"user_id": user_id, "status": "active"})
        contacted_leads = await db.leads.count_documents({"user_id": user_id, "status": "contacted"})
        converted_leads = await db.leads.count_documents({"user_id": user_id, "status": "converted"})
        
        # Get user's plan limit
        user = await db.users.find_one({"id": user_id})
        subscription = user.get('subscription', {}) if user else {}
        plan_name = subscription.get('plan_name', 'Free')
        
        plan_limits = {
            'Free': 0,
            'Starter': 100,
            'Professional': 1000,
            'Enterprise': 10000
        }
        
        max_leads = plan_limits.get(plan_name, 0)
        
        return {
            "total_leads": total_leads,
            "active_leads": active_leads,
            "contacted_leads": contacted_leads,
            "converted_leads": converted_leads,
            "max_leads": max_leads,
            "remaining_leads": max(0, max_leads - total_leads),
            "plan_name": plan_name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a specific lead (user can only delete their own leads)"""
    try:
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
