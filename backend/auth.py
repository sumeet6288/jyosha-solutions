from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import User
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Security configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database connection - will be initialized from server
mongo_client = None
db = None

def init_auth(database):
    """Initialize auth module with database connection."""
    global db
    db = database


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_email(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user email from JWT token."""
    token = credentials.credentials
    payload = decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email



async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token and return User object."""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database not initialized"
        )
    
    token = credentials.credentials
    payload = decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    users_collection = db.users
    user_doc = await users_collection.find_one({"email": email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Parse datetime fields if they are strings
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    if isinstance(user_doc.get('updated_at'), str):
        user_doc['updated_at'] = datetime.fromisoformat(user_doc['updated_at'])
    
    return User(**user_doc)


# Temporary bypass for development - returns a mock user without authentication
async def get_mock_user() -> User:
    """Mock user for development - bypass authentication"""
    if db is None:
        # Return hardcoded mock user if DB not available
        return User(
            id="demo-user-123",
            name="User demo-use",
            email="demo-user-123@botsmith.com",
            password_hash="mock-hash",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    
    # Try to fetch demo user from database
    users_collection = db.users
    user_doc = await users_collection.find_one({"email": "demo-user-123@botsmith.com"})
    
    if user_doc:
        # Convert datetime strings to datetime objects
        created_at = user_doc.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = user_doc.get('updated_at')
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        last_login = user_doc.get('last_login')
        if isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login)
        
        suspension_until = user_doc.get('suspension_until')
        if isinstance(suspension_until, str):
            suspension_until = datetime.fromisoformat(suspension_until)
        
        # Return user from database with all fields
        return User(
            id=user_doc.get('id', 'demo-user-123'),
            name=user_doc.get('name', 'User demo-use'),
            email=user_doc.get('email', 'demo-user-123@botsmith.com'),
            password_hash=user_doc.get('password_hash', 'mock-hash'),
            created_at=created_at or datetime.now(timezone.utc),
            updated_at=updated_at or datetime.now(timezone.utc),
            role=user_doc.get('role', 'user'),
            status=user_doc.get('status', 'active'),
            suspension_reason=user_doc.get('suspension_reason'),
            suspension_until=suspension_until,
            phone=user_doc.get('phone'),
            address=user_doc.get('address'),
            bio=user_doc.get('bio'),
            avatar_url=user_doc.get('avatar_url'),
            company=user_doc.get('company'),
            job_title=user_doc.get('job_title'),
            custom_max_chatbots=user_doc.get('custom_max_chatbots'),
            custom_max_messages=user_doc.get('custom_max_messages'),
            custom_max_file_uploads=user_doc.get('custom_max_file_uploads'),
            last_login=last_login,
            login_count=user_doc.get('login_count', 0),
            last_ip=user_doc.get('last_ip'),
            tags=user_doc.get('tags', []),
            admin_notes=user_doc.get('admin_notes')
        )
    else:
        # Create demo user if doesn't exist
        demo_user = User(
            id="demo-user-123",
            name="User demo-use",
            email="demo-user-123@botsmith.com",
            password_hash="mock-hash",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Store in database
        user_doc = demo_user.model_dump()
        user_doc['created_at'] = user_doc['created_at'].isoformat()
        user_doc['updated_at'] = user_doc['updated_at'].isoformat()
        if user_doc.get('last_login'):
            user_doc['last_login'] = user_doc['last_login'].isoformat()
        if user_doc.get('suspension_until'):
            user_doc['suspension_until'] = user_doc['suspension_until'].isoformat()
        
        await users_collection.insert_one(user_doc)
        
        return demo_user

