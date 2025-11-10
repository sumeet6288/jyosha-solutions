# Instagram Integration Guide

## Overview

The Instagram integration allows your chatbot to receive and respond to messages on Instagram Direct Messages (DMs) using the Instagram Messaging API (part of Facebook's Graph API).

## Features

✅ **Receive Instagram DMs** - Your chatbot can receive messages from Instagram users
✅ **Send AI Responses** - Automatically respond to Instagram messages with AI-generated replies
✅ **Knowledge Base Integration** - Responses use your chatbot's knowledge base from uploaded files and websites
✅ **Conversation History** - All conversations are stored and tracked
✅ **Webhook Support** - Real-time message delivery via Instagram webhooks
✅ **Connection Testing** - Verify your credentials before going live

## Backend Implementation

### 1. Models (models.py)

Added Instagram to the Integration model:
```python
integration_type: Literal["slack", "telegram", "discord", "whatsapp", "webchat", "api", "twilio", "messenger", "msteams", "instagram"]
```

Added Instagram-specific models:
```python
class InstagramWebhookSetup(BaseModel):
    base_url: str

class InstagramMessage(BaseModel):
    recipient_id: str  # Instagram user ID
    text: str
```

### 2. Instagram Service (services/instagram_service.py)

The `InstagramService` class provides methods for interacting with Instagram Graph API:

**Key Methods:**
- `send_message(recipient_id, text)` - Send messages to Instagram users
- `verify_token()` - Validate the page access token
- `get_user_profile(user_id)` - Get user profile information
- `set_webhook(webhook_url, verify_token)` - Get webhook setup instructions
- `get_account_info()` - Get Instagram Business Account information

**API Endpoint:** `https://graph.facebook.com/v18.0`

### 3. Instagram Router (routers/instagram.py)

The router handles all Instagram-related endpoints:

#### Endpoints:

**POST `/api/instagram/webhook/{chatbot_id}`**
- Handles webhook verification (GET query params)
- Receives incoming Instagram messages (POST)
- Processes messages in background tasks
- Returns AI-generated responses

**POST `/api/instagram/{chatbot_id}/setup-webhook`**
- Generates webhook URL
- Returns setup instructions
- Logs activity

**GET `/api/instagram/{chatbot_id}/webhook-info`**
- Get current webhook configuration
- Returns webhook URL and verify token

**DELETE `/api/instagram/{chatbot_id}/webhook`**
- Removes webhook configuration
- Disables integration

**POST `/api/instagram/{chatbot_id}/send-test-message`**
- Send test message to verify setup
- Requires recipient_id and text

### 4. Message Processing Flow

1. Instagram sends webhook event to `/api/instagram/webhook/{chatbot_id}`
2. System validates the integration is enabled
3. Extracts sender_id and message_text from webhook payload
4. Creates/retrieves conversation in database
5. Saves user message
6. Fetches relevant knowledge base context using vector store
7. Generates AI response using ChatService (supports OpenAI, Claude, Gemini)
8. Saves assistant message
9. Sends response back to Instagram via InstagramService
10. Updates conversation and subscription usage
11. Logs integration activity

## Frontend Implementation

### 1. Integration Definition (ChatbotIntegrations.jsx)

Added Instagram to `integrationDefinitions`:
```javascript
{
  id: 'instagram',
  name: 'Instagram',
  description: 'Connect your chatbot to Instagram Direct Messages',
  icon: <MessageCircle className="w-6 h-6" />,
  gradient: 'from-pink-500 to-purple-600',
  fields: [
    { name: 'page_access_token', label: 'Page Access Token', type: 'password', required: true },
    { name: 'verify_token', label: 'Verify Token', type: 'text', required: false },
    { name: 'app_secret', label: 'App Secret', type: 'password', required: false }
  ]
}
```

### 2. Webhook Setup Function

Added `handleSetupInstagramWebhook` function:
- Calls `/api/instagram/{chatbot_id}/setup-webhook`
- Displays webhook URL and verify token
- Shows setup instructions in console
- Provides user-friendly toast notifications

### 3. UI Components

**Integration Card:**
- Pink to purple gradient
- Instagram icon
- Setup/Reconfigure button
- Test connection button
- Webhook setup button (⚡)
- Enable/disable toggle
- Delete button

**Setup Modal:**
- Fields for Page Access Token, Verify Token, App Secret
- Masked password fields with show/hide toggle
- Save button with loading state

## Setup Instructions for Users

### Prerequisites

1. **Instagram Business Account** - Must be converted to a Business or Creator account
2. **Facebook Page** - Instagram account must be connected to a Facebook Page
3. **Facebook App** - Create a Facebook App with Instagram Basic Display or Instagram Messaging API
4. **Page Access Token** - Generate a Page Access Token with appropriate permissions

### Step-by-Step Setup

#### 1. Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "My Apps" → "Create App"
3. Select "Business" as app type
4. Fill in app details and create

#### 2. Add Instagram Product

1. In your app dashboard, go to "Products"
2. Find "Instagram" and click "Set Up"
3. Choose "Instagram Basic Display" or "Instagram Messaging"

#### 3. Connect Instagram Account

1. Go to app settings → Basic → Add Platform
2. Configure Instagram account linking
3. Connect your Instagram Business Account

#### 4. Generate Access Token

1. Go to "Instagram" → "Basic Display" (or Messenger)
2. Generate a long-lived Page Access Token
3. Token should have permissions:
   - `pages_messaging`
   - `pages_read_user_content`
   - `instagram_basic`
   - `instagram_manage_messages`

#### 5. Configure in BotSmith

1. Navigate to your chatbot in BotSmith
2. Go to "Integrations" tab
3. Click "Setup" on Instagram card
4. Enter:
   - **Page Access Token**: Your generated token
   - **Verify Token**: Any secret string (e.g., `my_verify_token_123`)
   - **App Secret**: (Optional) Your Facebook App Secret
5. Click "Save"

#### 6. Setup Webhook

1. Click the webhook setup button (⚡) on Instagram integration
2. Copy the Webhook URL and Verify Token from the toast/console
3. Go to Facebook App → Products → Webhooks
4. Click "Add Subscription" for Instagram
5. Enter:
   - **Callback URL**: The webhook URL from BotSmith
   - **Verify Token**: The verify token from BotSmith
6. Subscribe to webhook fields:
   - `messages`
   - `messaging_postbacks`
   - `message_echoes`
7. Save and verify

#### 7. Enable Integration

1. Toggle the "Enable Integration" switch in BotSmith
2. Test connection using the test button
3. Send a test message to your Instagram account
4. Check if the bot responds

## Testing

### Manual Testing

1. **Connection Test**: Click test button to verify credentials
2. **Webhook Verification**: Instagram will call your webhook with verification challenge
3. **Send Message**: DM your Instagram account to test end-to-end flow
4. **Check Logs**: View integration logs in BotSmith for debugging

### Webhook Verification

Instagram sends verification request:
```
GET /api/instagram/webhook/{chatbot_id}?hub.mode=subscribe&hub.challenge=123456&hub.verify_token=your_token
```

Your webhook should respond with the challenge value (as integer).

### Incoming Message Format

Instagram webhook payload:
```json
{
  "entry": [
    {
      "messaging": [
        {
          "sender": { "id": "instagram_user_id" },
          "recipient": { "id": "your_page_id" },
          "timestamp": 1234567890,
          "message": {
            "mid": "message_id",
            "text": "User's message"
          }
        }
      ]
    }
  ]
}
```

## API Routes

All Instagram routes are prefixed with `/api/instagram`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhook/{chatbot_id}` | Webhook for receiving messages |
| POST | `/{chatbot_id}/setup-webhook` | Generate webhook URL |
| GET | `/{chatbot_id}/webhook-info` | Get webhook configuration |
| DELETE | `/{chatbot_id}/webhook` | Remove webhook |
| POST | `/{chatbot_id}/send-test-message` | Send test message |

## Database Schema

### Integration Document
```javascript
{
  id: "uuid",
  chatbot_id: "chatbot_uuid",
  integration_type: "instagram",
  credentials: {
    page_access_token: "encrypted_token",
    verify_token: "verify_secret",
    app_secret: "app_secret"
  },
  enabled: true,
  status: "connected",
  created_at: "2025-11-10T...",
  updated_at: "2025-11-10T..."
}
```

### Conversation Document
```javascript
{
  id: "uuid",
  chatbot_id: "chatbot_uuid",
  session_id: "instagram_user_id",
  user_name: "Instagram User",
  user_email: "instagram_user_id",
  platform: "instagram",
  status: "active",
  message_count: 10,
  created_at: "2025-11-10T...",
  updated_at: "2025-11-10T..."
}
```

## Error Handling

The integration includes comprehensive error handling:

1. **Invalid Token**: Returns clear error message
2. **Missing Credentials**: Validates required fields
3. **API Failures**: Logs errors and returns graceful responses
4. **Integration Disabled**: Skips processing if integration is disabled
5. **Rate Limits**: Handles Facebook API rate limits

## Security

1. **Token Encryption**: Credentials stored securely in database
2. **Webhook Verification**: Validates incoming webhooks with verify token
3. **App Secret Validation**: Optional signature validation for webhooks
4. **HTTPS Required**: Instagram requires HTTPS for webhook endpoints

## Limitations

1. **Business Account Required**: Instagram Messaging API requires Business or Creator account
2. **Facebook App Required**: Must have a Facebook App with Instagram product
3. **Review Process**: Some features require Facebook app review
4. **Rate Limits**: Subject to Facebook Graph API rate limits
5. **24-hour Window**: Responses outside 24-hour window require approved message templates

## Troubleshooting

### Connection Test Fails
- Verify Page Access Token is valid and not expired
- Check token has required permissions
- Ensure Instagram account is connected to Facebook Page

### Webhook Not Receiving Messages
- Verify webhook URL is publicly accessible (HTTPS)
- Check verify token matches in both BotSmith and Facebook App
- Ensure webhook subscriptions are enabled for messages
- Check Facebook App is in live mode (not dev mode for real users)

### Messages Not Being Sent
- Check integration is enabled in BotSmith
- Verify bot has permissions to message the user
- Check if within 24-hour response window
- Review integration logs for errors

### Token Expired
- Page Access Tokens can expire
- Generate a new long-lived token
- Update credentials in BotSmith integration settings

## Support

For issues or questions:
1. Check integration logs in BotSmith
2. Review Facebook App webhook logs
3. Test with Facebook Graph API Explorer
4. Contact BotSmith support with error details

## Additional Resources

- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api)
- [Instagram Messaging API](https://developers.facebook.com/docs/messenger-platform/instagram)
- [Facebook Webhooks Guide](https://developers.facebook.com/docs/graph-api/webhooks)
- [Long-Lived Access Tokens](https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing)

---

**Version**: 1.0.0  
**Last Updated**: November 10, 2025  
**Author**: BotSmith Development Team
