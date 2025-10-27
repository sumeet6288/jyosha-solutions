# BotSmith Database Structure

## Database Overview
- **Database System**: MongoDB (NoSQL Document Database)
- **Databases**: 
  - `chatbase_db` - Main application database
  - `botsmith` - Plans and subscriptions database

---

## Collections & Schema

### Database: `chatbase_db`

#### 1. **users** Collection
Stores all user account information, profiles, and admin settings.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique user identifier | UUID v4 |
| `name` | String | User's full name | Required |
| `email` | EmailStr | User's email address | Required, unique |
| `password_hash` | String | Hashed password | Required |
| `created_at` | DateTime | Account creation timestamp | UTC timestamp |
| `updated_at` | DateTime | Last update timestamp | UTC timestamp |
| **Role & Permissions** | | | |
| `role` | String | User role | "user" / "moderator" / "admin" |
| **Account Status** | | | |
| `status` | String | Account status | "active" / "suspended" / "banned" |
| `suspension_reason` | String (Optional) | Reason for suspension | Null |
| `suspension_until` | DateTime (Optional) | Suspension end date | Null |
| **Profile Information** | | | |
| `phone` | String (Optional) | Phone number | Null |
| `address` | String (Optional) | Physical address | Null |
| `bio` | String (Optional) | User biography | Null |
| `avatar_url` | String (Optional) | Profile picture URL | Null |
| `company` | String (Optional) | Company name | Null |
| `job_title` | String (Optional) | Job title | Null |
| **Custom Usage Limits** | | | |
| `custom_max_chatbots` | Integer (Optional) | Override plan chatbot limit | Null |
| `custom_max_messages` | Integer (Optional) | Override plan message limit | Null |
| `custom_max_file_uploads` | Integer (Optional) | Override plan file limit | Null |
| **Activity Tracking** | | | |
| `last_login` | DateTime (Optional) | Last login timestamp | Null |
| `login_count` | Integer | Total login count | 0 |
| `last_ip` | String (Optional) | Last login IP address | Null |
| **Tags & Notes** | | | |
| `tags` | Array[String] | Admin tags for categorization | [] |
| `admin_notes` | String (Optional) | Internal admin notes | Null |

**Indexes**: 
- `id` (unique)
- `email` (unique)
- `status`
- `role`

---

#### 2. **chatbots** Collection
Stores chatbot configurations and settings.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique chatbot identifier | UUID v4 |
| `user_id` | String | Owner's user ID | Required, FK to users |
| `name` | String | Chatbot name | Required |
| `status` | String | Chatbot status | "active" / "inactive" |
| **AI Configuration** | | | |
| `model` | String | AI model name | "gpt-4o-mini" |
| `provider` | String | AI provider | "openai" / "anthropic" / "gemini" |
| `temperature` | Float | Response randomness | 0.7 (0.0-1.0) |
| `instructions` | String | System prompt/instructions | "You are a helpful assistant." |
| `welcome_message` | String | Initial greeting message | "Hello! How can I help you today?" |
| **Statistics** | | | |
| `conversations_count` | Integer | Total conversations | 0 |
| `messages_count` | Integer | Total messages processed | 0 |
| `created_at` | DateTime | Creation timestamp | UTC timestamp |
| `updated_at` | DateTime | Last update timestamp | UTC timestamp |
| `last_trained` | DateTime (Optional) | Last training/update time | Null |
| **Visual Customization** | | | |
| `primary_color` | String (Hex) | Main theme color | "#7c3aed" (purple) |
| `secondary_color` | String (Hex) | Secondary theme color | "#a78bfa" (light purple) |
| `accent_color` | String (Hex) | Accent color | "#ec4899" (pink) |
| `logo_url` | String (Optional) | Brand logo URL | Null |
| `avatar_url` | String (Optional) | Chatbot avatar URL | Null |
| **Widget Configuration** | | | |
| `widget_position` | String | Widget screen position | "bottom-right" / "bottom-left" / "top-right" / "top-left" |
| `widget_theme` | String | Widget color theme | "light" / "dark" / "auto" |
| `font_family` | String | Text font family | "Inter, system-ui, sans-serif" |
| `font_size` | String | Text size setting | "small" / "medium" / "large" |
| `bubble_style` | String | Chat bubble style | "rounded" / "square" / "smooth" |
| `widget_size` | String | Widget size | "small" / "medium" / "large" |
| `auto_expand` | Boolean | Auto-expand on load | false |
| **Sharing & Integration** | | | |
| `public_access` | Boolean | Public access enabled | false |
| `webhook_url` | String (Optional) | Webhook endpoint URL | Null |
| `webhook_enabled` | Boolean | Webhook notifications | false |

**Indexes**: 
- `id` (unique)
- `user_id`
- `status`

---

