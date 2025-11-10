#!/usr/bin/env python3
"""
Test script for Instagram integration
"""
import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8001/api"

# Mock user and chatbot IDs for testing
TEST_USER_ID = "test-user-123"
TEST_CHATBOT_ID = None  # Will be created

async def test_instagram_integration():
    """Test Instagram integration functionality"""
    
    print("=" * 60)
    print("Instagram Integration Test Suite")
    print("=" * 60)
    print()
    
    async with httpx.AsyncClient() as client:
        # Step 1: Check if chatbots exist
        print("Step 1: Checking existing chatbots...")
        try:
            response = await client.get(
                f"{BASE_URL}/chatbots/",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            chatbots = response.json()
            
            if chatbots:
                global TEST_CHATBOT_ID
                TEST_CHATBOT_ID = chatbots[0]['id']
                print(f"✅ Using existing chatbot: {TEST_CHATBOT_ID}")
            else:
                print("❌ No chatbots found. Please create a chatbot first.")
                return
        except Exception as e:
            print(f"❌ Error fetching chatbots: {str(e)}")
            return
        
        print()
        
        # Step 2: Create Instagram integration
        print("Step 2: Creating Instagram integration...")
        try:
            integration_data = {
                "integration_type": "instagram",
                "credentials": {
                    "page_access_token": "test_instagram_token_12345",
                    "verify_token": "instagram_verify_secret",
                    "app_secret": "test_app_secret"
                }
            }
            
            response = await client.post(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}",
                json=integration_data,
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code in [200, 201]:
                integration = response.json()
                print(f"✅ Instagram integration created successfully")
                print(f"   Integration ID: {integration['id']}")
                print(f"   Status: {integration['status']}")
                print(f"   Enabled: {integration['enabled']}")
                integration_id = integration['id']
            else:
                print(f"❌ Failed to create integration: {response.status_code}")
                print(f"   Response: {response.text}")
                return
        except Exception as e:
            print(f"❌ Error creating integration: {str(e)}")
            return
        
        print()
        
        # Step 3: Test connection (will fail with test token, but should handle gracefully)
        print("Step 3: Testing Instagram connection...")
        try:
            response = await client.post(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}/{integration_id}/test",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            result = response.json()
            if result.get('success'):
                print(f"✅ Connection test passed: {result.get('message')}")
            else:
                print(f"⚠️  Connection test failed (expected with test token): {result.get('message')}")
        except Exception as e:
            print(f"❌ Error testing connection: {str(e)}")
        
        print()
        
        # Step 4: Get integration list
        print("Step 4: Fetching all integrations...")
        try:
            response = await client.get(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code == 200:
                integrations = response.json()
                instagram_integrations = [i for i in integrations if i['integration_type'] == 'instagram']
                print(f"✅ Found {len(instagram_integrations)} Instagram integration(s)")
                for integ in instagram_integrations:
                    print(f"   - ID: {integ['id']}, Enabled: {integ['enabled']}, Status: {integ['status']}")
            else:
                print(f"❌ Failed to fetch integrations: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching integrations: {str(e)}")
        
        print()
        
        # Step 5: Setup webhook
        print("Step 5: Setting up Instagram webhook...")
        try:
            webhook_data = {
                "base_url": "https://yourdomain.com"
            }
            
            response = await client.post(
                f"{BASE_URL}/instagram/{TEST_CHATBOT_ID}/setup-webhook",
                json=webhook_data,
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code == 200:
                webhook_info = response.json()
                print(f"✅ Webhook setup successful")
                print(f"   Webhook URL: {webhook_info.get('webhook_url')}")
                print(f"   Verify Token: {webhook_info.get('verify_token')}")
                print(f"\n   Setup Instructions:")
                for instruction in webhook_info.get('instructions', []):
                    print(f"   {instruction}")
            else:
                print(f"❌ Failed to setup webhook: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error setting up webhook: {str(e)}")
        
        print()
        
        # Step 6: Toggle integration (enable)
        print("Step 6: Enabling Instagram integration...")
        try:
            response = await client.post(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}/{integration_id}/toggle",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Integration toggled: {result.get('message')}")
                print(f"   Enabled: {result.get('enabled')}")
            else:
                print(f"❌ Failed to toggle integration: {response.status_code}")
        except Exception as e:
            print(f"❌ Error toggling integration: {str(e)}")
        
        print()
        
        # Step 7: Get integration logs
        print("Step 7: Fetching integration logs...")
        try:
            response = await client.get(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}/logs",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code == 200:
                logs = response.json()
                print(f"✅ Found {len(logs)} log entries")
                for log in logs[:3]:  # Show first 3 logs
                    print(f"   - {log['event_type']}: {log['message']} (Status: {log['status']})")
            else:
                print(f"❌ Failed to fetch logs: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching logs: {str(e)}")
        
        print()
        
        # Step 8: Test webhook verification (simulating Instagram's verification request)
        print("Step 8: Testing webhook verification...")
        try:
            verify_params = {
                "hub.mode": "subscribe",
                "hub.challenge": "1234567890",
                "hub.verify_token": "instagram_verify_secret"
            }
            
            response = await client.post(
                f"{BASE_URL}/instagram/webhook/{TEST_CHATBOT_ID}",
                params=verify_params
            )
            
            if response.status_code == 200:
                challenge = response.text
                print(f"✅ Webhook verification successful")
                print(f"   Challenge response: {challenge}")
            else:
                print(f"❌ Webhook verification failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error testing webhook verification: {str(e)}")
        
        print()
        
        # Step 9: Cleanup - Delete integration
        print("Step 9: Cleaning up - Deleting Instagram integration...")
        try:
            response = await client.delete(
                f"{BASE_URL}/integrations/{TEST_CHATBOT_ID}/{integration_id}",
                headers={"Authorization": f"Bearer mock-token-{TEST_USER_ID}"}
            )
            
            if response.status_code == 200:
                print(f"✅ Integration deleted successfully")
            else:
                print(f"❌ Failed to delete integration: {response.status_code}")
        except Exception as e:
            print(f"❌ Error deleting integration: {str(e)}")
        
        print()
        print("=" * 60)
        print("Instagram Integration Test Complete!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_instagram_integration())
