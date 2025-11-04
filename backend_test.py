#!/usr/bin/env python3
"""
Backend Testing Suite for Subscription & Plan Enforcement System
Comprehensive testing of subscription system, plan limits, and usage tracking.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://preview-setup-7.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class SubscriptionTestSuite:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.mock_user_id = "demo-user-123"
        self.test_chatbot_ids = []
        self.test_source_ids = []
        
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

    async def test_plan_system_basics(self):
        """Test basic plan system endpoints"""
        print("\n🔍 Testing Plan System Basics...")
        
        # Test GET /api/plans/ - List all available plans
        try:
            async with self.session.get(f"{API_BASE}/plans/") as response:
                if response.status == 200:
                    plans = await response.json()
                    expected_plans = ["free", "starter", "professional", "enterprise"]
                    plan_ids = [plan.get("id") for plan in plans]
                    
                    if all(plan_id in plan_ids for plan_id in expected_plans):
                        self.log_test("GET /api/plans/ - List all plans", True, 
                                    f"Found all expected plans: {plan_ids}")
                    else:
                        self.log_test("GET /api/plans/ - List all plans", False, 
                                    f"Missing plans. Expected: {expected_plans}, Got: {plan_ids}")
                else:
                    error_text = await response.text()
                    self.log_test("GET /api/plans/ - List all plans", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("GET /api/plans/ - List all plans", False, f"Exception: {str(e)}")

        # Test GET /api/plans/current - Get current subscription
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    current_sub = await response.json()
                    if "subscription" in current_sub and "plan" in current_sub:
                        plan_id = current_sub["plan"]["id"]
                        self.log_test("GET /api/plans/current - Current subscription", True, 
                                    f"Current plan: {plan_id}")
                    else:
                        self.log_test("GET /api/plans/current - Current subscription", False, 
                                    f"Missing subscription or plan data: {current_sub}")
                else:
                    error_text = await response.text()
                    self.log_test("GET /api/plans/current - Current subscription", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("GET /api/plans/current - Current subscription", False, f"Exception: {str(e)}")

        # Test GET /api/plans/usage - Get usage statistics
        try:
            async with self.session.get(f"{API_BASE}/plans/usage") as response:
                if response.status == 200:
                    usage_stats = await response.json()
                    required_fields = ["plan", "usage", "last_reset"]
                    usage_fields = ["chatbots", "messages", "file_uploads", "website_sources", "text_sources"]
                    
                    if all(field in usage_stats for field in required_fields):
                        if all(field in usage_stats["usage"] for field in usage_fields):
                            self.log_test("GET /api/plans/usage - Usage statistics", True, 
                                        f"All usage fields present: {list(usage_stats['usage'].keys())}")
                        else:
                            missing = [f for f in usage_fields if f not in usage_stats["usage"]]
                            self.log_test("GET /api/plans/usage - Usage statistics", False, 
                                        f"Missing usage fields: {missing}")
                    else:
                        missing = [f for f in required_fields if f not in usage_stats]
                        self.log_test("GET /api/plans/usage - Usage statistics", False, 
                                    f"Missing top-level fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("GET /api/plans/usage - Usage statistics", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("GET /api/plans/usage - Usage statistics", False, f"Exception: {str(e)}")

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