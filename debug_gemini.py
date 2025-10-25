#!/usr/bin/env python3
"""
Debug Gemini responses to understand why it's not using knowledge base
"""

import requests
import json
import uuid

def test_gemini_response():
    base_url = "https://preview-hub-65.preview.emergentagent.com"
    
    # Create a test user and get auth token
    test_user_email = f"geminitest_{uuid.uuid4().hex[:8]}@example.com"
    test_user_password = "TestPassword123!"
    
    session = requests.Session()
    
    # Register
    register_payload = {
        "name": "Gemini Test User",
        "email": test_user_email,
        "password": test_user_password
    }
    
    response = session.post(f"{base_url}/api/auth/register", json=register_payload)
    print(f"Register: {response.status_code}")
    
    # Login
    login_payload = {
        "email": test_user_email,
        "password": test_user_password
    }
    
    response = session.post(f"{base_url}/api/auth/login", json=login_payload)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        auth_token = response.json().get('access_token')
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create Gemini chatbot
        chatbot_payload = {
            "name": "Debug Gemini Bot",
            "model": "gemini-2.0-flash",
            "provider": "gemini",
            "temperature": 0.7,
            "instructions": "You are a helpful assistant. Always use the provided knowledge base to answer questions.",
            "welcome_message": "Hello! I'm powered by Gemini."
        }
        
        response = session.post(f"{base_url}/api/chatbots", json=chatbot_payload, headers=headers)
        print(f"Create Chatbot: {response.status_code}")
        
        if response.status_code == 201:
            chatbot_id = response.json().get('id')
            print(f"Chatbot ID: {chatbot_id}")
            
            # Add knowledge source
            knowledge_payload = {
                "name": "Test Knowledge",
                "content": "IMPORTANT: The company name is TechCorp Solutions and it was founded in 2020. The company has 50+ employees."
            }
            
            response = session.post(f"{base_url}/api/sources/chatbot/{chatbot_id}/text", 
                                  data=knowledge_payload, headers=headers)
            print(f"Add Knowledge: {response.status_code}")
            
            # Wait a moment for processing
            import time
            time.sleep(2)
            
            # Test chat
            chat_payload = {
                "chatbot_id": chatbot_id,
                "message": "What is the company name and when was it founded?",
                "session_id": str(uuid.uuid4()),
                "user_name": "Test User",
                "user_email": "test@example.com"
            }
            
            response = session.post(f"{base_url}/api/chat", json=chat_payload, headers=headers)
            print(f"Chat: {response.status_code}")
            
            if response.status_code == 200:
                ai_response = response.json().get('message', '')
                print(f"\nGemini Response:")
                print(f"Length: {len(ai_response)} chars")
                print(f"Content: {ai_response}")
                print(f"\nContains 'TechCorp': {'techcorp' in ai_response.lower()}")
                print(f"Contains '2020': {'2020' in ai_response}")
                print(f"Contains 'company': {'company' in ai_response.lower()}")
            else:
                print(f"Chat failed: {response.text}")
            
            # Cleanup
            response = session.delete(f"{base_url}/api/chatbots/{chatbot_id}", headers=headers)
            print(f"Cleanup: {response.status_code}")

if __name__ == "__main__":
    test_gemini_response()