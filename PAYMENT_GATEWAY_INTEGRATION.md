# Payment Gateway Settings - LemonSqueezy Integration

## Overview
Added a comprehensive Payment Gateway Settings tab in the Admin Panel to manage LemonSqueezy integration for subscription payments.

## Features Implemented

### 1. Backend Implementation

#### File: `/app/backend/routers/payment_settings.py`
- **Complete CRUD API for payment gateway settings**
- MongoDB storage for persistent configuration
- Real-time connection testing with LemonSqueezy API

**API Endpoints:**
- `GET /api/admin/payment-settings` - Retrieve current settings
- `PUT /api/admin/payment-settings` - Update settings
- `POST /api/admin/payment-settings/test` - Test LemonSqueezy connection
- `DELETE /api/admin/payment-settings` - Reset to defaults

**Features:**
- Secure API key storage
- Connection validation
- Store information retrieval
- Automatic timestamps and audit trail

### 2. Frontend Implementation

#### File: `/app/frontend/src/components/admin/PaymentGatewaySettings.jsx`
Comprehensive UI component with the following features:

**Configuration Fields:**
1. **Enable/Disable Toggle** - Activate LemonSqueezy integration
2. **API Key** - Secure input with show/hide and copy functionality
3. **Store ID** - LemonSqueezy store identifier
4. **Webhook URL** - Auto-generated webhook endpoint
5. **Webhook Secret** - Signing secret for webhook verification
6. **Plan ID Mapping** - Map LemonSqueezy variant IDs to plans:
   - Free Plan ID
   - Starter Plan ID
   - Professional Plan ID
   - Enterprise Plan ID

**UI Features:**
- Password-style inputs with show/hide toggle
- Copy to clipboard functionality
- Real-time connection testing
- Success/error status indicators
- Comprehensive setup instructions
- Direct links to LemonSqueezy dashboard
- Gradient purple/pink theme matching app design
- Responsive and accessible design

**Interactive Elements:**
- Test Connection button validates credentials
- Automatic webhook URL generation
- Step-by-step setup instructions
- Color-coded status indicators (green for success, red for errors)
- Loading states for async operations

### 3. Admin Dashboard Integration

#### Files Modified:
- `/app/frontend/src/pages/admin/AdminDashboard.jsx`
- `/app/frontend/src/components/admin/AdminSidebar.jsx`
- `/app/backend/server.py`

**Changes:**
1. Added "Payment Gateway" tab to admin sidebar with CreditCard icon
2. Registered payment_settings router in main server
3. Integrated PaymentGatewaySettings component in dashboard

## Setup Instructions

### For Administrators:

1. **Access Payment Gateway Settings**
   - Login as admin: `admin@botsmith.com` / `admin123`
   - Navigate to Admin Panel
   - Click on "Payment Gateway" in the sidebar

2. **Configure LemonSqueezy**
   - Get your API key from: https://app.lemonsqueezy.com/settings/api
   - Find your Store ID from: https://app.lemonsqueezy.com/settings/stores
   - Enter both credentials and click "Test Connection"

3. **Setup Webhook**
   - Copy the generated webhook URL
   - Go to: https://app.lemonsqueezy.com/settings/webhooks
   - Create new webhook with the copied URL
   - Select events: `order_created`, `subscription_created`, `subscription_updated`, `subscription_cancelled`
   - Copy the signing secret and paste in the "Webhook Signing Secret" field

4. **Map Plan IDs**
   - Go to your LemonSqueezy products
   - Copy the Variant ID for each subscription tier
   - Paste them in the corresponding plan fields:
     - Starter → Starter Plan ID
     - Professional → Professional Plan ID
     - Enterprise → Enterprise Plan ID
   - Free plan ID is optional

5. **Enable Integration**
   - Toggle the "Enable" switch to ON
   - Click "Save Settings"

## Database Schema

### Collection: `payment_settings`
```javascript
{
  "lemonsqueezy": {
    "enabled": Boolean,
    "api_key": String,
    "store_id": String,
    "webhook_url": String,
    "webhook_secret": String,
    "plans": {
      "free": String,
      "starter": String,
      "professional": String,
      "enterprise": String
    }
  },
  "updated_at": DateTime,
  "updated_by": String (user_id)
}
```

## Security Features

1. **Secure Storage**
   - API keys and secrets stored in MongoDB
   - Password-style inputs prevent shoulder surfing
   - Copy functionality with temporary confirmation

2. **Validation**
   - Real-time connection testing before saving
   - Required field validation
   - Error handling with user-friendly messages

3. **Access Control**
   - Admin-only access via admin panel
   - Audit trail with timestamps and user IDs

## API Usage Examples

### Get Current Settings
```bash
curl -X GET http://localhost:8001/api/admin/payment-settings
```

### Update Settings
```bash
curl -X PUT http://localhost:8001/api/admin/payment-settings \
  -H "Content-Type: application/json" \
  -d '{
    "lemonsqueezy": {
      "enabled": true,
      "api_key": "your-api-key",
      "store_id": "12345",
      "webhook_secret": "your-webhook-secret",
      "plans": {
        "starter": "variant_123",
        "professional": "variant_456",
        "enterprise": "variant_789"
      }
    }
  }'
```

### Test Connection
```bash
curl -X POST http://localhost:8001/api/admin/payment-settings/test \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "your-api-key",
    "store_id": "12345"
  }'
```

## Webhook Endpoint

**URL:** `{BACKEND_URL}/api/webhooks/lemonsqueezy`

This endpoint will receive webhook events from LemonSqueezy for:
- New subscriptions
- Subscription updates
- Subscription cancellations
- Payment confirmations

## Future Enhancements

1. **Multiple Payment Gateways**
   - Add Stripe integration
   - Add PayPal integration
   - Add Paddle integration

2. **Advanced Features**
   - Automatic subscription sync
   - Payment history tracking
   - Failed payment handling
   - Dunning management
   - Revenue analytics

3. **Testing Tools**
   - Webhook testing interface
   - Sandbox mode toggle
   - Transaction simulator

## Troubleshooting

### Connection Test Fails
- Verify API key is correct
- Check Store ID matches your LemonSqueezy store
- Ensure API key has proper permissions

### Webhook Not Receiving Events
- Verify webhook URL is publicly accessible
- Check webhook secret matches LemonSqueezy settings
- Review webhook event subscriptions

### Settings Not Saving
- Check browser console for errors
- Verify backend is running
- Ensure MongoDB connection is active

## Testing Checklist

- [x] Backend API endpoints working
- [x] Frontend component renders correctly
- [x] Connection test validates credentials
- [x] Settings save to database
- [x] Settings persist on page reload
- [x] Show/hide password functionality works
- [x] Copy to clipboard functionality works
- [x] Navigation to LemonSqueezy links work
- [x] Admin sidebar shows Payment Gateway tab
- [x] Tab switching works properly

## Files Created/Modified

### Created:
1. `/app/backend/routers/payment_settings.py` - Backend API
2. `/app/frontend/src/components/admin/PaymentGatewaySettings.jsx` - Frontend UI
3. `/app/PAYMENT_GATEWAY_INTEGRATION.md` - This documentation

### Modified:
1. `/app/backend/server.py` - Registered payment_settings router
2. `/app/frontend/src/pages/admin/AdminDashboard.jsx` - Added tab integration
3. `/app/frontend/src/components/admin/AdminSidebar.jsx` - Added sidebar item

## Version Information
- **Feature Version:** 1.0.0
- **Date Created:** November 14, 2025
- **Status:** ✅ Production Ready
