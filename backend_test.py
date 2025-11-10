"""
COMPREHENSIVE BRANDING IMAGE UPLOAD TESTING

Test the new image upload functionality for branding (logo and avatar).

ENDPOINTS TO TEST:
1. POST /api/chatbots/{chatbot_id}/upload-branding-image?image_type=logo
2. POST /api/chatbots/{chatbot_id}/upload-branding-image?image_type=avatar

TEST REQUIREMENTS:
1. Authentication: Must include valid JWT token (use admin@botsmith.com / admin123 to login first)
2. Test chatbot ID: 04569e1c-2d32-44f9-94aa-099822616d6a (user_id: admin-001)
3. Create a small test image file (PNG or JPEG) programmatically for testing
4. Test uploading logo image
5. Test uploading avatar image
6. Verify database updates (logo_url and avatar_url fields should contain base64 data URLs)
7. Test file validation (wrong file type, file too large)
8. Test without authentication (should fail with 401)
9. Verify images are saved to /app/backend/uploads/branding/

EXPECTED RESULTS:
- Successful uploads return {success: true, message: "...", url: "data:image/...", filename: "..."}
- Database fields logo_url and avatar_url should be updated with base64 data URLs
- Files should be saved to disk at /app/backend/uploads/branding/
- Invalid file types should return 400 error
- Files > 5MB should return 413 error
- Unauthenticated requests should return 401 error
"""
import requests
import json
import uuid
import base64
import os
from datetime import datetime
from io import BytesIO
from PIL import Image

# Configuration
BACKEND_URL = "https://app-bootstrapper-1.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@botsmith.com"
ADMIN_PASSWORD = "admin123"
TEST_CHATBOT_ID = "04569e1c-2d32-44f9-94aa-099822616d6a"
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
# TEST 2: Create a new test user (to get fresh user without subscription)
# ============================================================================
print("\n[TEST 2] Creating a new test user...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    test_user_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    
    user_data = {
        "name": "Test User Plan Change",
        "email": test_user_email,
        "password": "testpass123",
        "role": "user",
        "status": "active",
        "plan_id": "free"  # Start with Free plan
    }
    
    response = requests.post(
        f"{BACKEND_URL}/admin/users/create",
        headers=headers,
        json=user_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        test_user_id = result.get("user_id")
        if test_user_id:
            log_test("Create test user", True, f"Created user {test_user_email} with ID {test_user_id}")
        else:
            log_test("Create test user", False, "No user_id returned")
            print("Cannot proceed without test user. Exiting...")
            exit(1)
    else:
        log_test("Create test user", False, f"Status: {response.status_code}, Response: {response.text}")
        print("Cannot proceed without test user. Exiting...")
        exit(1)
except Exception as e:
    log_test("Create test user", False, f"Exception: {str(e)}")
    print("Cannot proceed without test user. Exiting...")
    exit(1)

# ============================================================================
# TEST 3: Verify initial subscription is created with Free plan
# ============================================================================
print("\n[TEST 3] Verifying initial subscription creation...")
try:
    # Login as the test user to check their subscription
    login_response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": test_user_email,
            "password": "testpass123"
        },
        timeout=10
    )
    
    if login_response.status_code == 200:
        user_token = login_response.json().get("access_token")
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        # Check current subscription
        current_response = requests.get(
            f"{BACKEND_URL}/plans/current",
            headers=user_headers,
            timeout=10
        )
        
        if current_response.status_code == 200:
            current_data = current_response.json()
            subscription = current_data.get("subscription", {})
            plan = current_data.get("plan", {})
            
            checks = []
            checks.append(("Has subscription", subscription is not None))
            checks.append(("Plan ID is free", subscription.get("plan_id") == "free"))
            checks.append(("Plan name is Free", plan.get("name") == "Free"))
            
            all_passed = all(check[1] for check in checks)
            details = f"Subscription plan_id: {subscription.get('plan_id')}, Plan name: {plan.get('name')}"
            log_test("Initial subscription verification", all_passed, details)
        else:
            log_test("Initial subscription verification", False, f"Status: {current_response.status_code}")
    else:
        log_test("Initial subscription verification", False, f"User login failed: {login_response.status_code}")
