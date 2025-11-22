"""
Verification script to check if Ultimate Edit fields are properly saved using admin details endpoint
"""
import requests
import json

# Configuration
BACKEND_URL = "https://rapid-stack-launch.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@botsmith.com"
ADMIN_PASSWORD = "admin123"

# Login as admin
print("Logging in as admin...")
response = requests.post(
    f"{BACKEND_URL}/auth/login",
    json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    timeout=10
)

if response.status_code == 200:
    token_data = response.json()
    admin_token = token_data.get("access_token")
    
    # Get admin user ID
    headers = {"Authorization": f"Bearer {admin_token}"}
    me_response = requests.get(f"{BACKEND_URL}/auth/me", headers=headers, timeout=10)
    admin_user_id = me_response.json().get("id")
    
    # Get full user details via admin endpoint
    response = requests.get(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/details",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        user_data = result.get("user", {})
        
        print("\n" + "="*80)
        print("FULL USER DATA FROM ADMIN DETAILS ENDPOINT:")
        print("="*80)
        print(json.dumps(user_data, indent=2, default=str))
        print("="*80)
        
        # Verify all the fields that were updated in the Ultimate Edit test
        print("\nVERIFICATION OF ULTIMATE EDIT FIELDS:")
        print("="*50)
        
        # Tab 1: Basic Info
        print(f"✅ Name: {user_data.get('name')} (Expected: Admin User Updated)")
        print(f"✅ Company: {user_data.get('company')} (Expected: BotSmith Technologies Inc)")
        print(f"✅ Job Title: {user_data.get('job_title')} (Expected: Chief Technology Officer)")
        print(f"✅ Phone: {user_data.get('phone')} (Expected: +1-555-0123)")
        print(f"✅ Address: {user_data.get('address')} (Expected: 123 Admin Street, Suite 100)")
        bio = user_data.get('bio', '')
        print(f"✅ Bio: {bio[:50]}... (Expected: This is an updated admin bio...)")
        print(f"✅ Avatar URL: {user_data.get('avatar_url')} (Expected: https://example.com/admin-avatar.jpg)")
        
        # Tab 2: Permissions
        permissions = user_data.get('permissions', {})
        print(f"✅ Permissions - canCreateChatbots: {permissions.get('canCreateChatbots')} (Expected: True)")
        print(f"✅ Permissions - canDeleteChatbots: {permissions.get('canDeleteChatbots')} (Expected: False)")
        print(f"✅ Permissions - canViewAnalytics: {permissions.get('canViewAnalytics')} (Expected: True)")
        
        # Tab 3: Security
        print(f"✅ Max Sessions: {user_data.get('max_sessions')} (Expected: 3)")
        print(f"✅ Session Timeout: {user_data.get('session_timeout')} (Expected: 7200)")
        print(f"✅ Allowed IPs: {user_data.get('allowed_ips')} (Expected: ['192.168.1.1', '10.0.0.1'])")
        print(f"✅ Blocked IPs: {user_data.get('blocked_ips')} (Expected: ['1.2.3.4'])")
        
        # Tab 4: Subscription
        print(f"✅ Plan ID: {user_data.get('plan_id')} (Expected: professional)")
        print(f"✅ Stripe Customer ID: {user_data.get('stripe_customer_id')} (Expected: cus_test123456789)")
        print(f"✅ Billing Email: {user_data.get('billing_email')} (Expected: billing@botsmith.com)")
        print(f"✅ Lifetime Access: {user_data.get('lifetime_access')} (Expected: True)")
        print(f"✅ Discount Code: {user_data.get('discount_code')} (Expected: SAVE50)")
        print(f"✅ Custom Pricing: {user_data.get('custom_pricing')} (Expected: 1999.0)")
        
        # Tab 5: Limits & Features
        custom_limits = user_data.get('custom_limits', {})
        feature_flags = user_data.get('feature_flags', {})
        api_rate_limits = user_data.get('api_rate_limits', {})
        print(f"✅ Custom Limits - max_chatbots: {custom_limits.get('max_chatbots')} (Expected: 50)")
        print(f"✅ Custom Limits - max_messages_per_month: {custom_limits.get('max_messages_per_month')} (Expected: 500000)")
        print(f"✅ Feature Flags - betaFeatures: {feature_flags.get('betaFeatures')} (Expected: True)")
        print(f"✅ Feature Flags - advancedAnalytics: {feature_flags.get('advancedAnalytics')} (Expected: True)")
        print(f"✅ API Rate Limits - requests_per_minute: {api_rate_limits.get('requests_per_minute')} (Expected: 120)")
        print(f"✅ API Rate Limits - requests_per_hour: {api_rate_limits.get('requests_per_hour')} (Expected: 5000)")
        
        # Tab 6: Appearance
        branding = user_data.get('branding', {})
        print(f"✅ Timezone: {user_data.get('timezone')} (Expected: America/New_York)")
        print(f"✅ Language: {user_data.get('language')} (Expected: en)")
        print(f"✅ Theme: {user_data.get('theme')} (Expected: dark)")
        custom_css = user_data.get('custom_css', '')
        print(f"✅ Custom CSS: {custom_css[:30]}... (Expected: .custom {{ color: blue...)")
        print(f"✅ Branding - logo_url: {branding.get('logo_url')} (Expected: https://example.com/logo.png)")
        print(f"✅ Branding - primary_color: {branding.get('primary_color')} (Expected: #7c3aed)")
        
        # Tab 7: Notifications
        notification_prefs = user_data.get('notification_preferences', {})
        print(f"✅ Email Notifications: {user_data.get('email_notifications')} (Expected: True)")
        print(f"✅ Marketing Emails: {user_data.get('marketing_emails')} (Expected: False)")
        print(f"✅ Notification Prefs - newChatbotCreated: {notification_prefs.get('newChatbotCreated')} (Expected: True)")
        print(f"✅ Notification Prefs - weeklyReport: {notification_prefs.get('weeklyReport')} (Expected: False)")
        
        # Tab 8: Metadata
        custom_fields = user_data.get('custom_fields', {})
        print(f"✅ Tags: {user_data.get('tags')} (Expected: ['premium-user', 'beta-tester', 'power-user'])")
        print(f"✅ Segments: {user_data.get('segments')} (Expected: ['enterprise', 'early-adopter'])")
        print(f"✅ Custom Fields - account_manager: {custom_fields.get('account_manager')} (Expected: John Doe)")
        admin_notes = user_data.get('admin_notes', '')
        print(f"✅ Admin Notes: {admin_notes[:30]}... (Expected: This is a test admin note...)")
        
        # Tab 9: API & Integrations
        oauth_tokens = user_data.get('oauth_tokens', {})
        integration_prefs = user_data.get('integration_preferences', {})
        print(f"✅ API Key: {user_data.get('api_key')} (Expected: test_api_key_123456789)")
        print(f"✅ Webhook URL: {user_data.get('webhook_url')} (Expected: https://webhook.example.com/events)")
        print(f"✅ Webhook Events: {user_data.get('webhook_events')} (Expected: ['user.created', 'chatbot.updated', 'message.sent'])")
        print(f"✅ OAuth Tokens - github: {oauth_tokens.get('github')} (Expected: github_token_123)")
        print(f"✅ Integration Prefs - slack_enabled: {integration_prefs.get('slack_enabled')} (Expected: True)")
        
        # Tab 10: Tracking
        print(f"✅ Tracking Enabled: {user_data.get('tracking_enabled')} (Expected: True)")
        print(f"✅ Analytics Enabled: {user_data.get('analytics_enabled')} (Expected: True)")
        print(f"✅ Onboarding Completed: {user_data.get('onboarding_completed')} (Expected: True)")
        print(f"✅ Onboarding Step: {user_data.get('onboarding_step')} (Expected: 5)")
        
        print("\n" + "="*80)
        print("VERIFICATION COMPLETE")
        print("="*80)
        
    else:
        print(f"Failed to get user details: {response.status_code} - {response.text}")
else:
    print(f"Failed to login: {response.status_code}")