#### 3. **sources** Collection
Stores knowledge base sources (files, websites, text).

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique source identifier | UUID v4 |
| `chatbot_id` | String | Parent chatbot ID | Required, FK to chatbots |
| `type` | String | Source type | "file" / "website" / "text" |
| `name` | String | Source name/title | Required |
| `content` | String | Processed/extracted content | "" |
| `size` | String (Optional) | File size (for files) | Null |
| `url` | String (Optional) | Source URL (for websites) | Null |
| `status` | String | Processing status | "processing" / "processed" / "failed" |
| `error_message` | String (Optional) | Error details if failed | Null |
| `added_at` | DateTime | Addition timestamp | UTC timestamp |

**Indexes**: 
- `id` (unique)
- `chatbot_id`
- `type`
- `status`

---

#### 4. **conversations** Collection
Stores chat conversation metadata.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique conversation identifier | UUID v4 |
| `chatbot_id` | String | Related chatbot ID | Required, FK to chatbots |
| `session_id` | String | User session identifier | Required |
| `user_name` | String (Optional) | User's name | Null |
| `user_email` | String (Optional) | User's email | Null |
| `status` | String | Conversation status | "active" / "resolved" / "escalated" |
| `messages_count` | Integer | Number of messages | 0 |
| `created_at` | DateTime | Start timestamp | UTC timestamp |
| `updated_at` | DateTime | Last message timestamp | UTC timestamp |

**Indexes**: 
- `id` (unique)
- `chatbot_id`
- `session_id`
- `status`

---

#### 5. **messages** Collection
Stores individual chat messages.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique message identifier | UUID v4 |
| `conversation_id` | String | Parent conversation ID | Required, FK to conversations |
| `chatbot_id` | String | Related chatbot ID | Required, FK to chatbots |
| `role` | String | Message sender role | "user" / "assistant" |
| `content` | String | Message text content | Required |
| `timestamp` | DateTime | Message timestamp | UTC timestamp |

**Indexes**: 
- `id` (unique)
- `conversation_id`
- `chatbot_id`
- `timestamp`

---

#### 6. **conversation_ratings** Collection
Stores user satisfaction ratings for conversations.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique rating identifier | UUID v4 |
| `conversation_id` | String | Related conversation ID | Required, FK to conversations |
| `chatbot_id` | String | Related chatbot ID | Required, FK to chatbots |
| `rating` | Integer | Star rating | 1-5 (required) |
| `feedback` | String (Optional) | User feedback text | Null |
| `created_at` | DateTime | Rating timestamp | UTC timestamp |

**Indexes**: 
- `id` (unique)
- `conversation_id`
- `chatbot_id`
- `rating`

---

#### 7. **analytics** Collection
Stores daily analytics data per chatbot.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique analytics record ID | UUID v4 |
| `chatbot_id` | String | Related chatbot ID | Required, FK to chatbots |
| `date` | Date | Analytics date | Required |
| `total_conversations` | Integer | Conversations that day | 0 |
| `total_messages` | Integer | Messages that day | 0 |
| `active_chats` | Integer | Active chats that day | 0 |
| `avg_response_time` | Float | Avg response time (seconds) | 0.0 |
| `satisfaction_rate` | Float | Average satisfaction (%) | 0.0 |

**Indexes**: 
- `id` (unique)
- `chatbot_id` + `date` (compound, unique)

---

#### 8. **login_history** Collection
Tracks user login attempts and sessions.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique login record ID | UUID v4 |
| `user_id` | String | Related user ID | Required, FK to users |
| `timestamp` | DateTime | Login timestamp | UTC timestamp |
| `ip_address` | String (Optional) | Login IP address | Null |
| `user_agent` | String (Optional) | Browser/device info | Null |
| `location` | String (Optional) | Geographic location | Null |
| `success` | Boolean | Login success/failure | true |

**Indexes**: 
- `id` (unique)
- `user_id`
- `timestamp`

---

#### 9. **activity_logs** Collection
Tracks all user actions and system events.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String (UUID) | Unique activity log ID | UUID v4 |
| `user_id` | String | User who performed action | Required, FK to users |
| `action` | String | Action type | "created_chatbot", "deleted_source", etc. |
| `resource_type` | String (Optional) | Resource affected | "chatbot", "source", "user", etc. |
| `resource_id` | String (Optional) | ID of affected resource | Null |
| `details` | String (Optional) | Additional details | Null |
| `timestamp` | DateTime | Action timestamp | UTC timestamp |
| `ip_address` | String (Optional) | Request IP address | Null |

**Indexes**: 
- `id` (unique)
- `user_id`
- `action`
- `timestamp`

---

### Database: `botsmith`

