# Lemon Squeezy Integration Setup Guide

## ✅ Integration Status

Your BotSmith application is now integrated with Lemon Squeezy payment processing! 

## 📋 Configuration Summary

### Test Mode Credentials (Already Configured)
- **Store ID**: `234448`
- **Store Name**: botsmith
- **Currency**: INR (Indian Rupees)
- **API Key**: Configured in backend `.env` file
- **Signing Secret**: `LS_webhook_secret_2025_secure_key_xyz789`

### Products & Plans

1. **Starter Plan**
   - Price: ₹150/month
   - Type: Monthly subscription
   - Variant ID: `1052931`
   - Features:
     - 3 Chatbots
     - 1,000 messages/month
     - File uploads
     - Website scraping
     - Basic analytics

2. **Professional Plan**
   - Price: ₹499
   - Type: One-time payment
   - Variant ID: `1052933`
   - Features:
     - Unlimited chatbots
     - 10,000 messages/month
     - Priority support
     - Advanced analytics
     - Custom branding
     - API access

## 🔧 Webhook Setup (Important!)

To enable real-time subscription updates, you need to configure webhooks in your Lemon Squeezy dashboard:

### Step 1: Access Webhook Settings
1. Log into your Lemon Squeezy dashboard at https://app.lemonsqueezy.com
2. Select your store: **botsmith** (Store ID: 234448)
3. Navigate to: **Settings** → **Webhooks**
4. Click **Create Webhook** (the "+" button)

### Step 2: Configure Webhook

**Callback URL**: 
```
https://setup-preview.preview.emergentagent.com/api/lemonsqueezy/webhook
```

**Signing Secret**:
```
LS_webhook_secret_2025_secure_key_xyz789
```

⚠️ **Important**: Copy the signing secret exactly as shown above. This must match the value in your backend `.env` file.

### Step 3: Select Events to Subscribe

Select the following events:

✅ **Subscription Events:**
- `subscription_created` - New subscription created
- `subscription_updated` - Subscription details changed
- `subscription_payment_success` - Successful payment
- `subscription_cancelled` - Subscription cancelled
- `subscription_expired` - Subscription expired

✅ **Order Events:**
- `order_created` - One-time purchase completed

### Step 4: Save and Test

1. Click **Save** to create the webhook
2. Lemon Squeezy will test the webhook endpoint
3. If successful, you'll see a green checkmark ✅

## 🧪 Testing the Integration

### Test the Checkout Flow

1. Navigate to: https://setup-preview.preview.emergentagent.com/subscription
2. Click **Subscribe Now** on either plan (Starter or Professional)
3. You'll be redirected to Lemon Squeezy checkout page
4. Use test card details (provided by Lemon Squeezy in test mode)
5. Complete the test purchase
6. You'll be redirected back to your app with a success message

### Test Card Numbers (Test Mode)

Lemon Squeezy automatically provides test card numbers in test mode. Common test cards:
- **Success**: Use any valid card number format (e.g., 4242 4242 4242 4242)
- **Expiry**: Any future date
- **CVC**: Any 3 digits

## 🔍 Monitoring & Debugging

### Check Webhook Logs
Webhook events are logged in MongoDB collection: `webhook_logs`

Query example:
```javascript
db.webhook_logs.find().sort({received_at: -1}).limit(10)
```

### Check Subscriptions
Active subscriptions are stored in MongoDB collection: `subscriptions`

Query example:
```javascript
db.subscriptions.find({status: "active"})
```

### Backend Logs
Check backend logs for webhook processing:
```bash
tail -f /var/log/supervisor/backend.err.log | grep -i "webhook\|lemonsqueezy"
```

## 📊 API Endpoints

### Available Endpoints

1. **Get Available Plans**
   ```
   GET /api/lemonsqueezy/plans
   ```

