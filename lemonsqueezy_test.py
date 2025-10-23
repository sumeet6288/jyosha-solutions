#!/usr/bin/env python3
"""
Focused Lemon Squeezy Subscription Test Suite
Tests all Lemon Squeezy endpoints with detailed verification
"""

import requests
import json
import time
from typing import Dict, Any

class LemonSqueezyTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
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
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)
    
    def test_plans_endpoint(self):
        """Test GET /api/lemonsqueezy/plans - Should return available subscription plans"""
        print("\n🔍 Testing Plans Endpoint...")
        try:
            response = self.make_request('GET', '/api/lemonsqueezy/plans')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                plans = data.get('plans', [])
                
                print(f"   📋 Found {len(plans)} plans")
                
                # Detailed plan verification
                expected_plans = {'starter', 'professional'}
                found_plans = set()
                
                for plan in plans:
                    plan_id = plan.get('id')
                    found_plans.add(plan_id)
                    
                    print(f"   📦 Plan: {plan.get('name')} ({plan_id})")
                    print(f"      💰 Price: {plan.get('price')} {plan.get('currency')}")
                    print(f"      📅 Interval: {plan.get('interval')}")
                    print(f"      🔢 Variant ID: {plan.get('variant_id')}")
                    print(f"      ✨ Features: {len(plan.get('features', []))} items")
                    
                    # Verify required fields
                    required_fields = ['id', 'name', 'price', 'currency', 'interval', 'variant_id', 'features']
                    missing_fields = [field for field in required_fields if field not in plan]
                    if missing_fields:
                        print(f"      ⚠️  Missing fields: {missing_fields}")
                
                # Check if all expected plans are present
                missing_plans = expected_plans - found_plans
                extra_plans = found_plans - expected_plans
                
                success = len(missing_plans) == 0
                message = f"Plans: {', '.join(found_plans)}"
                if missing_plans:
                    message += f" | Missing: {', '.join(missing_plans)}"
                if extra_plans:
                    message += f" | Extra: {', '.join(extra_plans)}"
                
                # Verify specific plan details
                starter_plan = next((p for p in plans if p.get('id') == 'starter'), None)
                professional_plan = next((p for p in plans if p.get('id') == 'professional'), None)
                
                if starter_plan:
                    if starter_plan.get('variant_id') != '1052931':
                        success = False
                        message += " | Starter variant ID mismatch"
                    if starter_plan.get('price') != 150:
                        success = False
                        message += " | Starter price mismatch"
                
                if professional_plan:
                    if professional_plan.get('variant_id') != '1052933':
                        success = False
                        message += " | Professional variant ID mismatch"
                    if professional_plan.get('price') != 499:
                        success = False
                        message += " | Professional price mismatch"
                
                self.log_result("Plans Endpoint", success, message)
            else:
                error_msg = response.text
                self.log_result("Plans Endpoint", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Plans Endpoint", False, f"Exception: {str(e)}")
    
    def test_subscription_status(self):
        """Test GET /api/lemonsqueezy/subscription/status - Should return subscription status"""
        print("\n🔍 Testing Subscription Status...")
        try:
            response = self.make_request('GET', '/api/lemonsqueezy/subscription/status')
            success = response.status_code == 200
            
            if success:
                data = response.json()
                print(f"   📊 Subscription Status Response:")
                print(f"      🔒 Has Subscription: {data.get('has_subscription', 'N/A')}")
                print(f"      📋 Plan: {data.get('plan', 'N/A')}")
                print(f"      ⚡ Status: {data.get('status', 'N/A')}")
                
                if data.get('has_subscription'):
                    print(f"      🔄 Renews At: {data.get('renews_at', 'N/A')}")
                    print(f"      ⏰ Ends At: {data.get('ends_at', 'N/A')}")
                    print(f"      🆔 Subscription ID: {data.get('subscription_id', 'N/A')}")
                
                required_fields = ['has_subscription', 'plan', 'status']
                missing_fields = [field for field in required_fields if field not in data]
                
                success = len(missing_fields) == 0
                message = f"Plan: {data.get('plan')}, Status: {data.get('status')}"
                if missing_fields:
                    message += f" | Missing fields: {missing_fields}"
                
                self.log_result("Subscription Status", success, message)
            else:
                error_msg = response.text
                self.log_result("Subscription Status", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Subscription Status", False, f"Exception: {str(e)}")
    
    def test_checkout_creation(self, plan_name: str, expected_variant: str):
        """Test checkout creation for a specific plan"""
        print(f"\n🔍 Testing Checkout Creation ({plan_name.title()})...")
        try:
            checkout_data = {
                "plan": plan_name,
                "user_id": "demo-user-123",
                "user_email": "demo@botsmith.com"
            }
            
            print(f"   📤 Request Data:")
            print(f"      📋 Plan: {checkout_data['plan']}")
            print(f"      👤 User ID: {checkout_data['user_id']}")
            print(f"      📧 Email: {checkout_data['user_email']}")
            
            response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                checkout_url = data.get('checkout_url', '')
                message = data.get('message', '')
                
                print(f"   📥 Response Data:")
                print(f"      💬 Message: {message}")
                print(f"      🔗 Checkout URL: {checkout_url[:80]}...")
                
                # Verify checkout URL is valid Lemon Squeezy URL
                url_checks = {
                    'https': checkout_url.startswith('https://'),
                    'lemonsqueezy_domain': 'lemonsqueezy.com' in checkout_url,
                    'not_empty': checkout_url != '',
                    'checkout_path': '/checkout/' in checkout_url
                }
                
                print(f"   🔍 URL Validation:")
                for check, result in url_checks.items():
                    status = "✅" if result else "❌"
                    print(f"      {status} {check}: {result}")
                
                all_checks_pass = all(url_checks.values())
                success = all_checks_pass and 'Checkout created successfully' in message
                
                result_message = f"URL valid: {all_checks_pass}, Message: {message}"
                
                self.log_result(f"Checkout Creation ({plan_name.title()})", success, result_message)
            else:
                error_msg = response.text
                print(f"   ❌ Error Response: {error_msg}")
                self.log_result(f"Checkout Creation ({plan_name.title()})", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result(f"Checkout Creation ({plan_name.title()})", False, f"Exception: {str(e)}")
    
    def test_invalid_plan_checkout(self):
        """Test checkout creation with invalid plan (should fail)"""
        print(f"\n🔍 Testing Invalid Plan Checkout...")
        try:
            checkout_data = {
                "plan": "invalid_plan_name",
                "user_id": "demo-user-123",
                "user_email": "demo@botsmith.com"
            }
            
            print(f"   📤 Request Data (Invalid):")
            print(f"      📋 Plan: {checkout_data['plan']} (should be invalid)")
            print(f"      👤 User ID: {checkout_data['user_id']}")
            print(f"      📧 Email: {checkout_data['user_email']}")
            
            response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
            
            # Should return 400 for invalid plan
            success = response.status_code == 400
            
            print(f"   📥 Response:")
            print(f"      📊 Status Code: {response.status_code} (expected: 400)")
            print(f"      💬 Response: {response.text}")
            
            if success:
                self.log_result("Invalid Plan Checkout", success, "Correctly rejected invalid plan with 400 status")
            else:
                self.log_result("Invalid Plan Checkout", False, f"Expected 400, got {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Invalid Plan Checkout", False, f"Exception: {str(e)}")
    
    def test_missing_fields_checkout(self):
        """Test checkout creation with missing required fields"""
        print(f"\n🔍 Testing Missing Fields Checkout...")
        
        test_cases = [
            {"plan": "starter", "user_id": "demo-user-123"},  # Missing email
            {"plan": "starter", "user_email": "demo@botsmith.com"},  # Missing user_id
            {"user_id": "demo-user-123", "user_email": "demo@botsmith.com"}  # Missing plan
        ]
        
        for i, checkout_data in enumerate(test_cases, 1):
            try:
                missing_field = "email" if "user_email" not in checkout_data else "user_id" if "user_id" not in checkout_data else "plan"
                print(f"   📤 Test Case {i} - Missing {missing_field}:")
                print(f"      📋 Data: {checkout_data}")
                
                response = self.make_request('POST', '/api/lemonsqueezy/checkout/create', json=checkout_data)
                
                # Should return 422 for validation error
                success = response.status_code == 422
                
                print(f"      📊 Status Code: {response.status_code} (expected: 422)")
                
                if success:
                    self.log_result(f"Missing {missing_field} Checkout", success, f"Correctly rejected missing {missing_field} with 422 status")
                else:
                    self.log_result(f"Missing {missing_field} Checkout", False, f"Expected 422, got {response.status_code}: {response.text}")
            except Exception as e:
                self.log_result(f"Missing {missing_field} Checkout", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all Lemon Squeezy tests"""
        print("🍋 Starting Lemon Squeezy Subscription Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test sequence
        test_methods = [
            self.test_plans_endpoint,
            self.test_subscription_status,
            lambda: self.test_checkout_creation("starter", "1052931"),
            lambda: self.test_checkout_creation("professional", "1052933"),
            self.test_invalid_plan_checkout,
            self.test_missing_fields_checkout
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__ if hasattr(test_method, '__name__') else 'test'}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"CRITICAL ERROR - {str(e)}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 LEMON SQUEEZY TEST SUMMARY")
        print("=" * 80)
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
    base_url = "https://quick-preview-deps.preview.emergentagent.com"
    
    print(f"Testing Lemon Squeezy API at: {base_url}")
    
    # Initialize and run tests
    tester = LemonSqueezyTester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()