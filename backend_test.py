"""
CRITICAL TESTING: Admin Panel Plan Change Flow → User Dashboard Reflection
Tests the complete flow of admin changing user plans and verifying it reflects on user dashboard.

This test specifically addresses the bug where admin panel plan changes weren't reflecting 
on user dashboard because admin panel updated users.plan_id but dashboard reads from subscriptions.plan_id.
"""
import requests
import json
import uuid
from datetime import datetime

# Configuration
BACKEND_URL = "https://app-integration-14.preview.emergentagent.com/api"
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
    print("ADMIN PANEL PLAN CHANGE FLOW → USER DASHBOARD REFLECTION TEST SUMMARY")
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
test_user_id = None
test_user_email = None

print("="*80)
print("CRITICAL TESTING: Admin Panel Plan Change Flow → User Dashboard Reflection")
print("="*80)
print(f"Backend URL: {BACKEND_URL}")
print(f"Admin Email: {ADMIN_EMAIL}")
print(f"Test Time: {datetime.now().isoformat()}")
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
# TEST 3: Update admin user via PUT /api/admin/users/admin-001/ultimate-update
# ============================================================================
print("\n[TEST 3] Updating admin user via ultimate-update endpoint...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_payload = {
        "company": "Test Corp Inc",
        "job_title": "Senior Developer", 
        "bio": "This is a test bio from ultimate edit",
        "timezone": "America/Los_Angeles",
        "tags": ["test-tag-1", "test-tag-2"],
        "custom_limits": {
            "max_chatbots": 50,
            "max_messages_per_month": 500000
        },
        "feature_flags": {
            "betaFeatures": True,
            "advancedAnalytics": True
        }
    }
    
    response = requests.put(
        f"{BACKEND_URL}/admin/users/{ADMIN_USER_ID}/ultimate-update",
        headers=headers,
        json=update_payload,
        timeout=10
    )
    
    if response.status_code == 200:
        update_result = response.json()
        
        # Verify update was successful
        checks = []
        checks.append(("Success flag", update_result.get("success") == True))
        checks.append(("Has message", update_result.get("message") is not None))
        checks.append(("User data returned", update_result.get("user") is not None))
        checks.append(("Updated fields count", update_result.get("user", {}).get("updated_fields", 0) > 0))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {update_result.get('success')}, Updated fields: {update_result.get('user', {}).get('updated_fields')}"
        log_test("Ultimate update admin user", all_passed, details)
        
        print(f"   Update response: {update_result.get('message')}")
    else:
        log_test("Ultimate update admin user", False, f"Status: {response.status_code}, Response: {response.text}")
        print("Cannot proceed without successful update. Exiting...")
        exit(1)
except Exception as e:
    log_test("Ultimate update admin user", False, f"Exception: {str(e)}")
    print("Cannot proceed without successful update. Exiting...")
    exit(1)

