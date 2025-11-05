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
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://dep-installer-25.preview.emergentagent.com')
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
            "base_url": "https://dep-installer-25.preview.emergentagent.com"
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

    async def test_plan_upgrade_flow(self):
        """Test plan upgrade functionality"""
        print("\n🔄 Testing Plan Upgrade Flow...")
        
        # Get current plan first
        current_plan = None
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    current_sub = await response.json()
                    current_plan = current_sub["plan"]["id"]
        except:
            pass

        # Test upgrade from Free to Starter
        try:
            upgrade_data = {"plan_id": "starter"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    if "subscription" in result and result["subscription"]["plan_id"] == "starter":
                        self.log_test("Upgrade Free → Starter", True, 
                                    f"Successfully upgraded to Starter plan")
                    else:
                        self.log_test("Upgrade Free → Starter", False, 
                                    f"Plan not updated correctly: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade Free → Starter", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Upgrade Free → Starter", False, f"Exception: {str(e)}")

        # Test upgrade from Starter to Professional
        try:
            upgrade_data = {"plan_id": "professional"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    if "subscription" in result and result["subscription"]["plan_id"] == "professional":
                        self.log_test("Upgrade Starter → Professional", True, 
                                    f"Successfully upgraded to Professional plan")
                    else:
                        self.log_test("Upgrade Starter → Professional", False, 
                                    f"Plan not updated correctly: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade Starter → Professional", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Upgrade Starter → Professional", False, f"Exception: {str(e)}")

        # Test upgrade from Professional to Enterprise
        try:
            upgrade_data = {"plan_id": "enterprise"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    if "subscription" in result and result["subscription"]["plan_id"] == "enterprise":
                        self.log_test("Upgrade Professional → Enterprise", True, 
                                    f"Successfully upgraded to Enterprise plan")
                    else:
                        self.log_test("Upgrade Professional → Enterprise", False, 
                                    f"Plan not updated correctly: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade Professional → Enterprise", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Upgrade Professional → Enterprise", False, f"Exception: {str(e)}")

        # Reset to Free plan for limit testing
        try:
            upgrade_data = {"plan_id": "free"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    self.log_test("Reset to Free plan", True, "Reset to Free plan for limit testing")
                else:
                    self.log_test("Reset to Free plan", False, f"Failed to reset: {response.status}")
        except Exception as e:
            self.log_test("Reset to Free plan", False, f"Exception: {str(e)}")

    async def test_free_plan_limits(self):
        """Test FREE plan limits enforcement"""
        print("\n🚫 Testing FREE Plan Limits Enforcement...")
        
        # Ensure we're on Free plan
        await self.ensure_free_plan()
        
        # Test 1: Max 1 chatbot limit
        await self.test_chatbot_limit()
        
        # Test 2: Max 100 messages/month limit check
        await self.test_message_limit_check()
        
        # Test 3: Max 5 file uploads limit
        await self.test_file_upload_limit()
        
        # Test 4: Max 2 website sources limit
        await self.test_website_source_limit()
        
        # Test 5: Max 5 text sources limit
        await self.test_text_source_limit()

    async def ensure_free_plan(self):
        """Ensure user is on Free plan"""
        try:
            upgrade_data = {"plan_id": "free"}
            await self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data)
        except:
            pass

    async def test_chatbot_limit(self):
        """Test chatbot creation limit (Free: 1 chatbot)"""
        # First, delete any existing chatbots to start fresh
        await self.cleanup_existing_chatbots()
        
        # Try to create first chatbot (should succeed)
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
                                f"Successfully created first chatbot: {result['id']}")
                else:
                    error_text = await response.text()
                    self.log_test("Create 1st chatbot (Free plan)", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Create 1st chatbot (Free plan)", False, f"Exception: {str(e)}")

        # Try to create second chatbot (should fail with 403)
        chatbot_data["name"] = "Test Chatbot 2"
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
                elif response.status == 201:
                    self.log_test("Create 2nd chatbot (should fail)", False, 
                                "Should have been blocked but was allowed")
                else:
                    error_text = await response.text()
                    self.log_test("Create 2nd chatbot (should fail)", False, 
                                f"Unexpected status {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Create 2nd chatbot (should fail)", False, f"Exception: {str(e)}")

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

    async def test_message_limit_check(self):
        """Test message limit check endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/plans/check-limit/messages") as response:
                if response.status == 200:
                    result = await response.json()
                    if "current" in result and "max" in result and "reached" in result:
                        if result["max"] == 100:  # Free plan limit
                            self.log_test("Message limit check", True, 
                                        f"Correct limit: {result['current']}/{result['max']}, reached: {result['reached']}")
                        else:
                            self.log_test("Message limit check", False, 
                                        f"Wrong limit. Expected 100, got {result['max']}")
                    else:
                        self.log_test("Message limit check", False, 
                                    f"Missing fields in response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Message limit check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Message limit check", False, f"Exception: {str(e)}")

    async def test_file_upload_limit(self):
        """Test file upload limit (Free: 5 files)"""
        if not self.test_chatbot_ids:
            self.log_test("File upload limit test", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Try to upload 6 files, 6th should fail
        for i in range(1, 7):
            try:
                # Create a simple text file
                file_content = f"This is test file {i} content for testing file upload limits."
                
                form_data = aiohttp.FormData()
                form_data.add_field('chatbot_id', chatbot_id)
                form_data.add_field('file', file_content, filename=f'test_file_{i}.txt', content_type='text/plain')
                
                async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/file", data=form_data) as response:
                    if i <= 5:  # First 5 should succeed
                        if response.status == 201:
                            result = await response.json()
                            self.test_source_ids.append(result["id"])
                            self.log_test(f"Upload file {i}/5 (should succeed)", True, 
                                        f"Successfully uploaded file {i}")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Upload file {i}/5 (should succeed)", False, 
                                        f"Status: {response.status}, Error: {error_text}")
                    else:  # 6th should fail
                        if response.status == 403:
                            error_data = await response.json()
                            self.log_test(f"Upload file {i}/5 (should fail)", True, 
                                        f"Correctly blocked 6th file: {error_data}")
                        elif response.status == 201:
                            self.log_test(f"Upload file {i}/5 (should fail)", False, 
                                        "6th file should have been blocked but was allowed")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Upload file {i}/5 (should fail)", False, 
                                        f"Unexpected status {response.status}: {error_text}")
                            
            except Exception as e:
                self.log_test(f"Upload file {i} test", False, f"Exception: {str(e)}")

    async def test_website_source_limit(self):
        """Test website source limit (Free: 2 websites)"""
        if not self.test_chatbot_ids:
            self.log_test("Website source limit test", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Try to add 3 website sources, 3rd should fail
        websites = [
            "https://example.com",
            "https://httpbin.org/html",
            "https://jsonplaceholder.typicode.com"
        ]
        
        for i, url in enumerate(websites, 1):
            try:
                form_data = aiohttp.FormData()
                form_data.add_field('url', url)
                
                async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/website", data=form_data) as response:
                    if i <= 2:  # First 2 should succeed
                        if response.status == 201:
                            result = await response.json()
                            self.test_source_ids.append(result["id"])
                            self.log_test(f"Add website {i}/2 (should succeed)", True, 
                                        f"Successfully added website {i}")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Add website {i}/2 (should succeed)", False, 
                                        f"Status: {response.status}, Error: {error_text}")
                    else:  # 3rd should fail
                        if response.status == 403:
                            error_data = await response.json()
                            self.log_test(f"Add website {i}/2 (should fail)", True, 
                                        f"Correctly blocked 3rd website: {error_data}")
                        elif response.status == 201:
                            self.log_test(f"Add website {i}/2 (should fail)", False, 
                                        "3rd website should have been blocked but was allowed")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Add website {i}/2 (should fail)", False, 
                                        f"Unexpected status {response.status}: {error_text}")
                            
            except Exception as e:
                self.log_test(f"Add website {i} test", False, f"Exception: {str(e)}")

    async def test_text_source_limit(self):
        """Test text source limit (Free: 5 text sources)"""
        if not self.test_chatbot_ids:
            self.log_test("Text source limit test", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Try to add 6 text sources, 6th should fail
        for i in range(1, 7):
            try:
                form_data = aiohttp.FormData()
                form_data.add_field('name', f"Test Text Source {i}")
                form_data.add_field('content', f"This is test text content {i} for testing text source limits. It contains some sample information about our company policies and procedures.")
                
                async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/text", data=form_data) as response:
                    if i <= 5:  # First 5 should succeed
                        if response.status == 201:
                            result = await response.json()
                            self.test_source_ids.append(result["id"])
                            self.log_test(f"Add text source {i}/5 (should succeed)", True, 
                                        f"Successfully added text source {i}")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Add text source {i}/5 (should succeed)", False, 
                                        f"Status: {response.status}, Error: {error_text}")
                    else:  # 6th should fail
                        if response.status == 403:
                            error_data = await response.json()
                            self.log_test(f"Add text source {i}/5 (should fail)", True, 
                                        f"Correctly blocked 6th text source: {error_data}")
                        elif response.status == 201:
                            self.log_test(f"Add text source {i}/5 (should fail)", False, 
                                        "6th text source should have been blocked but was allowed")
                        else:
                            error_text = await response.text()
                            self.log_test(f"Add text source {i}/5 (should fail)", False, 
                                        f"Unexpected status {response.status}: {error_text}")
                            
            except Exception as e:
                self.log_test(f"Add text source {i} test", False, f"Exception: {str(e)}")

    async def test_starter_plan_features(self):
        """Test STARTER plan features after upgrade"""
        print("\n⭐ Testing STARTER Plan Features...")
        
        # Upgrade to Starter plan
        try:
            upgrade_data = {"plan_id": "starter"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    self.log_test("Upgrade to Starter plan", True, "Successfully upgraded to Starter")
                else:
                    self.log_test("Upgrade to Starter plan", False, f"Failed to upgrade: {response.status}")
                    return
        except Exception as e:
            self.log_test("Upgrade to Starter plan", False, f"Exception: {str(e)}")
            return

        # Test increased chatbot limit (5 chatbots)
        await self.test_starter_chatbot_limit()
        
        # Test increased message limit (10,000 messages/month)
        await self.test_starter_message_limit()
        
        # Test increased file upload limit (20 files)
        await self.test_starter_file_limit()

    async def test_starter_chatbot_limit(self):
        """Test Starter plan chatbot limit (5 chatbots)"""
        # Clean up existing chatbots first
        await self.cleanup_existing_chatbots()
        self.test_chatbot_ids = []
        
        # Try to create 5 chatbots (should all succeed)
        for i in range(1, 6):
            chatbot_data = {
                "name": f"Starter Test Chatbot {i}",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "temperature": 0.7,
                "instructions": f"You are test chatbot {i} for Starter plan."
            }
            
            try:
                async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                    if response.status == 201:
                        result = await response.json()
                        self.test_chatbot_ids.append(result["id"])
                        self.log_test(f"Create Starter chatbot {i}/5", True, 
                                    f"Successfully created chatbot {i}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Create Starter chatbot {i}/5", False, 
                                    f"Status: {response.status}, Error: {error_text}")
            except Exception as e:
                self.log_test(f"Create Starter chatbot {i}/5", False, f"Exception: {str(e)}")

    async def test_starter_message_limit(self):
        """Test Starter plan message limit check (10,000 messages)"""
        try:
            async with self.session.get(f"{API_BASE}/plans/check-limit/messages") as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("max") == 10000:  # Starter plan limit
                        self.log_test("Starter message limit check", True, 
                                    f"Correct Starter limit: {result['current']}/{result['max']}")
                    else:
                        self.log_test("Starter message limit check", False, 
                                    f"Wrong limit. Expected 10000, got {result.get('max')}")
                else:
                    error_text = await response.text()
                    self.log_test("Starter message limit check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Starter message limit check", False, f"Exception: {str(e)}")

    async def test_starter_file_limit(self):
        """Test Starter plan file upload limit check (20 files)"""
        try:
            async with self.session.get(f"{API_BASE}/plans/check-limit/file_uploads") as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("max") == 20:  # Starter plan limit
                        self.log_test("Starter file upload limit check", True, 
                                    f"Correct Starter limit: {result['current']}/{result['max']}")
                    else:
                        self.log_test("Starter file upload limit check", False, 
                                    f"Wrong limit. Expected 20, got {result.get('max')}")
                else:
                    error_text = await response.text()
                    self.log_test("Starter file upload limit check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Starter file upload limit check", False, f"Exception: {str(e)}")

    async def test_usage_tracking_accuracy(self):
        """Test usage tracking accuracy"""
        print("\n📊 Testing Usage Tracking Accuracy...")
        
        # Get initial usage stats
        initial_usage = await self.get_usage_stats()
        if not initial_usage:
            self.log_test("Get initial usage stats", False, "Failed to get initial usage")
            return

        # Test chatbot creation increments counter
        await self.test_chatbot_usage_tracking(initial_usage)
        
        # Test message sending increments counter
        await self.test_message_usage_tracking()
        
        # Test source creation increments counters
        await self.test_source_usage_tracking()
        
        # Test deletion decrements counters
        await self.test_deletion_usage_tracking()

    async def get_usage_stats(self):
        """Get current usage statistics"""
        try:
            async with self.session.get(f"{API_BASE}/plans/usage") as response:
                if response.status == 200:
                    return await response.json()
        except:
            pass
        return None

    async def test_chatbot_usage_tracking(self, initial_usage):
        """Test chatbot usage tracking"""
        initial_count = initial_usage["usage"]["chatbots"]["current"]
        
        # Create a chatbot
        chatbot_data = {
            "name": "Usage Tracking Test Bot",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "temperature": 0.7,
            "instructions": "Test bot for usage tracking."
        }
        
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    new_chatbot_id = result["id"]
                    self.test_chatbot_ids.append(new_chatbot_id)
                    
                    # Check if usage incremented
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_count = new_usage["usage"]["chatbots"]["current"]
                        if new_count == initial_count + 1:
                            self.log_test("Chatbot creation usage tracking", True, 
                                        f"Count incremented: {initial_count} → {new_count}")
                        else:
                            self.log_test("Chatbot creation usage tracking", False, 
                                        f"Count not incremented correctly: {initial_count} → {new_count}")
                    else:
                        self.log_test("Chatbot creation usage tracking", False, "Failed to get updated usage")
                else:
                    self.log_test("Chatbot creation usage tracking", False, f"Failed to create chatbot: {response.status}")
        except Exception as e:
            self.log_test("Chatbot creation usage tracking", False, f"Exception: {str(e)}")

    async def test_message_usage_tracking(self):
        """Test message usage tracking"""
        if not self.test_chatbot_ids:
            self.log_test("Message usage tracking", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Get initial message count
        initial_usage = await self.get_usage_stats()
        if not initial_usage:
            self.log_test("Message usage tracking", False, "Failed to get initial usage")
            return
            
        initial_messages = initial_usage["usage"]["messages"]["current"]
        
        # Send a message
        try:
            chat_data = {
                "message": "Hello, this is a test message for usage tracking.",
                "chatbot_id": chatbot_id,
                "session_id": "test-session-123"
            }
            
            async with self.session.post(f"{API_BASE}/chat", json=chat_data) as response:
                if response.status == 200:
                    # Check if usage incremented by 2 (user + assistant message)
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_messages = new_usage["usage"]["messages"]["current"]
                        if new_messages == initial_messages + 2:
                            self.log_test("Message usage tracking", True, 
                                        f"Messages incremented by 2: {initial_messages} → {new_messages}")
                        else:
                            self.log_test("Message usage tracking", False, 
                                        f"Messages not incremented correctly: {initial_messages} → {new_messages} (expected +2)")
                    else:
                        self.log_test("Message usage tracking", False, "Failed to get updated usage")
                else:
                    error_text = await response.text()
                    self.log_test("Message usage tracking", False, f"Chat failed: {response.status}, {error_text}")
        except Exception as e:
            self.log_test("Message usage tracking", False, f"Exception: {str(e)}")

    async def test_source_usage_tracking(self):
        """Test source creation usage tracking"""
        if not self.test_chatbot_ids:
            self.log_test("Source usage tracking", False, "No test chatbot available")
            return
            
        chatbot_id = self.test_chatbot_ids[0]
        
        # Get initial usage
        initial_usage = await self.get_usage_stats()
        if not initial_usage:
            return
            
        initial_files = initial_usage["usage"]["file_uploads"]["current"]
        initial_websites = initial_usage["usage"]["website_sources"]["current"]
        initial_texts = initial_usage["usage"]["text_sources"]["current"]
        
        # Test file upload tracking
        try:
            file_content = "Test file for usage tracking"
            form_data = aiohttp.FormData()
            form_data.add_field('chatbot_id', chatbot_id)
            form_data.add_field('file', file_content, filename='usage_test.txt', content_type='text/plain')
            
            async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/file", data=form_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_source_ids.append(result["id"])
                    
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_files = new_usage["usage"]["file_uploads"]["current"]
                        if new_files == initial_files + 1:
                            self.log_test("File upload usage tracking", True, 
                                        f"File count incremented: {initial_files} → {new_files}")
                        else:
                            self.log_test("File upload usage tracking", False, 
                                        f"File count not incremented: {initial_files} → {new_files}")
        except Exception as e:
            self.log_test("File upload usage tracking", False, f"Exception: {str(e)}")

        # Test website source tracking
        try:
            form_data = aiohttp.FormData()
            form_data.add_field('url', "https://example.com")
            
            async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/website", data=form_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_source_ids.append(result["id"])
                    
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_websites = new_usage["usage"]["website_sources"]["current"]
                        if new_websites == initial_websites + 1:
                            self.log_test("Website source usage tracking", True, 
                                        f"Website count incremented: {initial_websites} → {new_websites}")
                        else:
                            self.log_test("Website source usage tracking", False, 
                                        f"Website count not incremented: {initial_websites} → {new_websites}")
        except Exception as e:
            self.log_test("Website source usage tracking", False, f"Exception: {str(e)}")

        # Test text source tracking
        try:
            form_data = aiohttp.FormData()
            form_data.add_field('name', "Usage Tracking Text")
            form_data.add_field('content', "This is test text content for usage tracking verification.")
            
            async with self.session.post(f"{API_BASE}/sources/chatbot/{chatbot_id}/text", data=form_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_source_ids.append(result["id"])
                    
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_texts = new_usage["usage"]["text_sources"]["current"]
                        if new_texts == initial_texts + 1:
                            self.log_test("Text source usage tracking", True, 
                                        f"Text count incremented: {initial_texts} → {new_texts}")
                        else:
                            self.log_test("Text source usage tracking", False, 
                                        f"Text count not incremented: {initial_texts} → {new_texts}")
        except Exception as e:
            self.log_test("Text source usage tracking", False, f"Exception: {str(e)}")

    async def test_deletion_usage_tracking(self):
        """Test that deletion decrements usage counters"""
        if not self.test_chatbot_ids or not self.test_source_ids:
            self.log_test("Deletion usage tracking", False, "No test resources to delete")
            return
            
        # Get usage before deletion
        initial_usage = await self.get_usage_stats()
        if not initial_usage:
            return
            
        initial_chatbots = initial_usage["usage"]["chatbots"]["current"]
        
        # Delete a chatbot
        try:
            chatbot_to_delete = self.test_chatbot_ids.pop()
            async with self.session.delete(f"{API_BASE}/chatbots/{chatbot_to_delete}") as response:
                if response.status == 204:
                    new_usage = await self.get_usage_stats()
                    if new_usage:
                        new_chatbots = new_usage["usage"]["chatbots"]["current"]
                        if new_chatbots == initial_chatbots - 1:
                            self.log_test("Chatbot deletion usage tracking", True, 
                                        f"Chatbot count decremented: {initial_chatbots} → {new_chatbots}")
                        else:
                            self.log_test("Chatbot deletion usage tracking", False, 
                                        f"Chatbot count not decremented: {initial_chatbots} → {new_chatbots}")
                else:
                    self.log_test("Chatbot deletion usage tracking", False, f"Failed to delete chatbot: {response.status}")
        except Exception as e:
            self.log_test("Chatbot deletion usage tracking", False, f"Exception: {str(e)}")

        # Delete a source
        if self.test_source_ids:
            try:
                source_to_delete = self.test_source_ids.pop()
                async with self.session.delete(f"{API_BASE}/sources/{source_to_delete}") as response:
                    if response.status == 204:
                        self.log_test("Source deletion", True, "Source deleted successfully")
                    else:
                        self.log_test("Source deletion", False, f"Failed to delete source: {response.status}")
            except Exception as e:
                self.log_test("Source deletion", False, f"Exception: {str(e)}")

    async def test_limit_check_api(self):
        """Test limit check API endpoints"""
        print("\n🔍 Testing Limit Check API...")
        
        limit_types = ["chatbots", "messages", "file_uploads", "website_sources", "text_sources"]
        
        for limit_type in limit_types:
            try:
                async with self.session.get(f"{API_BASE}/plans/check-limit/{limit_type}") as response:
                    if response.status == 200:
                        result = await response.json()
                        required_fields = ["current", "max", "reached"]
                        if all(field in result for field in required_fields):
                            self.log_test(f"Check limit: {limit_type}", True, 
                                        f"Current: {result['current']}, Max: {result['max']}, Reached: {result['reached']}")
                        else:
                            missing = [f for f in required_fields if f not in result]
                            self.log_test(f"Check limit: {limit_type}", False, 
                                        f"Missing fields: {missing}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Check limit: {limit_type}", False, 
                                    f"Status: {response.status}, Error: {error_text}")
            except Exception as e:
                self.log_test(f"Check limit: {limit_type}", False, f"Exception: {str(e)}")

    async def test_error_messages(self):
        """Test error message format and content"""
        print("\n❌ Testing Error Messages...")
        
        # Ensure we're on Free plan for limit testing
        await self.ensure_free_plan()
        
        # Try to create chatbot when limit is reached (should give proper error)
        # First create one chatbot to reach limit
        await self.cleanup_existing_chatbots()
        
        chatbot_data = {
            "name": "Limit Test Bot",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "temperature": 0.7,
            "instructions": "Test bot."
        }
        
        # Create first chatbot
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    self.test_chatbot_ids.append(result["id"])
        except:
            pass
        
        # Try to create second chatbot (should fail with proper error)
        chatbot_data["name"] = "Second Bot (Should Fail)"
        try:
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 403:
                    error_data = await response.json()
                    
                    # Check error message format
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        required_fields = ["current", "max", "upgrade_required"]
                        
                        if all(field in detail for field in required_fields):
                            self.log_test("Error message format", True, 
                                        f"Proper error format with fields: {list(detail.keys())}")
                        else:
                            missing = [f for f in required_fields if f not in detail]
                            self.log_test("Error message format", False, 
                                        f"Missing error fields: {missing}")
                            
                        # Check if error message is actionable
                        if detail.get("upgrade_required") and "current" in detail and "max" in detail:
                            self.log_test("Error message actionability", True, 
                                        f"Clear actionable error: current={detail['current']}, max={detail['max']}")
                        else:
                            self.log_test("Error message actionability", False, 
                                        f"Error not actionable: {detail}")
                    else:
                        self.log_test("Error message format", False, 
                                    f"No detail field in error: {error_data}")
                else:
                    self.log_test("Error message format", False, 
                                f"Expected 403 error, got {response.status}")
        except Exception as e:
            self.log_test("Error message format", False, f"Exception: {str(e)}")

    async def cleanup_test_resources(self):
        """Clean up test resources"""
        print("\n🧹 Cleaning up test resources...")
        
        # Delete test chatbots
        for chatbot_id in self.test_chatbot_ids:
            try:
                await self.session.delete(f"{API_BASE}/chatbots/{chatbot_id}")
            except:
                pass
                
        # Delete test sources
        for source_id in self.test_source_ids:
            try:
                await self.session.delete(f"{API_BASE}/sources/{source_id}")
            except:
                pass

    async def run_all_tests(self):
        """Run all subscription system tests"""
        print("🚀 Starting Comprehensive Subscription & Plan Enforcement Testing")
        print(f"Backend URL: {API_BASE}")
        print(f"Mock User: {self.mock_user_id}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Run all test categories
            await self.test_plan_system_basics()
            await self.test_plan_upgrade_flow()
            await self.test_free_plan_limits()
            await self.test_starter_plan_features()
            await self.test_usage_tracking_accuracy()
            await self.test_limit_check_api()
            await self.test_error_messages()
            
        finally:
            await self.cleanup_test_resources()
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()
        
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n" + "=" * 80)
        print("📊 SUBSCRIPTION & PLAN ENFORCEMENT TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        # Categorize results
        categories = {
            "Plan System Basics": ["GET /api/plans/", "GET /api/plans/current", "GET /api/plans/usage"],
            "Plan Upgrades": ["Upgrade Free → Starter", "Upgrade Starter → Professional", "Upgrade Professional → Enterprise"],
            "Free Plan Limits": ["Create 1st chatbot", "Create 2nd chatbot", "Upload file", "Add website", "Add text source"],
            "Starter Plan Features": ["Starter chatbot", "Starter message limit", "Starter file upload limit"],
            "Usage Tracking": ["usage tracking", "deletion usage tracking"],
            "Limit Checks": ["Check limit:"],
            "Error Messages": ["Error message"]
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
        
        # Show critical subscription functionality status
        print(f"\n🎯 CRITICAL SUBSCRIPTION FUNCTIONALITY:")
        
        critical_tests = [
            ("Plan listing", "GET /api/plans/"),
            ("Current subscription", "GET /api/plans/current"),
            ("Usage statistics", "GET /api/plans/usage"),
            ("Plan upgrades", "Upgrade Free → Starter"),
            ("Free plan limits", "Create 2nd chatbot (should fail)"),
            ("Usage tracking", "usage tracking"),
            ("Limit enforcement", "should fail")
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
            print(f"\n🎉 ALL CRITICAL SUBSCRIPTION FEATURES WORKING!")
        else:
            print(f"\n⚠️  SOME CRITICAL SUBSCRIPTION FEATURES NEED ATTENTION")

async def main():
    """Main test execution"""
    test_suite = SubscriptionTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())