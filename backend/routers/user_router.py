from fastapi import APIRouter, HTTPException, status, Depends
from models import UserResponse, UserUpdate, PasswordChange
from auth import get_current_user_email, verify_password, get_password_hash
from datetime import datetime, timezone

router = APIRouter(prefix="/user", tags=["User Management"])

# Database will be injected
users_collection = None

def init_router(db):
    """Initialize router with database connection."""
    global users_collection
    users_collection = db.users


@router.put("/profile", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, email: str = Depends(get_current_user_email)):
    """Update user profile information."""
    # Check if new email is already taken
    if user_update.email and user_update.email != email:
        existing_user = await users_collection.find_one({"email": user_update.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    # Prepare update data
    update_data = {}
    if user_update.name:
        update_data['name'] = user_update.name
    if user_update.email:
        update_data['email'] = user_update.email
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    # Update user
    result = await users_collection.update_one(
        {"email": email},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get updated user
    user_doc = await users_collection.find_one({"email": user_update.email or email})
    
    return UserResponse(
        id=user_doc['id'],
        name=user_doc['name'],
        email=user_doc['email'],
        created_at=datetime.fromisoformat(user_doc['created_at'])
    )


@router.put("/password")
async def change_password(password_data: PasswordChange, email: str = Depends(get_current_user_email)):
    """Change user password."""
    # Get user
    user_doc = await users_collection.find_one({"email": email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password, user_doc['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    new_password_hash = get_password_hash(password_data.new_password)
    await users_collection.update_one(
        {"email": email},
        {"$set": {
            "password_hash": new_password_hash,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"message": "Password changed successfully"}


@router.delete("/account")
async def delete_account(email: str = Depends(get_current_user_email)):
    """Delete user account and all associated data."""
    # Delete user
    result = await users_collection.delete_one({"email": email})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # TODO: Delete associated chatbots, sources, conversations, etc.
    
    return {"message": "Account deleted successfully"}
