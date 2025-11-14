# Payment Gateway Troubleshooting Guide

## Issue: "Not Authenticated" Error When Making Test Payment

### ✅ Backend Verification (PASSED)
- Payment settings are correctly saved in database
- LemonSqueezy API key is configured and working
- Test mode is enabled
- Checkout endpoint (`/api/lemonsqueezy/create-checkout`) is working correctly
- Test checkout creation was successful (HTTP 201)

### 🔍 Common Causes & Solutions

#### 1. User Not Logged In
**Symptom:** Error occurs immediately when clicking "Upgrade" button
**Solution:**
- Ensure the second user account is logged in
- Check browser console for authentication errors
- Verify localStorage has a valid token: Open Dev Tools → Application → Local Storage → Check for 'token'

#### 2. Token Expired or Invalid
**Symptom:** Error says "not authenticated" or "401 Unauthorized"
**Solution:**
- Log out and log back in with the second account
- Clear browser cache and cookies
- Try in an incognito/private browser window

#### 3. Browser Not Sending Token
**Symptom:** Request fails before reaching LemonSqueezy
**Solution:**
- Check Network tab in Dev Tools
- Look for the request to `/api/lemonsqueezy/create-checkout`
- Verify the request has an `Authorization: Bearer <token>` header

### 📋 Step-by-Step Debugging

#### Step 1: Verify User Can Access Their Profile
1. Log in with the second account
2. Go to Account Settings page
3. If profile loads, authentication is working
4. If not, try logging in again

#### Step 2: Check Browser Console
1. Open browser Dev Tools (F12)
2. Go to Console tab
3. Click "Upgrade" button on subscription page
4. Look for error messages
5. Common errors:
   - "401 Unauthorized" → Token issue
   - "Network Error" → Backend not responding
   - "Failed to fetch" → CORS or network issue

#### Step 3: Check Network Requests
1. Open Dev Tools → Network tab
2. Click "Upgrade" button
3. Look for request to `/api/auth/me`
4. Check if it returns 200 OK
5. If it fails with 401, the token is invalid

#### Step 4: Test Checkout Endpoint Directly
```bash
# Get the user's token from browser
# 1. Open Dev Tools → Application → Local Storage → Copy 'token' value
# 2. Replace YOUR_TOKEN_HERE with the actual token

curl -X POST http://localhost:8001/api/lemonsqueezy/create-checkout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "plan_id": "starter",
    "user_id": "USER_ID_HERE",
    "user_email": "user@example.com",
    "user_name": "Test User"
  }'
```

### 🔧 Fixes

#### Fix 1: Clear Session and Re-login
```javascript
// In browser console:
localStorage.clear();
sessionStorage.clear();
location.reload();
// Then log in again
```

#### Fix 2: Check if User Exists in Database
```bash
mongosh chatbase_db --eval "db.users.find({email: 'SECOND_USER_EMAIL'}).pretty()"
```

#### Fix 3: Verify LemonSqueezy Integration
1. Go to Admin Panel
2. Click Payment Gateway tab
3. Verify "Test Mode" is enabled (blue toggle)
4. Click "Test Connection" button
5. Should show "Connection Successful! (Test Mode)"

### 🎯 Expected Behavior

When user clicks "Upgrade" button:
1. ✅ Frontend calls `/api/auth/me` to get user data
2. ✅ Frontend calls `/api/lemonsqueezy/create-checkout` with user data
3. ✅ Backend loads payment settings from database
4. ✅ Backend creates checkout with LemonSqueezy API
5. ✅ Backend returns checkout URL
6. ✅ Frontend redirects to LemonSqueezy checkout page
7. ✅ User completes payment on LemonSqueezy (test mode)
8. ✅ LemonSqueezy sends webhook to backend
9. ✅ Backend updates user subscription

### 🔴 Where "Not Authenticated" Can Occur

#### Scenario A: At `/api/auth/me` endpoint
**Error Message:** "Could not validate credentials" or "Not authenticated"
**Location:** Before checkout is created
**Solution:** User needs to log in again

#### Scenario B: At `/api/lemonsqueezy/create-checkout` endpoint
**Error Message:** If endpoint requires authentication (it doesn't currently)
**Location:** When creating checkout
**Solution:** Verify endpoint doesn't require auth token (it should be open)

#### Scenario C: At LemonSqueezy Checkout Page
**Error Message:** LemonSqueezy shows "Invalid" or authentication error
**Location:** After redirect to LemonSqueezy
**Solution:** Check API key and variant IDs in payment settings

### 📊 Check Backend Logs
```bash
# Real-time logs
tail -f /var/log/supervisor/backend.err.log | grep -i "checkout\|auth\|error"

# Recent errors
tail -100 /var/log/supervisor/backend.err.log | grep -i "error\|401\|403"
```

### ✅ Confirmed Working (From My Test)
- ✅ Payment gateway is configured correctly
- ✅ Test mode is enabled
- ✅ API key is valid
- ✅ Store ID is correct
- ✅ Variant IDs are mapped (starter: 1052931, professional: 1052933)
- ✅ Checkout endpoint creates checkout successfully
- ✅ Returns valid checkout URL with test_mode=true

### 🎯 Most Likely Issue

Based on the error "not authenticated" when the second user tries to pay:

1. **User's auth token is not being sent** - Check if localStorage has the token
2. **Token expired** - User needs to log in again
3. **Frontend trying to call wrong endpoint** - Check browser console for API call details

### 💡 Quick Fix to Try

1. **Log out the second user**
2. **Clear browser data** (Ctrl+Shift+Delete)
3. **Log in again** with second user credentials
4. **Try upgrading again**

If issue persists, please provide:
- Exact error message from browser console
- Network tab screenshot showing the failed request
- User email of the second account
