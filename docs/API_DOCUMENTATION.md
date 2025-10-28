# 📡 BotSmith API Documentation

## Base URL
```
http://localhost:8001/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🤖 Chatbots

### Create Chatbot
```http
POST /api/chatbots
```

**Request Body:**
```json
{
  "name": "Customer Support Bot",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "system_message": "You are a helpful customer support assistant.",
  "primary_color": "#9333ea",
  "secondary_color": "#ec4899",
  "logo_url": "https://example.com/logo.png",
  "avatar_url": "https://example.com/avatar.png",
  "welcome_message": "Hello! How can I help you today?",
  "widget_position": "bottom-right",
  "theme": "light"
}
```

**Response:**
```json
{
  "id": "chatbot-uuid",
  "name": "Customer Support Bot",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "is_active": true,
  "created_at": "2025-01-28T10:30:00Z"
}
```

### List Chatbots
```http
GET /api/chatbots
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": "chatbot-uuid",
    "name": "Customer Support Bot",
    "model": "gpt-4o-mini",
    "provider": "openai",
    "is_active": true,
    "sources_count": 5,
    "conversations_count": 120,
    "created_at": "2025-01-28T10:30:00Z"
  }
]
```

### Get Chatbot
```http
GET /api/chatbots/{chatbot_id}
```

**Response:**
```json
{
  "id": "chatbot-uuid",
  "name": "Customer Support Bot",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "system_message": "You are a helpful assistant.",
  "primary_color": "#9333ea",
  "secondary_color": "#ec4899",
  "logo_url": "https://example.com/logo.png",
  "welcome_message": "Hello!",
  "widget_position": "bottom-right",
  "theme": "light",
  "is_active": true,
  "sources_count": 5,
  "created_at": "2025-01-28T10:30:00Z"
}
```

### Update Chatbot
```http
PUT /api/chatbots/{chatbot_id}
```

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Bot Name",
  "model": "gpt-4o",
  "system_message": "New system message",
  "is_active": false
}
```

### Delete Chatbot
```http
DELETE /api/chatbots/{chatbot_id}
```

**Response:**
```json
{
  "message": "Chatbot deleted successfully"
}
```

---

## 📚 Sources (Knowledge Base)

### Add File Source
```http
POST /api/sources/file
```

**Request:** multipart/form-data
- `chatbot_id` (string): Chatbot UUID
- `file` (file): File to upload (PDF, DOCX, TXT, XLSX, CSV)

**Response:**
```json
{
  "id": "source-uuid",
  "chatbot_id": "chatbot-uuid",
  "type": "file",
  "name": "documentation.pdf",
  "status": "processing",
  "file_size": 2048576,
  "created_at": "2025-01-28T10:30:00Z"
}
```

### Add Website Source
```http
POST /api/sources/website
```

**Request Body:**
```json
{
  "chatbot_id": "chatbot-uuid",
  "url": "https://example.com/help"
}
```

**Response:**
```json
{
  "id": "source-uuid",
  "chatbot_id": "chatbot-uuid",
  "type": "website",
  "url": "https://example.com/help",
  "status": "processing",
  "created_at": "2025-01-28T10:30:00Z"
}
```

### Add Text Source
```http
POST /api/sources/text
```

**Request Body:**
```json
{
  "chatbot_id": "chatbot-uuid",
  "name": "Company Policies",
  "content": "Our company policies are..."
}
```

### List Sources
```http
GET /api/sources/{chatbot_id}
```

**Response:**
```json
[
  {
    "id": "source-uuid",
    "type": "file",
    "name": "documentation.pdf",
    "status": "completed",
    "file_size": 2048576,
    "created_at": "2025-01-28T10:30:00Z"
  },
  {
    "id": "source-uuid-2",
    "type": "website",
    "url": "https://example.com/help",
    "status": "completed",
    "created_at": "2025-01-28T10:35:00Z"
  }
]
```

### Delete Source
```http
DELETE /api/sources/{source_id}
```

---

## 💬 Chat

### Send Message
```http
POST /api/chat
```

**Request Body:**
```json
{
  "chatbot_id": "chatbot-uuid",
  "message": "What are your business hours?",
  "session_id": "session-uuid",
  "user_info": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Response:**
```json
{
  "response": "Our business hours are Monday to Friday, 9 AM to 5 PM EST.",
  "session_id": "session-uuid",
  "conversation_id": "conversation-uuid",
  "timestamp": "2025-01-28T10:30:00Z"
}
```

### Get Conversations
```http
GET /api/chat/conversations/{chatbot_id}
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Results per page

**Response:**
```json
[
  {
    "id": "conversation-uuid",
    "chatbot_id": "chatbot-uuid",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "status": "active",
    "message_count": 12,
    "started_at": "2025-01-28T10:30:00Z",
    "last_message_at": "2025-01-28T11:15:00Z"
  }
]
```

### Get Messages
```http
GET /api/chat/messages/{conversation_id}
```

**Response:**
```json
[
  {
    "id": "message-uuid",
    "role": "user",
    "content": "What are your business hours?",
    "timestamp": "2025-01-28T10:30:00Z"
  },
  {
    "id": "message-uuid-2",
    "role": "assistant",
    "content": "Our business hours are Monday to Friday, 9 AM to 5 PM EST.",
    "timestamp": "2025-01-28T10:30:05Z"
  }
]
```

---

