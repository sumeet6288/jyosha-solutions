# BotSmith Replica - API Contracts & Integration Plan

## Overview
This document outlines the API contracts, data models, and integration plan for the BotSmith replica application.

## Current Frontend Implementation

### Pages Built (with Mock Data)
1. **Landing Page** - Marketing page with features and CTA
2. **Sign In/Sign Up** - Authentication forms (currently using localStorage)
3. **Dashboard** - Overview with analytics cards and chatbot list
4. **Chatbot Builder** - Multi-tab interface for managing chatbots
   - Sources tab: Upload files, add websites, manage training data
   - Settings tab: Configure model, instructions, temperature
   - Widget tab: Customize appearance and get embed code
   - Analytics tab: Placeholder for analytics

### Mock Data Location
All mock data is in `/app/frontend/src/mock/mockData.js`:
- `mockChatbots`: List of chatbots with stats
- `mockAnalytics`: Dashboard analytics data
- `mockSources`: Training data sources
- `mockConversations`: Chat history
- `mockChatMessages`: Individual chat messages

## Data Models

### User
```python
{
    "id": str,
    "name": str,
    "email": str,
    "password_hash": str,
    "created_at": datetime
}
```

### Chatbot
```python
{
    "id": str,
    "user_id": str,
    "name": str,
    "status": str,  # "active" | "inactive"
    "model": str,  # "gpt-4" | "gpt-3.5-turbo" | "claude-3"
    "temperature": float,
    "instructions": str,
    "welcome_message": str,
    "conversations_count": int,
    "created_at": datetime,
    "last_trained": datetime
}
```

### Source
```python
{
    "id": str,
    "chatbot_id": str,
    "type": str,  # "file" | "website" | "text"
    "name": str,
    "content": str,  # Processed content
    "size": str,  # For files
    "url": str,  # For websites
    "status": str,  # "processing" | "processed" | "failed"
    "added_at": datetime
}
```

### Conversation
```python
{
    "id": str,
    "chatbot_id": str,
    "user_name": str,
    "user_email": str,
    "status": str,  # "active" | "resolved" | "escalated"
    "created_at": datetime,
    "updated_at": datetime
}
```

### Message
```python
{
    "id": str,
    "conversation_id": str,
    "role": str,  # "user" | "assistant"
    "content": str,
    "timestamp": datetime
}
```

### Analytics
```python
{
    "chatbot_id": str,
    "date": date,
    "total_conversations": int,
    "active_chats": int,
    "avg_response_time": float,
    "satisfaction_rate": float
}
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user

### Chatbots
- `GET /api/chatbots` - List all user's chatbots
- `POST /api/chatbots` - Create new chatbot
- `GET /api/chatbots/{id}` - Get chatbot details
- `PUT /api/chatbots/{id}` - Update chatbot settings
- `DELETE /api/chatbots/{id}` - Delete chatbot

### Sources
- `GET /api/chatbots/{id}/sources` - List chatbot sources
- `POST /api/chatbots/{id}/sources/file` - Upload file source
- `POST /api/chatbots/{id}/sources/website` - Add website source
- `POST /api/chatbots/{id}/sources/text` - Add text source
- `DELETE /api/sources/{id}` - Delete source

### Conversations
- `GET /api/chatbots/{id}/conversations` - List conversations
- `GET /api/conversations/{id}/messages` - Get conversation messages
- `POST /api/chat` - Send message to chatbot (public endpoint)

### Analytics
- `GET /api/chatbots/{id}/analytics` - Get chatbot analytics
- `GET /api/dashboard/analytics` - Get dashboard overview analytics

## Frontend-Backend Integration Plan

### Phase 1: Authentication
1. Replace localStorage with JWT-based authentication
2. Create auth context/provider in React
3. Store JWT token in localStorage
4. Add token to API requests
5. Implement protected routes properly

### Phase 2: Chatbot Management
1. Replace `mockChatbots` with API calls
2. Implement CRUD operations for chatbots
3. Connect dashboard to real data
4. Connect chatbot builder to real data

### Phase 3: Sources & Training
1. Implement file upload with multipart/form-data
2. Add website scraping functionality
3. Process and store training data
4. Implement text content ingestion

### Phase 4: Chat Functionality
1. Integrate OpenAI API using Emergent LLM key
2. Implement chat endpoint with context from sources
3. Store conversations and messages
4. Add real-time response streaming

### Phase 5: Analytics
1. Track conversation metrics
2. Calculate analytics in background
3. Store aggregated data
4. Connect dashboard and analytics tabs

## Files to Update After Backend Implementation

### Frontend Files
1. `/app/frontend/src/pages/Dashboard.jsx` - Replace mock data with API calls
2. `/app/frontend/src/pages/ChatbotBuilder.jsx` - Connect to API
3. `/app/frontend/src/pages/SignIn.jsx` - Implement real authentication
4. `/app/frontend/src/pages/SignUp.jsx` - Implement real registration
5. Create `/app/frontend/src/contexts/AuthContext.jsx` - Auth state management
6. Create `/app/frontend/src/utils/api.js` - API client helper

### Backend Files to Create
1. `/app/backend/models.py` - MongoDB models using Motor
2. `/app/backend/auth.py` - JWT authentication utilities
3. `/app/backend/routers/auth.py` - Auth endpoints
4. `/app/backend/routers/chatbots.py` - Chatbot CRUD
5. `/app/backend/routers/sources.py` - Sources management
6. `/app/backend/routers/chat.py` - Chat functionality
7. `/app/backend/routers/analytics.py` - Analytics endpoints
8. `/app/backend/services/openai_service.py` - OpenAI integration
9. `/app/backend/services/document_processor.py` - Process uploaded files

## Dependencies to Add

### Backend
- `python-multipart` - Already in requirements.txt
- `python-jose[cryptography]` - Already in requirements.txt
- `passlib[bcrypt]` - Already in requirements.txt
- `emergentintegrations` - For Emergent LLM key integration
- `beautifulsoup4` - For website scraping
- `PyPDF2` or `pypdf` - For PDF processing
- `docx2txt` - For DOCX processing

### Frontend
- No additional dependencies needed (axios already installed)

## Mock Data to Replace

Currently mocked in `/app/frontend/src/mock/mockData.js`:
- User authentication (localStorage)
- Chatbot list and details
- Analytics data
- Sources list
- Conversations and messages

All of these will be replaced with real API calls once backend is implemented.

## Security Considerations
1. JWT tokens with expiration
2. Password hashing with bcrypt
3. Input validation on all endpoints
4. Rate limiting for chat endpoints
5. File upload size limits
6. CORS configuration
7. API key protection (Emergent LLM key in .env)

## Testing Plan
1. Test authentication flow
2. Test chatbot CRUD operations
3. Test file upload and processing
4. Test chat functionality with AI
5. Test analytics calculation
6. Test all frontend integrations
