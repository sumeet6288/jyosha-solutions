#!/usr/bin/env python3
"""
Create sample data for testing admin panel analytics graphs
"""
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["chatbase_db"]

# Clear existing test data (except admin user)
print("Clearing existing test data...")
db.messages.delete_many({})
db.conversations.delete_many({})
db.chatbots.delete_many({})
# Keep admin user, but add more test users
admin_email = "admin@botsmith.com"

# Create test users (with dates spread over 30 days)
print("\nCreating test users...")
test_users = []
base_date = datetime.now() - timedelta(days=30)

for i in range(15):
    days_offset = i * 2  # Spread users over 30 days
    created_date = base_date + timedelta(days=days_offset)
    user_id = f"test-user-{i+1}"
    
    user = {
        "user_id": user_id,
        "email": f"testuser{i+1}@example.com",
        "name": f"Test User {i+1}",
        "role": "user",
        "created_at": created_date.isoformat(),
        "email_verified": True,
        "plan_id": random.choice(["free", "starter", "professional"])
    }
    
    result = db.users.update_one(
        {"email": user["email"]},
        {"$set": user},
        upsert=True
    )
    test_users.append(user)
    
print(f"Created {len(test_users)} test users")

# Create chatbots for test users
print("\nCreating test chatbots...")
chatbots = []
providers = ["openai", "anthropic", "google"]

for i, user in enumerate(test_users[:10]):  # First 10 users get chatbots
    created_date = datetime.fromisoformat(user["created_at"]) + timedelta(hours=random.randint(1, 24))
    
    for j in range(random.randint(1, 3)):  # Each user gets 1-3 chatbots
        chatbot_id = f"chatbot-{i}-{j}"
        chatbot = {
            "chatbot_id": chatbot_id,
            "user_id": user["user_id"],
            "name": f"{user['name']}'s Chatbot {j+1}",
            "ai_provider": random.choice(providers),
            "ai_model": "gpt-4o-mini",
            "created_at": created_date.isoformat(),
            "status": "active"
        }
        db.chatbots.insert_one(chatbot)
        chatbots.append(chatbot)

print(f"Created {len(chatbots)} test chatbots")

# Create conversations and messages
print("\nCreating test conversations and messages...")
total_messages = 0

for chatbot in chatbots:
    # Each chatbot gets 2-5 conversations
    for conv_num in range(random.randint(2, 5)):
        conversation_id = f"conv-{chatbot['chatbot_id']}-{conv_num}"
        
        # Conversation created sometime after chatbot
        chatbot_date = datetime.fromisoformat(chatbot["created_at"])
        days_after = random.randint(0, 15)
        conv_date = chatbot_date + timedelta(days=days_after)
        
        conversation = {
            "conversation_id": conversation_id,
            "chatbot_id": chatbot["chatbot_id"],
            "user_id": chatbot["user_id"],
            "status": "active",
            "created_at": conv_date.isoformat()
        }
        db.conversations.insert_one(conversation)
        
        # Each conversation gets 3-10 messages (pairs of user and assistant)
        num_message_pairs = random.randint(3, 10)
        
        for msg_num in range(num_message_pairs):
            msg_date = conv_date + timedelta(minutes=msg_num * 5)
            
            # User message
            user_message = {
                "message_id": f"msg-{conversation_id}-user-{msg_num}",
                "conversation_id": conversation_id,
                "chatbot_id": chatbot["chatbot_id"],
                "role": "user",
                "content": f"Test user message {msg_num + 1}",
                "timestamp": msg_date.isoformat()
            }
            db.messages.insert_one(user_message)
            total_messages += 1
            
            # Assistant message
            assistant_message = {
                "message_id": f"msg-{conversation_id}-assistant-{msg_num}",
                "conversation_id": conversation_id,
                "chatbot_id": chatbot["chatbot_id"],
                "role": "assistant",
                "content": f"Test assistant response {msg_num + 1}",
                "timestamp": (msg_date + timedelta(seconds=30)).isoformat()
            }
            db.messages.insert_one(assistant_message)
            total_messages += 1

print(f"Created {total_messages} test messages")

# Print summary
print("\n" + "="*50)
print("SAMPLE DATA CREATION COMPLETE")
print("="*50)
print(f"Total Users: {db.users.count_documents({})}")
print(f"Total Chatbots: {db.chatbots.count_documents({})}")
print(f"Total Conversations: {db.conversations.count_documents({})}")
print(f"Total Messages: {db.messages.count_documents({})}")
print("\nYou can now view the analytics graphs in the admin panel!")
print("="*50)

client.close()
