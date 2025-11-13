# Lemon Squeezy Setup Checklist

## Pre-Setup Requirements
- [ ] Lemon Squeezy account created
- [ ] Access to Lemon Squeezy dashboard
- [ ] Access to application backend `.env` file

---

## Step 1: Create Products in Lemon Squeezy

### Starter Plan Product
- [ ] Go to Products → Create Product
- [ ] Product Name: **Starter Plan**
- [ ] Price: **₹7,999**
- [ ] Billing Cycle: **Monthly**
- [ ] Description: **For growing businesses**
- [ ] Features to add:
  - [ ] 5 chatbots
  - [ ] 15,000 messages/month
  - [ ] Advanced analytics
  - [ ] Priority support
  - [ ] Custom branding
  - [ ] API access
  - [ ] All AI models
- [ ] Save and note the **Variant ID**: `________________`

### Professional Plan Product
- [ ] Go to Products → Create Product
- [ ] Product Name: **Professional Plan**
- [ ] Price: **₹24,999**
- [ ] Billing Cycle: **Monthly**
- [ ] Description: **For large teams & high volume**
- [ ] Features to add:
  - [ ] 25 chatbots
  - [ ] 1,25,000 messages/month
  - [ ] Advanced analytics
  - [ ] 24/7 priority support
  - [ ] Custom branding
  - [ ] Full API access
  - [ ] All AI models
  - [ ] Custom integrations
  - [ ] Dedicated account manager
- [ ] Save and note the **Variant ID**: `________________`

---

## Step 2: Get API Credentials

### API Key
- [ ] Go to Settings → API
- [ ] Click "Create API Key"
- [ ] Name: **BotSmith Application**
- [ ] Copy the API Key: `________________`

### Store ID
- [ ] Go to Settings → Stores
- [ ] Copy your Store ID: `________________`

---

## Step 3: Configure Webhook

- [ ] Go to Settings → Webhooks
- [ ] Click "Create Webhook"
- [ ] Webhook URL: `https://YOUR-DOMAIN.com/api/lemonsqueezy/webhook`
  - Replace `YOUR-DOMAIN.com` with your actual domain
  - For local testing with ngrok: `https://YOUR-NGROK-URL.ngrok.io/api/lemonsqueezy/webhook`
- [ ] Select Events to Subscribe:
  - [x] subscription_created
  - [x] subscription_updated
  - [x] subscription_payment_success
  - [x] subscription_cancelled
  - [x] subscription_expired
  - [x] order_created
- [ ] Save Webhook
- [ ] Copy the **Signing Secret**: `________________`

---

## Step 4: Update Backend Configuration

### Update Environment Variables
- [ ] Open `/app/backend/.env` file
- [ ] Add/Update these variables:

```bash
LEMONSQUEEZY_API_KEY=your_api_key_here
LEMONSQUEEZY_STORE_ID=your_store_id_here
LEMONSQUEEZY_SIGNING_SECRET=your_webhook_signing_secret_here
```

### Update Variant IDs
- [ ] Open `/app/backend/routers/lemonsqueezy.py`
- [ ] Find the `VARIANT_IDS` dictionary (around line 33)
- [ ] Update with your actual Variant IDs:

```python
VARIANT_IDS = {
    "starter": "YOUR_STARTER_VARIANT_ID",
    "professional": "YOUR_PROFESSIONAL_VARIANT_ID"
}
```

### Restart Backend Service
- [ ] Run: `sudo supervisorctl restart backend`
- [ ] Verify service is running: `sudo supervisorctl status backend`

---

## Step 5: Test in Test Mode

### Enable Test Mode
- [ ] Go to Settings → General in Lemon Squeezy
- [ ] Toggle **Test Mode** ON

### Test Checkout Flow
- [ ] Login to your application
- [ ] Go to Subscription/Pricing page
- [ ] Click "Upgrade" on Starter plan
- [ ] Complete checkout with test credit card:
  - Card: `4242 4242 4242 4242`
  - Expiry: Any future date
  - CVV: Any 3 digits
- [ ] Verify redirect to success page
- [ ] Check subscription appears in your account

### Test Webhook
- [ ] In Lemon Squeezy, go to Webhooks
- [ ] Click on your webhook
- [ ] View recent deliveries
- [ ] Verify webhooks are being received (Status 200)
- [ ] Check database for subscription entry

### Test Manual Sync
- [ ] Go to Subscription page in application
- [ ] Click "Sync" button
- [ ] Verify subscription updates

---

## Step 6: Production Deployment

### Verify Everything Works in Test Mode
- [ ] Checkout flow works
- [ ] Webhooks are received and processed
- [ ] Subscription limits are enforced
- [ ] Payments are tracked
- [ ] Usage is tracked correctly

### Switch to Production
- [ ] Go to Settings → General in Lemon Squeezy
- [ ] Toggle **Test Mode** OFF
- [ ] All test subscriptions will be cleared
- [ ] Ready for real payments!

### Update URLs
- [ ] Verify webhook URL is production domain
- [ ] Update redirect URLs in checkout if needed:
  - Success URL: `https://YOUR-DOMAIN.com/subscription?success=true`
  - Receipt URL: `https://YOUR-DOMAIN.com/dashboard`

---

## Step 7: Monitor and Maintain

### Set Up Monitoring
- [ ] Monitor webhook logs: Check `/webhook_logs` collection in MongoDB
- [ ] Set up alerts for failed webhooks
- [ ] Monitor subscription status changes
- [ ] Track payment failures

### Regular Tasks
- [ ] Weekly: Review webhook logs
- [ ] Weekly: Check failed payments
- [ ] Monthly: Verify subscription counts match
- [ ] Monthly: Review plan usage and limits

---

## Troubleshooting Guide

### Webhook Not Working
1. Check webhook URL is accessible from internet
2. Verify signing secret is correct in `.env`
3. Check backend logs: `tail -50 /var/log/supervisor/backend.err.log`
4. Test webhook with Lemon Squeezy test feature

### Checkout Not Creating
1. Verify API key is valid
2. Check store ID is correct
3. Ensure variant IDs are updated
4. Check backend logs for API errors

### Subscription Not Syncing
1. Check webhooks are configured
2. Try manual sync button
3. Verify database has subscriptions collection
4. Check network connectivity to Lemon Squeezy API

---

## Support Contacts

### Technical Issues
- Backend logs: `/var/log/supervisor/backend.err.log`
- Frontend logs: Browser console
- Database: MongoDB `chatbase_db` database

### Lemon Squeezy Support
- Documentation: https://docs.lemonsqueezy.com
- Support: support@lemonsqueezy.com
- Discord: https://discord.gg/lemonsqueezy

---

## Notes

- Test mode subscriptions don't charge real money
- Variant IDs are different for test and production
- Webhook signature verification is required for security
- All prices are in INR (Indian Rupees)
- Enterprise plan is custom pricing - not in Lemon Squeezy

---

## Completion Checklist

- [ ] All products created in Lemon Squeezy
- [ ] API credentials obtained and configured
- [ ] Webhook configured and tested
- [ ] Environment variables updated
- [ ] Variant IDs updated in code
- [ ] Backend service restarted
- [ ] Test checkout completed successfully
- [ ] Webhooks received and processed
- [ ] Subscription limits enforced
- [ ] Ready for production deployment

---

**Date Completed**: ________________

**Completed By**: ________________

**Notes**: ________________
