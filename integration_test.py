#!/usr/bin/env python3
"""
Integration Management API Test Suite
Tests all integration management endpoints systematically
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class IntegrationAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.test_chatbot_id = None
        self.created_integrations = []  # Track created integrations for cleanup
        
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
        
        # Use mock authentication as requested
        headers['X-User-ID'] = 'demo-user-123'
        headers['X-User-Email'] = 'demo@botsmith.com'
        headers['X-User-Name'] = 'Demo User'
        
        kwargs['headers'] = headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"  {method} {endpoint} -> {response.status_code}")
            return response
        except Exception as e:
            print(f"  {method} {endpoint} -> ERROR: {str(e)}")
            raise
    
    def setup_test_chatbot(self):
        """Create or get a test chatbot for integration testing"""
        try:
            # First try to get existing chatbots
            response = self.make_request('GET', '/api/chatbots')
            if response.status_code == 200:
                chatbots = response.json()
                if chatbots and len(chatbots) > 0:
                    self.test_chatbot_id = chatbots[0]['id']
                    self.log_result("Setup Test Chatbot", True, f"Using existing chatbot: {self.test_chatbot_id}")
                    return
            
            # Create a new chatbot if none exist
            payload = {
                "name": "Integration Test Chatbot",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "temperature": 0.7,
                "instructions": "You are a test chatbot for integration testing.",
                "welcome_message": "Hello! I'm a test chatbot for integrations."
            }
            
            response = self.make_request('POST', '/api/chatbots', json=payload)
            if response.status_code == 201:
                data = response.json()
                self.test_chatbot_id = data.get('id')
                self.log_result("Setup Test Chatbot", True, f"Created new chatbot: {self.test_chatbot_id}")
            else:
                self.log_result("Setup Test Chatbot", False, f"Failed to create chatbot: {response.status_code}")
                
        except Exception as e:
            self.log_result("Setup Test Chatbot", False, f"Exception: {str(e)}")
    
    def test_get_integrations_empty(self):
        """Test GET /api/integrations/{chatbot_id} - Should return empty array initially"""
        if not self.test_chatbot_id:
            self.log_result("Get Integrations (Empty)", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) == 0
                self.log_result("Get Integrations (Empty)", success, f"Found {len(data)} integrations (expected 0)")
            else:
                error_msg = response.text
                self.log_result("Get Integrations (Empty)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Integrations (Empty)", False, f"Exception: {str(e)}")
    
    def test_create_slack_integration(self):
        """Test POST /api/integrations/{chatbot_id} - Create Slack integration"""
        if not self.test_chatbot_id:
            self.log_result("Create Slack Integration", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "integration_type": "slack",
                "credentials": {
                    "bot_token": "xoxb-test-slack-bot-token-for-testing"
                },
                "metadata": {
                    "workspace_name": "Test Workspace"
                }
            }
            
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                integration_id = data.get('id')
                success = (
                    bool(integration_id) and 
                    data.get('integration_type') == 'slack' and
                    data.get('chatbot_id') == self.test_chatbot_id and
                    data.get('has_credentials') == True and
                    data.get('status') == 'pending'
                )
                if success:
                    self.created_integrations.append(integration_id)
                self.log_result("Create Slack Integration", success, f"Integration ID: {integration_id}")
            else:
                error_msg = response.text
                self.log_result("Create Slack Integration", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create Slack Integration", False, f"Exception: {str(e)}")
    
    def test_create_telegram_integration(self):
        """Test POST /api/integrations/{chatbot_id} - Create Telegram integration"""
        if not self.test_chatbot_id:
            self.log_result("Create Telegram Integration", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "integration_type": "telegram",
                "credentials": {
                    "bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
                },
                "metadata": {
                    "bot_username": "test_bot"
                }
            }
            
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                integration_id = data.get('id')
                success = (
                    bool(integration_id) and 
                    data.get('integration_type') == 'telegram' and
                    data.get('chatbot_id') == self.test_chatbot_id and
                    data.get('has_credentials') == True and
                    data.get('status') == 'pending'
                )
                if success:
                    self.created_integrations.append(integration_id)
                self.log_result("Create Telegram Integration", success, f"Integration ID: {integration_id}")
            else:
                error_msg = response.text
                self.log_result("Create Telegram Integration", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Create Telegram Integration", False, f"Exception: {str(e)}")
    
    def test_get_integrations_with_data(self):
        """Test GET /api/integrations/{chatbot_id} - Should return created integrations"""
        if not self.test_chatbot_id:
            self.log_result("Get Integrations (With Data)", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) >= 2  # Should have Slack and Telegram
                
                if success:
                    # Verify integration types
                    types = [integration.get('integration_type') for integration in data]
                    success = 'slack' in types and 'telegram' in types
                    
                self.log_result("Get Integrations (With Data)", success, f"Found {len(data)} integrations: {', '.join(types) if success else 'Invalid data'}")
            else:
                error_msg = response.text
                self.log_result("Get Integrations (With Data)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Integrations (With Data)", False, f"Exception: {str(e)}")
    
    def test_connection_with_invalid_credentials(self):
        """Test POST /api/integrations/{chatbot_id}/{integration_id}/test - Invalid credentials"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Test Connection (Invalid)", False, "No chatbot ID or integrations available")
            return
        
        try:
            integration_id = self.created_integrations[0]  # Use first created integration
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/test')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Should fail because we're using test credentials
                success = data.get('success') == False and 'message' in data
                self.log_result("Test Connection (Invalid)", success, f"Message: {data.get('message', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Test Connection (Invalid)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Test Connection (Invalid)", False, f"Exception: {str(e)}")
    
    def test_toggle_integration_enable(self):
        """Test POST /api/integrations/{chatbot_id}/{integration_id}/toggle - Enable integration"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Toggle Integration (Enable)", False, "No chatbot ID or integrations available")
            return
        
        try:
            integration_id = self.created_integrations[0]  # Use first created integration
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/toggle')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('success') == True and data.get('enabled') == True
                self.log_result("Toggle Integration (Enable)", success, f"Enabled: {data.get('enabled')}")
            else:
                error_msg = response.text
                self.log_result("Toggle Integration (Enable)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Toggle Integration (Enable)", False, f"Exception: {str(e)}")
    
    def test_toggle_integration_disable(self):
        """Test POST /api/integrations/{chatbot_id}/{integration_id}/toggle - Disable integration"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Toggle Integration (Disable)", False, "No chatbot ID or integrations available")
            return
        
        try:
            integration_id = self.created_integrations[0]  # Use first created integration
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/toggle')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('success') == True and data.get('enabled') == False
                self.log_result("Toggle Integration (Disable)", success, f"Enabled: {data.get('enabled')}")
            else:
                error_msg = response.text
                self.log_result("Toggle Integration (Disable)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Toggle Integration (Disable)", False, f"Exception: {str(e)}")
    
    def test_get_integration_logs(self):
        """Test GET /api/integrations/{chatbot_id}/logs - Get activity logs"""
        if not self.test_chatbot_id:
            self.log_result("Get Integration Logs", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}/logs')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list) and len(data) > 0
                
                if success:
                    # Verify log structure
                    log = data[0]
                    required_fields = ['id', 'chatbot_id', 'integration_id', 'integration_type', 'event_type', 'status', 'message', 'timestamp']
                    success = all(field in log for field in required_fields)
                    
                self.log_result("Get Integration Logs", success, f"Found {len(data)} logs")
            else:
                error_msg = response.text
                self.log_result("Get Integration Logs", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Get Integration Logs", False, f"Exception: {str(e)}")
    
    def test_delete_integration(self):
        """Test DELETE /api/integrations/{chatbot_id}/{integration_id} - Delete integration"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Delete Integration", False, "No chatbot ID or integrations available")
            return
        
        try:
            integration_id = self.created_integrations.pop()  # Remove and delete last integration
            response = self.make_request('DELETE', f'/api/integrations/{self.test_chatbot_id}/{integration_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('success') == True and 'message' in data
                self.log_result("Delete Integration", success, f"Message: {data.get('message', 'N/A')}")
            else:
                error_msg = response.text
                self.log_result("Delete Integration", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Delete Integration", False, f"Exception: {str(e)}")
    
    def test_verify_integration_deletion(self):
        """Test that deleted integration is no longer in the list"""
        if not self.test_chatbot_id:
            self.log_result("Verify Integration Deletion", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Should have one less integration now
                success = isinstance(data, list) and len(data) == len(self.created_integrations)
                self.log_result("Verify Integration Deletion", success, f"Remaining integrations: {len(data)}")
            else:
                error_msg = response.text
                self.log_result("Verify Integration Deletion", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Verify Integration Deletion", False, f"Exception: {str(e)}")
    
    def test_invalid_chatbot_id(self):
        """Test with invalid chatbot ID - should return 404"""
        try:
            invalid_id = str(uuid.uuid4())
            response = self.make_request('GET', f'/api/integrations/{invalid_id}')
            success = response.status_code == 404
            
            self.log_result("Invalid Chatbot ID", success, f"Status: {response.status_code} (expected 404)")
        except Exception as e:
            self.log_result("Invalid Chatbot ID", False, f"Exception: {str(e)}")
    
    def test_invalid_integration_id(self):
        """Test with invalid integration ID - should return 404"""
        if not self.test_chatbot_id:
            self.log_result("Invalid Integration ID", False, "No chatbot ID available")
            return
        
        try:
            invalid_id = str(uuid.uuid4())
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{invalid_id}/test')
            success = response.status_code == 404
            
            self.log_result("Invalid Integration ID", success, f"Status: {response.status_code} (expected 404)")
        except Exception as e:
            self.log_result("Invalid Integration ID", False, f"Exception: {str(e)}")
    
    def cleanup_remaining_integrations(self):
        """Clean up any remaining test integrations"""
        if not self.test_chatbot_id or not self.created_integrations:
            return
        
        for integration_id in self.created_integrations:
            try:
                response = self.make_request('DELETE', f'/api/integrations/{self.test_chatbot_id}/{integration_id}')
                if response.status_code == 200:
                    print(f"  Cleaned up integration: {integration_id}")
            except Exception as e:
                print(f"  Failed to cleanup integration {integration_id}: {str(e)}")
    
    def run_all_tests(self):
        """Run all integration tests in sequence"""
        print("🚀 Starting Integration Management API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence
        test_methods = [
            self.setup_test_chatbot,
            self.test_get_integrations_empty,
            self.test_create_slack_integration,
            self.test_create_telegram_integration,
            self.test_get_integrations_with_data,
            self.test_connection_with_invalid_credentials,
            self.test_toggle_integration_enable,
            self.test_toggle_integration_disable,
            self.test_get_integration_logs,
            self.test_delete_integration,
            self.test_verify_integration_deletion,
            self.test_invalid_chatbot_id,
            self.test_invalid_integration_id
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"{test_method.__name__}: CRITICAL ERROR - {str(e)}")
        
        # Cleanup
        self.cleanup_remaining_integrations()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
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
    base_url = "https://setup-snapshot.preview.emergentagent.com"
    
    print(f"Testing Integration Management APIs at: {base_url}")
    
    # Initialize and run tests
    tester = IntegrationAPITester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()