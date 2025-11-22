"""
Debug script to check what user data is actually returned from /api/auth/me
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
    
    # Get user data
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        user_data = response.json()
        print("\n" + "="*80)
        print("CURRENT USER DATA FROM /api/auth/me:")
        print("="*80)
        print(json.dumps(user_data, indent=2, default=str))
        print("="*80)
        
        # Check specific fields that failed verification
        print("\nFAILED VERIFICATION FIELDS:")
        print(f"permissions: {user_data.get('permissions')}")
        print(f"max_sessions: {user_data.get('max_sessions')}")
        print(f"session_timeout: {user_data.get('session_timeout')}")
        print(f"email_notifications: {user_data.get('email_notifications')}")
        print(f"notification_preferences: {user_data.get('notification_preferences')}")
        print(f"admin_notes: {user_data.get('admin_notes')}")
        print(f"api_key: {user_data.get('api_key')}")
        print(f"webhook_url: {user_data.get('webhook_url')}")
        print(f"tracking_enabled: {user_data.get('tracking_enabled')}")
        print(f"onboarding_completed: {user_data.get('onboarding_completed')}")
    else:
        print(f"Failed to get user data: {response.status_code}")
else:
    print(f"Failed to login: {response.status_code}")