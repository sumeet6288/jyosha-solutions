# Lemon Squeezy Integration Guide

## Overview
This application integrates with Lemon Squeezy for subscription payment processing. This guide covers the complete setup and configuration.

## Current Configuration

### Subscription Plans

The application offers 4 subscription tiers:

#### 1. Free Plan
- **Price**: ₹0/month
- **Features**:
  - 1 chatbot
  - 100 messages/month
  - 5 file uploads (max 10MB each)
  - 2 website sources
  - 5 text sources
  - 50 leads
  - 7 days conversation history
  - Basic analytics
  - Community support
  - OpenAI models only

#### 2. Starter Plan (Lemon Squeezy Integrated)
- **Price**: ₹7,999/month
- **Variant ID**: `1052931` (Update in production)
- **Features**:
  - 5 chatbots
  - 15,000 messages/month
  - 20 file uploads (max 50MB each)
  - 10 website sources
  - 20 text sources
  - 100 leads
  - 30 days conversation history
  - Advanced analytics
  - Priority support
  - Custom branding
  - API access
  - OpenAI + Anthropic models

#### 3. Professional Plan (Lemon Squeezy Integrated)
- **Price**: ₹24,999/month
- **Variant ID**: `1052933` (Update in production)
- **Features**:
  - 25 chatbots
  - 1,25,000 messages/month
  - 100 file uploads (max 100MB each)
  - 50 website sources
  - 100 text sources
  - 1,000 leads
  - 90 days conversation history
  - Advanced analytics
  - 24/7 priority support
  - Custom branding
  - Full API access
  - All AI models (OpenAI + Anthropic + Google)
  - Custom integrations
  - Dedicated account manager

#### 4. Enterprise Plan (Custom)
- **Price**: Custom pricing
- **Contact**: Contact sales team
- **Features**:
  - Unlimited chatbots
  - Unlimited messages
  - Unlimited file uploads
  - Unlimited sources
  - Unlimited leads
  - Unlimited conversation history
  - Custom analytics
  - Dedicated 24/7 support
  - White-label solution
  - Custom AI model training
  - On-premise deployment
  - SLA guarantee
  - Custom contracts
  - Enterprise security

---

## Environment Variables Setup

### Backend (.env file location: `/app/backend/.env`)

Add these environment variables:

```bash
# Lemon Squeezy Configuration
LEMONSQUEEZY_API_KEY=your_api_key_here
LEMONSQUEEZY_STORE_ID=your_store_id_here
LEMONSQUEEZY_SIGNING_SECRET=your_webhook_signing_secret_here
```

### Where to Get These Values:

1. **LEMONSQUEEZY_API_KEY**:
   - Login to Lemon Squeezy dashboard
   - Go to Settings → API
   - Create a new API key
   - Copy the key

2. **LEMONSQUEEZY_STORE_ID**:
   - Go to Settings → Stores
   - Copy your Store ID

3. **LEMONSQUEEZY_SIGNING_SECRET**:
   - Go to Settings → Webhooks
   - Create a new webhook
   - Copy the signing secret

---

## Lemon Squeezy Dashboard Setup

### Step 1: Create Products

1. Login to Lemon Squeezy
2. Go to Products → Create Product
3. Create two products:

   **Starter Plan Product**:
   - Name: "Starter Plan"
   - Price: ₹7,999
   - Billing Cycle: Monthly
   - Description: "For growing businesses"

   **Professional Plan Product**:
   - Name: "Professional Plan"
   - Price: ₹24,999
   - Billing Cycle: Monthly
   - Description: "For large teams & high volume"

### Step 2: Get Variant IDs

1. After creating products, go to each product
2. Copy the Variant ID
3. Update in `/app/backend/routers/lemonsqueezy.py`:

```python
VARIANT_IDS = {
    "starter": "YOUR_STARTER_VARIANT_ID",      # Replace with actual ID
    "professional": "YOUR_PROFESSIONAL_VARIANT_ID"  # Replace with actual ID
}
```

### Step 3: Configure Webhooks