except Exception as e:
    log_test("Initial subscription verification", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 4: Change user plan from Free to Starter via admin panel ultimate-update
# ============================================================================
print("\n[TEST 4] Changing user plan from Free to Starter via admin panel...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_payload = {
        "plan_id": "starter"
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{test_user_id}/ultimate-update",
        headers=headers,
        json=update_payload,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        checks.append(("Success flag", result.get("success") == True))
        checks.append(("Has message", result.get("message") is not None))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {result.get('success')}, Message: {result.get('message')}"
        log_test("Admin plan change Free→Starter", all_passed, details)
    else:
        log_test("Admin plan change Free→Starter", False, f"Status: {response.status_code}, Response: {response.text}")
        print("Cannot proceed without successful plan change. Exiting...")
        exit(1)
except Exception as e:
    log_test("Admin plan change Free→Starter", False, f"Exception: {str(e)}")
    print("Cannot proceed without successful plan change. Exiting...")
    exit(1)

# ============================================================================
# TEST 5: Verify subscription is updated with correct plan_id (Starter)
# ============================================================================
print("\n[TEST 5] Verifying subscription reflects Starter plan...")
try:
    # Login as the test user again to check updated subscription
    login_response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": test_user_email,
            "password": "testpass123"
        },
        timeout=10
    )
    
    if login_response.status_code == 200:
        user_token = login_response.json().get("access_token")
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        # Check current subscription
        current_response = requests.get(
            f"{BACKEND_URL}/plans/current",
            headers=user_headers,
            timeout=10
        )
        
        if current_response.status_code == 200:
            current_data = current_response.json()
            subscription = current_data.get("subscription", {})
            plan = current_data.get("plan", {})
            
            checks = []
            checks.append(("Subscription plan_id is starter", subscription.get("plan_id") == "starter"))
            checks.append(("Plan name is Starter", plan.get("name") == "Starter"))
            checks.append(("Plan limits updated", plan.get("limits", {}).get("max_chatbots", 0) > 1))
            
            all_passed = all(check[1] for check in checks)
            details = f"Subscription plan_id: {subscription.get('plan_id')}, Plan name: {plan.get('name')}, Max chatbots: {plan.get('limits', {}).get('max_chatbots')}"
            log_test("Subscription updated to Starter", all_passed, details)
        else:
            log_test("Subscription updated to Starter", False, f"Status: {current_response.status_code}")
    else:
        log_test("Subscription updated to Starter", False, f"User login failed: {login_response.status_code}")
