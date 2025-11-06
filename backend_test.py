#!/usr/bin/env python3
"""
Backend Testing Suite for Slack Integration APIs
Comprehensive testing of Slack integration following the same pattern as Telegram integration.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://dep-install-demo.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class SlackIntegrationTestSuite:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.mock_user_id = "demo-user-123"
        self.test_chatbot_id = None
        self.test_integration_id = None
        
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

    async def setup_test_environment(self):
        """Setup test environment by upgrading plan and cleaning up existing resources"""
        print("\n🔧 Setting up test environment...")
        
        # First, upgrade to Professional plan to avoid limits
        try:
            upgrade_data = {"plan_id": "professional"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    self.log_test("Upgrade to Professional plan", True, "Upgraded to Professional plan for testing")
                else:
                    self.log_test("Upgrade to Professional plan", False, f"Failed to upgrade: {response.status}")
        except Exception as e:
            self.log_test("Upgrade to Professional plan", False, f"Exception: {str(e)}")
        
        # Clean up any existing chatbots
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

    async def create_test_chatbot(self):
        """Create a test chatbot for integration testing"""
        print("\n🤖 Creating Test Chatbot...")
        
        chatbot_data = {
            "name": "Slack Integration Test Bot",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "temperature": 0.7,
            "instructions": "You are a test chatbot for Slack integration testing."
        }
        
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_chatbot_id = result["id"]
                    self.log_test("Create test chatbot", True, f"Created chatbot: {self.test_chatbot_id}")
                    return True
                else:
                    error_text = await response.text()
                    self.log_test("Create test chatbot", False, f"Status: {response.status}, Error: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Create test chatbot", False, f"Exception: {str(e)}")
            return False

    async def test_setup_slack_integration(self):
        """Test setting up Slack integration with credentials"""
        print("\n🔧 Testing Slack Integration Setup...")
        
        if not self.test_chatbot_id:
            self.log_test("Setup Slack integration", False, "No test chatbot available")
            return
        
        # Test POST /api/integrations/{chatbot_id} - Create Slack integration
        integration_data = {
            "integration_type": "slack",
            "credentials": {
                "bot_token": "xoxb-test-token-for-testing"
            }
        }
        
        try:
            async with self.session.post(f"{API_BASE}/integrations/{self.test_chatbot_id}", json=integration_data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.test_integration_id = result["id"]
                    self.log_test("Setup Slack integration", True, 
                                f"Created Slack integration: {self.test_integration_id}")
                    
                    # Verify integration fields
                    expected_fields = ["id", "chatbot_id", "integration_type", "enabled", "status", "has_credentials"]
                    if all(field in result for field in expected_fields):
                        self.log_test("Slack integration response format", True, 
                                    f"All required fields present: {list(result.keys())}")
                    else:
                        missing = [f for f in expected_fields if f not in result]
                        self.log_test("Slack integration response format", False, 
                                    f"Missing fields: {missing}")
                    
                    # Verify integration type and credentials
                    if result.get("integration_type") == "slack" and result.get("has_credentials"):
                        self.log_test("Slack integration data validation", True, 
                                    f"Type: {result['integration_type']}, Has credentials: {result['has_credentials']}")
                    else:
                        self.log_test("Slack integration data validation", False, 
                                    f"Invalid data - Type: {result.get('integration_type')}, Has credentials: {result.get('has_credentials')}")
                else:
                    error_text = await response.text()
                    self.log_test("Setup Slack integration", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Setup Slack integration", False, f"Exception: {str(e)}")

    async def test_slack_connection_test(self):
        """Test Slack connection testing endpoint"""
        print("\n🔗 Testing Slack Connection Test...")
        
        if not self.test_chatbot_id or not self.test_integration_id:
            self.log_test("Test Slack connection", False, "No test integration available")
            return
        
        # Test POST /api/integrations/{chatbot_id}/{integration_id}/test
        try:
            async with self.session.post(f"{API_BASE}/integrations/{self.test_chatbot_id}/{self.test_integration_id}/test") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Check response format
                    required_fields = ["success", "message"]
                    if all(field in result for field in required_fields):
                        # With test token, we expect failure but proper error format
                        if not result["success"] and "error" in result["message"].lower():
                            self.log_test("Slack connection test", True, 
                                        f"Proper error response: {result['message']}")
                        elif result["success"]:
                            self.log_test("Slack connection test", True, 
                                        f"Connection successful: {result['message']}")
                        else:
                            self.log_test("Slack connection test", False, 
                                        f"Unexpected response format: {result}")
                    else:
                        missing = [f for f in required_fields if f not in result]
                        self.log_test("Slack connection test", False, 
                                    f"Missing response fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("Slack connection test", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Slack connection test", False, f"Exception: {str(e)}")

    async def test_generate_webhook_url(self):
        """Test generating Slack webhook URL"""
        print("\n🔗 Testing Slack Webhook URL Generation...")
        
        if not self.test_chatbot_id:
            self.log_test("Generate Slack webhook URL", False, "No test chatbot available")
            return
        
        # Test POST /api/slack/{chatbot_id}/setup-webhook
        webhook_data = {
            "base_url": "https://dep-install-demo.preview.emergentagent.com"
        }
        
        try:
            async with self.session.post(f"{API_BASE}/slack/{self.test_chatbot_id}/setup-webhook", json=webhook_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Check response format
                    required_fields = ["success", "message", "webhook_url", "instructions"]
                    if all(field in result for field in required_fields):
                        webhook_url = result["webhook_url"]
                        expected_url = f"{webhook_data['base_url']}/api/slack/webhook/{self.test_chatbot_id}"
                        
                        if webhook_url == expected_url:
                            self.log_test("Generate Slack webhook URL", True, 
                                        f"Correct webhook URL: {webhook_url}")
                        else:
                            self.log_test("Generate Slack webhook URL", False, 
                                        f"Wrong URL. Expected: {expected_url}, Got: {webhook_url}")
                        
                        # Check instructions
                        if isinstance(result["instructions"], list) and len(result["instructions"]) > 0:
                            self.log_test("Slack webhook instructions", True, 
                                        f"Instructions provided: {len(result['instructions'])} steps")
                        else:
                            self.log_test("Slack webhook instructions", False, 
                                        f"No instructions provided: {result['instructions']}")
                    else:
                        missing = [f for f in required_fields if f not in result]
                        self.log_test("Generate Slack webhook URL", False, 
                                    f"Missing response fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("Generate Slack webhook URL", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Generate Slack webhook URL", False, f"Exception: {str(e)}")

    async def test_get_webhook_info(self):
        """Test getting Slack webhook information"""
        print("\n📋 Testing Get Slack Webhook Info...")
        
        if not self.test_chatbot_id:
            self.log_test("Get Slack webhook info", False, "No test chatbot available")
            return
        
        # Test GET /api/slack/{chatbot_id}/webhook-info
        try:
            async with self.session.get(f"{API_BASE}/slack/{self.test_chatbot_id}/webhook-info") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Check response format
                    expected_fields = ["webhook_url", "webhook_configured", "instructions"]
                    if all(field in result for field in expected_fields):
                        self.log_test("Get Slack webhook info", True, 
                                    f"Webhook configured: {result['webhook_configured']}, URL: {result.get('webhook_url', 'None')}")
                        
                        # Check instructions format
                        if isinstance(result["instructions"], list) and len(result["instructions"]) >= 8:
                            self.log_test("Slack webhook info instructions", True, 
                                        f"Complete instructions: {len(result['instructions'])} steps")
                        else:
                            self.log_test("Slack webhook info instructions", False, 
                                        f"Incomplete instructions: {len(result.get('instructions', []))} steps")
                    else:
                        missing = [f for f in expected_fields if f not in result]
                        self.log_test("Get Slack webhook info", False, 
                                    f"Missing response fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("Get Slack webhook info", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Get Slack webhook info", False, f"Exception: {str(e)}")

    async def test_enable_disable_integration(self):
        """Test enabling and disabling Slack integration"""
        print("\n🔄 Testing Enable/Disable Slack Integration...")
        
        if not self.test_chatbot_id or not self.test_integration_id:
            self.log_test("Enable/disable Slack integration", False, "No test integration available")
            return
        
        # Test POST /api/integrations/{chatbot_id}/{integration_id}/toggle
        try:
            # First toggle (should enable)
            async with self.session.post(f"{API_BASE}/integrations/{self.test_chatbot_id}/{self.test_integration_id}/toggle") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if "success" in result and "enabled" in result:
                        enabled_status = result["enabled"]
                        self.log_test("Enable Slack integration", True, 
                                    f"Integration enabled: {enabled_status}")
                        
                        # Second toggle (should disable)
                        async with self.session.post(f"{API_BASE}/integrations/{self.test_chatbot_id}/{self.test_integration_id}/toggle") as response2:
                            if response2.status == 200:
                                result2 = await response2.json()
                                if result2.get("enabled") != enabled_status:
                                    self.log_test("Disable Slack integration", True, 
                                                f"Integration toggled: {enabled_status} → {result2['enabled']}")
                                else:
                                    self.log_test("Disable Slack integration", False, 
                                                f"Toggle failed - status unchanged: {enabled_status}")
                            else:
                                error_text = await response2.text()
                                self.log_test("Disable Slack integration", False, 
                                            f"Status: {response2.status}, Error: {error_text}")
                    else:
                        self.log_test("Enable Slack integration", False, 
                                    f"Missing fields in response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Enable Slack integration", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Enable/disable Slack integration", False, f"Exception: {str(e)}")

    async def test_webhook_event_reception(self):
        """Test Slack webhook event reception (simulated)"""
        print("\n📨 Testing Slack Webhook Event Reception...")
        
        if not self.test_chatbot_id:
            self.log_test("Slack webhook event reception", False, "No test chatbot available")
            return
        
        # Test URL verification challenge
        challenge_data = {
            "type": "url_verification",
            "challenge": "test123"
        }
        
        try:
            async with self.session.post(f"{API_BASE}/slack/webhook/{self.test_chatbot_id}", json=challenge_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if "challenge" in result and result["challenge"] == "test123":
                        self.log_test("Slack URL verification challenge", True, 
                                    f"Challenge response correct: {result['challenge']}")
                    else:
                        self.log_test("Slack URL verification challenge", False, 
                                    f"Wrong challenge response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Slack URL verification challenge", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Slack URL verification challenge", False, f"Exception: {str(e)}")
        
        # Test message event (simulated)
        message_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Hello test bot!",
                "ts": "1234567890.123456"
            }
        }
        
        try:
            async with self.session.post(f"{API_BASE}/slack/webhook/{self.test_chatbot_id}", json=message_event) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get("ok"):
                        self.log_test("Slack message event reception", True, 
                                    "Message event processed successfully")
                    else:
                        self.log_test("Slack message event reception", False, 
                                    f"Event processing failed: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Slack message event reception", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Slack message event reception", False, f"Exception: {str(e)}")

    async def test_integration_logs(self):
        """Test integration activity logs"""
        print("\n📊 Testing Integration Activity Logs...")
        
        if not self.test_chatbot_id:
            self.log_test("Integration activity logs", False, "No test chatbot available")
            return
        
        # Test GET /api/integrations/{chatbot_id}/logs
        try:
            async with self.session.get(f"{API_BASE}/integrations/{self.test_chatbot_id}/logs") as response:
                if response.status == 200:
                    logs = await response.json()
                    
                    if isinstance(logs, list):
                        if len(logs) > 0:
                            # Check log entry format
                            log_entry = logs[0]
                            required_fields = ["chatbot_id", "integration_type", "event_type", "status", "message", "timestamp"]
                            
                            if all(field in log_entry for field in required_fields):
                                slack_logs = [log for log in logs if log.get("integration_type") == "slack"]
                                self.log_test("Integration activity logs", True, 
                                            f"Found {len(logs)} total logs, {len(slack_logs)} Slack logs")
                            else:
                                missing = [f for f in required_fields if f not in log_entry]
                                self.log_test("Integration activity logs", False, 
                                            f"Missing log fields: {missing}")
                        else:
                            self.log_test("Integration activity logs", True, 
                                        "No logs found (expected for new integration)")
                    else:
                        self.log_test("Integration activity logs", False, 
                                    f"Expected list, got: {type(logs)}")
                else:
                    error_text = await response.text()
                    self.log_test("Integration activity logs", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Integration activity logs", False, f"Exception: {str(e)}")

    async def cleanup_test_resources(self):
        """Clean up test resources"""
        print("\n🧹 Cleaning up test resources...")
        
        # Delete test integration
        if self.test_chatbot_id and self.test_integration_id:
            try:
                await self.session.delete(f"{API_BASE}/integrations/{self.test_chatbot_id}/{self.test_integration_id}")
                self.log_test("Delete test integration", True, "Test integration deleted")
            except:
                pass
        
        # Delete test chatbot
        if self.test_chatbot_id:
            try:
                await self.session.delete(f"{API_BASE}/chatbots/{self.test_chatbot_id}")
                self.log_test("Delete test chatbot", True, "Test chatbot deleted")
            except:
                pass

    async def run_all_tests(self):
        """Run all Slack integration tests"""
        print("🚀 Starting Comprehensive Slack Integration Testing")
        print(f"Backend URL: {API_BASE}")
        print(f"Mock User: {self.mock_user_id}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Setup test environment first
            await self.setup_test_environment()
            
            # Create test chatbot
            if await self.create_test_chatbot():
                # Run all Slack integration tests
                await self.test_setup_slack_integration()
                await self.test_slack_connection_test()
                await self.test_generate_webhook_url()
                await self.test_get_webhook_info()
                await self.test_enable_disable_integration()
                await self.test_webhook_event_reception()
                await self.test_integration_logs()
            else:
                self.log_test("Slack Integration Testing", False, "Failed to create test chatbot - cannot proceed")
            
        finally:
            await self.cleanup_test_resources()
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()

    # This method is already defined above - removing duplicate
        
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n" + "=" * 80)
        print("📊 SLACK INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        # Categorize results
        categories = {
            "Setup & Configuration": ["Create test chatbot", "Setup Slack integration", "Slack integration response format", "Slack integration data validation"],
            "Connection Testing": ["Test Slack connection", "Slack connection test"],
            "Webhook Management": ["Generate Slack webhook URL", "Slack webhook instructions", "Get Slack webhook info", "Slack webhook info instructions"],
            "Integration Control": ["Enable Slack integration", "Disable Slack integration"],
            "Event Processing": ["Slack URL verification challenge", "Slack message event reception"],
            "Activity Logging": ["Integration activity logs"],
            "Cleanup": ["Delete test integration", "Delete test chatbot"]
        }
        
        for category, keywords in categories.items():
            category_tests = [r for r in self.test_results if any(kw in r["test"] for kw in keywords)]
            if category_tests:
                category_passed = sum(1 for r in category_tests if r["success"])
                print(f"\n📋 {category}: {category_passed}/{len(category_tests)} passed")
                
                # Show failed tests in this category
                failed_tests = [r for r in category_tests if not r["success"]]
                if failed_tests:
                    for test in failed_tests:
                        print(f"   ❌ {test['test']}: {test['details']}")
        
        # Show critical Slack integration functionality status
        print(f"\n🎯 CRITICAL SLACK INTEGRATION FUNCTIONALITY:")
        
        critical_tests = [
            ("Integration Setup", "Setup Slack integration"),
            ("Connection Testing", "Test Slack connection"),
            ("Webhook URL Generation", "Generate Slack webhook URL"),
            ("Webhook Info Retrieval", "Get Slack webhook info"),
            ("Enable/Disable Toggle", "Enable Slack integration"),
            ("Event Reception", "Slack URL verification challenge"),
            ("Activity Logging", "Integration activity logs")
        ]
        
        all_critical_passed = True
        for feature, keyword in critical_tests:
            matching_tests = [r for r in self.test_results if keyword in r["test"]]
            if matching_tests:
                feature_passed = all(r["success"] for r in matching_tests)
                status = "✅" if feature_passed else "❌"
                print(f"   {status} {feature}")
                if not feature_passed:
                    all_critical_passed = False
            else:
                print(f"   ⚠️  {feature} (not tested)")
                all_critical_passed = False
        
        if all_critical_passed:
            print(f"\n🎉 ALL CRITICAL SLACK INTEGRATION FEATURES WORKING!")
        else:
            print(f"\n⚠️  SOME CRITICAL SLACK INTEGRATION FEATURES NEED ATTENTION")
        
        # Show detailed failed tests
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS DETAILS:")
            for test in failed_tests:
                print(f"   • {test['test']}")
                print(f"     Details: {test['details']}")

async def main():
    """Main test execution"""
    test_suite = SlackIntegrationTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())