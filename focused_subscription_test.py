#!/usr/bin/env python3
"""
Focused Subscription System Test - Critical Scenarios
Tests the exact scenarios requested in the review request.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://install-preview-7.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class FocusedSubscriptionTest:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.mock_user_id = "demo-user-123"
        self.test_chatbot_ids = []
        
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")

    async def cleanup_existing_chatbots(self):
        """Clean up existing chatbots"""
        try:
            async with self.session.get(f"{API_BASE}/chatbots") as response:
                if response.status == 200:
                    chatbots = await response.json()
                    for chatbot in chatbots:
                        try:
                            await self.session.delete(f"{API_BASE}/chatbots/{chatbot['id']}")
                        except:
                            pass
        except:
            pass

    async def test_critical_subscription_flow(self):
        """Test the most critical subscription flow as requested"""
        print("\n🎯 CRITICAL TEST: Free Plan → Professional Upgrade Flow")
        
        # Step 1: Ensure we're on Free plan
        try:
            upgrade_data = {"plan_id": "free"}
            await self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data)
            self.log_test("Reset to Free plan", True, "Starting with Free plan")
        except Exception as e:
            self.log_test("Reset to Free plan", False, f"Exception: {str(e)}")
            return

        # Clean up existing chatbots
        await self.cleanup_existing_chatbots()
        
        # Step 2: Verify Free plan limits
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    current_sub = await response.json()
                    plan_name = current_sub["plan"]["name"]
                    plan_limits = current_sub["plan"]["limits"]
                    self.log_test("Verify Free plan active", True, 
                                f"Plan: {plan_name}, Chatbot limit: {plan_limits['max_chatbots']}")
                else:
                    self.log_test("Verify Free plan active", False, f"Status: {response.status}")
                    return
        except Exception as e:
            self.log_test("Verify Free plan active", False, f"Exception: {str(e)}")
            return

        # Step 3: Create 1st chatbot on Free plan (should succeed)
        chatbot_data = {
            "name": "Test Chatbot 1",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "temperature": 0.7,
            "instructions": "You are a test chatbot."
        }
        
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_chatbot_ids.append(result["id"])
                    self.log_test("Create 1st chatbot (Free plan)", True, 
                                f"Successfully created: {result['id']}")
                else:
                    error_text = await response.text()
                    self.log_test("Create 1st chatbot (Free plan)", False, 
                                f"Status: {response.status}, Error: {error_text}")
                    return
        except Exception as e:
            self.log_test("Create 1st chatbot (Free plan)", False, f"Exception: {str(e)}")
            return

        # Step 4: Try to create 2nd chatbot (should FAIL with 403)
        chatbot_data["name"] = "Test Chatbot 2 (Should Fail)"
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 403:
                    error_data = await response.json()
                    if "detail" in error_data and "upgrade_required" in error_data["detail"]:
                        self.log_test("Create 2nd chatbot (should fail)", True, 
                                    f"Correctly blocked: {error_data['detail']}")
                    else:
                        self.log_test("Create 2nd chatbot (should fail)", False, 
                                    f"Wrong error format: {error_data}")
                        return
                elif response.status == 201:
                    self.log_test("Create 2nd chatbot (should fail)", False, 
                                "ERROR: Should have been blocked but was allowed!")
                    return
                else:
                    error_text = await response.text()
                    self.log_test("Create 2nd chatbot (should fail)", False, 
                                f"Unexpected status {response.status}: {error_text}")
                    return
        except Exception as e:
            self.log_test("Create 2nd chatbot (should fail)", False, f"Exception: {str(e)}")
            return

        # Step 5: Upgrade to Professional plan
        try:
            upgrade_data = {"plan_id": "professional"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    if "subscription" in result and result["subscription"]["plan_id"] == "professional":
                        self.log_test("Upgrade Free → Professional", True, 
                                    f"Successfully upgraded to Professional plan")
                    else:
                        self.log_test("Upgrade Free → Professional", False, 
                                    f"Plan not updated correctly: {result}")
                        return
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade Free → Professional", False, 
                                f"Status: {response.status}, Error: {error_text}")
                    return
        except Exception as e:
            self.log_test("Upgrade Free → Professional", False, f"Exception: {str(e)}")
            return

        # Step 6: Verify Professional plan limits
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    current_sub = await response.json()
                    plan_name = current_sub["plan"]["name"]
                    plan_limits = current_sub["plan"]["limits"]
                    if plan_name == "Professional" and plan_limits["max_chatbots"] == 25:
                        self.log_test("Verify Professional plan limits", True, 
                                    f"Plan: {plan_name}, Chatbot limit: {plan_limits['max_chatbots']}, Messages: {plan_limits['max_messages_per_month']}")
                    else:
                        self.log_test("Verify Professional plan limits", False, 
                                    f"Wrong limits: {plan_name}, chatbots: {plan_limits.get('max_chatbots')}")
                        return
                else:
                    self.log_test("Verify Professional plan limits", False, f"Status: {response.status}")
                    return
        except Exception as e:
            self.log_test("Verify Professional plan limits", False, f"Exception: {str(e)}")
            return

        # Step 7: Try to create 2nd chatbot (should now SUCCEED)
        chatbot_data["name"] = "Test Chatbot 2 (Should Now Succeed)"
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_chatbot_ids.append(result["id"])
                    self.log_test("Create 2nd chatbot (should now succeed)", True, 
                                f"Successfully created after upgrade: {result['id']}")
                else:
                    error_text = await response.text()
                    self.log_test("Create 2nd chatbot (should now succeed)", False, 
                                f"Status: {response.status}, Error: {error_text}")
                    return
        except Exception as e:
            self.log_test("Create 2nd chatbot (should now succeed)", False, f"Exception: {str(e)}")
            return

        # Step 8: Create multiple more chatbots to verify Professional limits
        for i in range(3, 8):  # Create chatbots 3, 4, 5, 6, 7
            chatbot_data["name"] = f"Professional Test Chatbot {i}"
            try:
                async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                    if response.status == 201:
                        result = await response.json()
                        self.test_chatbot_ids.append(result["id"])
                        self.log_test(f"Create chatbot {i}/25 (Professional)", True, 
                                    f"Successfully created chatbot {i}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Create chatbot {i}/25 (Professional)", False, 
                                    f"Status: {response.status}, Error: {error_text}")
            except Exception as e:
                self.log_test(f"Create chatbot {i}/25 (Professional)", False, f"Exception: {str(e)}")

        # Step 9: Verify usage tracking reflects new limits
        try:
            async with self.session.get(f"{API_BASE}/plans/usage") as response:
                if response.status == 200:
                    usage_stats = await response.json()
                    chatbot_usage = usage_stats["usage"]["chatbots"]
                    message_usage = usage_stats["usage"]["messages"]
                    
                    if chatbot_usage["limit"] == 25 and message_usage["limit"] == 100000:
                        self.log_test("Verify Professional usage limits", True, 
                                    f"Chatbots: {chatbot_usage['current']}/{chatbot_usage['limit']}, Messages: {message_usage['current']}/{message_usage['limit']}")
                    else:
                        self.log_test("Verify Professional usage limits", False, 
                                    f"Wrong limits: chatbots {chatbot_usage['limit']}, messages {message_usage['limit']}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify Professional usage limits", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify Professional usage limits", False, f"Exception: {str(e)}")

    async def test_all_limit_check_apis(self):
        """Test all limit check API endpoints"""
        print("\n🔍 Testing All Limit Check APIs...")
        
        limit_types = ["chatbots", "messages", "file_uploads", "website_sources", "text_sources"]
        
        for limit_type in limit_types:
            try:
                async with self.session.get(f"{API_BASE}/plans/check-limit/{limit_type}") as response:
                    if response.status == 200:
                        result = await response.json()
                        required_fields = ["current", "max", "reached"]
                        if all(field in result for field in required_fields):
                            self.log_test(f"Check limit API: {limit_type}", True, 
                                        f"Current: {result['current']}, Max: {result['max']}, Reached: {result['reached']}")
                        else:
                            missing = [f for f in required_fields if f not in result]
                            self.log_test(f"Check limit API: {limit_type}", False, 
                                        f"Missing fields: {missing}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Check limit API: {limit_type}", False, 
                                    f"Status: {response.status}, Error: {error_text}")
            except Exception as e:
                self.log_test(f"Check limit API: {limit_type}", False, f"Exception: {str(e)}")

    async def test_text_source_creation(self):
        """Test text source creation after fix"""
        print("\n📝 Testing Text Source Creation (After Fix)...")
        
        if not self.test_chatbot_ids:
            self.log_test("Text source creation test", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Try to add text sources
        for i in range(1, 4):  # Test 3 text sources
            try:
                form_data = aiohttp.FormData()
                form_data.add_field('name', f"Test Text Source {i}")
                form_data.add_field('content', f"This is test text content {i} for testing text source creation after the status fix. It contains sample information about our company policies and procedures.")
                
                async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/text", data=form_data) as response:
                    if response.status == 201:
                        result = await response.json()
                        self.log_test(f"Create text source {i}", True, 
                                    f"Successfully created text source {i}: {result['id']}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Create text source {i}", False, 
                                    f"Status: {response.status}, Error: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Create text source {i}", False, f"Exception: {str(e)}")

    async def cleanup_test_resources(self):
        """Clean up test resources"""
        print("\n🧹 Cleaning up test resources...")
        
        # Delete test chatbots
        for chatbot_id in self.test_chatbot_ids:
            try:
                await self.session.delete(f"{API_BASE}/chatbots/{chatbot_id}")
            except:
                pass

    async def run_focused_tests(self):
        """Run focused subscription tests"""
        print("🎯 Starting Focused Subscription System Testing")
        print(f"Backend URL: {API_BASE}")
        print(f"Mock User: {self.mock_user_id}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Run critical tests
            await self.test_critical_subscription_flow()
            await self.test_all_limit_check_apis()
            await self.test_text_source_creation()
            
        finally:
            await self.cleanup_test_resources()
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()
        
    def print_test_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 80)
        print("🎯 FOCUSED SUBSCRIPTION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        # Critical functionality check
        critical_tests = [
            "Reset to Free plan",
            "Create 1st chatbot (Free plan)",
            "Create 2nd chatbot (should fail)",
            "Upgrade Free → Professional",
            "Create 2nd chatbot (should now succeed)"
        ]
        
        critical_passed = all(
            any(r["test"] == test and r["success"] for r in self.test_results)
            for test in critical_tests
        )
        
        print(f"\n🎯 CRITICAL SUBSCRIPTION FLOW:")
        if critical_passed:
            print("   ✅ ALL CRITICAL TESTS PASSED!")
            print("   ✅ Free plan limits enforced correctly")
            print("   ✅ Professional upgrade works instantly")
            print("   ✅ New limits apply immediately after upgrade")
        else:
            print("   ❌ SOME CRITICAL TESTS FAILED")
            
        # Show text source fix status
        text_source_tests = [r for r in self.test_results if "text source" in r["test"].lower()]
        if text_source_tests:
            text_passed = all(r["success"] for r in text_source_tests)
            if text_passed:
                print("   ✅ Text source creation fixed and working")
            else:
                print("   ❌ Text source creation still has issues")

async def main():
    """Main test execution"""
    test_suite = FocusedSubscriptionTest()
    await test_suite.run_focused_tests()

if __name__ == "__main__":
    asyncio.run(main())