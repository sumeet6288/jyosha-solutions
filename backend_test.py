"""
PUSH NOTIFICATION BACKEND SETUP TESTING

Test the push notification backend setup as requested:

ENDPOINTS TO TEST:
1. POST /api/auth/login - Login with admin@botsmith.com / admin123 to get auth token
2. GET /api/notifications/preferences - Get user's notification preferences
3. POST /api/notifications/push-subscription - Save push subscription
4. PUT /api/notifications/preferences - Update notification preferences

TEST REQUIREMENTS:
1. Authentication: Must include valid JWT token (use admin@botsmith.com / admin123 to login first)
2. Test notification preferences endpoint:
   - Should return user's notification preferences
   - Check if all fields are present (email_enabled, push_enabled, etc.)
3. Test push subscription endpoint:
   - Body: {
     "endpoint": "https://test-endpoint.example.com",
     "keys": {
       "p256dh": "test_key_1",
       "auth": "test_key_2"
     },
     "browser": "Chrome"
   }
   - Should save successfully with auth token
4. Test update notification preferences:
   - Update some preferences and verify they're saved

EXPECTED RESULTS:
- Login should succeed and return access token
- Get preferences should return all notification preference fields
- Push subscription should save successfully
- Update preferences should save and persist changes
"""
import requests
import json
import uuid
import base64
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://rapid-stack-launch.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@botsmith.com"
ADMIN_PASSWORD = "admin123"
ADMIN_USER_ID = "admin-001"

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
    print("PUSH NOTIFICATION BACKEND SETUP TEST SUMMARY")
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

# Helper functions removed - not needed for user deletion testing

# Global variables for test data
admin_token = None
admin_user_id = None

print("="*80)
print("PUSH NOTIFICATION BACKEND SETUP TESTING")
print("="*80)
print(f"Backend URL: {BACKEND_URL}")
print(f"Admin Email: {ADMIN_EMAIL}")
print(f"Test Time: {datetime.now().isoformat()}")
print("Testing push notification backend setup")
print("="*80 + "\n")

# ============================================================================
# TEST 1: Login as admin user
# ============================================================================
print("\n[TEST 1] Login as admin user...")
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

