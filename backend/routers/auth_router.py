from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, UserLogin, UserResponse, Token, User
from auth import get_password_hash, verify_password, create_access_token, get_current_user_email, get_mock_user
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Database will be injected
users_collection = None

def init_router(db):
    """Initialize router with database connection."""
    global users_collection
    users_collection = db.users



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = user_data.model_dump()
    user_dict.pop('password')
    user = User(
        **user_dict,
        password_hash=get_password_hash(user_data.password)
    )
    
    # Store in database
    user_doc = user.model_dump()
    user_doc['created_at'] = user_doc['created_at'].isoformat()
    user_doc['updated_at'] = user_doc['updated_at'].isoformat()
    if user_doc.get('last_login'):
        user_doc['last_login'] = user_doc['last_login'].isoformat()
    if user_doc.get('suspension_until'):
        user_doc['suspension_until'] = user_doc['suspension_until'].isoformat()
    
    await users_collection.insert_one(user_doc)
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        role=user.role,
        status=user.status,
        phone=user.phone,
        avatar_url=user.avatar_url,
        last_login=user.last_login
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user and return access token."""
    # Find user
    user_doc = await users_collection.find_one({"email": user_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user_doc['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user_doc['email']})
    
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user(email: str = Depends(get_current_user_email)):
    """Get current authenticated user."""
    user_doc = await users_collection.find_one({"email": email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Handle datetime fields
    created_at = user_doc.get('created_at')
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    last_login = user_doc.get('last_login')
    if isinstance(last_login, str):
        last_login = datetime.fromisoformat(last_login)
    
    return UserResponse(
        id=user_doc['id'],
        name=user_doc['name'],
        email=user_doc['email'],
        created_at=created_at,
        role=user_doc.get('role', 'user'),
        status=user_doc.get('status', 'active'),
        phone=user_doc.get('phone'),
        avatar_url=user_doc.get('avatar_url'),
        last_login=last_login
    )


@router.post("/logout")
async def logout():
    """Logout user (client should remove token)."""
    return {"message": "Successfully logged out"}
