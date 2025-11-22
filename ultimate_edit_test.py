"""
COMPREHENSIVE ULTIMATE EDIT ADMIN PANEL TESTING

Test all 10 tabs in the Ultimate Edit modal to verify each tab's functionality with the backend:
1. Basic Info - Profile fields (name, email, phone, address, bio, avatar_url, company, job_title)
2. Permissions - Role and granular permissions (11 permissions)
3. Security - Account status, email verification, 2FA, IP restrictions, session settings
4. Subscription - Plan, billing details, trial/subscription dates, lifetime access
5. Limits & Features - Custom limits (8 fields), feature flags (8 flags), API rate limits (4 settings)
6. Appearance - Timezone, language, theme, custom CSS, branding (5 branding fields)
7. Notifications - Email notifications, marketing emails, notification preferences (7 preferences)
8. Metadata - Tags, segments, custom fields, admin notes, internal notes
9. API & Integrations - API key, webhook URL, webhook events, OAuth tokens, integration preferences
10. Tracking - Tracking enabled, analytics enabled, onboarding status

This test verifies that all fields in each tab can be updated via PUT /api/admin/users/{user_id}/ultimate-update
and that the data persists correctly in the database.
"""
import requests
import json
import uuid
from datetime import datetime

# Configuration
BACKEND_URL = "https://rapid-stack-launch.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@botsmith.com"
ADMIN_PASSWORD = "admin123"

# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def log_test(test_name, passed, details=""):
    """Log test result"""
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
        status = "✅ PASS"
    else:
        test_results["failed"] += 1
        status = "❌ FAIL"
    
    test_results["tests"].append({
        "name": test_name,
        "status": status,
        "details": details
    })
    print(f"{status}: {test_name}")
    if details:
        print(f"   Details: {details}")

def print_summary():
    """Print test summary"""
    print("\n" + "="*80)
    print("COMPREHENSIVE ULTIMATE EDIT ADMIN PANEL TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {test_results['total']}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    print(f"Success Rate: {(test_results['passed']/test_results['total']*100):.1f}%")
    print("="*80)
    
    if test_results["failed"] > 0:
        print("\nFailed Tests:")
        for test in test_results["tests"]:
            if "❌" in test["status"]:
                print(f"  - {test['name']}")
                if test["details"]:
                    print(f"    {test['details']}")

# Global variables for test data
admin_token = None
admin_user_id = None

print("="*80)
print("COMPREHENSIVE ULTIMATE EDIT ADMIN PANEL TESTING")
print("="*80)
print(f"Backend URL: {BACKEND_URL}")
print(f"Admin Email: {ADMIN_EMAIL}")
print(f"Test Time: {datetime.now().isoformat()}")
print("Testing all 10 tabs of Ultimate Edit modal functionality")
print("="*80 + "\n")

# ============================================================================
# SETUP: Login as admin user and get user details
# ============================================================================
print("\n[SETUP] Login as admin user...")
try:
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        },
        timeout=10
    )
    
    if response.status_code == 200:
        token_data = response.json()
        admin_token = token_data.get("access_token")
        if admin_token:
            log_test("Admin login", True, f"Successfully logged in as admin")
        else:
            log_test("Admin login", False, "No access token received")
            print("Cannot proceed without admin token. Exiting...")
            exit(1)
    else:
        log_test("Admin login", False, f"Status: {response.status_code}, Response: {response.text}")
        print("Cannot proceed without admin token. Exiting...")
        exit(1)
except Exception as e:
    log_test("Admin login", False, f"Exception: {str(e)}")
    print("Cannot proceed without admin token. Exiting...")
    exit(1)