1. Go to Settings → Webhooks
2. Create a new webhook with URL:
   ```
   https://your-domain.com/api/lemonsqueezy/webhook
   ```

3. Subscribe to these events:
   - ✅ subscription_created
   - ✅ subscription_updated
   - ✅ subscription_payment_success
   - ✅ subscription_cancelled
   - ✅ subscription_expired
   - ✅ order_created

4. Copy the Signing Secret and add to `.env` file

---

## API Endpoints

### 1. Create Checkout Session
**Endpoint**: `POST /api/lemonsqueezy/checkout/create`

**Request Body**:
```json
{
  "plan": "starter",  // or "professional"
  "user_id": "user123",
  "user_email": "user@example.com"
}
```

**Response**:
```json
{
  "checkout_url": "https://checkout.lemonsqueezy.com/...",
  "message": "Checkout created successfully"
}
```

### 2. Get Available Plans
**Endpoint**: `GET /api/lemonsqueezy/plans`

**Response**:
```json
{
  "plans": [
    {
      "id": "starter",
      "name": "Starter",
      "price": 7999,
      "currency": "INR",
      "interval": "month",
      "variant_id": "1052931",
      "description": "For growing businesses",
      "features": [...],
      "limits": {...}
    },
    {
      "id": "professional",
      "name": "Professional",
      "price": 24999,
      "currency": "INR",
      "interval": "month",
      "variant_id": "1052933",
      "description": "For large teams & high volume",
      "features": [...],
      "limits": {...}
    }
  ],
  "note": "Enterprise plan with custom pricing available - contact sales"
}
```

### 3. Get Subscription Status
**Endpoint**: `GET /api/lemonsqueezy/subscription/status`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "has_subscription": true,
  "plan": "Starter Plan",
  "status": "active",
  "renews_at": "2025-12-13T10:29:52.174Z",
  "ends_at": null,
  "subscription_id": "12345"
}
```

### 4. Manual Subscription Sync
**Endpoint**: `POST /api/lemonsqueezy/subscription/sync`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "plan": "starter",
  "plan_name": "Starter Plan",
  "status": "active",
  "message": "Successfully synced starter subscription"
}
```

### 5. Webhook Receiver
**Endpoint**: `POST /api/lemonsqueezy/webhook`

**Headers**: `X-Signature: <webhook_signature>`

This endpoint receives and processes webhook events from Lemon Squeezy automatically.

---

## Frontend Integration

### Upgrade Flow

The upgrade flow is handled in `/app/frontend/src/pages/Subscription.jsx`:

1. User clicks "Upgrade" button on a plan
2. Frontend sends request to create checkout session
3. User is redirected to Lemon Squeezy checkout
4. After payment, user is redirected back with success parameter
5. Frontend shows success message and syncs subscription

### Subscription Sync Button

There's a "Sync" button in the subscription page that manually syncs the subscription from Lemon Squeezy. This is useful when:
- Webhooks are not configured
- User made payment but subscription not reflecting
- Testing purposes

---

## Database Schema

### Subscriptions Collection

```javascript
{
  "user_id": "user123",
  "plan_id": "starter",  // "free", "starter", "professional", "enterprise"
  "lemonsqueezy_subscription_id": "12345",
  "status": "active",  // "active", "cancelled", "expired"
  "variant_id": "1052931",
  "product_id": "67890",
  "plan_name": "Starter Plan",
  "price": 7999,
  "renews_at": "2025-12-13T10:29:52.174Z",
  "ends_at": null,
  "started_at": "2025-11-13T10:29:52.174Z",
  "created_at": "2025-11-13T10:29:52.174Z",
  "updated_at": "2025-11-13T10:29:52.174Z",
  "auto_renew": true,
  "usage": {
    "chatbots_count": 2,
    "messages_this_month": 150,
    "file_uploads_count": 5,
    "website_sources_count": 3,
    "text_sources_count": 8,
    "last_reset": "2025-11-13T10:29:52.174Z"
  }
}
```

### Webhook Logs Collection

