#!/usr/bin/env python3
"""
Focused Backend API Tests for Chatbot Builder - Specific Review Request
Tests multi-provider AI support and comprehensive source management
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class FocusedChatbotTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = "demo-user-123"  # As requested in review
        self.chatbots = {}  # Store chatbot IDs by provider
        self.sources = {}   # Store source IDs
        
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
        """Make HTTP request with mocked authentication"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        # Mock authentication by adding user_id header
        headers['X-User-ID'] = self.user_id
        kwargs['headers'] = headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"  {method} {endpoint} -> {response.status_code}")
            return response
        except Exception as e:
            print(f"  {method} {endpoint} -> ERROR: {str(e)}")
            raise
    
    def test_create_openai_chatbot(self):
        """Test creating chatbot with OpenAI provider"""
        try:
            payload = {
                "name": "OpenAI Test Bot",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "temperature": 0.7,
                "instructions": "You are a helpful assistant powered by OpenAI GPT-4o-mini.",
                "welcome_message": "Hello! I'm powered by OpenAI."
            }
            
            response = self.make_request('POST', '/api/chatbots', json=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                chatbot_id = data.get('id')
                self.chatbots['openai'] = chatbot_id
                success = bool(chatbot_id) and data.get('provider') == 'openai'
                self.log_result("Create OpenAI Chatbot", success, f"ID: {chatbot_id}")
            else:
                error_msg = response.text
                self.log_result("Create OpenAI Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create OpenAI Chatbot", False, f"Exception: {str(e)}")
    
    def test_create_claude_chatbot(self):
        """Test creating chatbot with Claude provider"""
        try:
            payload = {
                "name": "Claude Test Bot",
                "model": "claude-3-5-sonnet-20241022",
                "provider": "anthropic",
                "temperature": 0.5,
                "instructions": "You are a helpful assistant powered by Claude 3.5 Sonnet.",
                "welcome_message": "Hello! I'm powered by Claude."
            }
            
            response = self.make_request('POST', '/api/chatbots', json=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                chatbot_id = data.get('id')
                self.chatbots['claude'] = chatbot_id
                success = bool(chatbot_id) and data.get('provider') == 'anthropic'
                self.log_result("Create Claude Chatbot", success, f"ID: {chatbot_id}")
            else:
                error_msg = response.text
                self.log_result("Create Claude Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create Claude Chatbot", False, f"Exception: {str(e)}")
    
    def test_create_gemini_chatbot(self):
        """Test creating chatbot with Gemini provider"""
        try:
            payload = {
                "name": "Gemini Test Bot",
                "model": "gemini-2.0-flash-exp",
                "provider": "google",
                "temperature": 0.8,
                "instructions": "You are a helpful assistant powered by Google Gemini 2.0 Flash.",
                "welcome_message": "Hello! I'm powered by Gemini."
            }
            
            response = self.make_request('POST', '/api/chatbots', json=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                chatbot_id = data.get('id')
                self.chatbots['gemini'] = chatbot_id
                success = bool(chatbot_id) and data.get('provider') == 'google'
                self.log_result("Create Gemini Chatbot", success, f"ID: {chatbot_id}")
            else:
                error_msg = response.text
                self.log_result("Create Gemini Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create Gemini Chatbot", False, f"Exception: {str(e)}")
    
    def test_comprehensive_source_management(self):
        """Test comprehensive source management for OpenAI chatbot"""
        chatbot_id = self.chatbots.get('openai')
        if not chatbot_id:
            self.log_result("Comprehensive Source Management", False, "No OpenAI chatbot available")
            return
        
        # Test 1: Add text source
        try:
            payload = {
                "name": "Company Policies",
                "content": "Our company has a flexible work-from-home policy. Employees can work remotely up to 3 days per week. We also offer comprehensive health insurance and 25 days of paid vacation annually."
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{chatbot_id}/text', data=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                source_id = data.get('id')
                self.sources['text'] = source_id
                success = bool(source_id) and data.get('type') == 'text'
                self.log_result("Add Text Source (Policies)", success, f"Source ID: {source_id}")
            else:
                self.log_result("Add Text Source (Policies)", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Add Text Source (Policies)", False, f"Exception: {str(e)}")
        
        # Test 2: Add website source
        try:
            payload = {
                "url": "https://example.com"
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{chatbot_id}/website', data=payload)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                source_id = data.get('id')
                self.sources['website'] = source_id
                success = data.get('type') == 'website' and data.get('url') == payload['url']
                self.log_result("Add Website Source (example.com)", success, f"Source ID: {source_id}")
            else:
                self.log_result("Add Website Source (example.com)", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Add Website Source (example.com)", False, f"Exception: {str(e)}")
        
        # Test 3: Upload file source
        try:
            test_content = """Product Documentation
            
Our main product is a chatbot builder platform that allows users to:
1. Create AI-powered chatbots with multiple provider support
2. Upload various document types as knowledge sources
3. Integrate with websites for real-time customer support
4. Track analytics and conversation metrics

Key Features:
- Multi-provider AI support (OpenAI, Claude, Gemini)
- Document processing (PDF, DOCX, TXT, CSV, XLSX)
- Website scraping capabilities
- Real-time chat interface
- Comprehensive analytics dashboard"""
            
            files = {
                'file': ('product_docs.txt', test_content, 'text/plain')
            }
            
            response = self.make_request('POST', f'/api/sources/chatbot/{chatbot_id}/file', files=files)
            success = response.status_code == 201
            
            if success:
                data = response.json()
                source_id = data.get('id')
                self.sources['file'] = source_id
                success = data.get('type') == 'file' and data.get('name') == 'product_docs.txt'
                self.log_result("Upload File Source (Product Docs)", success, f"Source ID: {source_id}")
            else:
                self.log_result("Upload File Source (Product Docs)", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Upload File Source (Product Docs)", False, f"Exception: {str(e)}")
        
        # Test 4: List all sources and verify count
        try:
            response = self.make_request('GET', f'/api/sources/chatbot/{chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                source_count = len(data)
                success = isinstance(data, list) and source_count >= 3
                self.log_result("List All Sources", success, f"Found {source_count} sources")
                
                # Verify source types
                source_types = [source.get('type') for source in data]
                expected_types = ['text', 'website', 'file']
                types_present = all(t in source_types for t in expected_types)
                self.log_result("Verify Source Types", types_present, f"Types: {source_types}")
            else:
                self.log_result("List All Sources", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("List All Sources", False, f"Exception: {str(e)}")
    
    def test_chat_without_sources(self):
        """Test chat functionality without sources (Claude chatbot)"""
        chatbot_id = self.chatbots.get('claude')
        if not chatbot_id:
            self.log_result("Chat Without Sources", False, "No Claude chatbot available")
            return
        
        try:
            payload = {
                "chatbot_id": chatbot_id,
                "message": "Hello! Can you tell me about yourself?",
                "session_id": str(uuid.uuid4()),
                "user_name": "Demo User",
                "user_email": "demo@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                success = bool(ai_message) and len(ai_message) > 0
                self.log_result("Chat Without Sources (Claude)", success, f"Response length: {len(ai_message)} chars")
            else:
                error_msg = response.text
                self.log_result("Chat Without Sources (Claude)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Chat Without Sources (Claude)", False, f"Exception: {str(e)}")
    
    def test_chat_with_sources(self):
        """Test chat functionality with sources (OpenAI chatbot)"""
        chatbot_id = self.chatbots.get('openai')
        if not chatbot_id:
            self.log_result("Chat With Sources", False, "No OpenAI chatbot available")
            return
        
        try:
            payload = {
                "chatbot_id": chatbot_id,
                "message": "What is our company's work-from-home policy?",
                "session_id": str(uuid.uuid4()),
                "user_name": "Demo User",
                "user_email": "demo@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                # Check if response mentions work-from-home or remote work
                contains_policy_info = any(keyword in ai_message.lower() for keyword in 
                                         ['work-from-home', 'remote', '3 days', 'flexible'])
                success = bool(ai_message) and len(ai_message) > 0 and contains_policy_info
                self.log_result("Chat With Sources (OpenAI)", success, 
                              f"Response mentions policy: {contains_policy_info}")
            else:
                error_msg = response.text
                self.log_result("Chat With Sources (OpenAI)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Chat With Sources (OpenAI)", False, f"Exception: {str(e)}")
    
    def test_gemini_chat_functionality(self):
        """Test chat functionality with Gemini provider"""
        chatbot_id = self.chatbots.get('gemini')
        if not chatbot_id:
            self.log_result("Gemini Chat Test", False, "No Gemini chatbot available")
            return
        
        try:
            payload = {
                "chatbot_id": chatbot_id,
                "message": "What are the key features of a chatbot builder platform?",
                "session_id": str(uuid.uuid4()),
                "user_name": "Demo User",
                "user_email": "demo@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                success = bool(ai_message) and len(ai_message) > 0
                self.log_result("Gemini Chat Test", success, f"Response length: {len(ai_message)} chars")
            else:
                error_msg = response.text
                self.log_result("Gemini Chat Test", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Gemini Chat Test", False, f"Exception: {str(e)}")
    
    def test_session_management(self):
        """Test chat session management with multiple messages"""
        chatbot_id = self.chatbots.get('openai')
        if not chatbot_id:
            self.log_result("Session Management", False, "No OpenAI chatbot available")
            return
        
        session_id = str(uuid.uuid4())
        
        # Send first message
        try:
            payload1 = {
                "chatbot_id": chatbot_id,
                "message": "What are our vacation benefits?",
                "session_id": session_id,
                "user_name": "Demo User",
                "user_email": "demo@example.com"
            }
            
            response1 = self.make_request('POST', '/api/chat', json=payload1)
            success1 = response1.status_code == 200
            
            if success1:
                # Send follow-up message
                payload2 = {
                    "chatbot_id": chatbot_id,
                    "message": "How many days exactly?",
                    "session_id": session_id,
                    "user_name": "Demo User",
                    "user_email": "demo@example.com"
                }
                
                response2 = self.make_request('POST', '/api/chat', json=payload2)
                success2 = response2.status_code == 200
                
                if success2:
                    data2 = response2.json()
                    ai_message2 = data2.get('message', '')
                    # Check if response mentions 25 days from the knowledge base
                    mentions_days = '25' in ai_message2
                    success = bool(ai_message2) and mentions_days
                    self.log_result("Session Management", success, 
                                  f"Follow-up response mentions 25 days: {mentions_days}")
                else:
                    self.log_result("Session Management", False, f"Second message failed: {response2.status_code}")
            else:
                self.log_result("Session Management", False, f"First message failed: {response1.status_code}")
        except Exception as e:
            self.log_result("Session Management", False, f"Exception: {str(e)}")
    
    def test_analytics_comprehensive(self):
        """Test comprehensive analytics functionality"""
        # Test dashboard analytics
        try:
            response = self.make_request('GET', '/api/analytics/dashboard')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['total_conversations', 'total_messages', 'active_chatbots', 'total_chatbots']
                success = all(field in data for field in required_fields)
                chatbot_count = data.get('total_chatbots', 0)
                self.log_result("Dashboard Analytics", success, f"Total chatbots: {chatbot_count}")
            else:
                self.log_result("Dashboard Analytics", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Dashboard Analytics", False, f"Exception: {str(e)}")
        
        # Test chatbot-specific analytics for each provider
        for provider, chatbot_id in self.chatbots.items():
            try:
                response = self.make_request('GET', f'/api/analytics/chatbot/{chatbot_id}')
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    required_fields = ['chatbot_id', 'total_conversations', 'total_messages']
                    success = all(field in data for field in required_fields)
                    message_count = data.get('total_messages', 0)
                    self.log_result(f"{provider.title()} Analytics", success, f"Messages: {message_count}")
                else:
                    self.log_result(f"{provider.title()} Analytics", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"{provider.title()} Analytics", False, f"Exception: {str(e)}")
    
    def test_source_deletion(self):
        """Test source deletion functionality"""
        # Delete text source
        source_id = self.sources.get('text')
        if source_id:
            try:
                response = self.make_request('DELETE', f'/api/sources/{source_id}')
                success = response.status_code == 204
                self.log_result("Delete Text Source", success, f"Source ID: {source_id}")
            except Exception as e:
                self.log_result("Delete Text Source", False, f"Exception: {str(e)}")
        
        # Verify source was deleted by listing sources
        chatbot_id = self.chatbots.get('openai')
        if chatbot_id:
            try:
                response = self.make_request('GET', f'/api/sources/chatbot/{chatbot_id}')
                if response.status_code == 200:
                    data = response.json()
                    remaining_count = len(data)
                    # Should have 2 sources left (website and file)
                    success = remaining_count == 2
                    self.log_result("Verify Source Deletion", success, f"Remaining sources: {remaining_count}")
                else:
                    self.log_result("Verify Source Deletion", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("Verify Source Deletion", False, f"Exception: {str(e)}")
    
    def run_focused_tests(self):
        """Run focused tests based on review request"""
        print("🎯 Starting Focused Chatbot Builder Backend Tests")
        print(f"📍 Base URL: {self.base_url}")
        print(f"👤 User ID: {self.user_id}")
        print("=" * 60)
        
        # Test sequence focusing on review requirements
        test_methods = [
            # Multi-provider chatbot creation
            self.test_create_openai_chatbot,
            self.test_create_claude_chatbot,
            self.test_create_gemini_chatbot,
            
            # Comprehensive source management
            self.test_comprehensive_source_management,
            
            # Chat functionality tests
            self.test_chat_without_sources,
            self.test_chat_with_sources,
            self.test_gemini_chat_functionality,
            self.test_session_management,
            
            # Analytics tests
            self.test_analytics_comprehensive,
            
            # Source deletion
            self.test_source_deletion
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
        print("📊 FOCUSED TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['passed'] + self.results['failed'] > 0:
            success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100)
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.results["errors"]:
            print("\n🔍 FAILED TESTS:")
            for error in self.results["errors"]:
                print(f"   • {error}")
        
        return self.results


def main():
    """Main test execution"""
    base_url = "https://repo-showcase-4.preview.emergentagent.com"
    
    print(f"Testing Chatbot Builder API (Focused) at: {base_url}")
    
    # Initialize and run focused tests
    tester = FocusedChatbotTester(base_url)
    results = tester.run_focused_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()