## 📊 Analytics

### Dashboard Analytics
```http
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "total_conversations": 1250,
  "total_messages": 8750,
  "active_chatbots": 5,
  "total_chatbots": 8,
  "avg_response_time": 1.2,
  "satisfaction_rate": 4.5
}
```

### Chatbot Analytics
```http
GET /api/analytics/chatbot/{chatbot_id}
```

**Query Parameters:**
- `start_date` (string): ISO format date
- `end_date` (string): ISO format date

**Response:**
```json
{
  "chatbot_id": "chatbot-uuid",
  "period": {
    "start": "2025-01-01",
    "end": "2025-01-28"
  },
  "conversations": 350,
  "messages": 2450,
  "avg_response_time": 1.1,
  "satisfaction_rate": 4.6,
  "top_questions": [
    {
      "question": "What are your business hours?",
      "count": 45
    }
  ]
}
```

### Response Time Trend
```http
GET /api/analytics/response-time-trend/{chatbot_id}
```

**Query Parameters:**
- `days` (int): 7, 30, or 90 (default: 7)

**Response:**
```json
[
  {
    "date": "2025-01-28",
    "avg_response_time": 1.2
  },
  {
    "date": "2025-01-27",
    "avg_response_time": 1.1
  }
]
```

### Hourly Activity
```http
GET /api/analytics/hourly-activity/{chatbot_id}
```

**Query Parameters:**
- `days` (int): Number of days to analyze (default: 30)

**Response:**
```json
[
  {
    "hour": 0,
    "message_count": 45
  },
  {
    "hour": 1,
    "message_count": 12
  }
]
```

### Top Questions
```http
GET /api/analytics/top-questions/{chatbot_id}
```

**Query Parameters:**
- `limit` (int): Number of top questions (default: 10)

**Response:**
```json
[
  {
    "question": "What are your business hours?",
    "count": 45
  },
  {
    "question": "How do I reset my password?",
    "count": 38
  }
]
```

---

## 👥 Admin - User Management

### List Users (Enhanced)
```http
GET /api/admin/users/enhanced
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Results per page
- `search` (string): Search by name/email
- `status` (string): Filter by status (active/suspended/banned)
- `role` (string): Filter by role (user/moderator/admin)
- `sort_by` (string): Sort field (created_at/last_login/name)

**Response:**
```json
{
  "users": [
    {
      "id": "user-uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "user",
      "status": "active",
      "chatbot_count": 3,
      "message_count": 150,
      "created_at": "2025-01-15T08:00:00Z",
      "last_login": "2025-01-28T10:30:00Z"
    }
  ],
  "total": 125
}
```

### Get User Details
```http
GET /api/admin/users/{user_id}/details
```

### Update User
```http
PUT /api/admin/users/{user_id}/update
```

**Request Body:**
```json
{
  "role": "moderator",
  "status": "active",
  "phone": "+1234567890",
  "custom_limits": {
    "chatbots": 10,
    "messages": 5000
  },
  "admin_notes": "VIP customer"
}
```

### Delete User
```http
DELETE /api/admin/users/{user_id}
```

### Reset User Password
```http
POST /api/admin/users/{user_id}/reset-password
```

**Request Body:**
```json
{
  "new_password": "SecurePassword123!"
}
```

### Get User Activity Logs
```http
GET /api/admin/users/{user_id}/activity
```

### Get Login History
```http
GET /api/admin/users/{user_id}/login-history
```

### Bulk Operations
```http
POST /api/admin/users/bulk-operation
```

**Request Body:**
```json
{
  "operation": "delete",
  "user_ids": ["user-uuid-1", "user-uuid-2"]
}
```

Operations: `delete`, `change_role`, `change_status`, `export`

---

## 🌐 Public Chat

### Send Public Message
```http
POST /api/public/chat/{chatbot_id}
```

**Request Body:**
```json
{
  "message": "Hello, I need help",
  "session_id": "session-uuid",
  "user_info": {
    "name": "Anonymous User",
    "email": "user@example.com"
  }
}
```

**Note:** No authentication required for public chat endpoints.

---

## ⚙️ User Settings

### Get Current User
```http
GET /api/user/me
```

### Update Profile
```http
PUT /api/user/profile
```

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "company": "Acme Inc"
}
```

### Change Email
```http
PUT /api/user/email
```

**Request Body:**
```json
{
  "email": "newemail@example.com"
}
```

### Change Password
```http
PUT /api/user/password
```

**Request Body:**
```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}
```

### Delete Account
```http
DELETE /api/user/account
```

---

## 📥 Export Data

### Export Conversations
```http
GET /api/export/conversations/{chatbot_id}
```

**Query Parameters:**
- `format` (string): `json` or `csv`
- `start_date` (string): ISO format
- `end_date` (string): ISO format

**Response:** File download

---

## ❌ Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

## 🔄 Rate Limiting

Rate limits (per IP/user):
- Chat endpoints: 60 requests/minute
- Analytics: 30 requests/minute
- Admin operations: 100 requests/minute
- Public endpoints: 30 requests/minute

---

## 📝 Notes

1. All timestamps are in UTC ISO 8601 format
2. UUIDs are used for all resource identifiers
3. File uploads limited to 100MB
4. Supported file types: PDF, DOCX, TXT, XLSX, CSV
5. Website scraping respects robots.txt
6. All API requests must include `/api` prefix