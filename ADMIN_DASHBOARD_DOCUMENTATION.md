# Admin Dashboard - Complete Feature Documentation

## Overview
The BotSmith Admin Dashboard provides comprehensive management capabilities for the entire chatbot platform. Located at `/admin`, it offers powerful tools for monitoring, managing, and analyzing all aspects of the system.

## Core Features Implemented

### 1. **Dashboard Overview (Stats Cards)**
- **Total Users**: Shows unique user count across the platform
- **Active Chatbots**: Displays count of all chatbots in the system
- **Total Messages**: Aggregate message count across all conversations
- **Active Integrations**: Count of AI providers being used
- **Quick Stats**: Real-time overview of sources and flagged content
- **Recent Sources**: Last 5 sources added to the system
- **Flagged Conversations**: List of conversations requiring moderation

### 2. **User Management**
**Features:**
- View all users with detailed statistics
- Search users by ID or email
- User metrics: chatbots count, messages count, conversations count
- View user plan and status
- Delete user and all associated data (chatbots, sources, conversations, messages)

**API Endpoints:**
- `GET /api/admin/users/detailed` - Get all users with detailed stats
- `PUT /api/admin/users/{user_id}` - Update user plan and limits
- `DELETE /api/admin/users/{user_id}` - Delete user and all data

**User Table Columns:**
- User ID
- Email
- Plan (Free/Starter/Professional/Enterprise)
- Chatbots count
- Messages count
- Conversations count
- Status (active/inactive)
- Actions (delete)

### 3. **Chatbot Management**
**Features:**
- View all chatbots across all users
- Search chatbots by name or owner
- Enable/disable individual chatbots
- Bulk operations: enable, disable, delete multiple chatbots
- View detailed metrics per chatbot
- Multi-select with checkboxes

**API Endpoints:**
- `GET /api/admin/chatbots/detailed` - Get all chatbots with detailed stats
- `PUT /api/admin/chatbots/{chatbot_id}/toggle` - Enable/disable chatbot
- `POST /api/admin/chatbots/bulk` - Bulk operations (delete, enable, disable)

**Chatbot Table Columns:**
- Checkbox for bulk selection
- Name
- Owner (user_id)
- AI Provider (OpenAI, Claude, Gemini)
- AI Model
- Sources count
- Conversations count
- Messages count
- Status (enabled/disabled)
- Actions (toggle enable/disable)

**Bulk Operations:**
- Select multiple chatbots
- Enable selected chatbots
- Disable selected chatbots
- Delete selected chatbots

### 4. **Conversations Management**
**Features:**
- View all conversations across all chatbots
- Advanced filtering:
  - By chatbot ID
  - By status (active/resolved/escalated)
  - By date range (start date - end date)
- Export conversations:
  - JSON format (includes full message history)
  - CSV format (summary data)
- Clear filters functionality
- Conversation limit: 100 per query

**API Endpoints:**
- `GET /api/admin/conversations` - Get conversations with filters
- `GET /api/admin/conversations/export` - Export conversations (JSON/CSV)

**Conversation Table Columns:**
- Conversation ID
- Chatbot ID
- User name
- User email
- Status badge (color-coded)
- Message count
- Created date

**Filter Options:**
- Status dropdown: All, Active, Resolved, Escalated
- Start date picker
- End date picker
- Clear all filters button

### 5. **Sources Management**
**Features:**
- View all sources (files, websites, text) across all chatbots
- Source details: name, type, chatbot, size, status, date
- Delete individual sources
- View file sizes in KB

**API Endpoints:**
- `GET /api/admin/sources` - Get all sources
- `DELETE /api/admin/sources/{source_id}` - Delete a source

**Source Table Columns:**
- Name
- Type (file/website/text)
- Chatbot ID
- File size (KB)
- Status
- Created date
- Actions (delete)

### 6. **System Monitoring** (Real-time)
**Features:**
- Auto-refresh every 10 seconds (toggleable)
- Manual refresh button

**System Health Monitoring:**
- **CPU Usage**: Percentage with color-coded progress bar
  - Green: < 50%
  - Yellow: 50-75%
  - Red: > 75%
- **Memory Usage**: Percentage + available MB
- **Disk Usage**: Percentage + free GB
- **System Status**: Healthy/Error badge
- Last updated timestamp

**Real-time Activity (Last Hour):**
- New conversations count
- Messages sent count
- Recent activity log (last 10 activities)
  - User name
  - Activity type
  - Timestamp

**Database Statistics:**
- Document counts:
  - Chatbots
  - Sources
  - Conversations
  - Messages
  - Total documents
- Collection details table:
  - Collection name
  - Document count
  - Size (bytes)
  - Average document size

**API Endpoints:**
- `GET /api/admin/system/health` - System health metrics
- `GET /api/admin/system/activity` - Real-time activity
- `GET /api/admin/database/stats` - Database statistics

### 7. **Content Moderation**
**Features:**
- View flagged/escalated conversations
- Review conversation details:
  - User information
  - Conversation ID
  - Status badge
  - Flag reason
  - Full message history
- Message thread view with role differentiation (user/assistant)
- Scrollable message area for long conversations

**API Endpoints:**
- `GET /api/admin/moderation/flagged` - Get flagged conversations

**Display:**
- Conversation cards with:
  - User name
  - Conversation ID
  - Status badge (red for escalated)
  - Flag reason description
  - Expandable message history
  - Role-based styling (blue for user, gray for assistant)

