"""
Seed script to create demo users for admin panel testing
"""
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from passlib.context import CryptContext
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample data for realistic users
FIRST_NAMES = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Jessica", "William", "Amanda"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
COMPANIES = ["TechCorp", "DataSystems", "CloudNet", "InnoSoft", "DigitalHub", "SmartAI", "WebFlow", "AppDev Co"]
JOB_TITLES = ["CEO", "CTO", "Product Manager", "Developer", "Marketing Director", "Sales Manager", "Operations Manager"]
STATUSES = ["active", "active", "active", "active", "suspended", "banned"]  # Weighted towards active
ROLES = ["user", "user", "user", "user", "moderator", "admin"]  # Weighted towards user

async def seed_users():
    """Seed the database with demo users"""
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    users_collection = db.users
    
    # Check if we already have enough users (more than just the demo user)
    existing_count = await users_collection.count_documents({})
    if existing_count > 1:
        print(f"Database already has {existing_count} users. Skipping seed.")
        client.close()
        return
    
    print("Creating additional demo users...")
    
    # Create demo users
    users = []
    
    # Update the existing demo user to be an admin
    await users_collection.update_one(
        {"id": "demo-user-123"},
        {"$set": {
            "role": "admin",
            "name": "Demo Admin",
            "company": "BotSmith Inc",
            "job_title": "Administrator",
            "bio": "Demo admin account for testing the BotSmith platform",
            "tags": ["demo", "admin"],
            "admin_notes": "Main demo account for development"
        }}
    )
    print("✅ Updated demo-user-123 to admin role")
    
    # Create 20 realistic demo users
    for i in range(20):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        role = random.choice(ROLES)
        status = random.choice(STATUSES)
        
        created_days_ago = random.randint(1, 90)
        created_at = datetime.now(timezone.utc) - timedelta(days=created_days_ago)
        last_login_hours_ago = random.randint(1, 168)  # Within last week
        
        user = {
            "id": f"user-{i+1:03d}",
            "name": name,
            "email": email,
            "password_hash": pwd_context.hash("password123"),
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat(),
            "role": role,
            "status": status,
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}, {random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])} {random.randint(10000, 99999)}",
            "bio": f"Professional working in {random.choice(['software', 'marketing', 'sales', 'operations', 'customer success'])}",
            "avatar_url": None,
            "company": random.choice(COMPANIES),
            "job_title": random.choice(JOB_TITLES),
            "custom_max_chatbots": random.choice([None, None, None, 10, 20, 50]),
            "custom_max_messages": random.choice([None, None, None, 1000, 5000, 10000]),
            "custom_max_file_uploads": random.choice([None, None, None, 20, 50, 100]),
            "last_login": (datetime.now(timezone.utc) - timedelta(hours=last_login_hours_ago)).isoformat(),
            "login_count": random.randint(1, 150),
            "last_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "tags": random.sample(["vip", "trial", "premium", "early-adopter", "enterprise"], k=random.randint(0, 2)),
            "admin_notes": random.choice([None, None, "Good customer", "Needs follow-up", "VIP client", "Active user"]),
            "suspension_reason": "Violated terms of service" if status == "suspended" else ("Spam activity detected" if status == "banned" else None),
            "suspension_until": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat() if status == "suspended" else None
        }
        users.append(user)
    
    # Insert all users
    result = await users_collection.insert_many(users)
    print(f"✅ Successfully created {len(result.inserted_ids)} demo users")
    
    # Print summary
    print("\nDemo users created:")
    print(f"- Total users: {len(users)}")
    print(f"- Admins: {sum(1 for u in users if u['role'] == 'admin')}")
    print(f"- Moderators: {sum(1 for u in users if u['role'] == 'moderator')}")
    print(f"- Regular users: {sum(1 for u in users if u['role'] == 'user')}")
    print(f"- Active: {sum(1 for u in users if u['status'] == 'active')}")
    print(f"- Suspended: {sum(1 for u in users if u['status'] == 'suspended')}")
    print(f"- Banned: {sum(1 for u in users if u['status'] == 'banned')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_users())
