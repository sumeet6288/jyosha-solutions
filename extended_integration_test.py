#!/usr/bin/env python3
"""
Extended Integration Management API Test Suite
Tests integration APIs with more comprehensive scenarios
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class ExtendedIntegrationTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_chatbot_id = None
        self.created_integrations = []
        
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
        
        # Use mock authentication
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
        """Get existing chatbot for testing"""
        try:
            response = self.make_request('GET', '/api/chatbots')
            if response.status_code == 200:
                chatbots = response.json()
                if chatbots and len(chatbots) > 0:
                    self.test_chatbot_id = chatbots[0]['id']
                    self.log_result("Setup Test Chatbot", True, f"Using chatbot: {self.test_chatbot_id}")
                    return
            
            self.log_result("Setup Test Chatbot", False, "No chatbots available")
        except Exception as e:
            self.log_result("Setup Test Chatbot", False, f"Exception: {str(e)}")
    
    def test_create_multiple_integration_types(self):
        """Test creating different types of integrations"""
        if not self.test_chatbot_id:
            self.log_result("Create Multiple Integration Types", False, "No chatbot ID available")
            return
        
        integration_types = [
            {
                "type": "slack",
                "credentials": {"bot_token": "xoxb-test-slack-token"},
                "metadata": {"workspace": "Test Workspace"}
            },
            {
                "type": "telegram", 
                "credentials": {"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"},
                "metadata": {"bot_username": "test_bot"}
            },
            {
                "type": "discord",
                "credentials": {"bot_token": "test-discord-token"},
                "metadata": {"server_name": "Test Server"}
            },
            {
                "type": "whatsapp",
                "credentials": {"api_key": "test-api-key", "phone_number": "+1234567890"},
                "metadata": {"business_name": "Test Business"}
            },
            {
                "type": "webchat",
                "credentials": {},
                "metadata": {"theme": "light"}
            }
        ]
        
        success_count = 0
        for integration in integration_types:
            try:
                payload = {
                    "integration_type": integration["type"],
                    "credentials": integration["credentials"],
                    "metadata": integration["metadata"]
                }
                
                response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}', json=payload)
                if response.status_code == 200:
                    data = response.json()
                    integration_id = data.get('id')
                    if integration_id:
                        self.created_integrations.append(integration_id)
                        success_count += 1
                        print(f"    Created {integration['type']}: {integration_id}")
                
            except Exception as e:
                print(f"    Failed to create {integration['type']}: {str(e)}")
        
        success = success_count == len(integration_types)
        self.log_result("Create Multiple Integration Types", success, f"Created {success_count}/{len(integration_types)} integrations")
    
    def test_connection_testing_all_types(self):
        """Test connection testing for all integration types"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Test All Connection Types", False, "No integrations available")
            return
        
        # Get all integrations
        response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
        if response.status_code != 200:
            self.log_result("Test All Connection Types", False, "Failed to get integrations")
            return
        
        integrations = response.json()
        success_count = 0
        
        for integration in integrations:
            try:
                integration_id = integration['id']
                integration_type = integration['integration_type']
                
                response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/test')
                if response.status_code == 200:
                    data = response.json()
                    success_count += 1
                    print(f"    {integration_type}: {data.get('message', 'No message')}")
                
            except Exception as e:
                print(f"    Failed to test {integration_type}: {str(e)}")
        
        success = success_count == len(integrations)
        self.log_result("Test All Connection Types", success, f"Tested {success_count}/{len(integrations)} integrations")
    
    def test_bulk_toggle_operations(self):
        """Test toggling multiple integrations"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Bulk Toggle Operations", False, "No integrations available")
            return
        
        # Get all integrations
        response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
        if response.status_code != 200:
            self.log_result("Bulk Toggle Operations", False, "Failed to get integrations")
            return
        
        integrations = response.json()
        success_count = 0
        
        # Enable all integrations
        for integration in integrations:
            try:
                integration_id = integration['id']
                response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/toggle')
                if response.status_code == 200:
                    data = response.json()
                    if data.get('enabled') == True:
                        success_count += 1
            except Exception as e:
                print(f"    Failed to enable integration: {str(e)}")
        
        # Disable all integrations
        for integration in integrations:
            try:
                integration_id = integration['id']
                response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}/{integration_id}/toggle')
                if response.status_code == 200:
                    data = response.json()
                    if data.get('enabled') == False:
                        success_count += 1
            except Exception as e:
                print(f"    Failed to disable integration: {str(e)}")
        
        expected_operations = len(integrations) * 2  # Enable + Disable for each
        success = success_count == expected_operations
        self.log_result("Bulk Toggle Operations", success, f"Completed {success_count}/{expected_operations} toggle operations")
    
    def test_integration_logs_detailed(self):
        """Test detailed integration logs functionality"""
        if not self.test_chatbot_id:
            self.log_result("Integration Logs Detailed", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}/logs?limit=100')
            success = response.status_code == 200
            
            if success:
                logs = response.json()
                success = isinstance(logs, list) and len(logs) > 0
                
                if success:
                    # Verify log structure and content
                    log_types = set()
                    statuses = set()
                    
                    for log in logs:
                        required_fields = ['id', 'chatbot_id', 'integration_id', 'integration_type', 
                                         'event_type', 'status', 'message', 'timestamp']
                        if not all(field in log for field in required_fields):
                            success = False
                            break
                        
                        log_types.add(log['event_type'])
                        statuses.add(log['status'])
                    
                    message = f"Found {len(logs)} logs with event types: {', '.join(log_types)} and statuses: {', '.join(statuses)}"
                    self.log_result("Integration Logs Detailed", success, message)
                else:
                    self.log_result("Integration Logs Detailed", False, "No logs found")
            else:
                self.log_result("Integration Logs Detailed", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Integration Logs Detailed", False, f"Exception: {str(e)}")
    
    def test_update_existing_integration(self):
        """Test updating an existing integration"""
        if not self.test_chatbot_id or not self.created_integrations:
            self.log_result("Update Existing Integration", False, "No integrations available")
            return
        
        try:
            # Create a Slack integration first
            payload = {
                "integration_type": "slack",
                "credentials": {"bot_token": "xoxb-original-token"},
                "metadata": {"workspace": "Original Workspace"}
            }
            
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}', json=payload)
            if response.status_code != 200:
                self.log_result("Update Existing Integration", False, "Failed to create initial integration")
                return
            
            # Update the same integration type with new credentials
            updated_payload = {
                "integration_type": "slack",
                "credentials": {"bot_token": "xoxb-updated-token"},
                "metadata": {"workspace": "Updated Workspace"}
            }
            
            response = self.make_request('POST', f'/api/integrations/{self.test_chatbot_id}', json=updated_payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('integration_type') == 'slack' and data.get('has_credentials') == True
                self.log_result("Update Existing Integration", success, f"Updated integration: {data.get('id')}")
            else:
                self.log_result("Update Existing Integration", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Update Existing Integration", False, f"Exception: {str(e)}")
    
    def test_error_handling(self):
        """Test various error conditions"""
        error_tests = [
            {
                "name": "Invalid Integration Type",
                "endpoint": f"/api/integrations/{self.test_chatbot_id}",
                "method": "POST",
                "payload": {"integration_type": "invalid_type", "credentials": {}},
                "expected_status": 422
            },
            {
                "name": "Missing Credentials",
                "endpoint": f"/api/integrations/{self.test_chatbot_id}",
                "method": "POST", 
                "payload": {"integration_type": "slack"},
                "expected_status": 422
            },
            {
                "name": "Non-existent Chatbot",
                "endpoint": f"/api/integrations/{str(uuid.uuid4())}",
                "method": "GET",
                "expected_status": 404
            },
            {
                "name": "Non-existent Integration",
                "endpoint": f"/api/integrations/{self.test_chatbot_id}/{str(uuid.uuid4())}/test",
                "method": "POST",
                "expected_status": 404
            }
        ]
        
        success_count = 0
        for test in error_tests:
            try:
                kwargs = {}
                if test.get("payload"):
                    kwargs["json"] = test["payload"]
                
                response = self.make_request(test["method"], test["endpoint"], **kwargs)
                if response.status_code == test["expected_status"]:
                    success_count += 1
                    print(f"    {test['name']}: ✅ Got expected {test['expected_status']}")
                else:
                    print(f"    {test['name']}: ❌ Got {response.status_code}, expected {test['expected_status']}")
                    
            except Exception as e:
                print(f"    {test['name']}: ❌ Exception: {str(e)}")
        
        success = success_count == len(error_tests)
        self.log_result("Error Handling", success, f"Passed {success_count}/{len(error_tests)} error tests")
    
    def cleanup_all_integrations(self):
        """Clean up all test integrations"""
        if not self.test_chatbot_id:
            return
        
        try:
            response = self.make_request('GET', f'/api/integrations/{self.test_chatbot_id}')
            if response.status_code == 200:
                integrations = response.json()
                cleanup_count = 0
                
                for integration in integrations:
                    try:
                        integration_id = integration['id']
                        response = self.make_request('DELETE', f'/api/integrations/{self.test_chatbot_id}/{integration_id}')
                        if response.status_code == 200:
                            cleanup_count += 1
                            print(f"  Cleaned up {integration['integration_type']}: {integration_id}")
                    except Exception as e:
                        print(f"  Failed to cleanup {integration_id}: {str(e)}")
                
                self.log_result("Cleanup All Integrations", True, f"Cleaned up {cleanup_count} integrations")
        except Exception as e:
            self.log_result("Cleanup All Integrations", False, f"Exception: {str(e)}")
    
    def run_extended_tests(self):
        """Run all extended integration tests"""
        print("🚀 Starting Extended Integration Management API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence
        test_methods = [
            self.setup_test_chatbot,
            self.test_create_multiple_integration_types,
            self.test_connection_testing_all_types,
            self.test_bulk_toggle_operations,
            self.test_integration_logs_detailed,
            self.test_update_existing_integration,
            self.test_error_handling,
            self.cleanup_all_integrations
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"{test_method.__name__}: CRITICAL ERROR - {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 EXTENDED INTEGRATION TEST SUMMARY")
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
    base_url = "https://setup-snapshot.preview.emergentagent.com"
    
    print(f"Testing Extended Integration Management APIs at: {base_url}")
    
    # Initialize and run tests
    tester = ExtendedIntegrationTester(base_url)
    results = tester.run_extended_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()