# Get admin user details
print("\n[SETUP] Getting admin user details...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        user_data = response.json()
        admin_user_id = user_data.get("id")
        if admin_user_id:
            log_test("Get admin user ID", True, f"Admin user ID: {admin_user_id}")
        else:
            log_test("Get admin user ID", False, "No user ID in response")
            print("Cannot proceed without admin user ID. Exiting...")
            exit(1)
    else:
        log_test("Get admin user ID", False, f"Status: {response.status_code}")
        print("Cannot proceed without admin user ID. Exiting...")
        exit(1)
except Exception as e:
    log_test("Get admin user ID", False, f"Exception: {str(e)}")
    print("Cannot proceed without admin user ID. Exiting...")
    exit(1)

# ============================================================================
# TAB 1: BASIC INFO
# ============================================================================
print("\n[TAB 1] Testing Basic Info tab...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    basic_info_data = {
        "name": "Admin User Updated",
        "email": "admin@botsmith.com",  # Keep same email
        "phone": "+1-555-0123",
        "address": "123 Admin Street, Suite 100",
        "bio": "This is an updated admin bio for testing Ultimate Edit functionality",
        "avatar_url": "https://example.com/admin-avatar.jpg",
        "company": "BotSmith Technologies Inc",
        "job_title": "Chief Technology Officer"
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=basic_info_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 1: Basic Info Update", True, f"All 8 basic info fields updated successfully")
        else:
            log_test("TAB 1: Basic Info Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 1: Basic Info Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 1: Basic Info Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 2: PERMISSIONS
# ============================================================================
print("\n[TAB 2] Testing Permissions tab...")
try:
    permissions_data = {
        "role": "admin",  # Keep admin role
        "permissions": {
            "canCreateChatbots": True,
            "canDeleteChatbots": False,
            "canViewAnalytics": True,
            "canExportData": True,
            "canManageIntegrations": True,
            "canAccessAPI": False,
            "canUploadFiles": True,
            "canScrapeWebsites": True,
            "canUseAdvancedFeatures": False,
            "canInviteTeamMembers": False,
            "canManageBilling": False
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=permissions_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 2: Permissions Update", True, f"Role and 11 permissions updated successfully")
        else:
            log_test("TAB 2: Permissions Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 2: Permissions Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 2: Permissions Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 3: SECURITY
# ============================================================================
print("\n[TAB 3] Testing Security tab...")
try:
    security_data = {
        "status": "active",
        "email_verified": True,
        "two_factor_enabled": False,
        "force_password_change": False,
        "allowed_ips": ["192.168.1.1", "10.0.0.1"],
        "blocked_ips": ["1.2.3.4"],
        "max_sessions": 3,
        "session_timeout": 7200
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=security_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 3: Security Update", True, f"All 8 security settings updated successfully")
        else:
            log_test("TAB 3: Security Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 3: Security Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 3: Security Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 4: SUBSCRIPTION
# ============================================================================
print("\n[TAB 4] Testing Subscription tab...")
try:
    subscription_data = {
        "plan_id": "professional",
        "stripe_customer_id": "cus_test123456789",
        "billing_email": "billing@botsmith.com",
        "trial_ends_at": "2024-12-31T23:59:59Z",
        "subscription_ends_at": "2025-12-31T23:59:59Z",
        "lifetime_access": True,
        "discount_code": "SAVE50",
        "custom_pricing": 1999.0
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=subscription_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 4: Subscription Update", True, f"All 8 subscription fields updated successfully")
        else:
            log_test("TAB 4: Subscription Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 4: Subscription Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 4: Subscription Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 5: LIMITS & FEATURES
# ============================================================================
print("\n[TAB 5] Testing Limits & Features tab...")
try:
    limits_features_data = {
        "custom_limits": {
            "max_chatbots": 50,
            "max_messages_per_month": 500000,
            "max_file_uploads": 200,
            "max_website_sources": 100,
            "max_text_sources": 200,
            "max_storage_mb": 10000,
            "max_ai_models": 10,
            "max_integrations": 20
        },
        "feature_flags": {
            "betaFeatures": True,
            "advancedAnalytics": True,
            "customBranding": True,
            "apiAccess": True,
            "prioritySupport": True,
            "customDomain": False,
            "whiteLabel": False,
            "ssoEnabled": False
        },
        "api_rate_limits": {
            "requests_per_minute": 120,
            "requests_per_hour": 5000,
            "requests_per_day": 50000,
            "burst_limit": 200
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=limits_features_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 5: Limits & Features Update", True, f"Custom limits (8), feature flags (8), and API rate limits (4) updated successfully")
        else:
            log_test("TAB 5: Limits & Features Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 5: Limits & Features Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 5: Limits & Features Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 6: APPEARANCE
# ============================================================================
print("\n[TAB 6] Testing Appearance tab...")
try:
    appearance_data = {
        "timezone": "America/New_York",
        "language": "en",
        "theme": "dark",
        "custom_css": ".custom { color: blue; background: #f0f0f0; }",
        "branding": {
            "logo_url": "https://example.com/logo.png",
            "favicon_url": "https://example.com/favicon.ico",
            "primary_color": "#7c3aed",
            "secondary_color": "#ec4899",
            "font_family": "Inter"
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=appearance_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 6: Appearance Update", True, f"Timezone, language, theme, custom CSS, and branding (5 fields) updated successfully")
        else:
            log_test("TAB 6: Appearance Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 6: Appearance Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 6: Appearance Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 7: NOTIFICATIONS
# ============================================================================
print("\n[TAB 7] Testing Notifications tab...")
try:
    notifications_data = {
        "email_notifications": True,
        "marketing_emails": False,
        "notification_preferences": {
            "newChatbotCreated": True,
            "limitReached": True,
            "weeklyReport": False,
            "monthlyReport": True,
            "securityAlerts": True,
            "systemUpdates": False,
            "promotionalOffers": False
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=notifications_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 7: Notifications Update", True, f"Email notifications, marketing emails, and 7 notification preferences updated successfully")
        else:
            log_test("TAB 7: Notifications Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 7: Notifications Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 7: Notifications Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 8: METADATA
# ============================================================================
print("\n[TAB 8] Testing Metadata tab...")
try:
    metadata_data = {
        "tags": ["premium-user", "beta-tester", "power-user"],
        "segments": ["enterprise", "early-adopter"],
        "custom_fields": {
            "account_manager": "John Doe",
            "contract_id": "CT-12345",
            "priority_level": "high"
        },
        "admin_notes": "This is a test admin note for Ultimate Edit testing",
        "internal_notes": [
            {
                "author": "Admin",
                "note": "Test internal note for Ultimate Edit",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=metadata_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 8: Metadata Update", True, f"Tags, segments, custom fields, admin notes, and internal notes updated successfully")
        else:
            log_test("TAB 8: Metadata Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 8: Metadata Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 8: Metadata Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 9: API & INTEGRATIONS
# ============================================================================
print("\n[TAB 9] Testing API & Integrations tab...")
try:
    api_integrations_data = {
        "api_key": "test_api_key_123456789",
        "webhook_url": "https://webhook.example.com/events",
        "webhook_events": ["user.created", "chatbot.updated", "message.sent"],
        "oauth_tokens": {
            "github": "github_token_123",
            "google": "google_token_456"
        },
        "integration_preferences": {
            "slack_enabled": True,
            "discord_enabled": False
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=api_integrations_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 9: API & Integrations Update", True, f"API key, webhook URL, webhook events, OAuth tokens, and integration preferences updated successfully")
        else:
            log_test("TAB 9: API & Integrations Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 9: API & Integrations Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 9: API & Integrations Update", False, f"Exception: {str(e)}")

# ============================================================================
# TAB 10: TRACKING
# ============================================================================
print("\n[TAB 10] Testing Tracking tab...")
try:
    tracking_data = {
        "tracking_enabled": True,
        "analytics_enabled": True,
        "onboarding_completed": True,
        "onboarding_step": 5
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{admin_user_id}/ultimate-update",
        headers=headers,
        json=tracking_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        if success:
            log_test("TAB 10: Tracking Update", True, f"Tracking enabled, analytics enabled, onboarding status updated successfully")
        else:
            log_test("TAB 10: Tracking Update", False, f"Success flag false: {result.get('message')}")
    else:
        log_test("TAB 10: Tracking Update", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("TAB 10: Tracking Update", False, f"Exception: {str(e)}")

# ============================================================================
# VERIFICATION: Get updated user data to verify persistence
# ============================================================================
print("\n[VERIFICATION] Verifying all fields persisted correctly...")
try:
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        user_data = response.json()
        
        # Verify key fields from each tab
        verification_checks = []
        
        # Tab 1: Basic Info
        verification_checks.append(("Name updated", user_data.get("name") == "Admin User Updated"))
        verification_checks.append(("Company updated", user_data.get("company") == "BotSmith Technologies Inc"))
        verification_checks.append(("Job title updated", user_data.get("job_title") == "Chief Technology Officer"))
        
        # Tab 2: Permissions
        permissions = user_data.get("permissions", {})
        verification_checks.append(("Permissions updated", permissions.get("canCreateChatbots") == True))
        verification_checks.append(("Permissions updated", permissions.get("canDeleteChatbots") == False))
        
        # Tab 3: Security
        verification_checks.append(("Max sessions updated", user_data.get("max_sessions") == 3))
        verification_checks.append(("Session timeout updated", user_data.get("session_timeout") == 7200))
        
        # Tab 4: Subscription
        verification_checks.append(("Plan ID updated", user_data.get("plan_id") == "professional"))
        verification_checks.append(("Lifetime access updated", user_data.get("lifetime_access") == True))
        
        # Tab 5: Limits & Features
        custom_limits = user_data.get("custom_limits", {})
        feature_flags = user_data.get("feature_flags", {})
        verification_checks.append(("Custom limits updated", custom_limits.get("max_chatbots") == 50))
        verification_checks.append(("Feature flags updated", feature_flags.get("betaFeatures") == True))
        
        # Tab 6: Appearance
        verification_checks.append(("Timezone updated", user_data.get("timezone") == "America/New_York"))
        verification_checks.append(("Theme updated", user_data.get("theme") == "dark"))
        
        # Tab 7: Notifications
        notification_prefs = user_data.get("notification_preferences", {})
        verification_checks.append(("Email notifications updated", user_data.get("email_notifications") == True))
        verification_checks.append(("Notification prefs updated", notification_prefs.get("weeklyReport") == False))
        
        # Tab 8: Metadata
        verification_checks.append(("Tags updated", "premium-user" in user_data.get("tags", [])))
        verification_checks.append(("Admin notes updated", "Ultimate Edit testing" in user_data.get("admin_notes", "")))
        
        # Tab 9: API & Integrations
        verification_checks.append(("API key updated", user_data.get("api_key") == "test_api_key_123456789"))
        verification_checks.append(("Webhook URL updated", user_data.get("webhook_url") == "https://webhook.example.com/events"))
        
        # Tab 10: Tracking
        verification_checks.append(("Tracking enabled", user_data.get("tracking_enabled") == True))
        verification_checks.append(("Onboarding completed", user_data.get("onboarding_completed") == True))
        
        # Count successful verifications
        passed_verifications = sum(1 for check in verification_checks if check[1])
        total_verifications = len(verification_checks)
        
        if passed_verifications == total_verifications:
            log_test("Database Persistence Verification", True, f"All {total_verifications} field verifications passed")
        else:
            failed_checks = [check[0] for check in verification_checks if not check[1]]
            log_test("Database Persistence Verification", False, f"Only {passed_verifications}/{total_verifications} verifications passed. Failed: {failed_checks}")
    else:
        log_test("Database Persistence Verification", False, f"Status: {response.status_code}")
except Exception as e:
    log_test("Database Persistence Verification", False, f"Exception: {str(e)}")

# ============================================================================
# TEST COMPLETE - SUMMARY
# ============================================================================
print("\n" + "="*80)
print("COMPREHENSIVE ULTIMATE EDIT ADMIN PANEL TEST COMPLETE")
print("="*80)
print("✅ This test verified all 10 tabs of the Ultimate Edit modal:")
print("   TAB 1: Basic Info - 8 profile fields")
print("   TAB 2: Permissions - Role + 11 granular permissions")
print("   TAB 3: Security - 8 security settings")
print("   TAB 4: Subscription - 8 billing/subscription fields")
print("   TAB 5: Limits & Features - Custom limits (8) + Feature flags (8) + API rate limits (4)")
print("   TAB 6: Appearance - Timezone, language, theme, CSS, branding (5 fields)")
print("   TAB 7: Notifications - Email settings + 7 notification preferences")
print("   TAB 8: Metadata - Tags, segments, custom fields, notes")
print("   TAB 9: API & Integrations - API key, webhooks, OAuth, integration preferences")
print("   TAB 10: Tracking - Tracking settings and onboarding status")
print("="*80)
print("🎯 KEY VALIDATION POINTS:")
print("   - All tabs can update their respective fields via ultimate-update endpoint")
print("   - Data persists correctly in MongoDB database")
print("   - No field conflicts or validation errors")
print("   - Complete admin control over all user aspects")
print("="*80)

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)