#!/usr/bin/env python3
"""
Backend Testing Suite for Chatbot Builder - Widget Settings Focus
Testing the Appearance tab Widget Settings functionality as requested.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://speedy-install-1.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class WidgetSettingsTestSuite:
    def __init__(self):
        self.session = None
        self.test_chatbot_id = None
        self.test_results = []
        
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
            
    async def create_test_chatbot(self) -> str:
        """Create a test chatbot for widget settings testing"""
        try:
            chatbot_data = {
                "name": "Widget Settings Test Bot",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "temperature": 0.7,
                "instructions": "You are a test chatbot for widget settings.",
                "welcome_message": "Hello! I'm testing widget settings.",
                # Default widget settings
                "widget_position": "bottom-right",
                "widget_theme": "light", 
                "widget_size": "medium",
                "auto_expand": False
            }
            
            async with self.session.post(f"{API_BASE}/chatbots", json=chatbot_data) as response:
                if response.status == 201:
                    result = await response.json()
                    chatbot_id = result["id"]
                    self.log_test("Create test chatbot", True, f"Created chatbot with ID: {chatbot_id}")
                    return chatbot_id
                else:
                    error_text = await response.text()
                    self.log_test("Create test chatbot", False, f"Status: {response.status}, Error: {error_text}")
                    return None
                    
        except Exception as e:
            self.log_test("Create test chatbot", False, f"Exception: {str(e)}")
            return None
            
    async def test_widget_position_updates(self, chatbot_id: str):
        """Test all widget position options"""
        positions = ["bottom-right", "bottom-left", "top-right", "top-left"]
        
        for position in positions:
            try:
                update_data = {"widget_position": position}
                
                async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("widget_position") == position:
                            self.log_test(f"Widget position: {position}", True, f"Successfully updated to {position}")
                        else:
                            self.log_test(f"Widget position: {position}", False, f"Expected {position}, got {result.get('widget_position')}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Widget position: {position}", False, f"Status: {response.status}, Error: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Widget position: {position}", False, f"Exception: {str(e)}")
                
    async def test_widget_theme_updates(self, chatbot_id: str):
        """Test all widget theme options"""
        themes = ["light", "dark", "auto"]
        
        for theme in themes:
            try:
                update_data = {"widget_theme": theme}
                
                async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("widget_theme") == theme:
                            self.log_test(f"Widget theme: {theme}", True, f"Successfully updated to {theme}")
                        else:
                            self.log_test(f"Widget theme: {theme}", False, f"Expected {theme}, got {result.get('widget_theme')}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Widget theme: {theme}", False, f"Status: {response.status}, Error: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Widget theme: {theme}", False, f"Exception: {str(e)}")
                
    async def test_widget_size_updates(self, chatbot_id: str):
        """Test all widget size options"""
        sizes = ["small", "medium", "large"]
        
        for size in sizes:
            try:
                update_data = {"widget_size": size}
                
                async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("widget_size") == size:
                            self.log_test(f"Widget size: {size}", True, f"Successfully updated to {size}")
                        else:
                            self.log_test(f"Widget size: {size}", False, f"Expected {size}, got {result.get('widget_size')}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Widget size: {size}", False, f"Status: {response.status}, Error: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Widget size: {size}", False, f"Exception: {str(e)}")
                
    async def test_auto_expand_toggle(self, chatbot_id: str):
        """Test auto-expand widget checkbox functionality"""
        auto_expand_values = [True, False]
        
        for auto_expand in auto_expand_values:
            try:
                update_data = {"auto_expand": auto_expand}
                
                async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("auto_expand") == auto_expand:
                            self.log_test(f"Auto-expand: {auto_expand}", True, f"Successfully updated to {auto_expand}")
                        else:
                            self.log_test(f"Auto-expand: {auto_expand}", False, f"Expected {auto_expand}, got {result.get('auto_expand')}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Auto-expand: {auto_expand}", False, f"Status: {response.status}, Error: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Auto-expand: {auto_expand}", False, f"Exception: {str(e)}")
                
    async def test_combined_widget_settings_update(self, chatbot_id: str):
        """Test updating multiple widget settings at once (Save Appearance functionality)"""
        try:
            # Test comprehensive widget settings update
            update_data = {
                "widget_position": "top-left",
                "widget_theme": "dark", 
                "widget_size": "large",
                "auto_expand": True,
                # Also test other appearance settings
                "primary_color": "#ff6b6b",
                "secondary_color": "#4ecdc4",
                "welcome_message": "Updated welcome message for widget testing!"
            }
            
            async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify all widget settings were updated
                    checks = [
                        ("widget_position", "top-left"),
                        ("widget_theme", "dark"),
                        ("widget_size", "large"),
                        ("auto_expand", True),
                        ("primary_color", "#ff6b6b"),
                        ("secondary_color", "#4ecdc4"),
                        ("welcome_message", "Updated welcome message for widget testing!")
                    ]
                    
                    all_correct = True
                    details = []
                    
                    for field, expected in checks:
                        actual = result.get(field)
                        if actual == expected:
                            details.append(f"{field}: ✓ {expected}")
                        else:
                            details.append(f"{field}: ✗ Expected {expected}, got {actual}")
                            all_correct = False
                            
                    self.log_test("Combined widget settings update", all_correct, "; ".join(details))
                else:
                    error_text = await response.text()
                    self.log_test("Combined widget settings update", False, f"Status: {response.status}, Error: {error_text}")
                    
        except Exception as e:
            self.log_test("Combined widget settings update", False, f"Exception: {str(e)}")
            
    async def test_database_persistence(self, chatbot_id: str):
        """Test that widget settings persist in database by fetching chatbot again"""
        try:
            # First, set specific widget settings
            update_data = {
                "widget_position": "bottom-left",
                "widget_theme": "auto",
                "widget_size": "small", 
                "auto_expand": False
            }
            
            # Update the chatbot
            async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                if response.status != 200:
                    self.log_test("Database persistence setup", False, f"Failed to update chatbot: {response.status}")
                    return
                    
            # Now fetch the chatbot to verify persistence
            async with self.session.get(f"{API_BASE}/chatbots/{chatbot_id}") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify the settings persisted
                    checks = [
                        ("widget_position", "bottom-left"),
                        ("widget_theme", "auto"),
                        ("widget_size", "small"),
                        ("auto_expand", False)
                    ]
                    
                    all_persisted = True
                    details = []
                    
                    for field, expected in checks:
                        actual = result.get(field)
                        if actual == expected:
                            details.append(f"{field}: ✓ {expected}")
                        else:
                            details.append(f"{field}: ✗ Expected {expected}, got {actual}")
                            all_persisted = False
                            
                    self.log_test("Database persistence verification", all_persisted, "; ".join(details))
                else:
                    error_text = await response.text()
                    self.log_test("Database persistence verification", False, f"Status: {response.status}, Error: {error_text}")
                    
        except Exception as e:
            self.log_test("Database persistence verification", False, f"Exception: {str(e)}")
            
    async def test_public_chat_widget_reflection(self, chatbot_id: str):
        """Test if public chat page reflects widget settings"""
        try:
            # Set distinctive widget settings
            update_data = {
                "widget_position": "top-right",
                "widget_theme": "light",
                "widget_size": "large",
                "auto_expand": True,
                "primary_color": "#9333ea",
                "secondary_color": "#a855f7"
            }
            
            # Update the chatbot
            async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                if response.status != 200:
                    self.log_test("Public chat widget setup", False, f"Failed to update chatbot: {response.status}")
                    return
                    
            # Test public chatbot info endpoint (used by public chat page)
            async with self.session.get(f"{API_BASE}/public/chatbot/{chatbot_id}") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify widget settings are available for public chat
                    expected_fields = ["primary_color", "secondary_color", "widget_theme"]
                    available_fields = []
                    missing_fields = []
                    
                    for field in expected_fields:
                        if field in result:
                            available_fields.append(f"{field}: {result[field]}")
                        else:
                            missing_fields.append(field)
                            
                    if not missing_fields:
                        self.log_test("Public chat widget reflection", True, f"Widget settings available: {', '.join(available_fields)}")
                    else:
                        self.log_test("Public chat widget reflection", False, f"Missing fields: {', '.join(missing_fields)}")
                        
                elif response.status == 404:
                    self.log_test("Public chat widget reflection", False, "Public chat endpoint not found - may not be implemented")
                else:
                    error_text = await response.text()
                    self.log_test("Public chat widget reflection", False, f"Status: {response.status}, Error: {error_text}")
                    
        except Exception as e:
            self.log_test("Public chat widget reflection", False, f"Exception: {str(e)}")
            
    async def test_invalid_widget_settings(self, chatbot_id: str):
        """Test validation of invalid widget settings"""
        invalid_tests = [
            {"widget_position": "invalid-position", "expected_error": "widget_position validation"},
            {"widget_theme": "invalid-theme", "expected_error": "widget_theme validation"},
            {"widget_size": "invalid-size", "expected_error": "widget_size validation"},
            {"auto_expand": "not-boolean", "expected_error": "auto_expand validation"}
        ]
        
        for test_case in invalid_tests:
            try:
                field = list(test_case.keys())[0]  # Get the field being tested
                invalid_value = test_case[field]
                expected_error = test_case["expected_error"]
                
                update_data = {field: invalid_value}
                
                async with self.session.put(f"{API_BASE}/chatbots/{chatbot_id}", json=update_data) as response:
                    if response.status == 422:  # Validation error expected
                        self.log_test(f"Invalid {field} validation", True, f"Correctly rejected invalid value: {invalid_value}")
                    elif response.status == 200:
                        self.log_test(f"Invalid {field} validation", False, f"Should have rejected invalid value: {invalid_value}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Invalid {field} validation", False, f"Unexpected status {response.status}: {error_text}")
                        
            except Exception as e:
                self.log_test(f"Invalid {field} validation", False, f"Exception: {str(e)}")
                
    async def cleanup_test_chatbot(self, chatbot_id: str):
        """Clean up test chatbot"""
        try:
            async with self.session.delete(f"{API_BASE}/chatbots/{chatbot_id}") as response:
                if response.status == 204:
                    self.log_test("Cleanup test chatbot", True, f"Successfully deleted chatbot {chatbot_id}")
                else:
                    error_text = await response.text()
                    self.log_test("Cleanup test chatbot", False, f"Status: {response.status}, Error: {error_text}")
                    
        except Exception as e:
            self.log_test("Cleanup test chatbot", False, f"Exception: {str(e)}")
            
    async def get_existing_chatbot(self) -> str:
        """Get existing chatbot for testing"""
        try:
            async with self.session.get(f"{API_BASE}/chatbots") as response:
                if response.status == 200:
                    chatbots = await response.json()
                    if chatbots:
                        chatbot_id = chatbots[0]["id"]
                        self.log_test("Get existing chatbot", True, f"Using existing chatbot: {chatbot_id}")
                        return chatbot_id
                    else:
                        self.log_test("Get existing chatbot", False, "No chatbots found")
                        return None
                else:
                    error_text = await response.text()
                    self.log_test("Get existing chatbot", False, f"Status: {response.status}, Error: {error_text}")
                    return None
        except Exception as e:
            self.log_test("Get existing chatbot", False, f"Exception: {str(e)}")
            return None

    async def run_all_tests(self):
        """Run all widget settings tests"""
        print("🚀 Starting Widget Settings Test Suite")
        print(f"Backend URL: {API_BASE}")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Get existing chatbot (avoid plan limits)
            chatbot_id = await self.get_existing_chatbot()
            if not chatbot_id:
                print("❌ No existing chatbot found. Cannot run tests.")
                return
                
            self.test_chatbot_id = chatbot_id
            
            # Run all widget settings tests
            await self.test_widget_position_updates(chatbot_id)
            await self.test_widget_theme_updates(chatbot_id)
            await self.test_widget_size_updates(chatbot_id)
            await self.test_auto_expand_toggle(chatbot_id)
            await self.test_combined_widget_settings_update(chatbot_id)
            await self.test_database_persistence(chatbot_id)
            await self.test_public_chat_widget_reflection(chatbot_id)
            await self.test_invalid_widget_settings(chatbot_id)
            
            # Skip cleanup for existing chatbot
            print("ℹ️  Skipping cleanup - using existing chatbot")
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()
        
    def print_test_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 WIDGET SETTINGS TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
                
        # Show critical widget settings status
        print(f"\n🎯 WIDGET SETTINGS FUNCTIONALITY:")
        widget_tests = [
            "Widget position: bottom-right", "Widget position: bottom-left", 
            "Widget position: top-right", "Widget position: top-left",
            "Widget theme: light", "Widget theme: dark", "Widget theme: auto",
            "Widget size: small", "Widget size: medium", "Widget size: large",
            "Auto-expand: True", "Auto-expand: False",
            "Combined widget settings update", "Database persistence verification"
        ]
        
        widget_results = [r for r in self.test_results if r["test"] in widget_tests]
        widget_passed = sum(1 for r in widget_results if r["success"])
        
        if widget_passed == len(widget_results) and len(widget_results) > 0:
            print("   ✅ All core widget settings functionality working")
        else:
            print(f"   ❌ Widget settings issues found ({widget_passed}/{len(widget_results)} passed)")

async def main():
    """Main test execution"""
    test_suite = WidgetSettingsTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())