# 🔒 Security Documentation

**BotSmith Security Guide** - Comprehensive security practices, implementation details, and best practices for the BotSmith chatbot platform.

---

## Table of Contents

1. [Authentication & Authorization](#1-authentication--authorization) ⏱️ 12 min read
2. [Data Protection](#2-data-protection) ⏱️ 10 min read
3. [API Security](#3-api-security) ⏱️ 15 min read
4. [Best Practices](#4-best-practices) ⏱️ 8 min read

---

## 1. Authentication & Authorization

### Overview

BotSmith implements a robust JWT (JSON Web Token) based authentication system with role-based access control (RBAC) to ensure secure user authentication and authorization.

### 1.1 JWT Token-Based Authentication

#### How It Works

1. **User Registration/Login**: User provides credentials (email + password)
2. **Token Generation**: Server validates credentials and generates a JWT token
3. **Token Storage**: Client stores token securely (localStorage/sessionStorage)
4. **Authenticated Requests**: Client includes token in Authorization header
5. **Token Validation**: Server validates token for each protected endpoint

#### Implementation Details

**Token Configuration** (`/app/backend/auth.py`):

```python
# Security configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Token Generation**:

```python
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
```

**Token Validation**:

```python
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
```

### 1.2 Password Security

#### Password Hashing with Bcrypt

BotSmith uses **bcrypt** algorithm for password hashing, which provides:
- **Salting**: Automatic salt generation for each password
- **Cost Factor**: Configurable computational cost to resist brute-force attacks
- **One-way Hashing**: Passwords cannot be reversed or decrypted

**Implementation**:

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)
```

**Password Requirements** (Recommended):
- Minimum 8 characters
- Mix of uppercase and lowercase letters
- At least one number
- At least one special character
- No common passwords or dictionary words

### 1.3 Role-Based Access Control (RBAC)

#### User Roles

BotSmith implements three distinct user roles:

1. **User** (Standard)
   - Create and manage own chatbots
   - Access personal analytics
   - Manage integrations
   - View subscription details

2. **Moderator**
   - All user permissions
   - View basic system analytics
   - Access to moderation tools
   - Flag inappropriate content

3. **Admin**
   - All moderator permissions
   - Full user management (CRUD operations)
   - System configuration access
   - View all analytics and logs
   - Manage subscriptions and plans
   - Access security audit tools

#### Role Implementation

**User Model** (`/app/backend/models.py`):

```python
class User(BaseModel):
    id: str
    name: str
    email: str
    password_hash: str
    role: str = "user"  # Options: "user", "moderator", "admin"
    status: str = "active"  # Options: "active", "suspended", "banned"
    created_at: datetime
    updated_at: datetime
```

**Role Checking Decorator Example**:

```python
from functools import wraps
from fastapi import HTTPException, status

def require_role(allowed_roles: list):
    """Decorator to enforce role-based access control"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

**Usage in Endpoints**:

```python
# Admin-only endpoint
@router.get("/admin/users")
async def get_all_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    # Return all users
```

### 1.4 Session Management

#### Token Expiration

- **Default Expiration**: 7 days
- **Sliding Window**: Token refreshed on active use
- **Automatic Logout**: Token invalidated after expiration

#### Token Refresh Strategy

```python
# Check if token is about to expire (within 1 day)
def should_refresh_token(token: str) -> bool:
    payload = decode_token(token)
    exp_timestamp = payload.get("exp")
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    time_until_expiry = exp_datetime - datetime.now(timezone.utc)
    return time_until_expiry.total_seconds() < 86400  # 1 day in seconds
```

### 1.5 Login History & Activity Tracking

BotSmith tracks all authentication events for security auditing:

**LoginHistory Model**:

```python
class LoginHistory(BaseModel):
    id: str
    user_id: str
    timestamp: datetime
    ip_address: str
    user_agent: str
    location: Optional[str] = None
    success: bool  # True for successful login, False for failed attempts
```

**Failed Login Attempts**:
- Maximum 5 failed attempts within 15 minutes
- Account temporarily locked for 30 minutes after exceeding limit
- Admin notification on repeated failed attempts

### 1.6 Security Recommendations

#### For Developers

1. **Never hardcode SECRET_KEY** - Always use environment variables
2. **Rotate SECRET_KEY regularly** - At least every 90 days
3. **Use HTTPS only** - Never transmit tokens over HTTP
4. **Implement token blacklisting** - For logout and compromised tokens
5. **Monitor authentication logs** - Set up alerts for suspicious activity

#### For Users

1. **Use strong, unique passwords** - Never reuse passwords
2. **Enable two-factor authentication** - When available (future feature)
3. **Review login history regularly** - Check for unauthorized access
4. **Log out from shared devices** - Never leave sessions active
5. **Report suspicious activity immediately** - Contact support if compromised

---

## 2. Data Protection

### Overview

BotSmith implements comprehensive data protection measures to ensure privacy, confidentiality, and integrity of user data across all system components.

### 2.1 Data Encryption

#### Encryption at Rest

**Database Encryption**:
- MongoDB encryption enabled for production environments
- Field-level encryption for sensitive data
- Encrypted backups with AES-256 encryption

**Sensitive Fields**:
```python
# Fields that require encryption/hashing
- password_hash: Bcrypt hashed (irreversible)
- api_keys: AES-256 encrypted (reversible for use)
- integration_credentials: Encrypted in database
- payment_information: Never stored directly (tokenized via Stripe)
```

**Implementation Example**:

```python
from cryptography.fernet import Fernet
import os

# Encryption key (stored in environment)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data like API keys"""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data for use"""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
```

#### Encryption in Transit

**TLS/SSL Implementation**:
- All API communications use HTTPS (TLS 1.2+)
- WebSocket connections use WSS (secure WebSocket)
- Certificate management via Let's Encrypt

**HTTPS Configuration** (Nginx):

```nginx
server {
    listen 443 ssl http2;
    server_name api.botsmith.com;
    
    ssl_certificate /etc/letsencrypt/live/botsmith.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/botsmith.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
}
```

### 2.2 Data Privacy

#### Personal Identifiable Information (PII)

**PII Data Collected**:
- Email address (authentication)
- Name (profile)
- Phone number (optional)
- IP address (security logging)
- Payment information (via Stripe - not stored)

**PII Protection Measures**:

1. **Minimal Data Collection**: Only collect necessary data
2. **Purpose Limitation**: Use data only for stated purposes
3. **Access Control**: Restrict PII access to authorized personnel
4. **Retention Policies**: Delete data after retention period
5. **Right to Deletion**: Users can request data deletion (GDPR compliance)

**Data Anonymization**:

```python
def anonymize_user_data(user_id: str):
    """Anonymize user data for analytics"""
    return {
        'user_id': hashlib.sha256(user_id.encode()).hexdigest()[:16],
        # Remove PII fields
        'location': 'Unknown',
        'ip_address': None
    }
```

#### GDPR Compliance

**User Rights Implementation**:

1. **Right to Access**: Users can export all their data
```python
@router.get("/user/data-export")
async def export_user_data(current_user: User = Depends(get_current_user)):
    """Export all user data in JSON format"""
    user_data = {
        'profile': current_user.model_dump(),
        'chatbots': await get_user_chatbots(current_user.id),
        'conversations': await get_user_conversations(current_user.id),
        'integrations': await get_user_integrations(current_user.id)
    }
    return user_data
```

2. **Right to Deletion**: Users can delete their account
```python
@router.delete("/user/account")
async def delete_account(current_user: User = Depends(get_current_user)):
    """Delete user account and all associated data"""
    # Delete all user data
    await delete_user_chatbots(current_user.id)
    await delete_user_sources(current_user.id)
    await delete_user_conversations(current_user.id)
    await delete_user_profile(current_user.id)
    return {"message": "Account deleted successfully"}
```

3. **Right to Rectification**: Users can update their data
4. **Right to Data Portability**: Export data in machine-readable format

### 2.3 Data Integrity

#### Database Integrity

**MongoDB Validation**:

```python
# Collection validation schema
chatbot_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['id', 'name', 'user_id', 'created_at'],
        'properties': {
            'id': {'bsonType': 'string'},
            'name': {'bsonType': 'string', 'minLength': 1, 'maxLength': 100},
            'user_id': {'bsonType': 'string'},
            'created_at': {'bsonType': 'date'}
        }
    }
}
```

**Transaction Support**:

```python
async def create_chatbot_with_defaults(user_id: str, chatbot_data: dict):
    """Create chatbot with transaction support"""
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Create chatbot
            chatbot = await db.chatbots.insert_one(chatbot_data, session=session)
            # Create default settings
            await db.settings.insert_one({
                'chatbot_id': chatbot.inserted_id,
                'defaults': True
            }, session=session)
            # Transaction commits automatically if no errors
```

#### Data Backup Strategy

**Automated Backups**:
- **Frequency**: Daily incremental, weekly full backups
- **Retention**: 30 days rolling backup
- **Storage**: Encrypted AWS S3 buckets
- **Recovery Time Objective (RTO)**: 4 hours
- **Recovery Point Objective (RPO)**: 24 hours

**Backup Verification**:
- Weekly restore tests on staging environment
- Checksum verification for data integrity
- Automated alerts for backup failures

### 2.4 Secure File Upload

#### File Upload Security

**File Validation**:

```python
ALLOWED_FILE_TYPES = ['.pdf', '.docx', '.txt', '.xlsx', '.csv']
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

async def validate_file_upload(file: UploadFile):
    """Validate uploaded files for security"""
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to start
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds {MAX_FILE_SIZE/1024/1024}MB limit"
        )
    
    # Virus scanning (integrate with ClamAV or similar)
    await scan_file_for_viruses(file)
    
    return True
```

**File Storage**:
- Files stored with random UUID filenames
- Original filenames never used in storage paths
- Directory traversal protection
- Separate storage from application code

### 2.5 Sensitive Data Handling

#### API Keys & Credentials

**Integration Credentials Storage**:

```python
class Integration(BaseModel):
    id: str
    chatbot_id: str
    integration_type: str  # slack, telegram, discord, etc.
    credentials: dict  # Encrypted credentials
    enabled: bool
    created_at: datetime

# Before storing
integration.credentials = encrypt_credentials(credentials_dict)

# Before using
decrypted_credentials = decrypt_credentials(integration.credentials)
```

**Credential Masking in Responses**:

```python
def mask_credentials(credentials: dict) -> dict:
    """Mask sensitive credentials in API responses"""
    masked = {}
    for key, value in credentials.items():
        if any(sensitive in key.lower() for sensitive in ['token', 'key', 'secret', 'password']):
            masked[key] = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '****'
        else:
            masked[key] = value
    return masked
```

#### Environment Variables

**Critical Environment Variables**:

```bash
# .env file (NEVER commit to version control)
SECRET_KEY=your-secret-key-min-32-characters
ENCRYPTION_KEY=your-encryption-key-fernet-format
MONGO_URL=mongodb://localhost:27017/
DB_NAME=chatbase_db
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
STRIPE_SECRET_KEY=sk_test_...
```

**Environment Variable Security**:
- Use `.env` files locally (gitignored)
- Use secrets management in production (AWS Secrets Manager, Azure Key Vault)
- Rotate keys regularly
- Never log environment variable values

### 2.6 Data Retention & Deletion

#### Retention Policies

**Data Type Retention Periods**:

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| User Accounts | Active + 30 days after deletion request | Soft delete, then hard delete |
| Chatbot Conversations | 90 days (configurable per plan) | Automated purge |
| Login History | 365 days | Automated purge |
| Activity Logs | 90 days | Automated purge |
| Audit Logs | 7 years (compliance) | Archived to cold storage |
| Uploaded Files | While source exists + 30 days | Secure deletion |

**Automated Cleanup Job**:

```python
async def cleanup_expired_data():
    """Daily cleanup job for expired data"""
    now = datetime.now(timezone.utc)
    
    # Delete old conversations
    retention_days = 90
    cutoff_date = now - timedelta(days=retention_days)
    await db.conversations.delete_many({
        'created_at': {'$lt': cutoff_date},
        'archived': False
    })
    
    # Delete old login history
    await db.login_history.delete_many({
        'timestamp': {'$lt': now - timedelta(days=365)}
    })
    
    logger.info("Data cleanup completed")
```

---

## 3. API Security

### Overview

BotSmith implements multiple layers of API security to protect against common vulnerabilities, abuse, and unauthorized access.

### 3.1 Rate Limiting

#### Implementation

**Rate Limit Configuration** (`/app/backend/server.py`):

```python
# Rate limiting middleware (200 requests/min, 5000 requests/hour)
app.add_middleware(
    RateLimitMiddleware, 
    requests_per_minute=200, 
    requests_per_hour=5000
)
```

**Rate Limit Middleware** (`/app/backend/middleware/security.py`):

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 200, requests_per_hour: int = 5000):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
    
    def is_rate_limited(self, client_ip: str) -> Tuple[bool, str]:
        """Check if client has exceeded rate limits"""
        now = datetime.now()
        
        # Clean old timestamps
        rate_limit_storage[client_ip] = [
            timestamp for timestamp in rate_limit_storage[client_ip]
            if (now - timestamp).total_seconds() < 3600  # Keep last hour
        ]
        
        requests = rate_limit_storage[client_ip]
        
        # Check per-minute limit
        recent_requests = [ts for ts in requests if (now - ts).total_seconds() < 60]
        if len(recent_requests) >= self.requests_per_minute:
            return True, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
        
        # Check per-hour limit
        if len(requests) >= self.requests_per_hour:
            return True, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
        
        return False, ""
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        # Check rate limit
        is_limited, message = self.is_rate_limited(client_ip)
        if is_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": message,
                    "retry_after": 60
                }
            )
        
        # Record request
        rate_limit_storage[client_ip].append(datetime.now())
        
        response = await call_next(request)
        return response
```

#### Rate Limit Headers

**Response Headers**:
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 195
X-RateLimit-Reset: 1699564800
```

#### Custom Rate Limits

**Per-Endpoint Rate Limits**:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/chat")
@limiter.limit("10/minute")  # Stricter limit for AI endpoints
async def chat_endpoint(request: Request):
    pass

@router.get("/analytics")
@limiter.limit("30/minute")  # Normal limit for analytics
async def analytics_endpoint(request: Request):
    pass
```

### 3.2 Input Validation & Sanitization

#### Request Validation

**Pydantic Models for Validation**:

```python
from pydantic import BaseModel, validator, Field
import re

class ChatbotCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    provider: str = Field(..., regex="^(openai|claude|gemini)$")
    model: str = Field(..., min_length=1, max_length=50)
    
    @validator('name')
    def validate_name(cls, v):
        # Remove potentially dangerous characters
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', v):
            raise ValueError('Name contains invalid characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v:
            # Basic XSS prevention
            if '<script' in v.lower() or 'javascript:' in v.lower():
                raise ValueError('Description contains potentially dangerous content')
        return v
```

#### Input Sanitization Middleware

**Sanitization Implementation** (`/app/backend/middleware/security.py`):

```python
def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks"""
    if not text:
        return text
    
    # Remove potentially dangerous HTML tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    
    # Encode special characters
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    
    return text.strip()

class InputValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Validate request size
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > 100 * 1024 * 1024:  # 100MB
            return JSONResponse(
                status_code=413,
                content={"error": "Request body too large"}
            )
        
        response = await call_next(request)
        return response
```

### 3.3 CORS (Cross-Origin Resource Sharing)

#### CORS Configuration

**Production CORS Settings** (`/app/backend/server.py`):

```python
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

**Environment-Based Configuration**:

```bash
# Development
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Production
CORS_ORIGINS=https://botsmith.com,https://app.botsmith.com
```

**Security Implications**:
- ⚠️ Never use `allow_origins=["*"]` in production
- ✅ Specify exact origins for production
- ✅ Use `allow_credentials=True` only with specific origins
- ✅ Limit allowed methods to necessary ones

### 3.4 SQL/NoSQL Injection Prevention

#### MongoDB Query Safety

**Safe Query Construction**:

```python
# ❌ UNSAFE - Never build queries with string concatenation
user_input = request.query_params.get('name')
# DON'T DO THIS:
query = f"{{'name': '{user_input}'}}"
result = await db.users.find(eval(query))

# ✅ SAFE - Use parameterized queries
user_input = request.query_params.get('name')
query = {'name': user_input}
result = await db.users.find(query)
```

**Query Sanitization**:

```python
def sanitize_mongodb_query(query: dict) -> dict:
    """Sanitize MongoDB query to prevent injection"""
    dangerous_operators = ['$where', '$regex', '$expr']
    
    def check_dict(d):
        for key, value in d.items():
            if key.startswith('$') and key in dangerous_operators:
                raise ValueError(f"Potentially dangerous operator: {key}")
            if isinstance(value, dict):
                check_dict(value)
    
    check_dict(query)
    return query
```

### 3.5 API Authentication

#### Bearer Token Authentication

**Implementation**:

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = decode_token(token)
    email = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
```

**Protected Endpoint Example**:

```python
@router.get("/chatbots")
async def get_chatbots(
    current_user: User = Depends(get_current_user)
):
    """Get all chatbots for authenticated user"""
    chatbots = await db.chatbots.find({'user_id': current_user.id}).to_list(100)
    return chatbots
```

#### API Key Authentication (for Integrations)

**API Key Generation**:

```python
import secrets

def generate_api_key() -> str:
    """Generate a secure API key"""
    return f"bsm_{secrets.token_urlsafe(32)}"

# Store API key hash, not the actual key
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
```

**API Key Middleware** (`/app/backend/middleware/security.py`):

```python
class APIKeyProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public endpoints don't need API keys
        if request.url.path.startswith('/api/public/'):
            return await call_next(request)
        
        # Check for API key in header
        api_key = request.headers.get('X-API-Key')
        if not api_key and not request.headers.get('Authorization'):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing authentication credentials"}
            )
        
        response = await call_next(request)
        return response
```

### 3.6 Security Headers

#### HTTP Security Headers

**Security Headers Middleware** (`/app/backend/middleware/security.py`):

```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.openai.com https://api.anthropic.com"
        )
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
```

**Header Explanations**:

| Header | Purpose | Value |
|--------|---------|-------|
| X-Content-Type-Options | Prevent MIME-sniffing | nosniff |
| X-Frame-Options | Prevent clickjacking | DENY |
| X-XSS-Protection | Enable XSS filter | 1; mode=block |
| Strict-Transport-Security | Force HTTPS | max-age=31536000 |
| Content-Security-Policy | Control resource loading | Restricted sources |
| Referrer-Policy | Control referrer info | strict-origin |

### 3.7 API Versioning

#### Version Strategy

**URL-Based Versioning**:

```python
# Version 1
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(chatbots_v1.router)

# Version 2
api_v2 = APIRouter(prefix="/api/v2")
api_v2.include_router(chatbots_v2.router)

app.include_router(api_v1)
app.include_router(api_v2)
```

**Deprecation Notice**:

```python
@router.get("/old-endpoint")
async def deprecated_endpoint():
    """
    Deprecated endpoint - use /api/v2/new-endpoint instead
    This endpoint will be removed on 2024-12-31
    """
    return {
        "warning": "This endpoint is deprecated",
        "deprecation_date": "2024-12-31",
        "replacement": "/api/v2/new-endpoint"
    }
```

### 3.8 Error Handling & Information Disclosure

#### Secure Error Responses

**Production Error Handler**:

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Generic exception handler - prevents information disclosure"""
    
    # Log the full error internally
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Return generic error to client (don't expose internals)
    if os.environ.get('ENVIRONMENT') == 'production':
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred. Please try again later.",
                "request_id": str(uuid.uuid4())  # For support tracking
            }
        )
    else:
        # Development: return detailed error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": str(exc),
                "type": type(exc).__name__,
                "traceback": traceback.format_exc()
            }
        )
```

**Validation Error Handler**:

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with safe error messages"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Invalid request data",
            "details": [
                {
                    "field": ".".join(str(x) for x in error["loc"]),
                    "message": error["msg"]
                }
                for error in exc.errors()
            ]
        }
    )
```

### 3.9 Audit Logging

#### Security Audit Logs

**Audit Log Model**:

```python
class AuditLog(BaseModel):
    id: str
    user_id: Optional[str]
    action: str  # login, create_chatbot, delete_user, etc.
    resource_type: str  # user, chatbot, integration, etc.
    resource_id: Optional[str]
    ip_address: str
    user_agent: str
    timestamp: datetime
    status: str  # success, failure, unauthorized
    details: Optional[dict] = None
```

**Audit Logging Function**:

```python
async def log_audit_event(
    user_id: Optional[str],
    action: str,
    resource_type: str,
    resource_id: Optional[str],
    request: Request,
    status: str = "success",
    details: Optional[dict] = None
):
    """Log security-relevant events"""
    audit_log = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'action': action,
        'resource_type': resource_type,
        'resource_id': resource_id,
        'ip_address': request.client.host,
        'user_agent': request.headers.get('user-agent', 'unknown'),
        'timestamp': datetime.now(timezone.utc),
        'status': status,
        'details': details
    }
    
    await db.audit_logs.insert_one(audit_log)
    
    # Alert on critical actions
    if action in ['delete_user', 'change_role', 'access_denied']:
        await send_security_alert(audit_log)
```

**Usage in Endpoints**:

```python
@router.delete("/chatbots/{chatbot_id}")
async def delete_chatbot(
    chatbot_id: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    # Perform deletion
    result = await db.chatbots.delete_one({'id': chatbot_id, 'user_id': current_user.id})
    
    # Log audit event
    await log_audit_event(
        user_id=current_user.id,
        action='delete_chatbot',
        resource_type='chatbot',
        resource_id=chatbot_id,
        request=request,
        status='success' if result.deleted_count > 0 else 'failure'
    )
    
    return {"success": True}
```

---

## 4. Best Practices

### Overview

This section provides security best practices for developers, administrators, and users to maintain a secure BotSmith environment.

### 4.1 Development Security Guidelines

#### Secure Coding Practices

**1. Input Validation**
```python
# ✅ Always validate and sanitize user input
from pydantic import validator

class UserInput(BaseModel):
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v) > 5000:
            raise ValueError('Message too long')
        return sanitize_input(v)

# ❌ Never trust user input directly
# dangerous_query = eval(user_input)  # NEVER DO THIS
```

**2. Secrets Management**
```python
# ✅ Use environment variables
api_key = os.environ.get('OPENAI_API_KEY')

# ❌ Never hardcode secrets
# api_key = "sk-1234567890abcdef"  # NEVER DO THIS
```

**3. Error Handling**
```python
# ✅ Log errors internally, return generic messages
try:
    result = await process_payment()
except Exception as e:
    logger.error(f"Payment error: {str(e)}", exc_info=True)
    return {"error": "Payment processing failed"}

# ❌ Don't expose internal errors
# return {"error": str(e)}  # May leak sensitive info
```

**4. Database Queries**
```python
# ✅ Use parameterized queries
query = {'user_id': user_id, 'status': 'active'}
users = await db.users.find(query)

# ❌ Never use string concatenation
# query = f"SELECT * FROM users WHERE id = '{user_id}'"  # SQL injection risk
```

#### Dependency Management

**Keep Dependencies Updated**:

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update dependencies regularly
pip install --upgrade package-name

# Use requirements.txt with pinned versions
fastapi==0.104.1
uvicorn==0.24.0
```

**Security Scanning**:

```bash
# Scan for vulnerabilities with Bandit
pip install bandit
bandit -r /app/backend

# Scan for secrets with truffleHog
trufflehog filesystem /app/backend --json
```

### 4.2 Deployment Security

#### Environment Configuration

**Production Environment Variables**:

```bash
# .env.production (use secrets manager in production)
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<strong-random-key-minimum-32-chars>
ENCRYPTION_KEY=<fernet-key>
DB_NAME=chatbase_production
CORS_ORIGINS=https://botsmith.com,https://app.botsmith.com
ALLOWED_HOSTS=botsmith.com,app.botsmith.com
```

**Docker Security**:

```dockerfile
# Use non-root user
FROM python:3.11-slim
RUN useradd -m -u 1000 appuser
USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set read-only root filesystem (when possible)
# docker run --read-only ...

# Drop capabilities
# docker run --cap-drop ALL --cap-add NET_BIND_SERVICE ...
```

**Kubernetes Security**:

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: backend
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      limits:
        memory: "512Mi"
        cpu: "500m"
```

#### SSL/TLS Configuration

**Nginx SSL Configuration**:

```nginx
server {
    listen 443 ssl http2;
    server_name api.botsmith.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/botsmith.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/botsmith.com/privkey.pem;
    
    # SSL protocols and ciphers
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
}
```

### 4.3 Monitoring & Alerting

#### Security Monitoring

**Key Metrics to Monitor**:

1. **Authentication Failures**
```python
# Alert on multiple failed login attempts
if failed_attempts > 5 in last_15_minutes:
    send_alert("Multiple failed login attempts detected")
```

2. **Rate Limit Violations**
```python
# Monitor rate limit hits
if rate_limit_exceeded_count > 100 in last_hour:
    send_alert("Potential DDoS attack detected")
```

3. **Unauthorized Access Attempts**
```python
# Track 401/403 responses
if unauthorized_responses > 50 in last_minute:
    send_alert("High number of unauthorized access attempts")
```

4. **Suspicious API Usage**
```python
# Monitor for unusual patterns
if chatbot_creations > 100 in last_hour:
    send_alert("Unusual chatbot creation activity")
```

**Monitoring Implementation**:

```python
from prometheus_client import Counter, Histogram

# Metrics
auth_failures = Counter('auth_failures_total', 'Total authentication failures')
request_duration = Histogram('request_duration_seconds', 'Request duration')
unauthorized_attempts = Counter('unauthorized_attempts_total', 'Unauthorized access attempts')

# Usage
@router.post("/login")
async def login(credentials: LoginCredentials):
    try:
        user = await authenticate(credentials)
        return {"token": create_token(user)}
    except AuthenticationError:
        auth_failures.inc()  # Increment failure counter
        raise HTTPException(status_code=401)
```

#### Log Analysis

**Security Log Monitoring**:

```python
# Critical events to log
CRITICAL_EVENTS = [
    'login_failure',
    'unauthorized_access',
    'rate_limit_exceeded',
    'suspicious_activity',
    'data_breach_attempt',
    'privilege_escalation',
    'account_lockout'
]

async def log_security_event(event_type: str, details: dict):
    """Log security events with structured data"""
    log_entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'event_type': event_type,
        'severity': 'CRITICAL' if event_type in CRITICAL_EVENTS else 'WARNING',
        'details': details
    }
    
    logger.warning(json.dumps(log_entry))
    
    # Send to SIEM (Security Information and Event Management)
    await send_to_siem(log_entry)
```

### 4.4 Incident Response

#### Security Incident Procedure

**1. Detection & Identification**
- Monitor alerts and logs
- Identify the nature and scope of the incident
- Classify severity (Low, Medium, High, Critical)

**2. Containment**
```python
# Emergency account suspension
async def emergency_suspend_user(user_id: str, reason: str):
    """Immediately suspend user account"""
    await db.users.update_one(
        {'id': user_id},
        {'$set': {
            'status': 'suspended',
            'suspension_reason': reason,
            'suspension_until': None  # Indefinite
        }}
    )
    
    # Revoke all active sessions
    await revoke_all_user_tokens(user_id)
    
    # Log incident
    await log_security_event('emergency_suspension', {
        'user_id': user_id,
        'reason': reason
    })
```

**3. Eradication & Recovery**
- Remove malicious content/accounts
- Patch vulnerabilities
- Restore from clean backups if needed

**4. Post-Incident Activities**
- Document the incident
- Update security measures
- Conduct post-mortem review

#### Data Breach Response

**Breach Detection**:

```python
async def detect_data_breach():
    """Monitor for potential data breaches"""
    # Check for unusual data access patterns
    recent_queries = await get_recent_database_queries()
    
    suspicious_patterns = [
        'SELECT * FROM users',  # Full table scans
        'large_data_export',    # Bulk exports
        'unusual_access_hours'  # Access at odd hours
    ]
    
    for pattern in suspicious_patterns:
        if pattern_detected(recent_queries, pattern):
            await trigger_breach_protocol(pattern)
```

**Breach Notification**:

```python
async def notify_affected_users(breach_details: dict):
    """Notify users affected by data breach"""
    affected_users = breach_details['affected_users']
    
    for user in affected_users:
        # Send email notification
        await send_breach_notification_email(
            email=user['email'],
            breach_type=breach_details['type'],
            data_affected=breach_details['data_types'],
            actions_taken=breach_details['remediation']
        )
        
        # Force password reset
        await invalidate_user_password(user['id'])
        
        # Log notification
        await log_audit_event(
            user_id=user['id'],
            action='breach_notification_sent',
            resource_type='security',
            details=breach_details
        )
```

### 4.5 User Security Guidelines

#### For End Users

**1. Account Security**
- ✅ Use strong, unique passwords (min 12 characters)
- ✅ Enable two-factor authentication when available
- ✅ Review login history regularly
- ✅ Log out from shared devices
- ❌ Don't share account credentials
- ❌ Don't use the same password across multiple sites

**2. API Key Management**
- ✅ Store API keys securely (use environment variables)
- ✅ Rotate API keys regularly (every 90 days)
- ✅ Use different API keys for development and production
- ✅ Revoke compromised keys immediately
- ❌ Don't commit API keys to version control
- ❌ Don't share API keys in public channels

**3. Data Protection**
- ✅ Only upload necessary documents
- ✅ Remove sensitive information before uploading
- ✅ Use the data deletion feature when done
- ✅ Export your data regularly
- ❌ Don't upload confidential business data without approval
- ❌ Don't share chatbot links publicly if they contain sensitive data

**4. Integration Security**
- ✅ Review integration permissions carefully
- ✅ Use OAuth when available (instead of API keys)
- ✅ Audit active integrations regularly
- ✅ Revoke unused integrations
- ❌ Don't grant more permissions than necessary
- ❌ Don't use personal credentials for team integrations

### 4.6 Compliance & Standards

#### Compliance Frameworks

**1. GDPR (General Data Protection Regulation)**
- ✅ Right to access (data export)
- ✅ Right to deletion (account deletion)
- ✅ Right to rectification (profile updates)
- ✅ Right to data portability (JSON/CSV export)
- ✅ Consent management
- ✅ Data processing agreements

**2. SOC 2 (Service Organization Control)**
- ✅ Security policies and procedures
- ✅ Access control and authentication
- ✅ Change management processes
- ✅ Incident response procedures
- ✅ Monitoring and logging
- ✅ Vendor management

**3. OWASP Top 10 Protection**

| Vulnerability | Protection Implemented |
|--------------|------------------------|
| Injection | Parameterized queries, input validation |
| Broken Authentication | JWT tokens, bcrypt hashing, MFA support |
| Sensitive Data Exposure | Encryption at rest & transit, secure headers |
| XML External Entities | N/A (no XML processing) |
| Broken Access Control | RBAC, permission checks |
| Security Misconfiguration | Security headers, secure defaults |
| XSS | Input sanitization, CSP headers |
| Insecure Deserialization | Pydantic validation, no pickle |
| Using Components with Known Vulnerabilities | Dependency scanning, regular updates |
| Insufficient Logging & Monitoring | Comprehensive audit logs, alerting |

### 4.7 Security Checklist

#### Pre-Deployment Security Checklist

**Infrastructure Security**
- [ ] SSL/TLS certificates configured and valid
- [ ] Firewall rules properly configured
- [ ] Database access restricted to application only
- [ ] Secrets stored in secure vault (not in code)
- [ ] Backup and disaster recovery tested
- [ ] DDoS protection enabled
- [ ] Security groups/network policies configured

**Application Security**
- [ ] All dependencies updated to latest secure versions
- [ ] Security middleware enabled (rate limiting, CORS, headers)
- [ ] Input validation on all endpoints
- [ ] Authentication required on protected endpoints
- [ ] Authorization checks implemented correctly
- [ ] Error messages don't leak sensitive information
- [ ] Logging and monitoring configured
- [ ] Security headers properly set

**Data Security**
- [ ] Database encryption enabled
- [ ] Sensitive data encrypted in database
- [ ] API keys and credentials encrypted
- [ ] File uploads validated and scanned
- [ ] Data retention policies implemented
- [ ] GDPR compliance features working
- [ ] Data backup and recovery tested

**Testing & Validation**
- [ ] Security scan completed (Bandit, safety)
- [ ] Penetration testing performed
- [ ] Load testing completed
- [ ] Authentication flows tested
- [ ] Authorization rules verified
- [ ] Rate limiting tested
- [ ] Error handling tested

---

## Additional Resources

### Security Tools

**Recommended Tools for Security Testing**:

1. **OWASP ZAP** - Web application security scanner
2. **Bandit** - Python security linter
3. **Safety** - Python dependency vulnerability checker
4. **truffleHog** - Secrets detection tool
5. **Nmap** - Network security scanner
6. **Burp Suite** - Web application security testing

### Security References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)

### Contact

For security concerns or to report vulnerabilities:

**Security Team**: security@botsmith.com  
**Bug Bounty Program**: https://botsmith.com/security/bug-bounty  
**PGP Key**: Available at https://botsmith.com/security/pgp

**Responsible Disclosure Policy**:
- Report vulnerabilities privately to security@botsmith.com
- Allow 90 days for remediation before public disclosure
- Include detailed reproduction steps
- Eligible for bounty rewards based on severity

---

## Document Version

- **Version**: 1.0.0
- **Last Updated**: November 2025
- **Next Review**: February 2026

---

*This document is maintained by the BotSmith Security Team. For questions or suggestions, please contact security@botsmith.com*
