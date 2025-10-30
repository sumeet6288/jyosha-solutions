#!/usr/bin/env python3
"""
AI Integration Test - Test different AI providers and chat functionality
"""

import requests
import json
import uuid
import time

class AIIntegrationTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_email = f"aitest_{uuid.uuid4().hex[:8]}@example.com"
        self.test_user_password = "TestPassword123!"
        self.test_user_name = "AI Test User"
        self.chatbots = {}  # Store chatbot IDs by provider
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
    
    def setup_auth(self):
        """Setup authentication"""
        try:
            # Register user
            payload = {
                "name": self.test_user_name,
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/register', json=payload)
            if response.status_code != 201:
                self.log_result("Setup Auth - Register", False, f"Status: {response.status_code}")
                return False
            
            # Login
            login_payload = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.make_request('POST', '/api/auth/login', json=login_payload)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                self.log_result("Setup Auth", True, "Authentication successful")
                return True
            else:
                self.log_result("Setup Auth - Login", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Setup Auth", False, f"Exception: {str(e)}")
            return False
    
    def test_create_chatbots_all_providers(self):
        """Test creating chatbots with different AI providers"""
        providers = [
            {"name": "OpenAI GPT-4o-mini", "provider": "openai", "model": "gpt-4o-mini"},
            {"name": "Claude 3.5 Sonnet", "provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
            {"name": "Gemini 2.0 Flash", "provider": "gemini", "model": "gemini-2.0-flash"}
        ]
        
        for provider_config in providers:
            try:
                payload = {
                    "name": f"Test Bot - {provider_config['name']}",
                    "model": provider_config["model"],
                    "provider": provider_config["provider"],
                    "temperature": 0.7,
                    "instructions": f"You are a helpful assistant powered by {provider_config['name']}. Always mention your provider in responses.",
                    "welcome_message": f"Hello! I'm powered by {provider_config['name']}."
                }
                
                response = self.make_request('POST', '/api/chatbots', json=payload)
                success = response.status_code == 201
                
                if success:
                    data = response.json()
                    chatbot_id = data.get('id')
                    self.chatbots[provider_config['provider']] = chatbot_id
                    self.log_result(f"Create {provider_config['name']} Chatbot", True, f"ID: {chatbot_id}")
                else:
                    error_msg = response.text
                    self.log_result(f"Create {provider_config['name']} Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
            except Exception as e:
                self.log_result(f"Create {provider_config['name']} Chatbot", False, f"Exception: {str(e)}")
    
    def test_add_knowledge_sources(self):
        """Add knowledge sources to all chatbots"""
        if not self.chatbots:
            self.log_result("Add Knowledge Sources", False, "No chatbots available")
            return
        
        # Test knowledge content
        knowledge_content = """
        Company Information:
        - Company Name: TechCorp Solutions
        - Founded: 2020
        - Services: AI consulting, software development, cloud solutions
        - Location: San Francisco, CA
        - Team Size: 50+ employees
        - Specialties: Machine Learning, Natural Language Processing, Cloud Architecture
        """
        
        for provider, chatbot_id in self.chatbots.items():
            try:
                payload = {
                    "name": f"Company Knowledge Base - {provider}",
                    "content": knowledge_content
                }
                
                response = self.make_request('POST', f'/api/sources/chatbot/{chatbot_id}/text', data=payload)
                success = response.status_code == 201
                
                if success:
                    data = response.json()
                    self.log_result(f"Add Knowledge to {provider.title()}", True, f"Source ID: {data.get('id')}")
                else:
                    error_msg = response.text
                    self.log_result(f"Add Knowledge to {provider.title()}", False, f"Status: {response.status_code}, Error: {error_msg}")
            except Exception as e:
                self.log_result(f"Add Knowledge to {provider.title()}", False, f"Exception: {str(e)}")
    
    def test_ai_chat_responses(self):
        """Test AI chat responses from all providers"""
        if not self.chatbots:
            self.log_result("AI Chat Responses", False, "No chatbots available")
            return
        
        test_questions = [
            "What is the company name and when was it founded?",
            "How many employees does the company have?",
            "What services does TechCorp Solutions provide?"
        ]
        
        for provider, chatbot_id in self.chatbots.items():
            for i, question in enumerate(test_questions):
                try:
                    payload = {
                        "chatbot_id": chatbot_id,
                        "message": question,
                        "session_id": f"{self.test_session_id}_{provider}",
                        "user_name": "Test User",
                        "user_email": "testuser@example.com"
                    }
                    
                    response = self.make_request('POST', '/api/chat', json=payload)
                    success = response.status_code == 200
                    
                    if success:
                        data = response.json()
                        ai_message = data.get('message', '')
                        # Check if response contains relevant information
                        relevant = any(keyword in ai_message.lower() for keyword in ['techcorp', 'company', '2020', '50'])
                        
                        if relevant:
                            self.log_result(f"{provider.title()} Chat Q{i+1}", True, f"Response length: {len(ai_message)} chars")
                        else:
                            self.log_result(f"{provider.title()} Chat Q{i+1}", False, "Response doesn't contain expected knowledge")
                    else:
                        error_msg = response.text
                        self.log_result(f"{provider.title()} Chat Q{i+1}", False, f"Status: {response.status_code}, Error: {error_msg}")
                    
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    self.log_result(f"{provider.title()} Chat Q{i+1}", False, f"Exception: {str(e)}")
    
    def test_conversation_history(self):
        """Test conversation history retrieval"""
        for provider, chatbot_id in self.chatbots.items():
            try:
                response = self.make_request('GET', f'/api/chat/conversations/{chatbot_id}')
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    conversation_count = len(data)
                    self.log_result(f"{provider.title()} Conversation History", True, f"Found {conversation_count} conversations")
                else:
                    error_msg = response.text
                    self.log_result(f"{provider.title()} Conversation History", False, f"Status: {response.status_code}, Error: {error_msg}")
            except Exception as e:
                self.log_result(f"{provider.title()} Conversation History", False, f"Exception: {str(e)}")
    
    def cleanup_chatbots(self):
        """Clean up created chatbots"""
        for provider, chatbot_id in self.chatbots.items():
            try:
                response = self.make_request('DELETE', f'/api/chatbots/{chatbot_id}')
                success = response.status_code == 204
                self.log_result(f"Cleanup {provider.title()} Chatbot", success, f"Deleted: {chatbot_id}")
            except Exception as e:
                self.log_result(f"Cleanup {provider.title()} Chatbot", False, f"Exception: {str(e)}")
    
    def run_ai_integration_tests(self):
        """Run all AI integration tests"""
        print("🤖 Starting AI Integration Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Setup
        if not self.setup_auth():
            print("❌ Authentication setup failed. Aborting tests.")
            return self.results
        
        # Test sequence
        test_methods = [
            self.test_create_chatbots_all_providers,
            self.test_add_knowledge_sources,
            self.test_ai_chat_responses,
            self.test_conversation_history,
            self.cleanup_chatbots
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(1)  # Small delay between test groups
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"{test_method.__name__}: CRITICAL ERROR - {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("🤖 AI INTEGRATION TEST SUMMARY")
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
    base_url = "https://deps-preview-2.preview.emergentagent.com"
    
    print(f"Testing AI Integration at: {base_url}")
    
    # Initialize and run tests
    tester = AIIntegrationTester(base_url)
    results = tester.run_ai_integration_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()