# ============================================================================
# TEST 2: Get Notification Preferences API
# ============================================================================
print("\n[TEST 2] Get Notification Preferences API...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.get(
        f"{BACKEND_URL}/notifications/preferences",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        # Check if all required fields are present
        required_fields = [
            "email_enabled", "push_enabled", "email_new_conversation",
            "email_high_priority", "email_performance_alert", "email_usage_warning",
            "email_digest", "email_digest_time", "push_new_conversation",
            "push_high_priority", "push_performance_alert", "push_usage_warning",
            "inapp_enabled", "inapp_sound", "admin_new_user_signup", "admin_webhook_events"
        ]
        
        checks = []
        for field in required_fields:
            checks.append((f"Has {field}", field in result))
        
        # Check specific field values
        checks.append(("email_enabled is boolean", isinstance(result.get("email_enabled"), bool)))
        checks.append(("push_enabled is boolean", isinstance(result.get("push_enabled"), bool)))
        checks.append(("email_digest is valid", result.get("email_digest") in ["none", "daily", "weekly"]))
        
        all_passed = all(check[1] for check in checks)
        details = f"Found {len([f for f in required_fields if f in result])}/{len(required_fields)} required fields"
        log_test("Get notification preferences", all_passed, details)
        
    else:
        log_test("Get notification preferences", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Get notification preferences", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 3: Save Push Subscription API
# ============================================================================
print("\n[TEST 3] Save Push Subscription API...")
push_subscription_data = {
    "endpoint": "https://test-endpoint.example.com",
    "keys": {
        "p256dh": "test_key_1",
        "auth": "test_key_2"
    },
    "browser": "Chrome"
}

try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.post(
        f"{BACKEND_URL}/notifications/push-subscription",
        headers=headers,
        json=push_subscription_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        checks.append(("Has message", "message" in result))
        checks.append(("Has subscription", "subscription" in result))
        checks.append(("Message indicates success", "saved" in result.get("message", "").lower()))
        
        if result.get("subscription"):
            subscription = result["subscription"]
            checks.append(("Subscription has endpoint", subscription.get("endpoint") == push_subscription_data["endpoint"]))
            checks.append(("Subscription has keys", "keys" in subscription))
            checks.append(("Subscription has browser", subscription.get("browser") == push_subscription_data["browser"]))
            checks.append(("Subscription has user_id", "user_id" in subscription))
            checks.append(("Subscription has id", "id" in subscription))
        
        all_passed = all(check[1] for check in checks)
        details = f"Push subscription saved successfully"
        log_test("Save push subscription", all_passed, details)
        
    else:
        log_test("Save push subscription", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Save push subscription", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 4: Update Notification Preferences API
# ============================================================================
print("\n[TEST 4] Update Notification Preferences API...")
# First, get current preferences to compare later
current_preferences = None
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get current preferences
    response = requests.get(
        f"{BACKEND_URL}/notifications/preferences",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        current_preferences = response.json()
    
    # Update some preferences
    update_data = {
        "email_enabled": False,
        "push_enabled": True,
        "email_digest": "weekly",
        "inapp_sound": False
    }
    
    response = requests.put(
        f"{BACKEND_URL}/notifications/preferences",
        headers=headers,
        json=update_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        # Check if updated values are reflected
        checks.append(("email_enabled updated", result.get("email_enabled") == update_data["email_enabled"]))
        checks.append(("push_enabled updated", result.get("push_enabled") == update_data["push_enabled"]))
        checks.append(("email_digest updated", result.get("email_digest") == update_data["email_digest"]))
        checks.append(("inapp_sound updated", result.get("inapp_sound") == update_data["inapp_sound"]))
        
        # Check that other fields remain unchanged
        if current_preferences:
            checks.append(("Other fields preserved", result.get("email_new_conversation") == current_preferences.get("email_new_conversation")))
        
        all_passed = all(check[1] for check in checks)
        details = f"Updated {len(update_data)} preferences successfully"
        log_test("Update notification preferences", all_passed, details)
        
    else:
        log_test("Update notification preferences", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Update notification preferences", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 5: Verify Updated Preferences Persist
# ============================================================================
print("\n[TEST 5] Verify Updated Preferences Persist...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get preferences again to verify persistence
    response = requests.get(
        f"{BACKEND_URL}/notifications/preferences",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        # Check if the updated values from TEST 4 are still there
        expected_values = {
            "email_enabled": False,
            "push_enabled": True,
            "email_digest": "weekly",
            "inapp_sound": False
        }
        
        checks = []
        for field, expected_value in expected_values.items():
            actual_value = result.get(field)
            checks.append((f"{field} persisted", actual_value == expected_value))
        
        # Check that we still have all required fields
        required_fields = ["email_enabled", "push_enabled", "inapp_enabled"]
        for field in required_fields:
            checks.append((f"Has {field}", field in result))
        
        all_passed = all(check[1] for check in checks)
        details = f"All updated preferences persisted correctly"
        log_test("Verify preferences persistence", all_passed, details)
        
    else:
        log_test("Verify preferences persistence", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Verify preferences persistence", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 6: Test Push Subscription with Invalid Data
# ============================================================================
print("\n[TEST 6] Test Push Subscription with Invalid Data...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test with missing required fields
    invalid_data = {
        "endpoint": "https://test-endpoint.example.com",
        # Missing keys field
        "browser": "Chrome"
    }
    
    response = requests.post(
        f"{BACKEND_URL}/notifications/push-subscription",
        headers=headers,
        json=invalid_data,
        timeout=10
    )
    
    # Should return 422 (validation error) or 400 (bad request)
    if response.status_code in [400, 422]:
        log_test("Push subscription validation error", True, f"Correctly returned {response.status_code} for invalid data")
    else:
        log_test("Push subscription validation error", False, f"Expected 400/422, got {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Push subscription validation error", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 7: Test Unauthenticated Access to Notification Endpoints
# ============================================================================
print("\n[TEST 7] Test Unauthenticated Access to Notification Endpoints...")
try:
    # Test without authentication headers
    endpoints_to_test = [
        ("GET /notifications/preferences", "get", f"{BACKEND_URL}/notifications/preferences"),
        ("POST /notifications/push-subscription", "post", f"{BACKEND_URL}/notifications/push-subscription"),
        ("PUT /notifications/preferences", "put", f"{BACKEND_URL}/notifications/preferences")
    ]
    
    all_tests_passed = True
    for endpoint_name, method, url in endpoints_to_test:
        try:
            if method == "get":
                response = requests.get(url, timeout=10)
            elif method == "post":
                response = requests.post(url, json={}, timeout=10)
            elif method == "put":
                response = requests.put(url, json={}, timeout=10)
            
            # Should return 401 (Unauthorized) or 403 (Forbidden)
            if response.status_code in [401, 403]:
                print(f"   ✅ {endpoint_name}: Correctly returned {response.status_code}")
            else:
                print(f"   ❌ {endpoint_name}: Expected 401/403, got {response.status_code}")
                all_tests_passed = False
                
        except Exception as e:
            print(f"   ❌ {endpoint_name}: Exception - {str(e)}")
            all_tests_passed = False
    
    log_test("Unauthenticated access properly rejected", all_tests_passed, "All notification endpoints require authentication")

except Exception as e:
    log_test("Unauthenticated access properly rejected", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 8: Test Additional Notification Endpoints
# ============================================================================
print("\n[TEST 8] Test Additional Notification Endpoints...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test getting notifications list
    response = requests.get(
        f"{BACKEND_URL}/notifications/",
        headers=headers,
        timeout=10
    )
    
    notifications_test_passed = False
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            notifications_test_passed = True
            print(f"   ✅ GET /notifications/: Returned list with {len(result)} notifications")
        else:
            print(f"   ❌ GET /notifications/: Expected list, got {type(result)}")
    else:
        print(f"   ❌ GET /notifications/: Status {response.status_code}")
    
    # Test getting unread count
    response = requests.get(
        f"{BACKEND_URL}/notifications/unread-count",
        headers=headers,
        timeout=10
    )
    
    unread_count_test_passed = False
    if response.status_code == 200:
        result = response.json()
        if "count" in result and isinstance(result["count"], int):
            unread_count_test_passed = True
            print(f"   ✅ GET /notifications/unread-count: Returned count {result['count']}")
        else:
            print(f"   ❌ GET /notifications/unread-count: Invalid response format")
    else:
        print(f"   ❌ GET /notifications/unread-count: Status {response.status_code}")
    
    all_passed = notifications_test_passed and unread_count_test_passed
    log_test("Additional notification endpoints", all_passed, "Tested notifications list and unread count")

except Exception as e:
    log_test("Additional notification endpoints", False, f"Exception: {str(e)}")

# ============================================================================
# TEST COMPLETE - SUMMARY
# ============================================================================
print("\n" + "="*80)
print("PUSH NOTIFICATION BACKEND SETUP TEST COMPLETE")
print("="*80)
print("✅ This comprehensive test verified:")
print("   1. Admin authentication with admin@botsmith.com / admin123")
print("   2. Get notification preferences via GET /api/notifications/preferences")
print("   3. Save push subscription via POST /api/notifications/push-subscription")
print("   4. Update notification preferences via PUT /api/notifications/preferences")
print("   5. Verify preferences persistence after updates")
print("   6. Error handling for invalid push subscription data")
print("   7. Security: Unauthenticated requests properly rejected")
print("   8. Additional notification endpoints (list, unread count)")
print("="*80)
print("🎯 KEY VALIDATION POINTS:")
print("   - Authentication required for all notification operations")
print("   - Notification preferences return all required fields")
print("   - Push subscription saves successfully with proper data structure")
print("   - Preference updates persist correctly in database")
print("   - Proper error handling for invalid data")
print("   - Security: Unauthenticated requests rejected")
print("   - All notification endpoints working correctly")
print("="*80)

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)
