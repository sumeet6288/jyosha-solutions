#!/usr/bin/env python3
"""
Backend Testing Suite for Leads Management System
Comprehensive testing of leads management with plan-based access control.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://dep-install-demo.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class LeadsManagementTestSuite:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.mock_user_id = "demo-user-123"
        self.created_leads = []  # Track created leads for cleanup
        
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

    async def setup_test_environment(self):
        """Setup test environment by resetting to Free plan and cleaning up existing leads"""
        print("\n🔧 Setting up test environment...")
        
        # First, reset to Free plan to test limits
        try:
            upgrade_data = {"plan_id": "free"}
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    self.log_test("Reset to Free plan", True, "Reset to Free plan for testing")
                else:
                    self.log_test("Reset to Free plan", False, f"Failed to reset: {response.status}")
        except Exception as e:
            self.log_test("Reset to Free plan", False, f"Exception: {str(e)}")
        
        # Clean up any existing leads
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    leads = result.get("leads", [])
                    for lead in leads:
                        try:
                            await self.session.delete(f"{API_BASE}/leads/leads/{lead['id']}")
                        except:
                            pass
        except:
            pass

    async def test_free_plan_access_denied(self):
        """Test Free Plan User - Access Denied"""
        print("\n🚫 Testing Free Plan Access Denied...")
        
        # Test GET /api/leads/leads - Should return 0 max_leads and "Free" plan
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify response structure
                    expected_fields = ["leads", "total", "max_leads", "remaining", "plan_name"]
                    if all(field in result for field in expected_fields):
                        max_leads = result.get("max_leads", -1)
                        plan_name = result.get("plan_name", "")
                        
                        if max_leads == 0 and plan_name == "Free":
                            self.log_test("Free plan leads limit check", True, 
                                        f"Correct limits: max_leads={max_leads}, plan={plan_name}")
                        else:
                            self.log_test("Free plan leads limit check", False, 
                                        f"Wrong limits: max_leads={max_leads}, plan={plan_name}")
                    else:
                        missing = [f for f in expected_fields if f not in result]
                        self.log_test("Free plan leads limit check", False, 
                                    f"Missing fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("Free plan leads limit check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Free plan leads limit check", False, f"Exception: {str(e)}")
        
        # Test POST /api/leads/leads - Should fail with 403 error
        lead_data = {
            "name": "Test Lead",
            "email": "test@example.com",
            "company": "Test Company",
            "status": "active"
        }
        
        try:
            async with self.session.post(f"{API_BASE}/leads/leads", json=lead_data) as response:
                if response.status == 403:
                    result = await response.json()
                    detail = result.get("detail", {})
                    
                    if isinstance(detail, dict) and "message" in detail:
                        message = detail["message"]
                        if "limit of 0" in message.lower():
                            self.log_test("Free plan create lead blocked", True, 
                                        f"Correctly blocked: {message}")
                        else:
                            self.log_test("Free plan create lead blocked", False, 
                                        f"Wrong error message: {message}")
                    else:
                        self.log_test("Free plan create lead blocked", False, 
                                    f"Unexpected error format: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Free plan create lead blocked", False, 
                                f"Expected 403, got {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Free plan create lead blocked", False, f"Exception: {str(e)}")

    async def test_upgrade_to_starter_plan(self):
        """Test upgrading user to Starter plan"""
        print("\n⬆️ Testing Upgrade to Starter Plan...")
        
        # Test PUT /api/plans/upgrade with plan_id="starter"
        upgrade_data = {"plan_id": "starter"}
        
        try:
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify upgrade success
                    if "message" in result and "subscription" in result:
                        message = result["message"]
                        subscription = result["subscription"]
                        
                        if "starter" in message.lower():
                            self.log_test("Upgrade to Starter plan", True, 
                                        f"Successfully upgraded: {message}")
                            
                            # Verify subscription details
                            if subscription.get("plan_name") == "Starter":
                                self.log_test("Starter plan subscription verification", True, 
                                            f"Plan name correct: {subscription['plan_name']}")
                            else:
                                self.log_test("Starter plan subscription verification", False, 
                                            f"Wrong plan name: {subscription.get('plan_name')}")
                        else:
                            self.log_test("Upgrade to Starter plan", False, 
                                        f"Unexpected message: {message}")
                    else:
                        self.log_test("Upgrade to Starter plan", False, 
                                    f"Missing fields in response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade to Starter plan", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Upgrade to Starter plan", False, f"Exception: {str(e)}")
        
        # Verify plan change was successful by checking current subscription
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    result = await response.json()
                    plan = result.get("plan", {})
                    
                    if plan.get("name") == "Starter":
                        self.log_test("Verify Starter plan active", True, 
                                    f"Current plan: {plan['name']}")
                    else:
                        self.log_test("Verify Starter plan active", False, 
                                    f"Expected Starter, got: {plan.get('name')}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify Starter plan active", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify Starter plan active", False, f"Exception: {str(e)}")

    async def test_starter_plan_100_leads_limit(self):
        """Test Starter Plan User - 100 Leads Limit"""
        print("\n📊 Testing Starter Plan 100 Leads Limit...")
        
        # Test GET /api/leads/leads - Should return max_leads=100, plan_name="Starter"
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    max_leads = result.get("max_leads", -1)
                    plan_name = result.get("plan_name", "")
                    
                    if max_leads == 100 and plan_name == "Starter":
                        self.log_test("Starter plan limits check", True, 
                                    f"Correct limits: max_leads={max_leads}, plan={plan_name}")
                    else:
                        self.log_test("Starter plan limits check", False, 
                                    f"Wrong limits: max_leads={max_leads}, plan={plan_name}")
                else:
                    error_text = await response.text()
                    self.log_test("Starter plan limits check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Starter plan limits check", False, f"Exception: {str(e)}")
        
        # Test POST /api/leads/leads - Create a new lead successfully
        lead_data = {
            "name": "John Smith",
            "email": "john.smith@techcorp.com",
            "phone": "+1-555-0123",
            "company": "TechCorp Solutions",
            "status": "active",
            "notes": "Interested in enterprise chatbot solution"
        }
        
        try:
            async with self.session.post(f"{API_BASE}/leads/leads", json=lead_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get("success") and "lead" in result:
                        lead = result["lead"]
                        lead_id = lead.get("id")
                        self.created_leads.append(lead_id)
                        
                        # Verify all fields were saved properly
                        fields_correct = (
                            lead.get("name") == lead_data["name"] and
                            lead.get("email") == lead_data["email"] and
                            lead.get("phone") == lead_data["phone"] and
                            lead.get("company") == lead_data["company"] and
                            lead.get("status") == lead_data["status"] and
                            lead.get("notes") == lead_data["notes"]
                        )
                        
                        if fields_correct:
                            self.log_test("Create lead successfully", True, 
                                        f"Lead created with ID: {lead_id}")
                        else:
                            self.log_test("Create lead successfully", False, 
                                        f"Lead fields not saved correctly: {lead}")
                    else:
                        self.log_test("Create lead successfully", False, 
                                    f"Unexpected response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Create lead successfully", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Create lead successfully", False, f"Exception: {str(e)}")
        
        # Verify lead count increments correctly
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    total = result.get("total", 0)
                    leads = result.get("leads", [])
                    
                    if total == 1 and len(leads) == 1:
                        self.log_test("Lead count increment verification", True, 
                                    f"Count correctly shows {total} lead")
                    else:
                        self.log_test("Lead count increment verification", False, 
                                    f"Count mismatch: total={total}, leads_length={len(leads)}")
                else:
                    error_text = await response.text()
                    self.log_test("Lead count increment verification", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Lead count increment verification", False, f"Exception: {str(e)}")

    async def test_create_multiple_leads(self):
        """Test creating 5 more leads (total 6)"""
        print("\n📝 Testing Create Multiple Leads...")
        
        # Create 5 more leads with different statuses
        leads_data = [
            {
                "name": "Sarah Johnson",
                "email": "sarah.johnson@innovate.com",
                "company": "Innovate Inc",
                "status": "contacted",
                "notes": "Follow up scheduled for next week"
            },
            {
                "name": "Mike Chen",
                "email": "mike.chen@startup.io",
                "company": "Startup.io",
                "status": "active",
                "notes": "Interested in AI chatbot for customer support"
            },
            {
                "name": "Emily Rodriguez",
                "email": "emily@consulting.com",
                "company": "Rodriguez Consulting",
                "status": "converted",
                "notes": "Signed up for Professional plan"
            },
            {
                "name": "David Kim",
                "email": "david.kim@enterprise.com",
                "company": "Enterprise Corp",
                "status": "active",
                "notes": "Evaluating multiple chatbot solutions"
            },
            {
                "name": "Lisa Wang",
                "email": "lisa.wang@growth.co",
                "company": "Growth Co",
                "status": "contacted",
                "notes": "Requested demo for team of 50+"
            }
        ]
        
        for i, lead_data in enumerate(leads_data, 2):  # Start from 2 since we already have 1 lead
            try:
                async with self.session.post(f"{API_BASE}/leads/leads", json=lead_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if result.get("success") and "lead" in result:
                            lead = result["lead"]
                            lead_id = lead.get("id")
                            self.created_leads.append(lead_id)
                            
                            self.log_test(f"Create lead {i} ({lead_data['name']})", True, 
                                        f"Lead created with status: {lead_data['status']}")
                        else:
                            self.log_test(f"Create lead {i} ({lead_data['name']})", False, 
                                        f"Unexpected response: {result}")
                    else:
                        error_text = await response.text()
                        self.log_test(f"Create lead {i} ({lead_data['name']})", False, 
                                    f"Status: {response.status}, Error: {error_text}")
            except Exception as e:
                self.log_test(f"Create lead {i} ({lead_data['name']})", False, f"Exception: {str(e)}")
        
        # Verify all 6 leads appear in GET /api/leads/leads
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    total = result.get("total", 0)
                    leads = result.get("leads", [])
                    
                    if total == 6 and len(leads) == 6:
                        # Verify different statuses are present
                        statuses = [lead.get("status") for lead in leads]
                        unique_statuses = set(statuses)
                        
                        expected_statuses = {"active", "contacted", "converted"}
                        if expected_statuses.issubset(unique_statuses):
                            self.log_test("Verify all 6 leads with statuses", True, 
                                        f"All leads present with statuses: {list(unique_statuses)}")
                        else:
                            missing_statuses = expected_statuses - unique_statuses
                            self.log_test("Verify all 6 leads with statuses", False, 
                                        f"Missing statuses: {missing_statuses}")
                    else:
                        self.log_test("Verify all 6 leads with statuses", False, 
                                    f"Expected 6 leads, got total={total}, leads_length={len(leads)}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify all 6 leads with statuses", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify all 6 leads with statuses", False, f"Exception: {str(e)}")

    async def test_upgrade_to_professional_plan(self):
        """Test upgrading to Professional plan"""
        print("\n⬆️ Testing Upgrade to Professional Plan...")
        
        # Test PUT /api/plans/upgrade with plan_id="professional"
        upgrade_data = {"plan_id": "professional"}
        
        try:
            async with self.session.post(f"{API_BASE}/plans/upgrade", json=upgrade_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Verify upgrade success
                    if "message" in result and "subscription" in result:
                        message = result["message"]
                        subscription = result["subscription"]
                        
                        if "professional" in message.lower():
                            self.log_test("Upgrade to Professional plan", True, 
                                        f"Successfully upgraded: {message}")
                            
                            # Verify subscription details
                            if subscription.get("plan_name") == "Professional":
                                self.log_test("Professional plan subscription verification", True, 
                                            f"Plan name correct: {subscription['plan_name']}")
                            else:
                                self.log_test("Professional plan subscription verification", False, 
                                            f"Wrong plan name: {subscription.get('plan_name')}")
                        else:
                            self.log_test("Upgrade to Professional plan", False, 
                                        f"Unexpected message: {message}")
                    else:
                        self.log_test("Upgrade to Professional plan", False, 
                                    f"Missing fields in response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Upgrade to Professional plan", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Upgrade to Professional plan", False, f"Exception: {str(e)}")
        
        # Verify plan change was successful
        try:
            async with self.session.get(f"{API_BASE}/plans/current") as response:
                if response.status == 200:
                    result = await response.json()
                    plan = result.get("plan", {})
                    
                    if plan.get("name") == "Professional":
                        self.log_test("Verify Professional plan active", True, 
                                    f"Current plan: {plan['name']}")
                    else:
                        self.log_test("Verify Professional plan active", False, 
                                    f"Expected Professional, got: {plan.get('name')}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify Professional plan active", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify Professional plan active", False, f"Exception: {str(e)}")

    async def test_professional_plan_500_leads_limit(self):
        """Test Professional Plan User - 500 Leads Limit"""
        print("\n📊 Testing Professional Plan 500 Leads Limit...")
        
        # Test GET /api/leads/leads - Should return max_leads=500, plan_name="Professional"
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    max_leads = result.get("max_leads", -1)
                    plan_name = result.get("plan_name", "")
                    total = result.get("total", 0)
                    
                    if max_leads == 500 and plan_name == "Professional":
                        self.log_test("Professional plan limits check", True, 
                                    f"Correct limits: max_leads={max_leads}, plan={plan_name}, current={total}")
                    else:
                        self.log_test("Professional plan limits check", False, 
                                    f"Wrong limits: max_leads={max_leads}, plan={plan_name}")
                else:
                    error_text = await response.text()
                    self.log_test("Professional plan limits check", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Professional plan limits check", False, f"Exception: {str(e)}")
        
        # Test POST /api/leads/leads - Create new lead successfully
        lead_data = {
            "name": "Alex Thompson",
            "email": "alex.thompson@bigcorp.com",
            "company": "BigCorp Industries",
            "status": "active",
            "notes": "Enterprise client interested in custom integration"
        }
        
        try:
            async with self.session.post(f"{API_BASE}/leads/leads", json=lead_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get("success") and "lead" in result:
                        lead = result["lead"]
                        lead_id = lead.get("id")
                        self.created_leads.append(lead_id)
                        
                        self.log_test("Create lead on Professional plan", True, 
                                    f"Lead created successfully with ID: {lead_id}")
                    else:
                        self.log_test("Create lead on Professional plan", False, 
                                    f"Unexpected response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Create lead on Professional plan", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Create lead on Professional plan", False, f"Exception: {str(e)}")
        
        # Verify lead count reflects Professional plan limits
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    total = result.get("total", 0)
                    remaining = result.get("remaining", 0)
                    
                    expected_total = 7  # 6 from previous tests + 1 new
                    expected_remaining = 500 - expected_total
                    
                    if total == expected_total and remaining == expected_remaining:
                        self.log_test("Professional plan count verification", True, 
                                    f"Correct counts: total={total}, remaining={remaining}")
                    else:
                        self.log_test("Professional plan count verification", False, 
                                    f"Count mismatch: total={total} (expected {expected_total}), remaining={remaining} (expected {expected_remaining})")
                else:
                    error_text = await response.text()
                    self.log_test("Professional plan count verification", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Professional plan count verification", False, f"Exception: {str(e)}")

    async def test_lead_management_operations(self):
        """Test Lead Management Operations - Update and Delete"""
        print("\n🔧 Testing Lead Management Operations...")
        
        if not self.created_leads:
            self.log_test("Lead management operations", False, "No leads available for testing")
            return
        
        # Get the first lead for testing
        test_lead_id = self.created_leads[0]
        
        # Test PUT /api/leads/leads/{lead_id} - Update a lead's information
        update_data = {
            "name": "John Smith (Updated)",
            "email": "john.smith.updated@techcorp.com",
            "phone": "+1-555-0124",
            "company": "TechCorp Solutions Inc",
            "status": "contacted",
            "notes": "Updated: Follow-up call completed, very interested"
        }
        
        try:
            async with self.session.put(f"{API_BASE}/leads/leads/{test_lead_id}", json=update_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get("success") and "lead" in result:
                        updated_lead = result["lead"]
                        
                        # Verify update was successful
                        fields_updated = (
                            updated_lead.get("name") == update_data["name"] and
                            updated_lead.get("email") == update_data["email"] and
                            updated_lead.get("phone") == update_data["phone"] and
                            updated_lead.get("company") == update_data["company"] and
                            updated_lead.get("status") == update_data["status"] and
                            updated_lead.get("notes") == update_data["notes"]
                        )
                        
                        if fields_updated:
                            self.log_test("Update lead information", True, 
                                        f"Lead updated successfully: {updated_lead['name']}")
                        else:
                            self.log_test("Update lead information", False, 
                                        f"Lead fields not updated correctly: {updated_lead}")
                    else:
                        self.log_test("Update lead information", False, 
                                    f"Unexpected response: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Update lead information", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Update lead information", False, f"Exception: {str(e)}")
        
        # Test DELETE /api/leads/leads/{lead_id} - Delete a lead
        delete_lead_id = self.created_leads[-1]  # Delete the last created lead
        
        try:
            async with self.session.delete(f"{API_BASE}/leads/leads/{delete_lead_id}") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get("success"):
                        self.log_test("Delete lead", True, 
                                    f"Lead deleted successfully: {result.get('message')}")
                        
                        # Remove from our tracking list
                        self.created_leads.remove(delete_lead_id)
                    else:
                        self.log_test("Delete lead", False, 
                                    f"Delete failed: {result}")
                else:
                    error_text = await response.text()
                    self.log_test("Delete lead", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Delete lead", False, f"Exception: {str(e)}")
        
        # Verify deletion and count decrements
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    total = result.get("total", 0)
                    leads = result.get("leads", [])
                    
                    expected_total = 6  # 7 - 1 deleted
                    if total == expected_total and len(leads) == expected_total:
                        # Verify deleted lead is not in the list
                        lead_ids = [lead.get("id") for lead in leads]
                        if delete_lead_id not in lead_ids:
                            self.log_test("Verify deletion and count decrement", True, 
                                        f"Count correctly decremented to {total}, deleted lead not found")
                        else:
                            self.log_test("Verify deletion and count decrement", False, 
                                        f"Deleted lead still appears in list")
                    else:
                        self.log_test("Verify deletion and count decrement", False, 
                                    f"Count mismatch: total={total} (expected {expected_total}), leads_length={len(leads)}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify deletion and count decrement", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify deletion and count decrement", False, f"Exception: {str(e)}")

    async def test_lead_statistics_endpoint(self):
        """Test GET /api/leads/stats - Check lead statistics endpoint"""
        print("\n📊 Testing Lead Statistics Endpoint...")
        
        try:
            async with self.session.get(f"{API_BASE}/leads/stats") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Check required fields
                    required_fields = ["total_leads", "active_leads", "contacted_leads", "converted_leads", 
                                     "max_leads", "remaining_leads", "plan_name"]
                    
                    if all(field in result for field in required_fields):
                        total_leads = result["total_leads"]
                        active_leads = result["active_leads"]
                        contacted_leads = result["contacted_leads"]
                        converted_leads = result["converted_leads"]
                        max_leads = result["max_leads"]
                        plan_name = result["plan_name"]
                        
                        # Verify statistics make sense
                        stats_valid = (
                            total_leads == active_leads + contacted_leads + converted_leads and
                            max_leads == 500 and  # Professional plan
                            plan_name == "Professional" and
                            total_leads >= 0 and active_leads >= 0 and contacted_leads >= 0 and converted_leads >= 0
                        )
                        
                        if stats_valid:
                            self.log_test("Lead statistics endpoint", True, 
                                        f"Stats: total={total_leads}, active={active_leads}, contacted={contacted_leads}, converted={converted_leads}, plan={plan_name}")
                        else:
                            self.log_test("Lead statistics endpoint", False, 
                                        f"Invalid stats: total={total_leads}, breakdown={active_leads + contacted_leads + converted_leads}, max={max_leads}, plan={plan_name}")
                    else:
                        missing = [f for f in required_fields if f not in result]
                        self.log_test("Lead statistics endpoint", False, 
                                    f"Missing fields: {missing}")
                else:
                    error_text = await response.text()
                    self.log_test("Lead statistics endpoint", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Lead statistics endpoint", False, f"Exception: {str(e)}")
        
        # Test search and filter by verifying different statuses exist
        try:
            async with self.session.get(f"{API_BASE}/leads/leads") as response:
                if response.status == 200:
                    result = await response.json()
                    leads = result.get("leads", [])
                    
                    # Check that we have leads with different statuses
                    statuses = [lead.get("status") for lead in leads]
                    unique_statuses = set(statuses)
                    
                    expected_statuses = {"active", "contacted", "converted"}
                    if expected_statuses.issubset(unique_statuses):
                        self.log_test("Verify different lead statuses", True, 
                                    f"All expected statuses found: {list(unique_statuses)}")
                    else:
                        missing_statuses = expected_statuses - unique_statuses
                        self.log_test("Verify different lead statuses", False, 
                                    f"Missing statuses: {missing_statuses}, found: {list(unique_statuses)}")
                else:
                    error_text = await response.text()
                    self.log_test("Verify different lead statuses", False, 
                                f"Status: {response.status}, Error: {error_text}")
        except Exception as e:
            self.log_test("Verify different lead statuses", False, f"Exception: {str(e)}")

    async def cleanup_test_resources(self):
        """Clean up test resources"""
        print("\n🧹 Cleaning up test resources...")
        
        # Delete test integration
        if self.test_chatbot_id and self.test_integration_id:
            try:
                await self.session.delete(f"{API_BASE}/integrations/{self.test_chatbot_id}/{self.test_integration_id}")
                self.log_test("Delete test integration", True, "Test integration deleted")
            except:
                pass
        
        # Delete test chatbot
        if self.test_chatbot_id:
            try:
                await self.session.delete(f"{API_BASE}/chatbots/{self.test_chatbot_id}")
                self.log_test("Delete test chatbot", True, "Test chatbot deleted")
            except:
                pass

    async def run_all_tests(self):
        """Run all Slack integration tests"""
        print("🚀 Starting Comprehensive Slack Integration Testing")
        print(f"Backend URL: {API_BASE}")
        print(f"Mock User: {self.mock_user_id}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Setup test environment first
            await self.setup_test_environment()
            
            # Create test chatbot
            if await self.create_test_chatbot():
                # Run all Slack integration tests
                await self.test_setup_slack_integration()
                await self.test_slack_connection_test()
                await self.test_generate_webhook_url()
                await self.test_get_webhook_info()
                await self.test_enable_disable_integration()
                await self.test_webhook_event_reception()
                await self.test_integration_logs()
            else:
                self.log_test("Slack Integration Testing", False, "Failed to create test chatbot - cannot proceed")
            
        finally:
            await self.cleanup_test_resources()
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()

    # This method is already defined above - removing duplicate
        
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n" + "=" * 80)
        print("📊 SLACK INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        # Categorize results
        categories = {
            "Setup & Configuration": ["Create test chatbot", "Setup Slack integration", "Slack integration response format", "Slack integration data validation"],
            "Connection Testing": ["Test Slack connection", "Slack connection test"],
            "Webhook Management": ["Generate Slack webhook URL", "Slack webhook instructions", "Get Slack webhook info", "Slack webhook info instructions"],
            "Integration Control": ["Enable Slack integration", "Disable Slack integration"],
            "Event Processing": ["Slack URL verification challenge", "Slack message event reception"],
            "Activity Logging": ["Integration activity logs"],
            "Cleanup": ["Delete test integration", "Delete test chatbot"]
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
        
        # Show critical Slack integration functionality status
        print(f"\n🎯 CRITICAL SLACK INTEGRATION FUNCTIONALITY:")
        
        critical_tests = [
            ("Integration Setup", "Setup Slack integration"),
            ("Connection Testing", "Test Slack connection"),
            ("Webhook URL Generation", "Generate Slack webhook URL"),
            ("Webhook Info Retrieval", "Get Slack webhook info"),
            ("Enable/Disable Toggle", "Enable Slack integration"),
            ("Event Reception", "Slack URL verification challenge"),
            ("Activity Logging", "Integration activity logs")
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
            print(f"\n🎉 ALL CRITICAL SLACK INTEGRATION FEATURES WORKING!")
        else:
            print(f"\n⚠️  SOME CRITICAL SLACK INTEGRATION FEATURES NEED ATTENTION")
        
        # Show detailed failed tests
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS DETAILS:")
            for test in failed_tests:
                print(f"   • {test['test']}")
                print(f"     Details: {test['details']}")

async def main():
    """Main test execution"""
    test_suite = SlackIntegrationTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())