#### 10. **plans** Collection
Stores subscription plan definitions.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `id` | String | Plan identifier | "free" / "starter" / "professional" / "enterprise" |
| `name` | String | Plan display name | Required |
| `price` | Float | Monthly price (USD) | 0 for free, -1 for custom |
| `description` | String | Plan description | Required |
| **Limits Object** | | | |
| `limits.max_chatbots` | Integer | Max chatbots allowed | Required |
| `limits.max_messages_per_month` | Integer | Max messages/month | Required |
| `limits.max_file_uploads` | Integer | Max file uploads | Required |
| `limits.max_file_size_mb` | Integer | Max file size (MB) | Required |
| `limits.max_website_sources` | Integer | Max website sources | Required |
| `limits.max_text_sources` | Integer | Max text sources | Required |
| `limits.conversation_history_days` | Integer | Days to keep history | Required |
| `limits.allowed_ai_providers` | Array[String] | Allowed AI providers | ["openai"] |
| `limits.api_access` | Boolean | API access enabled | false |
| `limits.custom_branding` | Boolean | Custom branding enabled | false |
| `limits.analytics_level` | String | Analytics level | "basic" / "advanced" |
| `limits.support_level` | String | Support tier | "community" / "email" / "priority" |
| **Other Fields** | | | |
| `features` | Array[String] | List of features | [] |
| `is_active` | Boolean | Plan availability | true |
| `created_at` | DateTime | Plan creation timestamp | UTC timestamp |

**Indexes**: 
- `id` (unique)
- `is_active`

**Sample Plans**:
- **Free**: 1 chatbot, 100 msgs/month, $0
- **Starter**: 5 chatbots, 5,000 msgs/month, $150/month
- **Professional**: 20 chatbots, 50,000 msgs/month, $499/month
- **Enterprise**: Unlimited, custom pricing

---

#### 11. **subscriptions** Collection
Stores user subscription information and usage tracking.

| Field | Type | Description | Default/Constraints |
|-------|------|-------------|---------------------|
| `_id` | ObjectId | MongoDB auto-generated ID | Auto |
| `user_id` | String | Subscriber user ID | Required, FK to users |
| `plan_id` | String | Current plan ID | Required, FK to plans |
| `status` | String | Subscription status | "active" / "canceled" / "expired" |
| `started_at` | DateTime | Subscription start date | UTC timestamp |
| `expires_at` | DateTime (Optional) | Expiration date | Null for active |
| `auto_renew` | Boolean | Auto-renewal enabled | true |
| **Usage Object** | | | |
| `usage.chatbots_count` | Integer | Current chatbot count | 0 |
| `usage.messages_this_month` | Integer | Messages this month | 0 |
| `usage.file_uploads_count` | Integer | File uploads count | 0 |
| `usage.website_sources_count` | Integer | Website sources count | 0 |
| `usage.text_sources_count` | Integer | Text sources count | 0 |
| `usage.last_reset` | DateTime | Last usage reset date | UTC timestamp |

**Indexes**: 
- `user_id` (unique)
- `plan_id`
- `status`

---

## Relationships Diagram

```
users (chatbase_db)
  └─── chatbots
         ├─── sources (knowledge base files/websites/text)
         ├─── conversations
         │      ├─── messages
         │      └─── conversation_ratings
         └─── analytics (daily stats)

users (chatbase_db)
  ├─── login_history
  ├─── activity_logs
  └─── subscriptions (botsmith)
         └─── plans (botsmith)
```

## Key Features

### Multi-Tenancy
- Each user can have multiple chatbots
- Each chatbot is isolated by `user_id`
- Proper indexing ensures fast queries

### Knowledge Base
- Supports 3 source types: files, websites, text
- Content is processed and stored in `content` field
- Async processing with status tracking

### Analytics & Insights
- Daily analytics aggregation
- Conversation ratings (1-5 stars)
- Activity tracking for audit trail
- Login history for security

### Subscription Management
- Plan-based limits enforcement
- Custom override limits per user (admin feature)
- Usage tracking per subscription period
- Auto-renewal support

### Admin Features
- User role management (user/moderator/admin)
- Account status control (active/suspended/banned)
- Activity logging for all actions
- Login history tracking
- Custom limits per user

---

## Sample Queries

### Get all chatbots for a user
```javascript
db.chatbots.find({ user_id: "user-uuid-here" })
```

### Get conversation history with messages
```javascript
// Get conversation
const conversation = db.conversations.findOne({ id: "conv-uuid" })

// Get all messages
db.messages.find({ conversation_id: conversation.id }).sort({ timestamp: 1 })
```

### Get user's subscription and limits
```javascript
const subscription = db.subscriptions.findOne({ user_id: "user-uuid" })
const plan = db.plans.findOne({ id: subscription.plan_id })
```

### Get analytics for date range
```javascript
db.analytics.find({
  chatbot_id: "chatbot-uuid",
  date: { $gte: ISODate("2025-01-01"), $lte: ISODate("2025-01-31") }
})
```

---

## Notes

- All IDs use UUID v4 format (except MongoDB's internal `_id`)
- All timestamps are in UTC
- MongoDB ObjectIDs are NOT used as primary keys to ensure JSON serialization compatibility
- Indexes are crucial for query performance on large datasets
- The app uses mocked authentication in development (demo-user-123)
