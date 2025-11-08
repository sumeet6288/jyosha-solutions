"""
CRITICAL TESTING: Ultimate Edit Admin Panel → Dashboard Data Reflection
Tests the complete flow of data synchronization between admin panel ultimate edit and user dashboard.
"""
import requests
import json
import uuid
from datetime import datetime

# Configuration
BACKEND_URL = "https://ready-dep-setup.preview.emergentagent.com/api"
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
    print("ULTIMATE EDIT ADMIN PANEL → DASHBOARD DATA REFLECTION TEST SUMMARY")
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
original_user_data = None
updated_user_data = None

print("="*80)
print("CRITICAL TESTING: Ultimate Edit Admin Panel → Dashboard Data Reflection")
print("="*80)
print(f"Backend URL: {BACKEND_URL}")
print(f"Admin Email: {ADMIN_EMAIL}")
print(f"Admin User ID: {ADMIN_USER_ID}")
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
# TEST 2: Get admin user's current data via GET /api/auth/me
# ============================================================================
print("\n[TEST 2] Getting admin user's current data...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        original_user_data = response.json()
        
        # Verify we got the admin user
        checks = []
        checks.append(("Correct user ID", original_user_data.get("id") == ADMIN_USER_ID))
        checks.append(("Correct email", original_user_data.get("email") == ADMIN_EMAIL))
        checks.append(("Has name", original_user_data.get("name") is not None))
        checks.append(("Is admin role", original_user_data.get("role") == "admin"))
        
        all_passed = all(check[1] for check in checks)
        details = f"User ID: {original_user_data.get('id')}, Email: {original_user_data.get('email')}, Role: {original_user_data.get('role')}"
        log_test("Get admin user current data", all_passed, details)
        
        # Store original values for comparison
        print(f"   Original company: {original_user_data.get('company')}")
        print(f"   Original job_title: {original_user_data.get('job_title')}")
        print(f"   Original bio: {original_user_data.get('bio')}")
        print(f"   Original timezone: {original_user_data.get('timezone')}")
        print(f"   Original tags: {original_user_data.get('tags')}")
        print(f"   Original custom_limits: {original_user_data.get('custom_limits')}")
        print(f"   Original feature_flags: {original_user_data.get('feature_flags')}")
    else:
        log_test("Get admin user current data", False, f"Status: {response.status_code}, Response: {response.text}")
        print("Cannot proceed without original user data. Exiting...")
        exit(1)
except Exception as e:
    log_test("Get admin user current data", False, f"Exception: {str(e)}")
    print("Cannot proceed without original user data. Exiting...")
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
# TEST 5: Setup MS Teams Webhook
# ============================================================================
print("\n[TEST 5] Setting up MS Teams webhook...")
try:
    response = requests.post(
        f"{BACKEND_URL}/msteams/{chatbot_id}/setup-webhook",
        timeout=10
    )
    
    if response.status_code == 200:
        webhook_data = response.json()
        webhook_url = webhook_data.get("webhook_url")
        instructions = webhook_data.get("instructions")
        status = webhook_data.get("status")
        
        checks = []
        checks.append(("Has webhook_url", webhook_url is not None))
        checks.append(("Webhook URL format", webhook_url and "/api/msteams/webhook/" in webhook_url))
        checks.append(("Has instructions", instructions is not None and len(instructions) > 0))
        checks.append(("Status is configured", status == "configured"))
        
        all_passed = all(check[1] for check in checks)
        details = f"Webhook URL: {webhook_url}, Status: {status}"
        log_test("Setup MS Teams webhook", all_passed, details)
    else:
        log_test("Setup MS Teams webhook", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Setup MS Teams webhook", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 6: Get MS Teams Webhook Info
# ============================================================================
print("\n[TEST 6] Getting MS Teams webhook info...")
try:
    response = requests.get(
        f"{BACKEND_URL}/msteams/{chatbot_id}/webhook-info",
        timeout=10
    )
    
    if response.status_code == 200:
        webhook_info = response.json()
        configured = webhook_info.get("configured")
        webhook_url = webhook_info.get("webhook_url")
        
        if configured:
            checks = []
            checks.append(("Configured is True", configured == True))
            checks.append(("Has webhook_url", webhook_url is not None))
            checks.append(("Has status", webhook_info.get("status") is not None))
            
            all_passed = all(check[1] for check in checks)
            details = f"Configured: {configured}, URL: {webhook_url}"
            log_test("Get webhook info", all_passed, details)
        else:
            log_test("Get webhook info", False, "Webhook not configured after setup")
    else:
        log_test("Get webhook info", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Get webhook info", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 7: Toggle Integration (Enable)
# ============================================================================
print("\n[TEST 7] Enabling MS Teams integration...")
try:
    response = requests.post(
        f"{BACKEND_URL}/integrations/{chatbot_id}/{integration_id}/toggle",
        timeout=10
    )
    
    if response.status_code == 200:
        toggle_result = response.json()
        success = toggle_result.get("success")
        enabled = toggle_result.get("enabled")
        
        if success and enabled == True:
            log_test("Enable integration", True, f"Integration enabled: {enabled}")
        else:
            log_test("Enable integration", False, f"Unexpected result: {toggle_result}")
    else:
        log_test("Enable integration", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Enable integration", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 8: Verify integration is enabled
# ============================================================================
print("\n[TEST 8] Verifying integration is enabled...")
try:
    response = requests.get(
        f"{BACKEND_URL}/integrations/{chatbot_id}",
        timeout=10
    )
    
    if response.status_code == 200:
        integrations = response.json()
        msteams_integration = next((i for i in integrations if i.get("integration_type") == "msteams"), None)
        
        if msteams_integration and msteams_integration.get("enabled") == True:
            log_test("Verify integration enabled", True, "Integration is enabled")
        else:
            log_test("Verify integration enabled", False, f"Integration enabled status: {msteams_integration.get('enabled') if msteams_integration else 'Not found'}")
    else:
        log_test("Verify integration enabled", False, f"Status: {response.status_code}")
except Exception as e:
    log_test("Verify integration enabled", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 9: Toggle Integration (Disable)
# ============================================================================
print("\n[TEST 9] Disabling MS Teams integration...")
try:
    response = requests.post(
        f"{BACKEND_URL}/integrations/{chatbot_id}/{integration_id}/toggle",
        timeout=10
    )
    
    if response.status_code == 200:
        toggle_result = response.json()
        success = toggle_result.get("success")
        enabled = toggle_result.get("enabled")
        
        if success and enabled == False:
            log_test("Disable integration", True, f"Integration disabled: {enabled}")
        else:
            log_test("Disable integration", False, f"Unexpected result: {toggle_result}")
    else:
        log_test("Disable integration", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Disable integration", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 10: Get Integration Logs
# ============================================================================
print("\n[TEST 10] Getting integration activity logs...")
try:
    response = requests.get(
        f"{BACKEND_URL}/integrations/{chatbot_id}/logs",
        timeout=10
    )
    
    if response.status_code == 200:
        logs = response.json()
        
        if isinstance(logs, list):
            # Check if we have logs for our MS Teams integration
            msteams_logs = [log for log in logs if log.get("integration_id") == integration_id]
            
            if len(msteams_logs) > 0:
                log_test("Get integration logs", True, f"Found {len(msteams_logs)} MS Teams integration logs")
            else:
                log_test("Get integration logs", True, f"No MS Teams logs yet (total logs: {len(logs)})")
        else:
            log_test("Get integration logs", False, f"Unexpected response format: {type(logs)}")
    else:
        log_test("Get integration logs", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Get integration logs", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 11: Update MS Teams Integration Credentials
# ============================================================================
print("\n[TEST 11] Updating MS Teams integration credentials...")
try:
    response = requests.post(
        f"{BACKEND_URL}/integrations/{chatbot_id}",
        json={
            "integration_type": "msteams",
            "credentials": {
                "app_id": "updated-app-id-99999",
                "app_password": "updated-app-password-88888"
            },
            "metadata": {
                "description": "Updated MS Teams integration"
            }
        },
        timeout=10
    )
    
    if response.status_code == 200:
        integration_data = response.json()
        
        # Verify it's the same integration (updated, not new)
        if integration_data.get("id") == integration_id:
            log_test("Update integration credentials", True, f"Integration updated successfully")
        else:
            log_test("Update integration credentials", False, f"Got different integration ID: {integration_data.get('id')}")
    else:
        log_test("Update integration credentials", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Update integration credentials", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 12: Test with invalid chatbot ID
# ============================================================================
print("\n[TEST 12] Testing with invalid chatbot ID...")
try:
    invalid_chatbot_id = str(uuid.uuid4())
    response = requests.post(
        f"{BACKEND_URL}/msteams/{invalid_chatbot_id}/setup-webhook",
        timeout=10
    )
    
    if response.status_code == 404:
        log_test("Invalid chatbot ID handling", True, "Properly returned 404 for invalid chatbot")
    else:
        log_test("Invalid chatbot ID handling", False, f"Expected 404, got {response.status_code}")
except Exception as e:
    log_test("Invalid chatbot ID handling", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 13: Test with invalid integration ID
# ============================================================================
print("\n[TEST 13] Testing with invalid integration ID...")
try:
    invalid_integration_id = str(uuid.uuid4())
    response = requests.post(
        f"{BACKEND_URL}/integrations/{chatbot_id}/{invalid_integration_id}/toggle",
        timeout=10
    )
    
    if response.status_code == 404:
        log_test("Invalid integration ID handling", True, "Properly returned 404 for invalid integration")
    else:
        log_test("Invalid integration ID handling", False, f"Expected 404, got {response.status_code}")
except Exception as e:
    log_test("Invalid integration ID handling", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 14: Create MS Teams integration with missing credentials
# ============================================================================
print("\n[TEST 14] Testing with missing credentials...")
try:
    response = requests.post(
        f"{BACKEND_URL}/integrations/{chatbot_id}",
        json={
            "integration_type": "msteams",
            "credentials": {
                "app_id": "only-app-id"
                # Missing app_password
            }
        },
        timeout=10
    )
    
    # Should still create but fail on test
    if response.status_code in [200, 400, 422]:
        log_test("Missing credentials handling", True, f"Handled missing credentials (status: {response.status_code})")
    else:
        log_test("Missing credentials handling", False, f"Unexpected status: {response.status_code}")
except Exception as e:
    log_test("Missing credentials handling", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 15: Delete MS Teams webhook configuration
# ============================================================================
print("\n[TEST 15] Deleting MS Teams webhook configuration...")
try:
    response = requests.delete(
        f"{BACKEND_URL}/msteams/{chatbot_id}/webhook",
        timeout=10
    )
    
    if response.status_code == 200:
        delete_result = response.json()
        success = delete_result.get("success")
        
        if success:
            log_test("Delete webhook config", True, "Webhook configuration deleted")
        else:
            log_test("Delete webhook config", False, f"Delete failed: {delete_result}")
    else:
        log_test("Delete webhook config", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Delete webhook config", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 16: Verify webhook is deleted
# ============================================================================
print("\n[TEST 16] Verifying webhook is deleted...")
try:
    response = requests.get(
        f"{BACKEND_URL}/msteams/{chatbot_id}/webhook-info",
        timeout=10
    )
    
    if response.status_code == 200:
        webhook_info = response.json()
        configured = webhook_info.get("configured")
        
        if configured == False:
            log_test("Verify webhook deleted", True, "Webhook properly marked as not configured")
        else:
            log_test("Verify webhook deleted", False, f"Webhook still configured: {webhook_info}")
    else:
        log_test("Verify webhook deleted", False, f"Status: {response.status_code}")
except Exception as e:
    log_test("Verify webhook deleted", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 17: Delete MS Teams Integration
# ============================================================================
print("\n[TEST 17] Deleting MS Teams integration...")
try:
    response = requests.delete(
        f"{BACKEND_URL}/integrations/{chatbot_id}/{integration_id}",
        timeout=10
    )
    
    if response.status_code == 200:
        delete_result = response.json()
        success = delete_result.get("success")
        
        if success:
            log_test("Delete integration", True, "Integration deleted successfully")
        else:
            log_test("Delete integration", False, f"Delete failed: {delete_result}")
    else:
        log_test("Delete integration", False, f"Status: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Delete integration", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 18: Verify integration is deleted
# ============================================================================
print("\n[TEST 18] Verifying integration is deleted...")
try:
    response = requests.get(
        f"{BACKEND_URL}/integrations/{chatbot_id}",
        timeout=10
    )
    
    if response.status_code == 200:
        integrations = response.json()
        msteams_integration = next((i for i in integrations if i.get("integration_type") == "msteams"), None)
        
        if msteams_integration is None:
            log_test("Verify integration deleted", True, "MS Teams integration not found in list")
        else:
            log_test("Verify integration deleted", False, f"Integration still exists: {msteams_integration.get('id')}")
    else:
        log_test("Verify integration deleted", False, f"Status: {response.status_code}")
except Exception as e:
    log_test("Verify integration deleted", False, f"Exception: {str(e)}")

# ============================================================================
# CLEANUP: Delete test chatbot
# ============================================================================
print("\n[CLEANUP] Deleting test chatbot...")
try:
    response = requests.delete(
        f"{BACKEND_URL}/chatbots/{chatbot_id}",
        timeout=10
    )
    
    if response.status_code in [200, 204]:
        log_test("Cleanup: Delete test chatbot", True, "Test chatbot deleted")
    else:
        log_test("Cleanup: Delete test chatbot", False, f"Status: {response.status_code}")
except Exception as e:
    log_test("Cleanup: Delete test chatbot", False, f"Exception: {str(e)}")

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)
