#!/usr/bin/env python3
"""
Comprehensive Backend API Test Suite for Chatbot Builder
Tests all backend endpoints systematically with proper authentication
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class ChatbotAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        self.test_user_password = "TestPassword123!"
        self.test_user_name = "Test User"
        self.created_chatbot_id = None
        self.created_source_id = None
        self.test_session_id = str(uuid.uuid4())
        
        # Test results tracking
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {message}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        kwargs['headers'] = headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"  {method} {endpoint} -> {response.status_code}")
            return response
        except Exception as e:
            print(f"  {method} {endpoint} -> ERROR: {str(e)}")
            raise
    
    def test_health_check(self):
        """Test API health check"""
        try:
            response = self.make_request('GET', '/api/')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('status') == 'running'
                self.log_result("Health Check", success, f"API Status: {data.get('status', 'unknown')}")
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            payload = {
                "name": self.test_user_name,
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/register', json=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                success = data.get('email') == self.test_user_email
                self.log_result("User Registration", success, f"User ID: {data.get('id', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("User Registration", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("User Registration", False, f"Exception: {str(e)}")
    
    def test_user_login(self):
        """Test user login and get auth token"""
        try:
            payload = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/login', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.auth_token = data.get('access_token')
                success = bool(self.auth_token)
                self.log_result("User Login", success, f"Token received: {bool(self.auth_token)}")
            else:
                error_msg = response.text
                self.log_result("User Login", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("User Login", False, f"Exception: {str(e)}")
    
    def test_get_current_user(self):
        """Test getting current user info"""
        try:
            response = self.make_request('GET', '/api/auth/me')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('email') == self.test_user_email
                self.log_result("Get Current User", success, f"User: {data.get('name', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Get Current User", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Current User", False, f"Exception: {str(e)}")
    
    def test_create_chatbot(self):
        """Test creating a new chatbot"""
        try:
            payload = {
                "name": "Test Chatbot",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "temperature": 0.7,
                "instructions": "You are a helpful test assistant.",
                "welcome_message": "Hello! I'm a test chatbot."
            }
            
            response = self.make_request('POST', '/api/chatbots', json=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                self.created_chatbot_id = data.get('id')
                success = bool(self.created_chatbot_id) and data.get('name') == payload['name']
                self.log_result("Create Chatbot", success, f"Chatbot ID: {self.created_chatbot_id}")
            else:
                error_msg = response.text
                self.log_result("Create Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create Chatbot", False, f"Exception: {str(e)}")
    
    def test_list_chatbots(self):
        """Test listing all chatbots"""
        try:
            response = self.make_request('GET', '/api/chatbots')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) > 0
                self.log_result("List Chatbots", success, f"Found {len(data)} chatbots")
            else:
                error_msg = response.text
                self.log_result("List Chatbots", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("List Chatbots", False, f"Exception: {str(e)}")
    
    def test_get_chatbot_details(self):
        """Test getting single chatbot details"""
        if not self.created_chatbot_id:
            self.log_result("Get Chatbot Details", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/chatbots/{self.created_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('id') == self.created_chatbot_id
                self.log_result("Get Chatbot Details", success, f"Name: {data.get('name', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Get Chatbot Details", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Chatbot Details", False, f"Exception: {str(e)}")
    
    def test_update_chatbot(self):
        """Test updating chatbot settings"""
        if not self.created_chatbot_id:
            self.log_result("Update Chatbot", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "provider": "anthropic",
                "instructions": "You are an updated test assistant with Claude."
            }
            
            response = self.make_request('PUT', f'/api/chatbots/{self.created_chatbot_id}', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = (data.get('model') == payload['model'] and 
                          data.get('provider') == payload['provider'])
                self.log_result("Update Chatbot", success, f"Model: {data.get('model', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Update Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Update Chatbot", False, f"Exception: {str(e)}")
    
    def test_verify_chatbot_update(self):
        """Test verifying chatbot update was successful"""
        if not self.created_chatbot_id:
            self.log_result("Verify Chatbot Update", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/chatbots/{self.created_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('model') == "claude-3-5-sonnet-20241022"
                self.log_result("Verify Chatbot Update", success, f"Updated model: {data.get('model', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Verify Chatbot Update", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Verify Chatbot Update", False, f"Exception: {str(e)}")
    
    def test_add_text_source(self):
        """Test adding text content as source"""
        if not self.created_chatbot_id:
            self.log_result("Add Text Source", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "name": "Test Knowledge Base",
                "content": "This is test knowledge content for the chatbot. It contains information about our company policies and procedures."
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{self.created_chatbot_id}/text', data=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                self.created_source_id = data.get('id')
                success = bool(self.created_source_id) and data.get('type') == 'text'
                self.log_result("Add Text Source", success, f"Source ID: {self.created_source_id}")
            else:
                error_msg = response.text
                self.log_result("Add Text Source", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Add Text Source", False, f"Exception: {str(e)}")
    
    def test_add_website_source(self):
        """Test adding website URL as source"""
        if not self.created_chatbot_id:
            self.log_result("Add Website Source", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "url": "https://example.com"
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{self.created_chatbot_id}/website', data=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                success = data.get('type') == 'website' and data.get('url') == payload['url']
                self.log_result("Add Website Source", success, f"URL: {data.get('url', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Add Website Source", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Add Website Source", False, f"Exception: {str(e)}")
    
    def test_upload_file_source(self):
        """Test uploading a file as source"""
        if not self.created_chatbot_id:
            self.log_result("Upload File Source", False, "No chatbot ID available")
            return
        
        try:
            # Create a test text file
            test_content = "This is a test document for file upload. It contains sample content for training the chatbot."
            files = {
                'file': ('test_document.txt', test_content, 'text/plain')
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{self.created_chatbot_id}/file', files=files)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                success = data.get('type') == 'file' and data.get('name') == 'test_document.txt'
                self.log_result("Upload File Source", success, f"File: {data.get('name', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Upload File Source", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Upload File Source", False, f"Exception: {str(e)}")
    
    def test_list_sources(self):
        """Test listing all sources for chatbot"""
        if not self.created_chatbot_id:
            self.log_result("List Sources", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/sources/chatbot/{self.created_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) > 0
                self.log_result("List Sources", success, f"Found {len(data)} sources")
            else:
                error_msg = response.text
                self.log_result("List Sources", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("List Sources", False, f"Exception: {str(e)}")
    
    def test_send_chat_message(self):
        """Test sending a message to chatbot"""
        if not self.created_chatbot_id:
            self.log_result("Send Chat Message", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "chatbot_id": self.created_chatbot_id,
                "message": "Hello! Can you tell me about the test knowledge base?",
                "session_id": self.test_session_id,
                "user_name": "Test User",
                "user_email": "testuser@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                success = bool(ai_message) and len(ai_message) > 0
                self.log_result("Send Chat Message", success, f"AI Response length: {len(ai_message)} chars")
            else:
                error_msg = response.text
                self.log_result("Send Chat Message", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Send Chat Message", False, f"Exception: {str(e)}")
    
    def test_get_conversations(self):
        """Test getting conversations for chatbot"""
        if not self.created_chatbot_id:
            self.log_result("Get Conversations", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/chat/conversations/{self.created_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list)
                self.log_result("Get Conversations", success, f"Found {len(data)} conversations")
            else:
                error_msg = response.text
                self.log_result("Get Conversations", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Conversations", False, f"Exception: {str(e)}")
    
    def test_dashboard_analytics(self):
        """Test getting dashboard analytics"""
        try:
            response = self.make_request('GET', '/api/analytics/dashboard')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['total_conversations', 'total_messages', 'active_chatbots', 'total_chatbots']
                success = all(field in data for field in required_fields)
                self.log_result("Dashboard Analytics", success, f"Chatbots: {data.get('total_chatbots', 0)}")
            else:
                error_msg = response.text
                self.log_result("Dashboard Analytics", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Dashboard Analytics", False, f"Exception: {str(e)}")
    
    def test_chatbot_analytics(self):
        """Test getting chatbot-specific analytics"""
        if not self.created_chatbot_id:
            self.log_result("Chatbot Analytics", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/analytics/chatbot/{self.created_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['chatbot_id', 'total_conversations', 'total_messages']
                success = all(field in data for field in required_fields)
                self.log_result("Chatbot Analytics", success, f"Messages: {data.get('total_messages', 0)}")
            else:
                error_msg = response.text
                self.log_result("Chatbot Analytics", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Chatbot Analytics", False, f"Exception: {str(e)}")
    
    def test_delete_source(self):
        """Test deleting a source"""
        if not self.created_source_id:
            self.log_result("Delete Source", False, "No source ID available")
            return
        
        try:
            response = self.make_request('DELETE', f'/api/sources/{self.created_source_id}')
            success = response.status_code == 204
            
            self.log_result("Delete Source", success, f"Source deleted: {self.created_source_id}")
        except Exception as e:
            self.log_result("Delete Source", False, f"Exception: {str(e)}")
    
    def test_delete_chatbot(self):
        """Test deleting chatbot"""
        if not self.created_chatbot_id:
            self.log_result("Delete Chatbot", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('DELETE', f'/api/chatbots/{self.created_chatbot_id}')
            success = response.status_code == 204
            
            self.log_result("Delete Chatbot", success, f"Chatbot deleted: {self.created_chatbot_id}")
        except Exception as e:
            self.log_result("Delete Chatbot", False, f"Exception: {str(e)}")
    
    def test_verify_deletion(self):
        """Test verifying chatbot deletion"""
        if not self.created_chatbot_id:
            self.log_result("Verify Deletion", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/chatbots/{self.created_chatbot_id}')
            success = response.status_code == 404
            
            self.log_result("Verify Deletion", success, "Chatbot not found (expected)")
        except Exception as e:
            self.log_result("Verify Deletion", False, f"Exception: {str(e)}")
    
    def test_lemonsqueezy_plans(self):
        """Test GET /api/lemonsqueezy/plans - Should return available subscription plans"""
        try:
            response = self.make_request('GET', '/api/lemonsqueezy/plans')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                plans = data.get('plans', [])
                
                # Check if we have both starter and professional plans
                plan_ids = [plan.get('id') for plan in plans]
                has_starter = 'starter' in plan_ids
                has_professional = 'professional' in plan_ids
                
                # Verify plan structure
                valid_plans = True
                for plan in plans:
                    required_fields = ['id', 'name', 'price', 'currency', 'interval', 'variant_id', 'features']
                    if not all(field in plan for field in required_fields):
                        valid_plans = False
                        break
                
                success = has_starter and has_professional and valid_plans
                message = f"Found {len(plans)} plans: {', '.join(plan_ids)}"
                if not valid_plans:
                    message += " (Invalid plan structure)"
                
                self.log_result("Lemon Squeezy Plans", success, message)
            else:
                error_msg = response.text
                self.log_result("Lemon Squeezy Plans", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Lemon Squeezy Plans", False, f"Exception: {str(e)}")
    
    def test_lemonsqueezy_subscription_status(self):
        """Test GET /api/lemonsqueezy/subscription/status - Should return subscription status for demo user"""
        try:
            response = self.make_request('GET', '/api/lemonsqueezy/subscription/status')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['has_subscription', 'plan', 'status']
                success = all(field in data for field in required_fields)
                
                message = f"Plan: {data.get('plan', 'unknown')}, Status: {data.get('status', 'unknown')}"
                if data.get('has_subscription'):
                    message += f", Subscription ID: {data.get('subscription_id', 'N/A')}"
                
                self.log_result("Lemon Squeezy Subscription Status", success, message)
            else:
                error_msg = response.text
                self.log_result("Lemon Squeezy Subscription Status", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Lemon Squeezy Subscription Status", False, f"Exception: {str(e)}")
    
    def test_lemonsqueezy_checkout_starter(self):
        """Test POST /api/lemonsqueezy/checkout/create with starter plan"""
        try:
            checkout_data = {
                "plan": "starter",
                "user_id": "demo-user-123",
                "user_email": "demo@botsmith.com"
            }
            
            response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                checkout_url = data.get('checkout_url', '')
                message = data.get('message', '')
                
                # Verify checkout URL is valid Lemon Squeezy URL
                is_valid_url = checkout_url.startswith('https://') and 'lemonsqueezy.com' in checkout_url
                success = is_valid_url and checkout_url != ''
                
                result_message = f"Message: {message}"
                if is_valid_url:
                    result_message += f", URL: {checkout_url[:50]}..."
                else:
                    result_message += f", Invalid URL: {checkout_url}"
                
                self.log_result("Lemon Squeezy Checkout (Starter)", success, result_message)
            else:
                error_msg = response.text
                self.log_result("Lemon Squeezy Checkout (Starter)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Lemon Squeezy Checkout (Starter)", False, f"Exception: {str(e)}")
    
    def test_lemonsqueezy_checkout_professional(self):
        """Test POST /api/lemonsqueezy/checkout/create with professional plan"""
        try:
            checkout_data = {
                "plan": "professional",
                "user_id": "demo-user-123",
                "user_email": "demo@botsmith.com"
            }
            
            response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                checkout_url = data.get('checkout_url', '')
                message = data.get('message', '')
                
                # Verify checkout URL is valid Lemon Squeezy URL
                is_valid_url = checkout_url.startswith('https://') and 'lemonsqueezy.com' in checkout_url
                success = is_valid_url and checkout_url != ''
                
                result_message = f"Message: {message}"
                if is_valid_url:
                    result_message += f", URL: {checkout_url[:50]}..."
                else:
                    result_message += f", Invalid URL: {checkout_url}"
                
                self.log_result("Lemon Squeezy Checkout (Professional)", success, result_message)
            else:
                error_msg = response.text
                self.log_result("Lemon Squeezy Checkout (Professional)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Lemon Squeezy Checkout (Professional)", False, f"Exception: {str(e)}")
    
    def test_lemonsqueezy_checkout_invalid_plan(self):
        """Test POST /api/lemonsqueezy/checkout/create with invalid plan (should fail)"""
        try:
            checkout_data = {
                "plan": "invalid_plan",
                "user_id": "demo-user-123",
                "user_email": "demo@botsmith.com"
            }
            
            response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
            # Should return 400 for invalid plan
            success = response.status_code == 400
            
            if success:
                self.log_result("Lemon Squeezy Invalid Plan", success, "Correctly rejected invalid plan")
            else:
                error_msg = response.text
                self.log_result("Lemon Squeezy Invalid Plan", False, f"Status: {response.status_code}, Expected 400, Error: {error_msg}")
        except Exception as e:
            self.log_result("Lemon Squeezy Invalid Plan", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Chatbot Builder Backend API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence
        test_methods = [
            self.test_health_check,
            self.test_user_registration,
            self.test_user_login,
            self.test_get_current_user,
            self.test_create_chatbot,
            self.test_list_chatbots,
            self.test_get_chatbot_details,
            self.test_update_chatbot,
            self.test_verify_chatbot_update,
            self.test_add_text_source,
            self.test_add_website_source,
            self.test_upload_file_source,
            self.test_list_sources,
            self.test_send_chat_message,
            self.test_get_conversations,
            self.test_dashboard_analytics,
            self.test_chatbot_analytics,
            # Lemon Squeezy subscription tests
            self.test_lemonsqueezy_plans,
            self.test_lemonsqueezy_subscription_status,
            self.test_lemonsqueezy_checkout_starter,
            self.test_lemonsqueezy_checkout_professional,
            self.test_lemonsqueezy_checkout_invalid_plan,
            # Cleanup tests
            self.test_delete_source,
            self.test_delete_chatbot,
            self.test_verify_deletion
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"{test_method.__name__}: CRITICAL ERROR - {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results["errors"]:
            print("\n🔍 FAILED TESTS:")
            for error in self.results["errors"]:
                print(f"   • {error}")
        
        return self.results


def main():
    """Main test execution"""
    # Get base URL from environment or use default
    base_url = "https://quickinstall-2.preview.emergentagent.com"
    
    print(f"Testing Chatbot Builder API at: {base_url}")
    
    # Initialize and run tests
    tester = ChatbotAPITester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()