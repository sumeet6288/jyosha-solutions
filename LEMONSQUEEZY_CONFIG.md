# Lemon Squeezy Configuration

## Credentials (Saved in `/app/backend/.env`)

```
LEMONSQUEEZY_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiJjYWZjOTEzN2FjYTI2YmE5ZTg2NzM1NzVkNmRiZWI1ZmJiZmZhYTE3MGM4YjU3Y2VhOTE5MmNlODFiMDE3YTMwOGI3NGIyOGZiYTAyZjk0NCIsImlhdCI6MTc2MTkwMzE2OS4xMTEzMTYsIm5iZiI6MTc2MTkwMzE2OS4xMTEzMTksImV4cCI6MjA3NzQzNTk2OS4wOTUyMDIsInN1YiI6IjU2NTY0NjMiLCJzY29wZXMiOltdfQ.byF15AAjdAfamvffPPBKIePTHsUACsciWWwhdFdosHe-lLI-pDL0UOxsHxykemIIJsvCad2yUlrwaRtQxf0XzhXKFIwfYVTff43BilLSbSGZUqTVe8HyFjvUT3G_BIOvK92H_lJ9uFQrDvugPFK3P6feV3CapYskpwrgBED3EsLDYbfrapcqQCkSjAmSsfkrMYIU3RdV6dTK1tq2Q8Dv8jhoyNZUHjmy55RUq_k8O5gFlz1Q0FFj54a9b_D0OT2ujnswjqxJ5DSmnVukHlebKs-iNlmwVM2CtOFLu-qw11ttTwccMcYG_ULg5JNaDy0RWdrBCjEP_Rsblwzd54u1rxf8dfScz71qK4w-fhwjmHpDvfPnr2Xeag5gbA9hGYLuunDY6nOi6-kCDKO71YKdd5Wldw6hv4XbvLUJsiAP_dvu301Q3sDdl8xhZG4vuYCMGuzxC7pNSSvHIxxnGUNmIbtri5tnmC25_m30w_SdPkD3JGbQF-J949QofCWS_vi9PEiHC-DThDdbz0ID7vsuN42xl-Zkn2Ak4di4ZkHW6yqqGLkmBHNWG0ZObbTbDSzAdszFoBlID1HCNVJe4ORxN4nD1g-yG-ycuNSQPvzfwhAhEa-Pak5WRfAaen_CMtvTNsjgUqyINA53rAcxKPCvfgS-zsKbRsSLk43NI0ymdKE
LEMONSQUEEZY_STORE_ID=234448
LEMONSQUEEZY_SIGNING_SECRET=LS_webhook_secret_2025_secure_key_xyz789
```

**Note:** This is a TEST MODE API key. Use for development and testing only.

## Store Information

- **Store ID**: 234448
- **Store Name**: BotSmith
- **Test Mode**: Enabled
- **Currency**: INR (Indian Rupee) - Used as USD for testing

## Products & Variants

### 1. Starter Plan
- **Product ID**: 669987
- **Product Name**: starter
- **Variant ID**: 1052931
- **Price**: ₹150/month (displayed as $150/month in UI)
- **Type**: Subscription (monthly)
- **Status**: Published, Test Mode

### 2. Professional Plan
- **Product ID**: 669989
- **Product Name**: Professional
- **Variant ID**: 1052933
- **Price**: ₹499 (displayed as $499 in UI)
- **Type**: One-time payment
- **Status**: Published, Test Mode

## Plan Features

### Free Plan ($0/month)
- 1 chatbot
- 100 messages/month
- Basic analytics
- Community support
- Standard AI models

### Starter Plan ($150/month)
- 5 chatbots
- 10,000 messages/month
- Advanced analytics
- Priority support
- Custom branding
- API access
- All AI models

### Professional Plan ($499/month)
- 25 chatbots
- 100,000 messages/month
- Advanced analytics
- 24/7 priority support
- Custom branding
- Full API access
- All AI models
- Custom integrations
- Dedicated account manager

### Enterprise Plan (Custom)
- Unlimited chatbots
- Unlimited messages
- Custom analytics
- Dedicated 24/7 support
- White-label solution
- Custom AI model training
- On-premise deployment
- SLA guarantee
- Custom contracts
- Enterprise security

## API Endpoints

### 1. Get Plans
```
GET /api/lemonsqueezy/plans
```
Returns list of available subscription plans

### 2. Get Subscription Status
```
GET /api/lemonsqueezy/subscription/status
```
Returns current user's subscription status

### 3. Create Checkout
```
POST /api/lemonsqueezy/checkout/create
Body: {
  "plan": "starter" | "professional",
  "user_id": "demo-user-123",
  "user_email": "demo@botsmith.com"
}
```
Returns checkout URL from Lemon Squeezy

### 4. Webhook Handler
```
POST /api/lemonsqueezy/webhook
```
Handles Lemon Squeezy webhook events for subscription updates

## Testing Status

✅ All endpoints tested and working
✅ Checkout creation successful
✅ Plans API working
✅ Subscription status working
✅ Authentication fixed (User object type annotation)

## Important Notes

1. **Currency Display**: Products are in INR but displayed as USD in the UI for consistency
2. **Test Mode**: All transactions are in test mode - no real charges
3. **Demo User**: Using mock authentication with user ID "demo-user-123"
4. **Redirect URLs**: Configured to return to the application after checkout
5. **Webhook Secret**: Not configured yet - add if webhook verification is needed

## Future Enhancements

- [ ] Add webhook signing secret for production
- [ ] Implement subscription upgrade/downgrade logic
- [ ] Add payment history and invoices
- [ ] Implement usage-based billing
- [ ] Add proration for plan changes
- [ ] Configure production mode credentials

## Dashboard Links

- Lemon Squeezy Dashboard: https://app.lemonsqueezy.com/
- Store Settings: https://app.lemonsqueezy.com/settings/stores/234448
- Products: https://app.lemonsqueezy.com/products
- Subscriptions: https://app.lemonsqueezy.com/subscriptions
- Webhooks: https://app.lemonsqueezy.com/settings/webhooks

## Last Updated
October 22, 2025