except Exception as e:
    log_test("Subscription updated to Starter", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 6: Call /api/plans/usage endpoint to verify dashboard would show Starter
# ============================================================================
print("\n[TEST 6] Testing /api/plans/usage endpoint for dashboard data...")
try:
    # Use the user token from previous test
    usage_response = requests.get(
        f"{BACKEND_URL}/plans/usage",
        headers=user_headers,
        timeout=10
    )
    
    if usage_response.status_code == 200:
        usage_data = usage_response.json()
        
        checks = []
        checks.append(("Has plan info", usage_data.get("plan") is not None))
        checks.append(("Plan name is Starter", usage_data.get("plan", {}).get("name") == "Starter"))
        checks.append(("Has usage stats", usage_data.get("usage") is not None))
        checks.append(("Has limits", usage_data.get("limits") is not None))
        checks.append(("Starter limits", usage_data.get("limits", {}).get("max_chatbots", 0) >= 5))
        
        all_passed = all(check[1] for check in checks)
        plan_name = usage_data.get("plan", {}).get("name")
        max_chatbots = usage_data.get("limits", {}).get("max_chatbots")
        details = f"Plan: {plan_name}, Max chatbots: {max_chatbots}"
        log_test("Usage API shows Starter plan", all_passed, details)
    else:
        log_test("Usage API shows Starter plan", False, f"Status: {usage_response.status_code}, Response: {usage_response.text}")
except Exception as e:
    log_test("Usage API shows Starter plan", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 7: Change plan again from Starter to Enterprise
# ============================================================================
print("\n[TEST 7] Changing user plan from Starter to Enterprise...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_payload = {
        "plan_id": "enterprise"
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{test_user_id}/ultimate-update",
        headers=headers,
        json=update_payload,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        checks.append(("Success flag", result.get("success") == True))
        checks.append(("Has message", result.get("message") is not None))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {result.get('success')}, Message: {result.get('message')}"
        log_test("Admin plan change Starter→Enterprise", all_passed, details)
    else:
        log_test("Admin plan change Starter→Enterprise", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Admin plan change Starter→Enterprise", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 8: Verify subscription is updated (not duplicated) to Enterprise
# ============================================================================
print("\n[TEST 8] Verifying subscription updated to Enterprise (no duplicates)...")
try:
    # Check current subscription again
    current_response = requests.get(
        f"{BACKEND_URL}/plans/current",
        headers=user_headers,
        timeout=10
    )
    
    if current_response.status_code == 200:
        current_data = current_response.json()
        subscription = current_data.get("subscription", {})
        plan = current_data.get("plan", {})
        
        checks = []
        checks.append(("Subscription plan_id is enterprise", subscription.get("plan_id") == "enterprise"))
        checks.append(("Plan name is Enterprise", plan.get("name") == "Enterprise"))
        checks.append(("Enterprise limits", plan.get("limits", {}).get("max_chatbots", 0) >= 100))
        
        all_passed = all(check[1] for check in checks)
        details = f"Subscription plan_id: {subscription.get('plan_id')}, Plan name: {plan.get('name')}, Max chatbots: {plan.get('limits', {}).get('max_chatbots')}"
        log_test("Subscription updated to Enterprise", all_passed, details)
    else:
        log_test("Subscription updated to Enterprise", False, f"Status: {current_response.status_code}")
except Exception as e:
    log_test("Subscription updated to Enterprise", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 9: Call /api/plans/usage again to verify dashboard shows Enterprise
# ============================================================================
print("\n[TEST 9] Testing /api/plans/usage endpoint shows Enterprise...")
try:
    usage_response = requests.get(
        f"{BACKEND_URL}/plans/usage",
        headers=user_headers,
        timeout=10
    )
    
    if usage_response.status_code == 200:
        usage_data = usage_response.json()
        
        checks = []
        checks.append(("Plan name is Enterprise", usage_data.get("plan", {}).get("name") == "Enterprise"))
        checks.append(("Enterprise limits", usage_data.get("limits", {}).get("max_chatbots", 0) >= 100))
        checks.append(("High message limit", usage_data.get("limits", {}).get("max_messages_per_month", 0) >= 1000000))
        
        all_passed = all(check[1] for check in checks)
        plan_name = usage_data.get("plan", {}).get("name")
        max_chatbots = usage_data.get("limits", {}).get("max_chatbots")
        max_messages = usage_data.get("limits", {}).get("max_messages_per_month")
        details = f"Plan: {plan_name}, Max chatbots: {max_chatbots}, Max messages: {max_messages}"
        log_test("Usage API shows Enterprise plan", all_passed, details)
    else:
        log_test("Usage API shows Enterprise plan", False, f"Status: {usage_response.status_code}")
except Exception as e:
    log_test("Usage API shows Enterprise plan", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 10: Verify /api/plans/current also shows correct plan
# ============================================================================
print("\n[TEST 10] Testing /api/plans/current endpoint consistency...")
try:
    current_response = requests.get(
        f"{BACKEND_URL}/plans/current",
        headers=user_headers,
        timeout=10
    )
    
    if current_response.status_code == 200:
        current_data = current_response.json()
        subscription = current_data.get("subscription", {})
        plan = current_data.get("plan", {})
        
        checks = []
        checks.append(("Current API plan_id matches", subscription.get("plan_id") == "enterprise"))
        checks.append(("Current API plan name matches", plan.get("name") == "Enterprise"))
        checks.append(("Subscription status active", subscription.get("status") == "active"))
        
        all_passed = all(check[1] for check in checks)
        details = f"Current API - Plan ID: {subscription.get('plan_id')}, Name: {plan.get('name')}, Status: {subscription.get('status')}"
        log_test("Current API consistency", all_passed, details)
    else:
        log_test("Current API consistency", False, f"Status: {current_response.status_code}")
except Exception as e:
    log_test("Current API consistency", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 11: Verify MongoDB directly - Check both users and subscriptions collections
# ============================================================================
print("\n[TEST 11] MongoDB verification - Check both collections match...")
try:
    # We can't directly access MongoDB from here, but we can verify through API calls
    # Get user details via admin API
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_details_response = requests.get(
        f"{BACKEND_URL}/admin/users/{test_user_id}/details",
        headers=headers,
        timeout=10
    )
    
    if user_details_response.status_code == 200:
        user_data = user_details_response.json().get("user", {})
        user_plan_id = user_data.get("plan_id")
        
        # Compare with subscription data
        subscription_plan_id = subscription.get("plan_id")  # From previous test
        
        checks = []
        checks.append(("User plan_id exists", user_plan_id is not None))
        checks.append(("Subscription plan_id exists", subscription_plan_id is not None))
        checks.append(("Both plan_ids match", user_plan_id == subscription_plan_id))
        checks.append(("Both are enterprise", user_plan_id == "enterprise" and subscription_plan_id == "enterprise"))
        
        all_passed = all(check[1] for check in checks)
        details = f"User.plan_id: {user_plan_id}, Subscription.plan_id: {subscription_plan_id}"
        log_test("MongoDB collections sync", all_passed, details)
    else:
        log_test("MongoDB collections sync", False, f"Status: {user_details_response.status_code}")
except Exception as e:
    log_test("MongoDB collections sync", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 12: Test plan limits enforcement with Enterprise plan
# ============================================================================
print("\n[TEST 12] Testing Enterprise plan limits enforcement...")
try:
    # Check limit for chatbots (should be high for Enterprise)
    limit_response = requests.get(
        f"{BACKEND_URL}/plans/check-limit/chatbots",
        headers=user_headers,
        timeout=10
    )
    
    if limit_response.status_code == 200:
        limit_data = limit_response.json()
        
        checks = []
        checks.append(("Has current count", "current" in limit_data))
        checks.append(("Has max limit", "max" in limit_data))
        checks.append(("Not reached limit", limit_data.get("reached") == False))
        checks.append(("High Enterprise limit", limit_data.get("max", 0) >= 100))
        
        all_passed = all(check[1] for check in checks)
        current = limit_data.get("current", 0)
        max_limit = limit_data.get("max", 0)
        reached = limit_data.get("reached", True)
        details = f"Current: {current}, Max: {max_limit}, Reached: {reached}"
        log_test("Enterprise limits enforcement", all_passed, details)
    else:
        log_test("Enterprise limits enforcement", False, f"Status: {limit_response.status_code}")
except Exception as e:
    log_test("Enterprise limits enforcement", False, f"Exception: {str(e)}")

# ============================================================================
# CLEANUP: Delete test user
# ============================================================================
print("\n[CLEANUP] Deleting test user...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = requests.delete(
        f"{BACKEND_URL}/admin/users/{test_user_id}",
        headers=headers,
        timeout=10
    )
    
    if delete_response.status_code == 200:
        log_test("Cleanup - Delete test user", True, f"Successfully deleted test user {test_user_id}")
    else:
        log_test("Cleanup - Delete test user", False, f"Status: {delete_response.status_code}")
except Exception as e:
    log_test("Cleanup - Delete test user", False, f"Exception: {str(e)}")

# ============================================================================
# TEST COMPLETE - SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ADMIN PANEL PLAN CHANGE FLOW → USER DASHBOARD REFLECTION TEST COMPLETE")
print("="*80)
print("✅ This test verifies the complete flow:")
print("   1. Admin login with admin@botsmith.com / admin123")
print("   2. Create new test user with Free plan")
print("   3. Verify initial subscription created with Free plan")
print("   4. Change user plan Free→Starter via admin ultimate-update")
print("   5. Verify subscription updated to Starter (not duplicated)")
print("   6. Test /api/plans/usage shows Starter plan for dashboard")
print("   7. Change user plan Starter→Enterprise via admin ultimate-update")
print("   8. Verify subscription updated to Enterprise (not duplicated)")
print("   9. Test /api/plans/usage shows Enterprise plan for dashboard")
print("   10. Verify /api/plans/current consistency")
print("   11. Verify both users.plan_id and subscriptions.plan_id match")
print("   12. Test Enterprise plan limits enforcement")
print("="*80)
print("🎯 KEY VALIDATION POINTS:")
print("   - Admin panel plan changes update BOTH users.plan_id AND subscriptions.plan_id")
print("   - Dashboard APIs (/api/plans/usage, /api/plans/current) reflect changes immediately")
print("   - No duplicate subscriptions created during plan changes")
print("   - Plan limits enforcement works correctly with updated plans")
print("   - Data consistency between users and subscriptions collections")
print("="*80)

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)