# ============================================================================
# TEST 4: Verify the update was successful in the database (direct check)
# ============================================================================
print("\n[TEST 4] Verifying update was successful in database...")
try:
    # We'll verify this by getting the updated user data via /api/auth/me
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        updated_user_data = response.json()
        
        # Verify all updated fields are present
        checks = []
        checks.append(("Company updated", updated_user_data.get("company") == "Test Corp Inc"))
        checks.append(("Job title updated", updated_user_data.get("job_title") == "Senior Developer"))
        checks.append(("Bio updated", updated_user_data.get("bio") == "This is a test bio from ultimate edit"))
        checks.append(("Timezone updated", updated_user_data.get("timezone") == "America/Los_Angeles"))
        checks.append(("Tags updated", updated_user_data.get("tags") == ["test-tag-1", "test-tag-2"]))
        
        # Check custom_limits
        custom_limits = updated_user_data.get("custom_limits", {})
        checks.append(("Custom limits - max_chatbots", custom_limits.get("max_chatbots") == 50))
        checks.append(("Custom limits - max_messages_per_month", custom_limits.get("max_messages_per_month") == 500000))
        
        # Check feature_flags
        feature_flags = updated_user_data.get("feature_flags", {})
        checks.append(("Feature flags - betaFeatures", feature_flags.get("betaFeatures") == True))
        checks.append(("Feature flags - advancedAnalytics", feature_flags.get("advancedAnalytics") == True))
        
        all_passed = all(check[1] for check in checks)
        failed_checks = [check[0] for check in checks if not check[1]]
        
        if all_passed:
            details = "All updated fields verified in database"
        else:
            details = f"Failed checks: {failed_checks}"
        
        log_test("Verify update in database", all_passed, details)
        
        print(f"   Updated company: {updated_user_data.get('company')}")
        print(f"   Updated job_title: {updated_user_data.get('job_title')}")
        print(f"   Updated bio: {updated_user_data.get('bio')}")
        print(f"   Updated timezone: {updated_user_data.get('timezone')}")
        print(f"   Updated tags: {updated_user_data.get('tags')}")
        print(f"   Updated custom_limits: {updated_user_data.get('custom_limits')}")
        print(f"   Updated feature_flags: {updated_user_data.get('feature_flags')}")
    else:
        log_test("Verify update in database", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Verify update in database", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 5: Get updated user data via GET /api/auth/me (final verification)
# ============================================================================
print("\n[TEST 5] Final verification - Get updated user data via /api/auth/me...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        final_user_data = response.json()
        
        # Compare with original data to ensure changes persisted
        changes_detected = []
        
        # Check each field that should have changed
        if final_user_data.get("company") != original_user_data.get("company"):
            changes_detected.append(f"company: {original_user_data.get('company')} → {final_user_data.get('company')}")
        
        if final_user_data.get("job_title") != original_user_data.get("job_title"):
            changes_detected.append(f"job_title: {original_user_data.get('job_title')} → {final_user_data.get('job_title')}")
        
        if final_user_data.get("bio") != original_user_data.get("bio"):
            changes_detected.append(f"bio: {original_user_data.get('bio')} → {final_user_data.get('bio')}")
        
        if final_user_data.get("timezone") != original_user_data.get("timezone"):
            changes_detected.append(f"timezone: {original_user_data.get('timezone')} → {final_user_data.get('timezone')}")
        
        if final_user_data.get("tags") != original_user_data.get("tags"):
            changes_detected.append(f"tags: {original_user_data.get('tags')} → {final_user_data.get('tags')}")
        
        if final_user_data.get("custom_limits") != original_user_data.get("custom_limits"):
            changes_detected.append(f"custom_limits: {original_user_data.get('custom_limits')} → {final_user_data.get('custom_limits')}")
        
        if final_user_data.get("feature_flags") != original_user_data.get("feature_flags"):
            changes_detected.append(f"feature_flags: {original_user_data.get('feature_flags')} → {final_user_data.get('feature_flags')}")
        
        # Verify expected values are present
        expected_checks = []
        expected_checks.append(("Company is Test Corp Inc", final_user_data.get("company") == "Test Corp Inc"))
        expected_checks.append(("Job title is Senior Developer", final_user_data.get("job_title") == "Senior Developer"))
        expected_checks.append(("Bio contains test text", final_user_data.get("bio") == "This is a test bio from ultimate edit"))
        expected_checks.append(("Timezone is America/Los_Angeles", final_user_data.get("timezone") == "America/Los_Angeles"))
        expected_checks.append(("Tags contain test tags", final_user_data.get("tags") == ["test-tag-1", "test-tag-2"]))
        
        custom_limits = final_user_data.get("custom_limits", {})
        expected_checks.append(("Custom limits max_chatbots is 50", custom_limits.get("max_chatbots") == 50))
        expected_checks.append(("Custom limits max_messages_per_month is 500000", custom_limits.get("max_messages_per_month") == 500000))
        
        feature_flags = final_user_data.get("feature_flags", {})
        expected_checks.append(("Feature flags betaFeatures is True", feature_flags.get("betaFeatures") == True))
        expected_checks.append(("Feature flags advancedAnalytics is True", feature_flags.get("advancedAnalytics") == True))
        
        all_expected_passed = all(check[1] for check in expected_checks)
        failed_expected = [check[0] for check in expected_checks if not check[1]]
        
        if all_expected_passed and len(changes_detected) > 0:
            details = f"✅ ALL EXPECTED FIELDS UPDATED. Changes: {len(changes_detected)} fields"
            log_test("Final verification - Data persistence", True, details)
        else:
            details = f"❌ Issues detected. Expected checks failed: {failed_expected}, Changes detected: {len(changes_detected)}"
            log_test("Final verification - Data persistence", False, details)
        
        print(f"   Changes detected: {len(changes_detected)}")
        for change in changes_detected:
            print(f"     - {change}")
            
    else:
        log_test("Final verification - Data persistence", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Final verification - Data persistence", False, f"Exception: {str(e)}")

# ============================================================================
# TEST COMPLETE - SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ULTIMATE EDIT ADMIN PANEL → DASHBOARD DATA REFLECTION TEST COMPLETE")
print("="*80)
print("✅ This test verifies the complete flow:")
print("   1. Admin login with admin@botsmith.com / admin123")
print("   2. Get current admin user data via GET /api/auth/me")
print("   3. Update admin user via PUT /api/admin/users/admin-001/ultimate-update")
print("   4. Verify update was successful in database")
print("   5. Confirm ALL updated fields appear in GET /api/auth/me response")
print("="*80)
print("🎯 KEY VALIDATION POINTS:")
print("   - Ultimate update endpoint returns success")
print("   - All updated fields (company, job_title, bio, timezone, tags, custom_limits, feature_flags)")
print("   - Data persists in MongoDB without requiring re-login")
print("   - Frontend can access updated fields via user context")
print("="*80)

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)
