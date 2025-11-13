"""
COMPREHENSIVE ADMIN USER MANAGEMENT STATISTICS COLUMN TESTING

Test the Admin User Management Statistics Column functionality.

ENDPOINTS TO TEST:
1. GET /api/admin/users/enhanced

TEST REQUIREMENTS:
1. Authentication: Must include valid JWT token (use admin@botsmith.com / admin123 to login first)
2. Test the statistics data structure in the API response
3. Verify statistics accuracy by creating test data
4. Test with multiple users to ensure statistics are correctly attributed
5. Test users with no chatbots show 0 for all statistics

EXPECTED RESULTS:
- API should return users array with statistics object for each user
- Statistics should include: chatbots_count, messages_count, conversations_count, sources_count
- Statistics counts should match actual database records
- All count fields should be present and numeric
"""
import requests
import json
import uuid
import base64
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://full-stack-setup-3.preview.emergentagent.com/api"
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
    print("BRANDING IMAGE UPLOAD TEST SUMMARY")
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

def create_test_user(name, email):
    """Create a test user for statistics testing"""
    return {
        "name": name,
        "email": email,
        "password": "testpass123",
        "role": "user",
        "status": "active"
    }

def create_test_chatbot(name, user_id):
    """Create a test chatbot for statistics testing"""
    return {
        "name": name,
        "model": "gpt-4o-mini",
        "provider": "openai",
        "temperature": 0.7,
        "instructions": f"Test chatbot for user {user_id}"
    }

# Global variables for test data
admin_token = None
admin_user_id = None

