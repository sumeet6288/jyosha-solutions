"""
Seed demo user into the database for development
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_demo_user():
    # Get MongoDB URL and DB name from environment
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'chatbase_db')
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    users_collection = db.users
    
    print(f"Using database: {db_name}")
    
    # Check if demo user already exists
    existing_user = await users_collection.find_one({"email": "demo-user-123@botsmith.com"})
    
    if existing_user:
        print("✅ Demo user already exists in database")
        print(f"   ID: {existing_user.get('id')}")
        print(f"   Name: {existing_user.get('name')}")
        print(f"   Email: {existing_user.get('email')}")
        print(f"   Role: {existing_user.get('role', 'user')}")
        print(f"   Status: {existing_user.get('status', 'active')}")
        return
    
    # Create demo user
    demo_user = {
        "id": "demo-user-123",
        "name": "User demo-use",
        "email": "demo-user-123@botsmith.com",
        "password_hash": pwd_context.hash("password123"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "role": "admin",  # Make demo user an admin
        "status": "active",
        "phone": None,
        "address": None,
        "bio": "Demo user for development and testing",
        "avatar_url": None,
        "company": "BotSmith Demo",
        "job_title": "Administrator",
        "custom_limits": {
            "max_chatbots": 100,
            "max_messages": 10000,
            "max_file_uploads": 100
        },
        "tags": ["demo", "development"],
        "admin_notes": "Demo user created for development and testing purposes",
        "last_login": datetime.now(timezone.utc).isoformat(),
        "login_count": 1,
        "last_ip": "127.0.0.1"
    }
    
    # Insert demo user
    result = await users_collection.insert_one(demo_user)
    
    if result.inserted_id:
        print("✅ Demo user created successfully!")
        print(f"   ID: {demo_user['id']}")
        print(f"   Name: {demo_user['name']}")
        print(f"   Email: {demo_user['email']}")
        print(f"   Role: {demo_user['role']}")
        print(f"   Status: {demo_user['status']}")
        print(f"   Password: password123")
    else:
        print("❌ Failed to create demo user")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_demo_user())