2. **Create Checkout Session**
   ```
   POST /api/lemonsqueezy/checkout/create
   Body: {
     "plan": "starter" or "professional",
     "user_id": "user-id",
     "user_email": "user@example.com"
   }
   ```

3. **Get Subscription Status**
   ```
   GET /api/lemonsqueezy/subscription/status
   ```

4. **Webhook Handler** (Called by Lemon Squeezy)
   ```
   POST /api/lemonsqueezy/webhook
   ```

## 🔐 Security Features

✅ **Implemented Security Measures:**

1. **Webhook Signature Verification**
   - All webhooks are verified using HMAC-SHA256
   - Invalid signatures are rejected with 401 Unauthorized

2. **HTTPS Only**
   - All communication uses secure HTTPS

3. **API Key Protection**
   - API keys stored in environment variables
   - Never exposed to frontend

4. **User Authentication**
   - Checkout endpoints require authentication
   - User ID embedded in checkout custom data

## 🚀 Going Live (Production Mode)

When you're ready to accept real payments:

### 1. Create Production API Key
- In Lemon Squeezy dashboard, switch to **Live Mode**
- Generate a new API key
- Update backend `.env` file with live API key

### 2. Update Webhook
- Create new webhook with production callback URL
- Use the same signing secret or generate a new one
- Update `.env` if using new secret

### 3. Create Production Products
- Create your products/variants in live mode
- Update `VARIANT_IDS` in `/app/backend/routers/lemonsqueezy.py` with live variant IDs

### 4. Update Frontend URLs
- Ensure `REACT_APP_BACKEND_URL` points to production API
- Test complete checkout flow in live mode

## 🎨 Customization

### Modify Plans
Edit `/app/backend/routers/lemonsqueezy.py`:
```python
VARIANT_IDS = {
    "starter": "YOUR_STARTER_VARIANT_ID",
    "professional": "YOUR_PRO_VARIANT_ID"
}
```

### Update Plan Features
Edit `/app/frontend/src/pages/Subscription.jsx` to modify displayed features.

### Customize Checkout Experience
Configure in Lemon Squeezy dashboard:
- Checkout page branding
- Logo and colors
- Email templates
- Receipt settings

## 📚 Resources

- **Lemon Squeezy Dashboard**: https://app.lemonsqueezy.com
- **API Documentation**: https://docs.lemonsqueezy.com/api
- **Webhook Guide**: https://docs.lemonsqueezy.com/guides/developer-guide/webhooks
- **Test Mode Guide**: https://docs.lemonsqueezy.com/help/getting-started/test-mode

## 🐛 Troubleshooting

### Checkout Creation Fails
- Check API key is correct in `.env`
- Verify store ID and variant IDs
- Check backend logs for errors

### Webhooks Not Received
- Verify webhook URL is publicly accessible
- Check signing secret matches
- Ensure HTTPS is used
- Review webhook logs in Lemon Squeezy dashboard

### Subscription Status Not Updating
- Verify webhooks are configured correctly
- Check MongoDB subscriptions collection
- Review backend logs for webhook processing errors

## ✨ Features Implemented

✅ Subscription page with plan comparison
✅ Secure checkout creation
✅ Webhook handling with signature verification
✅ Subscription status tracking
✅ MongoDB integration for subscription data
✅ Success message on payment completion
✅ Beautiful UI with Tailwind CSS
✅ Test mode enabled for safe testing
✅ Support for both subscription and one-time payments

## 🎉 Next Steps

1. **Set up webhooks** in Lemon Squeezy dashboard (instructions above)
2. **Test the complete flow** with test purchases
3. **Customize branding** in Lemon Squeezy checkout settings
4. **Monitor webhook logs** to ensure proper synchronization
5. **When ready, switch to live mode** for production

---

**Need Help?**
- Lemon Squeezy Support: https://docs.lemonsqueezy.com
- Check `/var/log/supervisor/backend.err.log` for backend errors
- Review MongoDB collections: `subscriptions` and `webhook_logs`
