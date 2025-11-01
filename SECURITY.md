# Security Configuration for BotSmith

## Environment Variables Security

### Backend (.env)
CRITICAL: Never commit these to Git!
- SECRET_KEY: JWT signing key (use 64+ character random string)
- MONGO_URL: Database connection string
- EMERGENT_LLM_KEY: AI provider API key
- CORS_ORIGINS: Comma-separated allowed origins

### Frontend (.env)
- REACT_APP_BACKEND_URL: Backend API URL (safe to commit)

## Rate Limiting

Current limits (per IP):
- 60 requests per minute
- 1000 requests per hour

To adjust: Edit SecurityMiddleware in backend/middleware/security.py

## Security Headers

All responses include:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000
- Content-Security-Policy: (see middleware/security.py)
- Referrer-Policy: strict-origin-when-cross-origin

## Input Validation

Automatically blocks:
- XSS attempts (script tags, javascript:, event handlers)
- SQL injection patterns
- Path traversal attempts (..)
- Hex-encoded attacks

## Authentication

- JWT tokens with 7-day expiration
- Bcrypt password hashing
- HTTP Bearer token scheme
- Mock authentication for development (to be replaced)

## API Security

All API endpoints (except public ones) require:
- Valid JWT token in Authorization header
- Rate limiting enforcement
- Input validation
- CSRF protection (to be implemented)

## File Upload Security

Allowed file types:
- Documents: .txt, .pdf, .doc, .docx, .xls, .xlsx, .csv
- Images: .png, .jpg, .jpeg
- Data: .json, .xml, .md

Max file size: 100MB

File validation:
- No path traversal in filenames
- Extension whitelist enforcement
- Content-type verification

## Database Security

- MongoDB with authentication
- Connection string in environment variable
- No exposed credentials in code
- ObjectId replaced with UUIDs for API responses

## Production Deployment Checklist

Before deploying to production:

1. Environment Variables:
   [ ] Change SECRET_KEY to strong random value
   [ ] Set CORS_ORIGINS to specific domains (not *)
   [ ] Use production MONGO_URL
   [ ] Add EMERGENT_LLM_KEY for AI features

2. Security:
   [ ] Enable HTTPS/TLS
   [ ] Configure firewall rules
   [ ] Set up SSL certificates
   [ ] Enable database authentication
   [ ] Configure backup strategy

3. Application:
   [ ] Run security audit: python backend/security_audit.py
   [ ] Build production frontend: cd frontend && ./build-production.sh
   [ ] Remove mock authentication
   [ ] Enable real user registration/login
   [ ] Test rate limiting
   [ ] Verify CORS settings

4. Monitoring:
   [ ] Set up logging aggregation
   [ ] Configure error tracking
   [ ] Enable performance monitoring
   [ ] Set up security alerts

5. Testing:
   [ ] Run penetration tests
   [ ] Test authentication flows
   [ ] Verify rate limiting
   [ ] Test input validation
   [ ] Check for exposed secrets

## Security Audit

Run security audit before each deployment:
```bash
cd /app/backend
python security_audit.py
```

This checks for:
- Exposed API keys and secrets
- Missing security headers
- Insecure CORS configuration
- Environment variable issues

## Incident Response

If a security issue is discovered:

1. Immediate Actions:
   - Rotate all API keys and secrets
   - Reset all user passwords
   - Enable additional logging
   - Block suspicious IPs

2. Investigation:
   - Review logs for unauthorized access
   - Check database for data breaches
   - Analyze API usage patterns
   - Document the incident

3. Remediation:
   - Apply security patches
   - Update dependencies
   - Enhance validation rules
   - Deploy fixes

4. Post-Incident:
   - Conduct security review
   - Update documentation
   - Train team on new procedures
   - Implement additional monitoring

## Contact

For security issues, contact: security@botsmith.ai