### 8. **Analytics Tab**
**Prepared for:**
- System-wide analytics
- Provider usage statistics
- Conversation trends over time
- Custom reports

## Technical Implementation

### Backend Architecture
**File:** `/app/backend/routers/admin.py`

**Dependencies:**
- FastAPI for API endpoints
- Motor (async MongoDB driver)
- psutil for system monitoring
- CSV and JSON export functionality

**Key Features:**
- Async/await patterns for non-blocking operations
- MongoDB aggregation pipelines for complex queries
- Streaming responses for file exports
- Error handling with try-catch blocks
- System resource monitoring

### Frontend Architecture
**Main File:** `/app/frontend/src/pages/admin/AdminDashboard.jsx`

**Component Files:**
- `/app/frontend/src/components/admin/UsersManagement.jsx`
- `/app/frontend/src/components/admin/ChatbotsManagement.jsx`
- `/app/frontend/src/components/admin/ConversationsManagement.jsx`
- `/app/frontend/src/components/admin/SystemMonitoring.jsx`

**UI Framework:**
- React with Hooks (useState, useEffect)
- Tailwind CSS for styling
- Lucide React for icons
- Custom UI components (Button, Tabs)

**Features:**
- Tab-based navigation
- Real-time data fetching
- Search and filter functionality
- Responsive design
- Loading states
- Empty states with icons
- Color-coded status indicators
- Confirmation dialogs for destructive actions

## Security Considerations

### Current Implementation:
- Demo mode with default admin user
- No authentication required for `/admin` route

### Production Recommendations:
1. **Add Authentication:**
   - Implement admin login system
   - Use JWT tokens for session management
   - Role-based access control (RBAC)

2. **API Security:**
   - Add API key authentication
   - Rate limiting for admin endpoints
   - Audit logging for all admin actions

3. **Data Protection:**
   - Encrypt sensitive data
   - Implement backup before delete operations
   - Add undo functionality for critical operations

## Usage Guide

### Accessing Admin Dashboard
1. Navigate to `https://deps-quickview.preview.emergentagent.com/admin`
2. Dashboard loads with overview tab by default
3. Use tab navigation to access different sections

### Common Tasks

**Managing Users:**
1. Click "Users" tab
2. Search for specific user
3. View user statistics
4. Click delete to remove user (confirmation required)

**Managing Chatbots:**
1. Click "Chatbots" tab
2. Search or browse chatbots
3. Select multiple chatbots using checkboxes
4. Use bulk actions: Enable, Disable, or Delete
5. Toggle individual chatbot status

**Viewing Conversations:**
1. Click "Conversations" tab
2. Apply filters (status, date range)
3. Export data using JSON or CSV buttons
4. Clear filters to see all conversations

**Monitoring System:**
1. Click "Monitoring" tab
2. View real-time system health
3. Check database statistics
4. Enable auto-refresh for live updates

**Reviewing Flagged Content:**
1. Click "Moderation" tab
2. Review flagged conversations
3. Read full message history
4. Take appropriate action

## API Reference

### Stats Endpoint
```
GET /api/admin/stats
Response: {
  totalUsers: number,
  activeChatbots: number,
  totalMessages: number,
  activeIntegrations: number
}
```

### Users Endpoint
```
GET /api/admin/users/detailed
Response: {
  users: Array<{
    user_id: string,
    email: string,
    chatbots_count: number,
    messages_count: number,
    conversations_count: number,
    plan: string,
    status: string
  }>,
  total: number
}
```

### Chatbots Endpoints
```
GET /api/admin/chatbots/detailed
PUT /api/admin/chatbots/{id}/toggle
POST /api/admin/chatbots/bulk
Body: { ids: string[], operation: 'delete'|'enable'|'disable' }
```

### Conversations Endpoints
```
GET /api/admin/conversations?status=&start_date=&end_date=
GET /api/admin/conversations/export?format=json|csv
```

### System Monitoring Endpoints
```
GET /api/admin/system/health
GET /api/admin/system/activity
GET /api/admin/database/stats
```

### Sources Endpoints
```
GET /api/admin/sources
DELETE /api/admin/sources/{id}
```

### Moderation Endpoint
```
GET /api/admin/moderation/flagged
```

## Future Enhancements

### Planned Features:
1. **Advanced Analytics:**
   - Charts and graphs for trends
   - Revenue analytics
   - User growth metrics
   - AI provider performance comparison

2. **AI Provider Management:**
   - Configure API keys
   - Set rate limits
   - Monitor usage and costs
   - Enable/disable providers

3. **Automated Actions:**
   - Auto-flagging based on keywords
   - Automatic backup schedules
   - Alert notifications
   - Webhook integrations

4. **Enhanced User Management:**
   - Edit user details
   - Manual plan assignment
   - Usage limit overrides
   - User activity timeline

5. **Audit Logs:**
   - Track all admin actions
   - User login history
   - Data modification logs
   - Export audit trails

6. **System Configuration:**
   - Global settings management
   - Email template editor
   - Customizable limits
   - Feature flags

## Performance Optimization

### Current Optimizations:
- Async database operations
- Pagination for large datasets (limit: 100)
- Efficient MongoDB queries
- Auto-refresh with configurable intervals

### Recommended Optimizations:
- Implement pagination UI for large tables
- Add database indexing for frequently queried fields
- Cache frequently accessed data
- Implement lazy loading for tabs
- Add virtual scrolling for long lists

## Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Support
For issues or questions, contact the development team or refer to the main application documentation.
