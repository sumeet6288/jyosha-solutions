# 🛠️ BotSmith Developer Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Database Schema](#database-schema)
6. [AI Integration](#ai-integration)
7. [Testing](#testing)
8. [Code Style](#code-style)
9. [Contributing](#contributing)
10. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### System Architecture

```
┌─────────────────┐
│   Frontend (React)  │
│   Port: 3000       │
└───────┬─────────┘
        │
        │ HTTP/REST
        │
┌───────┴─────────┐
│   Backend (FastAPI) │
│   Port: 8001       │
└───┬────┬────┬───┘
    │    │    │
    │    │    └───────────────────────┐
    │    │                             │
    │    └───────────────┐           │
    │                      │           │
┌───┴──────┐  ┌──────┴──────┐  ┌─┴────────────┐
│  MongoDB   │  │  AI Providers  │  │ File Storage │
│ Port: 27017│  │ (OpenAI, etc)│  │    /uploads  │
└───────────┘  └─────────────┘  └─────────────┘
```

### Technology Stack

**Backend:**
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.11+
- **Database Driver**: Motor (async MongoDB)
- **AI Library**: emergentintegrations
- **Authentication**: JWT (python-jose)
- **File Processing**: pypdf, python-docx, openpyxl
- **Web Scraping**: BeautifulSoup4, lxml

**Frontend:**
- **Framework**: React 18
- **Styling**: Tailwind CSS 3
- **Charts**: Recharts
- **HTTP**: Axios
- **Routing**: React Router v6
- **Build Tool**: Create React App

**Database:**
- **MongoDB 6.0+**: Document-based NoSQL
- **Collections**: users, chatbots, sources, conversations, messages, activity_logs, login_history

---

## Development Setup

### Prerequisites

```bash
# Check versions
python --version  # 3.11+
node --version    # 18+
yarn --version    # 1.22+
mongod --version  # 6.0+
```

### Environment Setup

**1. Clone Repository**
```bash
git clone <repository-url>
cd botsmith
```

**2. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install emergentintegrations
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Create .env file
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017/botsmith
EMERGENT_LLM_KEY=your_key_here
SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
EOF
```

**3. Frontend Setup**

```bash
cd ../frontend

# Install dependencies (use yarn, not npm)
yarn install

# Create .env file
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=true
EOF
```

**4. MongoDB Setup**

```bash
# Start MongoDB
mongod --dbpath /data/db

# Create database (automatic on first write)
mongo
> use botsmith
> db.createCollection('users')
> exit
```

**5. Start Development Servers**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

**6. Verify Setup**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- MongoDB: mongodb://localhost:27017

---

## Backend Development

### Project Structure

```
backend/
├── routers/
│   ├── __init__.py
│   ├── chatbots.py          # Chatbot CRUD
│   ├── sources.py           # Knowledge base
│   ├── chat.py              # Chat endpoints
│   ├── analytics.py         # Basic analytics
│   ├── advanced_analytics.py # Advanced insights
│   ├── admin_users.py       # Admin operations
│   └── public_chat.py       # Public chat API
├── services/
│   ├── __init__.py
│   ├── chat_service.py      # AI integration
│   ├── document_processor.py # File processing
│   └── website_scraper.py   # Web scraping
├── models.py                # Pydantic models
├── auth.py                  # Authentication
├── server.py                # FastAPI app
├── requirements.txt         # Dependencies
└── .env                     # Environment vars
```

### Adding a New Router

**1. Create Router File**

```python
# routers/my_feature.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models import User
from auth import get_current_user

router = APIRouter(prefix="/api/my-feature", tags=["My Feature"])

@router.get("/")
async def list_items(user: User = Depends(get_current_user)):
    """List all items for current user"""
    # Implementation
    return {"items": []}

@router.post("/")
async def create_item(data: dict, user: User = Depends(get_current_user)):
    """Create new item"""
    # Implementation
    return {"id": "new-item-id"}
```

**2. Register Router**

```python
# server.py
from routers import my_feature

app.include_router(my_feature.router)
```

### Database Operations

**Get Database Instance:**

```python
from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
db = client.get_database()
```

**CRUD Examples:**

```python
# Create
result = await db.collection.insert_one({
    "id": str(uuid.uuid4()),
    "name": "Example",
    "created_at": datetime.utcnow()
})

# Read
item = await db.collection.find_one({"id": item_id})
items = await db.collection.find({"user_id": user_id}).to_list(100)

# Update
await db.collection.update_one(
    {"id": item_id},
    {"$set": {"name": "Updated"}}
)

# Delete
await db.collection.delete_one({"id": item_id})
```

### Error Handling

```python
from fastapi import HTTPException

# Not found
if not item:
    raise HTTPException(status_code=404, detail="Item not found")

# Validation error
if not valid:
    raise HTTPException(status_code=400, detail="Invalid input")

# Unauthorized
if user.id != item.user_id:
    raise HTTPException(status_code=403, detail="Access denied")

# Internal error
try:
    # risky operation
    pass
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### Adding Dependencies

```bash
# Install package
pip install package-name

# Add to requirements.txt
echo "package-name==version" >> requirements.txt

# Or regenerate
pip freeze > requirements.txt
```

---

## Frontend Development

### Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── AddSourceModal.jsx
│   │   ├── ChatPreviewModal.jsx
│   │   ├── AdvancedAnalytics.jsx
│   │   └── admin/
│   │       └── EnhancedUsersManagement.jsx
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── ChatbotBuilder.jsx
│   │   ├── Analytics.jsx
│   │   ├── Subscription.jsx
│   │   ├── AccountSettings.jsx
│   │   └── PublicChat.jsx
│   ├── utils/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
├── tailwind.config.js
└── .env
```

### Creating a New Page

**1. Create Page Component**

```jsx
// src/pages/MyPage.jsx
import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';

function MyPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await api.get('/my-endpoint');
      setData(response.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">My Page</h1>
        {/* Content */}
      </div>
    </div>
  );
}

export default MyPage;
```

**2. Add Route**

```jsx
// src/App.js
import MyPage from './pages/MyPage';

function App() {
  return (
    <Router>
      <Routes>
        {/* Existing routes */}
        <Route path="/my-page" element={<MyPage />} />
      </Routes>
    </Router>
  );
}
```

### API Integration

**API Client Setup:**

```javascript
// src/utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth token)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (handle errors)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export { api };
```

**Making API Calls:**

```javascript
// GET request
const response = await api.get('/api/chatbots');
const chatbots = response.data;

// POST request
const response = await api.post('/api/chatbots', {
  name: 'New Bot',
  model: 'gpt-4o-mini',
});

// PUT request
await api.put(`/api/chatbots/${id}`, { name: 'Updated' });

// DELETE request
await api.delete(`/api/chatbots/${id}`);

// File upload
const formData = new FormData();
formData.append('file', file);
formData.append('chatbot_id', chatbotId);

const response = await api.post('/api/sources/file', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
});
```

### Tailwind CSS Utilities

**Common Patterns:**

```jsx
{/* Gradient background */}
<div className="bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">

{/* Card */}
<div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">

{/* Button - Primary */}
<button className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-all">

{/* Button - Secondary */}
<button className="bg-white text-purple-600 border border-purple-200 px-6 py-3 rounded-lg hover:bg-purple-50 transition-all">

{/* Input */}
<input className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" />

{/* Badge */}
<span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">

{/* Loading spinner */}
<div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
```

### Adding Dependencies

```bash
# Always use yarn (not npm)
yarn add package-name

# Dev dependencies
yarn add -D package-name

# Remove package
yarn remove package-name
```

---

## Database Schema

### Users Collection

```javascript
{
  id: "uuid",
  email: "user@example.com",
  name: "John Doe",
  password_hash: "hashed_password",
  role: "user", // user, moderator, admin
  status: "active", // active, suspended, banned
  phone: "+1234567890",
  company: "Acme Inc",
  job_title: "Manager",
  bio: "User bio",
  avatar_url: "https://...",
  custom_limits: {
    chatbots: 5,
    messages: 10000
  },
  created_at: ISODate("2025-01-15T08:00:00Z"),
  last_login: ISODate("2025-01-28T10:30:00Z"),
  login_count: 45,
  last_ip: "192.168.1.1"
}
```

### Chatbots Collection

```javascript
{
  id: "uuid",
  user_id: "uuid",
  name: "Customer Support Bot",
  model: "gpt-4o-mini",
  provider: "openai",
  system_message: "You are a helpful assistant",
  primary_color: "#9333ea",
  secondary_color: "#ec4899",
  logo_url: "https://...",
  avatar_url: "https://...",
  welcome_message: "Hello! How can I help?",
  widget_position: "bottom-right",
  theme: "light",
  is_active: true,
  public_access: true,
  webhook_url: "https://...",
  created_at: ISODate("2025-01-20T10:00:00Z"),
  updated_at: ISODate("2025-01-28T10:30:00Z")
}
```

### Sources Collection

```javascript
{
  id: "uuid",
  chatbot_id: "uuid",
  type: "file", // file, website, text
  name: "documentation.pdf",
  content: "Extracted text content...",
  url: "https://example.com", // for website type
  file_path: "/uploads/abc123.pdf", // for file type
  file_size: 2048576,
  status: "completed", // processing, completed, failed
  error_message: null,
  created_at: ISODate("2025-01-20T10:05:00Z"),
  processed_at: ISODate("2025-01-20T10:06:00Z")
}
```

### Conversations Collection

```javascript
{
  id: "uuid",
  chatbot_id: "uuid",
  session_id: "session-uuid",
  user_name: "John Doe",
  user_email: "john@example.com",
  status: "active", // active, resolved, escalated
  rating: 5, // 1-5 stars
  started_at: ISODate("2025-01-28T10:30:00Z"),
  last_message_at: ISODate("2025-01-28T10:45:00Z")
}
```

### Messages Collection

```javascript
{
  id: "uuid",
  conversation_id: "uuid",
  role: "user", // user, assistant
  content: "What are your business hours?",
  response_time: 1.2, // seconds (for assistant messages)
  created_at: ISODate("2025-01-28T10:30:00Z")
}
```

---

## AI Integration

### Using emergentintegrations

**Installation:**
```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

**Basic Usage:**

```python
from emergentintegrations import get_client
import os

# Initialize client
client = get_client(
    provider='openai',  # or 'anthropic', 'google'
    api_key=os.environ.get('EMERGENT_LLM_KEY')
)

# Generate response
response = await client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=500
)

answer = response.choices[0].message.content
```

**With Context:**

```python
# Add knowledge base context
context = await get_chatbot_context(chatbot_id)

system_message = f"""
You are a helpful assistant. Use the following context to answer questions:

{context}

If the answer is not in the context, say so politely.
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_question}
]
```

**Supported Models:**

```python
MODELS = {
    'openai': ['gpt-4o', 'gpt-4o-mini'],
    'anthropic': ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229'],
    'google': ['gemini-2.0-flash-exp', 'gemini-1.5-pro']
}
```

---

## Testing

### Backend Testing

**Setup pytest:**

```bash
pip install pytest pytest-asyncio httpx
```

**Test Example:**

```python
# tests/test_chatbots.py
import pytest
from httpx import AsyncClient
from server import app

@pytest.mark.asyncio
async def test_create_chatbot():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chatbots",
            json={
                "name": "Test Bot",
                "model": "gpt-4o-mini",
                "provider": "openai"
            },
            headers={"Authorization": "Bearer test_token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Bot"
```

**Run tests:**
```bash
pytest tests/
```

### Frontend Testing

**Test Example:**

```javascript
// src/components/__tests__/Dashboard.test.js
import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';

test('renders dashboard heading', () => {
  render(<Dashboard />);
  const heading = screen.getByText(/Welcome back/i);
  expect(heading).toBeInTheDocument();
});
```

**Run tests:**
```bash
yarn test
```

---

## Code Style

### Python (Backend)

**Follow PEP 8:**

```python
# Good
async def get_chatbot(chatbot_id: str, user: User = Depends(get_current_user)):
    """Get chatbot by ID"""
    chatbot = await db.chatbots.find_one({"id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return chatbot

# Bad
def getChatbot(id,user):
    chatbot=db.chatbots.find_one({"id":id})
    if not chatbot:raise HTTPException(404,"Not found")
    return chatbot
```

**Format with Black:**
```bash
pip install black
black .
```

**Lint with Flake8:**
```bash
pip install flake8
flake8 .
```

### JavaScript (Frontend)

**Use ESLint:**

```bash
yarn add -D eslint
yarn run eslint src/
```

**Format with Prettier:**
```bash
yarn add -D prettier
yarn run prettier --write src/
```

---

## Contributing

### Workflow

1. **Create Branch**
```bash
git checkout -b feature/my-feature
```

2. **Make Changes**
- Write code
- Add tests
- Update documentation

3. **Test**
```bash
# Backend
pytest

# Frontend
yarn test
```

4. **Commit**
```bash
git add .
git commit -m "feat: add my feature"
```

5. **Push**
```bash
git push origin feature/my-feature
```

6. **Create Pull Request**
- Describe changes
- Link related issues
- Request review

### Commit Messages

**Format:**
```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Example:**
```
feat(chatbots): add model selection

- Add dropdown for AI model selection
- Support OpenAI, Claude, and Gemini
- Update API to accept model parameter

Closes #123
```

---

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check MongoDB
mongod --version
sudo systemctl start mongodb

# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check logs
tail -f /var/log/supervisor/backend.err.log
```

**Frontend build errors:**
```bash
# Clear cache
rm -rf node_modules
rm yarn.lock
yarn install

# Check Node version
node --version

# Update dependencies
yarn upgrade
```

**Database connection errors:**
```bash
# Check MongoDB status
sudo systemctl status mongodb

# Restart MongoDB
sudo systemctl restart mongodb

# Check connection
mongo --eval "db.version()"
```

---

**Need help?** Contact the development team or open an issue on GitHub.