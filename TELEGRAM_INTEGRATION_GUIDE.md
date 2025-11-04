# 📱 Telegram Integration Guide for BotSmith

## Overview
Connect your AI chatbot to Telegram and let users interact with it directly through Telegram messenger. Your chatbot will respond automatically to messages using your configured AI provider (OpenAI, Claude, or Gemini) and knowledge base.

---

## 🚀 Step-by-Step Setup Guide

### **Step 1: Create a Telegram Bot**

1. Open Telegram app (mobile or desktop)
2. Search for **@BotFather** (this is Telegram's official bot for creating bots)
3. Start a conversation with BotFather
4. Send the command: `/newbot`
5. BotFather will ask you to provide:
   - **Bot Name**: Display name (e.g., "My Support Bot")
   - **Bot Username**: Must end with 'bot' (e.g., "mysupport_bot" or "customercare_bot")
6. **Save the Bot Token** - BotFather will give you a token like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz-123456
   ```
   ⚠️ **Keep this token secret!** Anyone with this token can control your bot.

### **Step 2: Configure Your Bot (Optional)**

You can customize your bot by sending these commands to BotFather:

```
/setdescription  - Set a description shown in bot profile
/setabouttext    - Set "About" text
/setuserpic      - Upload profile picture for your bot
/setcommands     - Set command list (e.g., /help, /start)
```

Example commands you might want to set:
```
start - Start conversation with the bot
help - Get help information
```

### **Step 3: Add Telegram Integration in BotSmith**

1. Go to your **Chatbot Builder** page
2. Click on the **Integrations** tab
3. Find the **Telegram** card (blue icon)
4. Click **Setup**
5. Enter your **Bot Token** from Step 1
6. (Optional) Enter your bot's username
7. Click **Save Integration**

### **Step 4: Setup Webhook**

After saving your Telegram integration, you need to setup the webhook so Telegram can send messages to your bot:

1. In the Telegram integration card, you'll see a **green lightning bolt icon (⚡)**
2. Click this icon to **Setup Webhook**
3. The system will automatically:
   - Configure the webhook URL
   - Set a secure secret token
   - Register it with Telegram
4. You'll see a success message when the webhook is configured

**Webhook URL Format:**
```
https://yourdomain.com/api/telegram/webhook/{chatbot_id}
```

### **Step 5: Test Your Bot**

1. Open Telegram and search for your bot by username (e.g., @mysupport_bot)
2. Click **Start** or send `/start`
3. Your bot should respond with your configured welcome message
4. Send any question - your bot will respond using AI and your knowledge base!

---

## 🔧 How It Works

### Message Flow:
1. **User sends message** → Telegram
2. **Telegram forwards** → Your BotSmith webhook
3. **BotSmith processes**:
   - Retrieves chatbot configuration
   - Searches knowledge base for relevant context
   - Generates AI response using configured provider
   - Saves conversation history
4. **Response sent** → User via Telegram

### Features:
- ✅ Real-time AI responses
- ✅ Knowledge base integration
- ✅ Conversation history tracking
- ✅ Multi-provider AI support (OpenAI, Claude, Gemini)
- ✅ Automatic typing indicators
- ✅ Session management per user
- ✅ Activity logging

---

## 📊 Monitoring & Logs

### View Integration Logs:
1. Go to **Integrations** tab in your chatbot
2. Click the **Activity** icon on Telegram card
3. View all events:
   - Messages processed
   - Webhook configurations
   - Connection tests
   - Errors

### Webhook Information:
You can check your webhook status:
- **API Endpoint**: `GET /api/telegram/{chatbot_id}/webhook-info`
- Shows: webhook URL, pending updates, last error time

---

## 🎯 Best Practices

### 1. **Welcome Message**
Set a clear welcome message in Settings tab:
```
👋 Welcome! I'm here to help you 24/7.
Ask me anything about our products and services!
```

### 2. **Knowledge Base**
Add comprehensive content to your knowledge base:
- Product documentation
- FAQs
- Company policies
- Support articles

### 3. **Test Before Launch**
- Test with various questions
- Check response quality
- Verify knowledge base citations
- Test error handling

### 4. **Monitor Performance**
- Check Analytics tab regularly
- Review conversation logs
- Identify common questions
- Update knowledge base based on gaps

---

## 🔐 Security

### Bot Token Security:
- **Never share** your bot token publicly
- **Never commit** tokens to git/GitHub
- Store tokens securely in BotSmith (they're encrypted)
- **Regenerate** token if compromised (via @BotFather: `/revoke`)

### Webhook Security:
- Webhooks use secret tokens for validation
- All communication over HTTPS
- Automatic verification of Telegram requests

---

## 🐛 Troubleshooting

### Bot Not Responding?

**Check #1: Webhook Status**
```bash
# Check if webhook is configured
GET /api/telegram/{chatbot_id}/webhook-info
```

**Check #2: Integration Enabled**
- Go to Integrations tab
- Ensure toggle switch is ON (green)

**Check #3: Test Connection**
- Click the refresh icon to test connection
- Should show "Connected to @your_bot_username"

**Check #4: View Logs**
- Click Activity icon
- Check for errors
- Look for "message_processed" events

### Common Issues:

#### "Webhook setup failed"
- **Cause**: Invalid bot token or network issue
- **Fix**: Verify bot token with @BotFather, try again

#### "Bot token not configured"
- **Cause**: Integration not saved properly
- **Fix**: Re-enter bot token and save

#### "Messages not getting AI responses"
- **Cause**: Chatbot provider/model not configured
- **Fix**: Go to Settings tab, configure AI provider

#### "Connection test failed"
- **Cause**: Invalid or revoked token
- **Fix**: Get new token from @BotFather

---

## 📱 Advanced Features

### Sending Test Messages:
```bash
POST /api/telegram/{chatbot_id}/send-test-message
{
  "chat_id": 123456789,
  "text": "Hello! This is a test message."
}
```

### Delete Webhook:
```bash
DELETE /api/telegram/{chatbot_id}/webhook
```

### Manual Webhook Setup:
```bash
POST /api/telegram/{chatbot_id}/setup-webhook
{
  "base_url": "https://yourdomain.com"
}
```

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/telegram/webhook/{chatbot_id}` | Receive messages from Telegram |
| POST | `/api/telegram/{chatbot_id}/setup-webhook` | Configure webhook |
| GET | `/api/telegram/{chatbot_id}/webhook-info` | Get webhook status |
| DELETE | `/api/telegram/{chatbot_id}/webhook` | Remove webhook |
| POST | `/api/telegram/{chatbot_id}/send-test-message` | Send test message |

---

## 🎓 Tips for Success

1. **Clear Instructions**: Use welcome message to guide users on what they can ask
2. **Rich Knowledge Base**: More content = better answers
3. **Regular Updates**: Keep knowledge base current
4. **Monitor Analytics**: Track popular questions and improve responses
5. **Quick Responses**: AI responds instantly, but quality depends on your content

---

## 🆘 Need Help?

If you encounter issues:
1. Check the **Integration Logs** for errors
2. Review **Chatbot Analytics** for conversation data
3. Test with `/start` command to verify basic functionality
4. Ensure your **AI provider** is configured correctly
5. Verify your **knowledge base** has relevant content

---

## ✨ Example Use Cases

### Customer Support Bot
```
Knowledge Base: FAQs, product docs, policies
Use Case: Answer customer questions 24/7
```

### Sales Assistant Bot
```
Knowledge Base: Product catalog, pricing, features
Use Case: Help prospects learn about products
```

### HR Helper Bot
```
Knowledge Base: Company policies, benefits, procedures
Use Case: Answer employee questions
```

### Educational Bot
```
Knowledge Base: Course materials, tutorials, guides
Use Case: Help students learn
```

---

## 🎉 You're All Set!

Your Telegram bot is now connected and ready to help users! Your AI chatbot will:
- ✅ Respond to messages automatically
- ✅ Use your knowledge base to provide accurate answers
- ✅ Track all conversations for analytics
- ✅ Provide 24/7 support through Telegram

**Next Steps:**
1. Share your bot link: `https://t.me/your_bot_username`
2. Test with real users
3. Monitor analytics
4. Improve knowledge base based on feedback

Happy chatting! 🚀
