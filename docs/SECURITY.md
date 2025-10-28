# \ud83d\udd12 BotSmith Security Guide

## Table of Contents
1. [Security Overview](#security-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Protection](#data-protection)
4. [API Security](#api-security)
5. [File Upload Security](#file-upload-security)
6. [Database Security](#database-security)
7. [Infrastructure Security](#infrastructure-security)
8. [Security Best Practices](#security-best-practices)
9. [Vulnerability Reporting](#vulnerability-reporting)
10. [Security Checklist](#security-checklist)

---

## Security Overview

BotSmith implements multiple layers of security to protect user data and ensure safe operation:

### Security Features

✅ **Authentication**: JWT-based token authentication  
✅ **Password Security**: Bcrypt hashing with salt  
✅ **Data Encryption**: TLS 1.3 for data in transit  
✅ **Input Validation**: Pydantic models for all inputs  
✅ **File Security**: Type and size validation  
✅ **CORS**: Controlled cross-origin requests  
✅ **Rate Limiting**: Protection against abuse  
✅ **SQL Injection Protection**: MongoDB parameterized queries  
✅ **XSS Protection**: Content Security Policy headers  
✅ **CSRF Protection**: Token-based verification  

---

## Authentication & Authorization

### JWT Token Authentication

**Implementation:**

```python
# backend/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Best Practices:**

1. **Strong Secret Key**: Use 32+ character random string
   ```bash
   openssl rand -hex 32
   ```

2. **Token Expiration**: Set appropriate expiration times
   - Access tokens: 7 days (configurable)
   - Refresh tokens: 30 days

3. **Secure Storage**: Store tokens securely in frontend
   ```javascript
   // Good
   localStorage.setItem('token', token);
   
   // Better (for sensitive apps)
   // Use httpOnly cookies
   ```

4. **Token Rotation**: Implement token refresh mechanism

### Password Security

**Hashing:**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)
```

**Password Requirements:**

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

**Validation:**

```python
import re

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Z]", password):
        return False
    
    if not re.search(r"[a-z]", password):
        return False
    
    if not re.search(r"\d", password):
        return False
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    
    return True
```

### Role-Based Access Control (RBAC)

**User Roles:**

```python
class UserRole(str, Enum):
    USER = "user"          # Regular user
    MODERATOR = "moderator"  # Can view all content
    ADMIN = "admin"        # Full access

def require_role(required_role: UserRole):
    """Decorator to require specific role"""
    def decorator(func):
        async def wrapper(*args, user: User = Depends(get_current_user), **kwargs):
            if user.role not in [required_role, UserRole.ADMIN]:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# Usage
@router.delete("/users/{user_id}")
@require_role(UserRole.ADMIN)
async def delete_user(user_id: str, user: User = Depends(get_current_user)):
    # Only admins can delete users
    pass
```

---

## Data Protection

### Data Encryption

**In Transit (TLS/SSL):**

```nginx
# nginx/nginx.conf
server {
    listen 443 ssl http2;
    
    # SSL certificates
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

**At Rest (Database):**

MongoDB encryption at rest (Enterprise feature):
```yaml
# mongod.conf
security:
  enableEncryption: true
  encryptionKeyFile: /path/to/keyfile
```

For community edition, use file system encryption:
```bash
# LUKS encryption on Linux
cryptsetup luksFormat /dev/sdb
cryptsetup open /dev/sdb mongodb_encrypted
mkfs.ext4 /dev/mapper/mongodb_encrypted
```

### Sensitive Data Handling

**Don't Store:**
- Credit card numbers (use Stripe tokens)
- Plain text passwords
- API keys in database (use environment variables)
- Social security numbers

**Do Store:**
- Hashed passwords
- Encrypted tokens (if necessary)
- PII with proper encryption

**Sanitize Logs:**

```python
import logging

def sanitize_log_data(data: dict) -> dict:
    """Remove sensitive data from logs"""
    sensitive_fields = ['password', 'api_key', 'token', 'ssn']
    sanitized = data.copy()
    
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = '***REDACTED***'
    
    return sanitized

# Usage
logger.info(f"User data: {sanitize_log_data(user_dict)}")
```

---

## API Security

### Input Validation

**Pydantic Models:**

```python
from pydantic import BaseModel, validator, Field
from typing import Optional

class ChatbotCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., regex="^(gpt-4o|gpt-4o-mini|claude-3-5-sonnet|gemini-2.0-flash)$")
    system_message: Optional[str] = Field(None, max_length=5000)
    
    @validator('name')
    def validate_name(cls, v):
        # Remove potentially dangerous characters
        if any(char in v for char in ['<', '>', '{', '}', '`']):
            raise ValueError('Name contains invalid characters')
        return v
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

# Strict CORS in production
if os.environ.get("ENVIRONMENT") == "production":
    allowed_origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]
else:
    allowed_origins = ["*"]  # Only for development!

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)
```

### Rate Limiting

**Implementation:**

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests: int = 60, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)
    
    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.clients[client_ip]) >= self.requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."}
            )
        
        self.clients[client_ip].append(now)
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests - len(self.clients[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(now + self.window)
        )
        
        return response

# Apply middleware
app.middleware("http")(RateLimiter(requests=60, window=60))
```

### Security Headers

```python
from fastapi import Response

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
        "style-src 'self' 'unsafe-inline' https:; "
        "img-src 'self' data: https:; "
        "font-src 'self' data: https:; "
        "connect-src 'self' https:; "
    )
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions Policy
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=()"
    )
    
    return response
```

---

## File Upload Security

### File Validation

```python
from fastapi import UploadFile, HTTPException
import magic
import os

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.csv'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

async def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Check MIME type (prevent extension spoofing)
    file_content = await file.read(2048)
    file.file.seek(0)
    
    mime = magic.from_buffer(file_content, mime=True)
    allowed_mimes = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv'
    }
    
    if mime not in allowed_mimes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {mime}"
        )
    
    return True

async def save_file_securely(file: UploadFile) -> str:
    """Save file with secure filename"""
    import uuid
    
    # Validate file
    await validate_file(file)
    
    # Generate secure filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    secure_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Save to secure directory
    upload_dir = "/app/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, secure_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Set proper permissions (read-only)
    os.chmod(file_path, 0o444)
    
    return file_path
```

### Virus Scanning

**ClamAV Integration:**

```python
import clamd

def scan_file_for_viruses(file_path: str) -> bool:
    """Scan file for viruses using ClamAV"""
    try:
        cd = clamd.ClamdUnixSocket()
        result = cd.scan(file_path)
        
        if result[file_path][0] == 'OK':
            return True
        else:
            # Virus found, delete file
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="File contains malicious content"
            )
    except Exception as e:
        logger.error(f"Virus scan failed: {str(e)}")
        # Fail secure - reject file
        return False
```

---

## Database Security

### MongoDB Security

**Authentication:**

```javascript
// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "strong_password_here",
  roles: ["root"]
})

// Create application user
use botsmith
db.createUser({
  user: "botsmith_app",
  pwd: "app_password_here",
  roles: [
    { role: "readWrite", db: "botsmith" }
  ]
})
```

**Connection String:**

```bash
# With authentication
MONGO_URL=mongodb://botsmith_app:app_password@localhost:27017/botsmith?authSource=botsmith
```

**Network Security:**

```yaml
# mongod.conf
net:
  bindIp: 127.0.0.1  # Only localhost
  port: 27017

security:
  authorization: enabled
```

### Query Security

**Prevent NoSQL Injection:**

```python
# Bad - vulnerable to injection
chatbot_id = request.query_params.get('id')
chatbot = await db.chatbots.find_one({"id": chatbot_id})

# Good - use Pydantic validation
class ChatbotQuery(BaseModel):
    id: str = Field(..., regex="^[a-f0-9-]{36}$")

@router.get("/chatbots/{chatbot_id}")
async def get_chatbot(chatbot_id: str):
    # Validate UUID format
    try:
        uuid.UUID(chatbot_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    chatbot = await db.chatbots.find_one({"id": chatbot_id})
    return chatbot
```

### Data Sanitization

```python
from bleach import clean

def sanitize_html(text: str) -> str:
    """Remove potentially dangerous HTML"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u']
    return clean(text, tags=allowed_tags, strip=True)

def sanitize_user_input(data: dict) -> dict:
    """Sanitize all string fields in user input"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Remove null bytes
            value = value.replace('\\x00', '')
            # Limit length
            value = value[:10000]
            # Remove control characters
            value = ''.join(char for char in value if char.isprintable() or char in '\\n\\r\\t')
        sanitized[key] = value
    return sanitized
```

---

## Infrastructure Security

### Firewall Configuration

**UFW (Ubuntu):**

```bash
# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### Docker Security

**Best Practices:**

```dockerfile
# Use specific versions, not 'latest'
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser . .

# Set read-only filesystem where possible
VOLUME /app/uploads

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8001/health || exit 1
```

**Docker Compose Security:**

```yaml
services:
  backend:
    # Limit resources
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          memory: 512M
    
    # Security options
    security_opt:
      - no-new-privileges:true
    
    # Read-only root filesystem
    read_only: true
    tmpfs:
      - /tmp
    
    # Drop capabilities
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Environment Variables

**Never Commit:**

```bash
# .gitignore
.env
.env.local
.env.production
*.key
*.pem
secrets/
```

**Use Secrets Management:**

```yaml
# docker-compose.yml with secrets
services:
  backend:
    secrets:
      - mongo_password
      - emergent_llm_key
    environment:
      MONGO_PASSWORD_FILE: /run/secrets/mongo_password
      EMERGENT_LLM_KEY_FILE: /run/secrets/emergent_llm_key

secrets:
  mongo_password:
    file: ./secrets/mongo_password.txt
  emergent_llm_key:
    file: ./secrets/emergent_llm_key.txt
```

---

## Security Best Practices

### Development

- [ ] Never commit secrets to version control
- [ ] Use environment variables for configuration
- [ ] Keep dependencies updated
- [ ] Run security linters (Bandit for Python)
- [ ] Use HTTPS in development
- [ ] Implement proper logging (without sensitive data)
- [ ] Regular code reviews
- [ ] Use virtual environments

### Production

- [ ] Enable HTTPS/TLS
- [ ] Use strong passwords (16+ characters)
- [ ] Implement rate limiting
- [ ] Enable firewall
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Backup encryption keys securely
- [ ] Use intrusion detection (fail2ban)
- [ ] Regular security audits
- [ ] Implement monitoring and alerting

### API Keys

- [ ] Rotate keys regularly (every 90 days)
- [ ] Use different keys for dev/staging/prod
- [ ] Never expose keys in client-side code
- [ ] Implement key revocation
- [ ] Monitor key usage
- [ ] Use key restrictions (IP whitelist, domain restrictions)

### User Data

- [ ] Collect only necessary data
- [ ] Implement data retention policy
- [ ] Provide data export
- [ ] Implement right to be forgotten
- [ ] Encrypt sensitive data
- [ ] Pseudonymize where possible
- [ ] Regular privacy audits

---

## Vulnerability Reporting

### Responsible Disclosure

We take security seriously. If you discover a security vulnerability:

**DO:**
- Report privately to security@botsmith.ai
- Provide detailed description
- Include steps to reproduce
- Give us time to fix (90 days)
- Work with us on disclosure

**DON'T:**
- Publicly disclose before fix
- Test on production systems
- Access user data
- Perform DoS attacks
- Demand payment

### Report Template

```
Subject: [SECURITY] Vulnerability in BotSmith

Vulnerability Type: [e.g., SQL Injection, XSS, Authentication Bypass]

Affected Component: [e.g., User Login, File Upload]

Description:
[Detailed description of the vulnerability]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Impact:
[What can an attacker do with this vulnerability?]

Suggested Fix:
[Optional: Your suggestions for fixing the issue]

Contact:
[Your name and email for follow-up]
```

### Bug Bounty

We offer rewards for valid security vulnerabilities:

- **Critical**: $500-$2000
- **High**: $200-$500
- **Medium**: $50-$200
- **Low**: Recognition + Swag

---

## Security Checklist

### Pre-Deployment

- [ ] All secrets in environment variables
- [ ] HTTPS/TLS enabled
- [ ] Strong passwords set
- [ ] Database authentication enabled
- [ ] Firewall configured
- [ ] Security headers enabled
- [ ] Rate limiting enabled
- [ ] File upload validation implemented
- [ ] Input validation on all endpoints
- [ ] CORS configured properly
- [ ] Monitoring and logging enabled

### Post-Deployment

- [ ] SSL certificate valid and auto-renewing
- [ ] Regular backups configured
- [ ] Security monitoring active
- [ ] Log analysis set up
- [ ] Intrusion detection active
- [ ] Regular security updates scheduled
- [ ] Incident response plan documented
- [ ] Team trained on security practices

### Regular Tasks

**Daily:**
- [ ] Review error logs
- [ ] Check failed login attempts

**Weekly:**
- [ ] Review access logs
- [ ] Check for suspicious activity
- [ ] Update dependencies

**Monthly:**
- [ ] Security audit
- [ ] Review access permissions
- [ ] Test backup restoration
- [ ] Update documentation

**Quarterly:**
- [ ] Penetration testing
- [ ] Code security review
- [ ] Rotate API keys
- [ ] Update security policies

---

## Compliance

### GDPR Compliance

- [ ] Privacy policy
- [ ] Data processing agreement
- [ ] User consent mechanism
- [ ] Right to access data
- [ ] Right to deletion
- [ ] Data portability
- [ ] Breach notification process

### SOC 2 Compliance

- [ ] Access controls
- [ ] Encryption (transit and rest)
- [ ] Monitoring and logging
- [ ] Incident response
- [ ] Change management
- [ ] Vendor management
- [ ] Regular audits

---

## Security Tools

### Recommended Tools

**Static Analysis:**
- Bandit (Python)
- ESLint security plugins (JavaScript)
- Safety (Python dependencies)
- npm audit (Node dependencies)

**Dynamic Analysis:**
- OWASP ZAP
- Burp Suite
- sqlmap (if using SQL)

**Monitoring:**
- Sentry (Error tracking)
- Datadog (Infrastructure)
- CloudFlare (DDoS protection)
- fail2ban (Intrusion prevention)

**Secrets Scanning:**
- GitGuardian
- TruffleHog
- git-secrets

---

## Contact

For security concerns:
- **Email**: security@botsmith.ai
- **PGP Key**: [Link to public key]
- **Response Time**: Within 24 hours

---

**Last Updated**: January 2025  
**Version**: 1.0