All webhook events are logged for audit purposes:

```javascript
{
  "event_name": "subscription_created",
  "event_id": "evt_abc123",
  "data": {...},  // Full webhook payload
  "received_at": "2025-11-13T10:29:52.174Z",
  "processed": true
}
```

---

## Testing

### Test Mode

Lemon Squeezy provides a test mode. To enable:

1. Go to Settings → General
2. Toggle "Test Mode" on
3. Use test credit cards provided by Lemon Squeezy
4. All subscriptions will be test subscriptions

### Testing Webhooks Locally

For local development, use tools like ngrok:

```bash
# Start ngrok
ngrok http 8001

# Update webhook URL in Lemon Squeezy to:
https://your-ngrok-url.ngrok.io/api/lemonsqueezy/webhook
```

### Manual Testing Flow

1. **Create Checkout**:
   ```bash
   curl -X POST http://localhost:8001/api/lemonsqueezy/checkout/create \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
       "plan": "starter",
       "user_id": "test-user-123",
       "user_email": "test@example.com"
     }'
   ```

2. **Check Subscription Status**:
   ```bash
   curl -X GET http://localhost:8001/api/lemonsqueezy/subscription/status \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Sync Subscription**:
   ```bash
   curl -X POST http://localhost:8001/api/lemonsqueezy/subscription/sync \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

---

## Security Considerations

1. **Webhook Signature Verification**: 
   - All webhooks are verified using HMAC-SHA256
   - Requests without valid signatures are rejected

2. **API Key Protection**:
   - Never commit API keys to git
   - Keep them in `.env` file
   - Use environment variables in production

3. **User Verification**:
   - All endpoints (except webhook) require authentication
   - User ID is passed in checkout custom data

4. **Audit Logging**:
   - All webhook events are logged
   - Failed events are tracked for debugging

---

## Troubleshooting

### Issue: Subscription not syncing after payment

**Solution**:
1. Check if webhooks are configured correctly
2. Verify webhook signing secret is correct
3. Use manual sync button in frontend
4. Check webhook logs in database

### Issue: Invalid signature error

**Solution**:
1. Verify `LEMONSQUEEZY_SIGNING_SECRET` is correct
2. Check webhook configuration in Lemon Squeezy dashboard
3. Ensure webhook URL is accessible from internet

### Issue: Checkout creation fails

**Solution**:
1. Verify `LEMONSQUEEZY_API_KEY` is valid
2. Check `LEMONSQUEEZY_STORE_ID` is correct
3. Ensure variant IDs are updated
4. Check API quota/limits

### Issue: Plan limits not enforcing

**Solution**:
1. Verify subscription is synced in database
2. Check `plan_id` field matches plan limits
3. Restart backend service
4. Check plan service configuration

---

## Production Deployment Checklist

- [ ] Update `VARIANT_IDS` with production variant IDs
- [ ] Configure environment variables in production
- [ ] Set up webhook URL with production domain
- [ ] Verify webhook signature verification works
- [ ] Test complete payment flow in test mode
- [ ] Switch to production mode in Lemon Squeezy
- [ ] Monitor webhook logs for issues
- [ ] Set up alerts for failed payments
- [ ] Configure email notifications
- [ ] Test subscription sync functionality

---

## Support & Resources

- **Lemon Squeezy Docs**: https://docs.lemonsqueezy.com
- **Lemon Squeezy API Reference**: https://docs.lemonsqueezy.com/api
- **Lemon Squeezy Discord**: https://discord.gg/lemonsqueezy

---

## Changelog

### Version 1.0.0 (Current)
- Initial Lemon Squeezy integration
- Support for Starter and Professional plans
- Webhook event processing
- Manual subscription sync
- Complete API documentation
- Plan limits aligned with database configuration

### Future Enhancements
- [ ] Add support for annual billing
- [ ] Implement discount codes
- [ ] Add subscription pause/resume
- [ ] Implement usage-based billing
- [ ] Add subscription downgrade flow
- [ ] Implement refund handling
- [ ] Add subscription analytics
