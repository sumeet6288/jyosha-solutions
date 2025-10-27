#!/usr/bin/env python3
"""
Chat Logs Endpoints Test Suite
Tests the chat logs endpoints for chatbot builder analytics feature
"""

import requests
import json
import time
import uuid
from typing import Dict, Any, Optional

class ChatLogsAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        self.test_user_password = "TestPassword123!"
        self.test_user_name = "Test User"
        self.existing_chatbot_id = None
        self.test_session_id = str(uuid.uuid4())
        self.test_conversation_id = None
        
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
    
    def setup_authentication(self):
        """Setup authentication for testing"""
        try:
            # Register user
            payload = {
                "name": self.test_user_name,
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/register', json=payload)
            if response.status_code != 201:
                print(f"Registration failed: {response.text}")
                return False
            
            # Login user
            login_payload = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/login', json=login_payload)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                return bool(self.auth_token)
            else:
                print(f"Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"Authentication setup failed: {str(e)}")
            return False
    
    def get_existing_chatbot(self):
        """Get existing chatbot from the database"""
        try:
            response = self.make_request('GET', '/api/chatbots')
            if response.status_code == 200:
                chatbots = response.json()
                if chatbots and len(chatbots) > 0:
                    self.existing_chatbot_id = chatbots[0]['id']
                    self.log_result("Get Existing Chatbot", True, f"Found chatbot ID: {self.existing_chatbot_id}")
                    return True
                else:
                    self.log_result("Get Existing Chatbot", False, "No chatbots found in database")
                    return False
            else:
                self.log_result("Get Existing Chatbot", False, f"Status: {response.status_code}, Error: {response.text}")
                return False
        except Exception as e:
            self.log_result("Get Existing Chatbot", False, f"Exception: {str(e)}")
            return False
    
    def create_test_conversation(self):
        """Create a test conversation by sending a chat message"""
        if not self.existing_chatbot_id:
            self.log_result("Create Test Conversation", False, "No chatbot ID available")
            return False
        
        try:
            payload = {
                "chatbot_id": self.existing_chatbot_id,
                "message": "Hello! This is a test message for analytics. Can you tell me about your capabilities?",
                "session_id": self.test_session_id,
                "user_name": "Analytics Test User",
                "user_email": "analytics.test@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.test_conversation_id = data.get('conversation_id')
                ai_message = data.get('message', '')
                success = bool(self.test_conversation_id) and bool(ai_message)
                self.log_result("Create Test Conversation", success, 
                              f"Conversation ID: {self.test_conversation_id}, AI Response: {len(ai_message)} chars")
            else:
                error_msg = response.text
                self.log_result("Create Test Conversation", False, f"Status: {response.status_code}, Error: {error_msg}")
            
            return success
        except Exception as e:
            self.log_result("Create Test Conversation", False, f"Exception: {str(e)}")
            return False
    
    def send_additional_messages(self):
        """Send additional messages to create more conversation data"""
        if not self.existing_chatbot_id:
            return False
        
        messages = [
            "What are your main features?",
            "How can you help me with my business?",
            "Thank you for the information!"
        ]
        
        success_count = 0
        for i, message in enumerate(messages):
            try:
                payload = {
                    "chatbot_id": self.existing_chatbot_id,
                    "message": message,
                    "session_id": self.test_session_id,
                    "user_name": "Analytics Test User",
                    "user_email": "analytics.test@example.com"
                }
                
                response = self.make_request('POST', '/api/chat', json=payload)
                if response.status_code == 200:
                    success_count += 1
                    time.sleep(0.5)  # Small delay between messages
                
            except Exception as e:
                print(f"Failed to send message {i+1}: {str(e)}")
        
        self.log_result("Send Additional Messages", success_count == len(messages), 
                       f"Sent {success_count}/{len(messages)} additional messages")
        return success_count > 0
    
    def test_get_conversations(self):
        """Test GET /api/chat/conversations/{chatbot_id}"""
        if not self.existing_chatbot_id:
            self.log_result("Get Conversations", False, "No chatbot ID available")
            return False
        
        try:
            response = self.make_request('GET', f'/api/chat/conversations/{self.existing_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list)
                
                if success and len(data) > 0:
                    # Verify response format matches ConversationResponse model
                    conversation = data[0]
                    required_fields = ['id', 'chatbot_id', 'session_id', 'status', 'messages_count', 'created_at', 'updated_at']
                    missing_fields = [field for field in required_fields if field not in conversation]
                    
                    if missing_fields:
                        success = False
                        self.log_result("Get Conversations", False, f"Missing fields: {missing_fields}")
                    else:
                        # Check data types and format
                        issues = []
                        if not isinstance(conversation['messages_count'], int):
                            issues.append("messages_count should be integer")
                        if conversation['chatbot_id'] != self.existing_chatbot_id:
                            issues.append("chatbot_id mismatch")
                        
                        if issues:
                            success = False
                            self.log_result("Get Conversations", False, f"Format issues: {issues}")
                        else:
                            self.log_result("Get Conversations", True, 
                                          f"Found {len(data)} conversations, first has {conversation['messages_count']} messages")
                else:
                    self.log_result("Get Conversations", True, "Found 0 conversations (valid response)")
            else:
                error_msg = response.text
                self.log_result("Get Conversations", False, f"Status: {response.status_code}, Error: {error_msg}")
            
            return success
        except Exception as e:
            self.log_result("Get Conversations", False, f"Exception: {str(e)}")
            return False
    
    def test_get_messages(self):
        """Test GET /api/chat/messages/{conversation_id}"""
        if not self.test_conversation_id:
            self.log_result("Get Messages", False, "No conversation ID available")
            return False
        
        try:
            response = self.make_request('GET', f'/api/chat/messages/{self.test_conversation_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list)
                
                if success and len(data) > 0:
                    # Verify response format matches MessageResponse model
                    message = data[0]
                    required_fields = ['id', 'conversation_id', 'chatbot_id', 'role', 'content', 'timestamp']
                    missing_fields = [field for field in required_fields if field not in message]
                    
                    if missing_fields:
                        success = False
                        self.log_result("Get Messages", False, f"Missing fields: {missing_fields}")
                    else:
                        # Check data types and format
                        issues = []
                        if message['role'] not in ['user', 'assistant']:
                            issues.append(f"Invalid role: {message['role']}")
                        if message['conversation_id'] != self.test_conversation_id:
                            issues.append("conversation_id mismatch")
                        if not message['content']:
                            issues.append("Empty content")
                        
                        # Check if we have both user and assistant messages
                        roles = [msg['role'] for msg in data]
                        if 'user' not in roles or 'assistant' not in roles:
                            issues.append("Missing user or assistant messages")
                        
                        if issues:
                            success = False
                            self.log_result("Get Messages", False, f"Format issues: {issues}")
                        else:
                            user_msgs = len([m for m in data if m['role'] == 'user'])
                            assistant_msgs = len([m for m in data if m['role'] == 'assistant'])
                            self.log_result("Get Messages", True, 
                                          f"Found {len(data)} messages ({user_msgs} user, {assistant_msgs} assistant)")
                else:
                    self.log_result("Get Messages", True, "Found 0 messages (valid response)")
            else:
                error_msg = response.text
                self.log_result("Get Messages", False, f"Status: {response.status_code}, Error: {error_msg}")
            
            return success
        except Exception as e:
            self.log_result("Get Messages", False, f"Exception: {str(e)}")
            return False
    
    def test_conversations_endpoint_accessibility(self):
        """Test that conversations endpoint is accessible without authentication"""
        try:
            # Test without auth token
            temp_token = self.auth_token
            self.auth_token = None
            
            response = self.make_request('GET', f'/api/chat/conversations/{self.existing_chatbot_id}')
            
            # Restore auth token
            self.auth_token = temp_token
            
            # The endpoint should be accessible (it's a public analytics endpoint)
            success = response.status_code == 200
            self.log_result("Conversations Endpoint Accessibility", success, 
                          f"Public access: {response.status_code == 200}")
            return success
        except Exception as e:
            self.log_result("Conversations Endpoint Accessibility", False, f"Exception: {str(e)}")
            return False
    
    def test_messages_endpoint_accessibility(self):
        """Test that messages endpoint is accessible without authentication"""
        if not self.test_conversation_id:
            self.log_result("Messages Endpoint Accessibility", False, "No conversation ID available")
            return False
        
        try:
            # Test without auth token
            temp_token = self.auth_token
            self.auth_token = None
            
            response = self.make_request('GET', f'/api/chat/messages/{self.test_conversation_id}')
            
            # Restore auth token
            self.auth_token = temp_token
            
            # The endpoint should be accessible (it's a public analytics endpoint)
            success = response.status_code == 200
            self.log_result("Messages Endpoint Accessibility", success, 
                          f"Public access: {response.status_code == 200}")
            return success
        except Exception as e:
            self.log_result("Messages Endpoint Accessibility", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_chatbot_id(self):
        """Test conversations endpoint with invalid chatbot ID"""
        try:
            fake_id = str(uuid.uuid4())
            response = self.make_request('GET', f'/api/chat/conversations/{fake_id}')
            
            # Should return empty list for non-existent chatbot
            success = response.status_code == 200
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) == 0
                self.log_result("Invalid Chatbot ID", success, "Returns empty list for non-existent chatbot")
            else:
                self.log_result("Invalid Chatbot ID", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_result("Invalid Chatbot ID", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_conversation_id(self):
        """Test messages endpoint with invalid conversation ID"""
        try:
            fake_id = str(uuid.uuid4())
            response = self.make_request('GET', f'/api/chat/messages/{fake_id}')
            
            # Should return empty list for non-existent conversation
            success = response.status_code == 200
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) == 0
                self.log_result("Invalid Conversation ID", success, "Returns empty list for non-existent conversation")
            else:
                self.log_result("Invalid Conversation ID", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_result("Invalid Conversation ID", False, f"Exception: {str(e)}")
            return False
    
    def run_chat_logs_tests(self):
        """Run all chat logs related tests"""
        print("🚀 Starting Chat Logs Analytics API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Setup
        if not self.setup_authentication():
            print("❌ Authentication setup failed, cannot continue")
            return self.results
        
        if not self.get_existing_chatbot():
            print("❌ No existing chatbot found, cannot test chat logs")
            return self.results
        
        # Create test data
        self.create_test_conversation()
        self.send_additional_messages()
        
        # Wait a moment for data to be processed
        time.sleep(2)
        
        # Test chat logs endpoints
        test_methods = [
            self.test_get_conversations,
            self.test_get_messages,
            self.test_conversations_endpoint_accessibility,
            self.test_messages_endpoint_accessibility,
            self.test_invalid_chatbot_id,
            self.test_invalid_conversation_id
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
        print("📊 CHAT LOGS TEST SUMMARY")
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
    # Get base URL from environment
    base_url = "https://setup-glimpse.preview.emergentagent.com"
    
    print(f"Testing Chat Logs Analytics API at: {base_url}")
    
    # Initialize and run tests
    tester = ChatLogsAPITester(base_url)
    results = tester.run_chat_logs_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()