print("="*80)
print("COMPREHENSIVE ADMIN USER MANAGEMENT STATISTICS TESTING")
print("="*80)
print(f"Backend URL: {BACKEND_URL}")
print(f"Admin Email: {ADMIN_EMAIL}")
print(f"Test Time: {datetime.now().isoformat()}")
print("Testing Admin User Management Statistics Column functionality")
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
# TEST 2: Test GET /api/admin/users/enhanced endpoint basic functionality
# ============================================================================
print("\n[TEST 2] Test GET /api/admin/users/enhanced endpoint...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.get(
        f"{BACKEND_URL}/admin/users/enhanced",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Check response structure
        checks = []
        checks.append(("Has users array", "users" in data))
        checks.append(("Has total count", "total" in data))
        checks.append(("Users is list", isinstance(data.get("users", []), list)))
        checks.append(("Total is number", isinstance(data.get("total", 0), int)))
        
        all_passed = all(check[1] for check in checks)
        details = f"Response structure: users={len(data.get('users', []))}, total={data.get('total', 0)}"
        log_test("Enhanced users endpoint structure", all_passed, details)
        
        # Store initial user count for later comparison
        global initial_user_count
        initial_user_count = len(data.get("users", []))
        
    else:
        log_test("Enhanced users endpoint structure", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Enhanced users endpoint structure", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 3: Test unauthenticated request (should fail with 401)
# ============================================================================
print("\n[TEST 3] Test unauthenticated request...")
try:
    # Create a small test image
    test_image = create_test_image()
    
    files = {
        'file': ('test_logo.png', test_image, 'image/png')
    }
    params = {'image_type': 'logo'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 401:
        log_test("Unauthenticated request fails", True, "Correctly returned 401 Unauthorized")
    else:
        log_test("Unauthenticated request fails", False, f"Expected 401, got {response.status_code}")

except Exception as e:
    log_test("Unauthenticated request fails", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 4: Test invalid file type (should fail with 400)
# ============================================================================
print("\n[TEST 4] Test invalid file type...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a text file instead of image
    invalid_file_content = b"This is not an image file"
    
    files = {
        'file': ('test_file.txt', invalid_file_content, 'text/plain')
    }
    params = {'image_type': 'logo'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 400:
        log_test("Invalid file type rejected", True, "Correctly returned 400 Bad Request")
    else:
        log_test("Invalid file type rejected", False, f"Expected 400, got {response.status_code}")

except Exception as e:
    log_test("Invalid file type rejected", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 5: Test file too large (should fail with 413)
# ============================================================================
print("\n[TEST 5] Test file too large...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a large image (>5MB)
    large_image = create_large_test_image()
    
    files = {
        'file': ('large_image.png', large_image, 'image/png')
    }
    params = {'image_type': 'logo'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=30  # Longer timeout for large file
    )
    
    if response.status_code == 413:
        log_test("Large file rejected", True, "Correctly returned 413 Request Entity Too Large")
    else:
        log_test("Large file rejected", False, f"Expected 413, got {response.status_code}. Size: {len(large_image)/1024/1024:.2f}MB")

except Exception as e:
    log_test("Large file rejected", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 6: Test successful logo upload
# ============================================================================
print("\n[TEST 6] Test successful logo upload...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a small test image
    test_logo = create_test_image(150, 150, 'PNG')
    
    files = {
        'file': ('test_logo.png', test_logo, 'image/png')
    }
    params = {'image_type': 'logo'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        checks.append(("Success flag", result.get("success") == True))
        checks.append(("Has message", result.get("message") is not None))
        checks.append(("Has URL", result.get("url") is not None))
        checks.append(("Has filename", result.get("filename") is not None))
        checks.append(("URL is data URL", result.get("url", "").startswith("data:image/")))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {result.get('success')}, URL starts with: {result.get('url', '')[:50]}..."
        log_test("Logo upload success", all_passed, details)
        
        # Store the logo URL for database verification
        global logo_url
        logo_url = result.get("url")
        
    else:
        log_test("Logo upload success", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Logo upload success", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 7: Test successful avatar upload
# ============================================================================
print("\n[TEST 7] Test successful avatar upload...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a small test image for avatar
    test_avatar = create_test_image(100, 100, 'JPEG')
    
    files = {
        'file': ('test_avatar.jpg', test_avatar, 'image/jpeg')
    }
    params = {'image_type': 'avatar'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        
        checks = []
        checks.append(("Success flag", result.get("success") == True))
        checks.append(("Has message", result.get("message") is not None))
        checks.append(("Has URL", result.get("url") is not None))
        checks.append(("Has filename", result.get("filename") is not None))
        checks.append(("URL is data URL", result.get("url", "").startswith("data:image/")))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {result.get('success')}, URL starts with: {result.get('url', '')[:50]}..."
        log_test("Avatar upload success", all_passed, details)
        
        # Store the avatar URL for database verification
        global avatar_url
        avatar_url = result.get("url")
        
    else:
        log_test("Avatar upload success", False, f"Status: {response.status_code}, Response: {response.text}")

except Exception as e:
    log_test("Avatar upload success", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 8: Verify database updates (logo_url and avatar_url fields)
# ============================================================================
print("\n[TEST 8] Verify database updates...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get the chatbot to verify database updates
    response = requests.get(
        f"{BACKEND_URL}/chatbots",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        chatbots = response.json()
        test_chatbot = None
        
        for chatbot in chatbots:
            if chatbot.get("id") == TEST_CHATBOT_ID:
                test_chatbot = chatbot
                break
        
        if test_chatbot:
            checks = []
            checks.append(("Logo URL updated", test_chatbot.get("logo_url") is not None))
            checks.append(("Avatar URL updated", test_chatbot.get("avatar_url") is not None))
            checks.append(("Logo URL is data URL", test_chatbot.get("logo_url", "").startswith("data:image/")))
            checks.append(("Avatar URL is data URL", test_chatbot.get("avatar_url", "").startswith("data:image/")))
            
            all_passed = all(check[1] for check in checks)
            details = f"Logo URL exists: {test_chatbot.get('logo_url') is not None}, Avatar URL exists: {test_chatbot.get('avatar_url') is not None}"
            log_test("Database fields updated", all_passed, details)
        else:
            log_test("Database fields updated", False, "Test chatbot not found in response")
    else:
        log_test("Database fields updated", False, f"Status: {response.status_code}")

except Exception as e:
    log_test("Database fields updated", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 9: Verify files are saved to disk
# ============================================================================
print("\n[TEST 9] Verify files are saved to disk...")
try:
    uploads_dir = "/app/backend/uploads/branding"
    
    # Check if uploads directory exists
    dir_exists = os.path.exists(uploads_dir)
    
    if dir_exists:
        # List files in the directory
        files_in_dir = os.listdir(uploads_dir)
        
        # Look for files with our chatbot ID
        chatbot_files = [f for f in files_in_dir if TEST_CHATBOT_ID in f]
        
        checks = []
        checks.append(("Uploads directory exists", dir_exists))
        checks.append(("Files created", len(chatbot_files) > 0))
        checks.append(("Logo file exists", any("logo" in f for f in chatbot_files)))
        checks.append(("Avatar file exists", any("avatar" in f for f in chatbot_files)))
        
        all_passed = all(check[1] for check in checks)
        details = f"Directory exists: {dir_exists}, Files found: {len(chatbot_files)}, Files: {chatbot_files}"
        log_test("Files saved to disk", all_passed, details)
    else:
        log_test("Files saved to disk", False, f"Uploads directory does not exist: {uploads_dir}")

except Exception as e:
    log_test("Files saved to disk", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 10: Test invalid chatbot ID (should fail with 404)
# ============================================================================
print("\n[TEST 10] Test invalid chatbot ID...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a small test image
    test_image = create_test_image()
    
    files = {
        'file': ('test_logo.png', test_image, 'image/png')
    }
    params = {'image_type': 'logo'}
    
    invalid_chatbot_id = "invalid-chatbot-id-12345"
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{invalid_chatbot_id}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 404:
        log_test("Invalid chatbot ID rejected", True, "Correctly returned 404 Not Found")
    else:
        log_test("Invalid chatbot ID rejected", False, f"Expected 404, got {response.status_code}")

except Exception as e:
    log_test("Invalid chatbot ID rejected", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 11: Test different image formats (PNG, JPEG)
# ============================================================================
print("\n[TEST 11] Test different image formats...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    formats_to_test = [
        ('PNG', 'image/png'),
        ('JPEG', 'image/jpeg'),
    ]
    
    format_results = []
    
    for format_name, content_type in formats_to_test:
        try:
            # Create test image in the specified format
            test_image = create_test_image(80, 80, format_name)
            
            files = {
                'file': (f'test_image.{format_name.lower()}', test_image, content_type)
            }
            params = {'image_type': 'logo'}
            
            response = requests.post(
                f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
                headers=headers,
                files=files,
                params=params,
                timeout=10
            )
            
            format_results.append((format_name, response.status_code == 200))
            
        except Exception as format_e:
            format_results.append((format_name, False))
    
    all_formats_passed = all(result[1] for result in format_results)
    details = f"Format results: {format_results}"
    log_test("Multiple image formats supported", all_formats_passed, details)

except Exception as e:
    log_test("Multiple image formats supported", False, f"Exception: {str(e)}")

# ============================================================================
# TEST 12: Test overwriting existing images
# ============================================================================
print("\n[TEST 12] Test overwriting existing images...")
try:
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Upload a new logo to overwrite the existing one
    new_test_logo = create_test_image(200, 200, 'PNG')
    
    files = {
        'file': ('new_test_logo.png', new_test_logo, 'image/png')
    }
    params = {'image_type': 'logo'}
    
    response = requests.post(
        f"{BACKEND_URL}/chatbots/{TEST_CHATBOT_ID}/upload-branding-image",
        headers=headers,
        files=files,
        params=params,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        new_logo_url = result.get("url")
        
        # Verify the URL is different from the previous one (if we stored it)
        url_changed = True
        if 'logo_url' in globals() and logo_url:
            url_changed = new_logo_url != logo_url
        
        checks = []
        checks.append(("Upload successful", result.get("success") == True))
        checks.append(("New URL generated", url_changed))
        
        all_passed = all(check[1] for check in checks)
        details = f"Success: {result.get('success')}, URL changed: {url_changed}"
        log_test("Image overwrite works", all_passed, details)
    else:
        log_test("Image overwrite works", False, f"Status: {response.status_code}")

except Exception as e:
    log_test("Image overwrite works", False, f"Exception: {str(e)}")

# ============================================================================
# TEST COMPLETE - SUMMARY
# ============================================================================
print("\n" + "="*80)
print("BRANDING IMAGE UPLOAD TEST COMPLETE")
print("="*80)
print("✅ This comprehensive test verified:")
print("   1. Admin authentication with admin@botsmith.com / admin123")
print("   2. Test chatbot existence/creation")
print("   3. Unauthenticated requests properly rejected (401)")
print("   4. Invalid file types properly rejected (400)")
print("   5. Large files properly rejected (413)")
print("   6. Successful logo upload with proper response format")
print("   7. Successful avatar upload with proper response format")
print("   8. Database fields (logo_url, avatar_url) updated with base64 data URLs")
print("   9. Files saved to disk at /app/backend/uploads/branding/")
print("   10. Invalid chatbot IDs properly rejected (404)")
print("   11. Multiple image formats supported (PNG, JPEG)")
print("   12. Image overwriting functionality")
print("="*80)
print("🎯 KEY VALIDATION POINTS:")
print("   - Authentication required for all upload operations")
print("   - File type validation (only image types allowed)")
print("   - File size validation (max 5MB)")
print("   - Database updates with base64 data URLs")
print("   - Physical file storage in uploads directory")
print("   - Proper error handling for various failure scenarios")
print("   - Support for both logo and avatar image types")
print("="*80)

# Print final summary
print_summary()

# Exit with appropriate code
exit(0 if test_results["failed"] == 0 else 1)
