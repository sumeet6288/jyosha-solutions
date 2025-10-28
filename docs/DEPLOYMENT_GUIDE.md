# 🚀 BotSmith Deployment Guide

## Table of Contents
1. [Deployment Options](#deployment-options)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Checklist](#production-checklist)
6. [Monitoring & Logging](#monitoring--logging)
7. [Backup & Recovery](#backup--recovery)
8. [Scaling](#scaling)
9. [Security](#security)
10. [Troubleshooting](#troubleshooting)

---

## Deployment Options

### 1. Docker Deployment (Recommended)
- ✅ Consistent environment
- ✅ Easy scaling
- ✅ Simplified management
- Best for: Most production deployments

### 2. Cloud Platforms
- **AWS**: EC2, ECS, or Elastic Beanstalk
- **Google Cloud**: Cloud Run, GKE
- **Azure**: App Service, AKS
- **DigitalOcean**: Droplets, App Platform

### 3. Traditional VPS
- Ubuntu 22.04 LTS
- Manual setup
- Full control

---

## Environment Configuration

### Production Environment Variables

**Backend `.env`:**
```env
# Database
MONGO_URL=mongodb://mongo_user:mongo_password@mongodb:27017/botsmith?authSource=admin

# AI Integration
EMERGENT_LLM_KEY=your_production_key_here

# Or individual keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Security
SECRET_KEY=your_secure_random_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# File Upload
MAX_UPLOAD_SIZE=104857600  # 100MB in bytes
UPLOAD_DIR=/app/uploads

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your_smtp_password
FROM_EMAIL=noreply@yourdomain.com

# Environment
ENVIRONMENT=production
DEBUG=false
```

**Frontend `.env`:**
```env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
REACT_APP_ENABLE_VISUAL_EDITS=false
```

### Generating Secure Keys

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate random password
openssl rand -base64 24
```

---

## Docker Deployment

### 1. Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install emergentintegrations
RUN pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Start server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 2. Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy application
COPY . .

# Build
RUN yarn build

# Production stage
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Create nginx.conf

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 4. Create docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: botsmith-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
      MONGO_INITDB_DATABASE: botsmith
    volumes:
      - mongodb_data:/data/db
      - ./mongodb-init.js:/docker-entrypoint-initdb.d/init.js:ro
    networks:
      - botsmith-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongo localhost:27017/botsmith --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: botsmith-backend
    restart: unless-stopped
    environment:
      MONGO_URL: mongodb://admin:${MONGO_PASSWORD}@mongodb:27017/botsmith?authSource=admin
      EMERGENT_LLM_KEY: ${EMERGENT_LLM_KEY}
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
    volumes:
      - uploads:/app/uploads
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - botsmith-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        REACT_APP_BACKEND_URL: https://api.${DOMAIN}
    container_name: botsmith-frontend
    restart: unless-stopped
    depends_on:
      - backend
    networks:
      - botsmith-network
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: botsmith-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - certbot_data:/var/www/certbot:ro
    depends_on:
      - frontend
      - backend
    networks:
      - botsmith-network

  certbot:
    image: certbot/certbot
    container_name: botsmith-certbot
    volumes:
      - certbot_data:/var/www/certbot
      - ./nginx/ssl:/etc/letsencrypt
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  mongodb_data:
    driver: local
  uploads:
    driver: local
  certbot_data:
    driver: local

networks:
  botsmith-network:
    driver: bridge
```

### 5. Create .env file

```bash
# .env
MONGO_PASSWORD=your_secure_mongo_password
EMERGENT_LLM_KEY=your_emergent_key
SECRET_KEY=your_secret_key_from_openssl
DOMAIN=yourdomain.com
```

### 6. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (data loss!)
docker-compose down -v
```

---

## Cloud Deployment

### AWS Deployment (EC2)

**1. Launch EC2 Instance:**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium (minimum)
- Storage: 30GB SSD
- Security Group:
  - Port 22 (SSH)
  - Port 80 (HTTP)
  - Port 443 (HTTPS)

**2. Connect and Setup:**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <your-repo-url>
cd botsmith

# Create .env file
nano .env
# (Add your environment variables)

# Deploy
docker-compose up -d --build
```

**3. Configure Domain:**

- Point your domain A record to EC2 Elastic IP
- Wait for DNS propagation

**4. Setup SSL:**

```bash
# Install Certbot
sudo snap install --classic certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Google Cloud Run

**1. Prepare Backend:**

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/botsmith-backend backend/

# Deploy
gcloud run deploy botsmith-backend \
  --image gcr.io/PROJECT_ID/botsmith-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MONGO_URL=your_mongo_url,EMERGENT_LLM_KEY=your_key"
```

**2. Deploy Frontend:**

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/botsmith-frontend frontend/

# Deploy
gcloud run deploy botsmith-frontend \
  --image gcr.io/PROJECT_ID/botsmith-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### DigitalOcean App Platform

**1. Create `app.yaml`:**

```yaml
name: botsmith
region: nyc

services:
  - name: backend
    build_command: pip install -r requirements.txt
    run_command: uvicorn server:app --host 0.0.0.0 --port 8001
    source_dir: backend
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: MONGO_URL
        value: ${MONGO_URL}
      - key: EMERGENT_LLM_KEY
        value: ${EMERGENT_LLM_KEY}
    routes:
      - path: /api

  - name: frontend
    build_command: yarn build
    source_dir: frontend
    environment_slug: node-js
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: REACT_APP_BACKEND_URL
        value: ${APP_URL}/api
    routes:
      - path: /

databases:
  - name: mongodb
    engine: MONGODB
    version: "6.0"
```

**2. Deploy:**

```bash
# Install doctl
brew install doctl  # macOS
# or download from DigitalOcean

# Authenticate
doctl auth init

# Deploy
doctl apps create --spec app.yaml
```

---

## Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set secure headers
- [ ] Enable rate limiting
- [ ] Review file upload restrictions
- [ ] Implement API authentication
- [ ] Setup firewall rules
- [ ] Regular security updates

### Performance
- [ ] Enable gzip compression
- [ ] Configure caching
- [ ] Optimize database indexes
- [ ] Use CDN for static assets
- [ ] Enable database connection pooling
- [ ] Configure proper timeouts
- [ ] Setup load balancing (if needed)

### Monitoring
- [ ] Setup application monitoring
- [ ] Configure error tracking (Sentry)
- [ ] Enable logging
- [ ] Setup uptime monitoring
- [ ] Configure alerts
- [ ] Monitor resource usage

### Database
- [ ] Setup automated backups
- [ ] Test backup restoration
- [ ] Enable authentication
- [ ] Configure replica set (production)
- [ ] Setup monitoring
- [ ] Plan scaling strategy

### Documentation
- [ ] Update API documentation
- [ ] Document deployment process
- [ ] Create runbook for incidents
- [ ] Document environment variables
- [ ] Setup change log

---

## Monitoring & Logging

### Application Monitoring

**1. Sentry (Error Tracking):**

```python
# backend/server.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    environment="production",
    traces_sample_rate=0.1
)
```

**2. Prometheus Metrics:**

```python
# Install prometheus client
pip install prometheus-client

# Add metrics endpoint
from prometheus_client import Counter, generate_latest

request_count = Counter('http_requests_total', 'Total HTTP requests')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Logging Configuration

```python
# backend/server.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"User {user_id} created chatbot {chatbot_id}")
logger.error(f"Failed to process file: {str(e)}")
```

### Uptime Monitoring

**Use services like:**
- UptimeRobot (Free)
- Pingdom
- StatusCake
- DataDog

**Configure endpoints:**
- Frontend: `https://yourdomain.com/`
- Backend: `https://api.yourdomain.com/health`
- Check interval: 5 minutes

---

## Backup & Recovery

### MongoDB Backup

**1. Automated Daily Backup:**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"
MONGO_URI="mongodb://user:password@localhost:27017/botsmith"

# Create backup
mongodump --uri="$MONGO_URI" --out="$BACKUP_DIR/$DATE"

# Compress
tar -czf "$BACKUP_DIR/$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Delete backups older than 30 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE.tar.gz"
```

**2. Setup Cron:**

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup.sh >> /var/log/mongodb-backup.log 2>&1
```

**3. Restore from Backup:**

```bash
# Extract backup
tar -xzf backup_20250128_020000.tar.gz

# Restore
mongorestore --uri="mongodb://user:password@localhost:27017/botsmith" backup_20250128_020000/
```

### File Uploads Backup

```bash
# Sync uploads to S3
aws s3 sync /app/uploads s3://your-bucket/backups/uploads/

# Or use rsync to remote server
rsync -avz /app/uploads/ user@backup-server:/backups/uploads/
```

---

## Scaling

### Horizontal Scaling

**1. Multiple Backend Instances:**

```yaml
# docker-compose.yml
services:
  backend:
    # ... existing config
    deploy:
      replicas: 3
```

**2. Load Balancer Configuration:**

```nginx
# nginx/nginx.conf
upstream backend {
    least_conn;
    server backend1:8001;
    server backend2:8001;
    server backend3:8001;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

### Database Scaling

**MongoDB Replica Set:**

```yaml
# docker-compose.yml
services:
  mongodb-primary:
    image: mongo:6.0
    command: mongod --replSet rs0
    
  mongodb-secondary1:
    image: mongo:6.0
    command: mongod --replSet rs0
    
  mongodb-secondary2:
    image: mongo:6.0
    command: mongod --replSet rs0
```

**Initialize Replica Set:**

```javascript
// Connect to primary
mongo

// Initialize
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb-primary:27017" },
    { _id: 1, host: "mongodb-secondary1:27017" },
    { _id: 2, host: "mongodb-secondary2:27017" }
  ]
})
```

### Caching Layer

**Redis for Session/Cache:**

```yaml
services:
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
```

**Backend Integration:**

```python
import redis
import os

redis_client = redis.Redis(
    host='redis',
    port=6379,
    password=os.environ.get('REDIS_PASSWORD'),
    decode_responses=True
)

# Cache chatbot data
async def get_chatbot_cached(chatbot_id: str):
    cached = redis_client.get(f"chatbot:{chatbot_id}")
    if cached:
        return json.loads(cached)
    
    chatbot = await db.chatbots.find_one({"id": chatbot_id})
    redis_client.setex(
        f"chatbot:{chatbot_id}",
        3600,  # 1 hour TTL
        json.dumps(chatbot)
    )
    return chatbot
```

---

## Security

### SSL/TLS Configuration

**Nginx SSL Configuration:**

```nginx
# nginx/nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:;" always;

    location / {
        proxy_pass http://frontend;
    }

    location /api {
        proxy_pass http://backend:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Rate Limiting

```python
# backend/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import time

# Simple in-memory rate limiter
rate_limit_data = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # Clean old requests (older than 1 minute)
    rate_limit_data[client_ip] = [
        req_time for req_time in rate_limit_data[client_ip]
        if now - req_time < 60
    ]
    
    # Check rate limit (60 requests per minute)
    if len(rate_limit_data[client_ip]) >= 60:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )
    
    rate_limit_data[client_ip].append(now)
    response = await call_next(request)
    return response

# Add to server.py
app.middleware("http")(rate_limit_middleware)
```

### Environment Variable Management

**Use secrets management:**
- **AWS**: Secrets Manager
- **Google Cloud**: Secret Manager
- **Azure**: Key Vault
- **HashiCorp Vault**

```python
# Example: AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret('botsmith/production')
EMERGENT_LLM_KEY = secrets['emergent_llm_key']
SECRET_KEY = secrets['secret_key']
```

---

## Troubleshooting

### Common Production Issues

**1. High Memory Usage**

```bash
# Check memory
docker stats

# Limit container memory
docker-compose.yml:
  backend:
    mem_limit: 1g
    mem_reservation: 512m
```

**2. Slow Database Queries**

```javascript
// Create indexes
db.chatbots.createIndex({ "user_id": 1 })
db.conversations.createIndex({ "chatbot_id": 1, "started_at": -1 })
db.messages.createIndex({ "conversation_id": 1, "created_at": 1 })

// Check slow queries
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

**3. Container Health Issues**

```bash
# Check container logs
docker-compose logs -f backend

# Restart specific service
docker-compose restart backend

# Recreate container
docker-compose up -d --force-recreate backend
```

**4. SSL Certificate Issues**

```bash
# Test certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Renew certificate
sudo certbot renew --force-renewal

# Check expiration
sudo certbot certificates
```

### Emergency Procedures

**1. Database Corruption:**

```bash
# Stop services
docker-compose down

# Repair database
docker run -it --rm -v mongodb_data:/data/db mongo:6.0 mongod --repair

# Restore from backup if repair fails
mongorestore --uri="mongodb://..." backup/
```

**2. Out of Disk Space:**

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes

# Remove old logs
sudo journalctl --vacuum-time=7d
```

**3. Service Crash Loop:**

```bash
# Check logs
docker-compose logs --tail=100 backend

# Restart with fresh container
docker-compose down
docker-compose up -d --force-recreate

# Rollback to previous version if needed
git checkout <previous-commit>
docker-compose up -d --build
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check uptime status
- Review key metrics

**Weekly:**
- Review database performance
- Check disk space
- Analyze slow queries
- Review user feedback

**Monthly:**
- Security updates
- Database optimization
- Backup verification
- Review and update documentation
- Capacity planning

### Update Procedure

```bash
# 1. Backup everything
./backup.sh

# 2. Pull latest code
git pull origin main

# 3. Rebuild and restart
docker-compose down
docker-compose up -d --build

# 4. Monitor logs
docker-compose logs -f

# 5. Test critical features
curl https://api.yourdomain.com/health

# 6. Rollback if issues
git checkout <previous-commit>
docker-compose up -d --build
```

---

**Deployment Support:** deployment@botsmith.ai
