# Slack Integration - Quick Start Checklist ✅

## 📋 Complete This Checklist in Order

### Part A: Slack App Setup (5 minutes)

- [ ] **1. Create Slack App**
  - Go to: https://api.slack.com/apps
  - Click "Create New App" → "From scratch"
  - Name your app and select workspace

- [ ] **2. Add Bot Permissions**
  - Go to: OAuth & Permissions
  - Add Bot Token Scopes:
    - ✅ `chat:write`
    - ✅ `chat:write.public`
    - ✅ `users:read`
    - ✅ `channels:history`
    - ✅ `im:history`
    - ✅ `groups:history`

- [ ] **3. Install App & Get Token**
  - Click "Install to Workspace"
  - Click "Allow"
  - **Copy Bot User OAuth Token** (starts with `xoxb-`)
  - 📝 Save it: `_______________________________`

---

### Part B: BotSmith Configuration (2 minutes)

- [ ] **4. Open BotSmith Dashboard**
  - URL: https://setup-view.preview.emergentagent.com

- [ ] **5. Configure Slack Integration**
  - Go to: Dashboard → Your Chatbot → Integrations
  - Click "Setup" on Slack card
  - Paste Bot Token: `xoxb-...`
  - Enable integration
  - Click "Save"
  - Verify: ✅ "Connection successful"

- [ ] **6. Get Webhook URL**
  - Click "⚡ Setup Webhook" button
  - **Copy Webhook URL**
  - 📝 Save it: `_______________________________`

---

### Part C: Slack Event Configuration (3 minutes)

- [ ] **7. Enable Event Subscriptions**
  - Back to: https://api.slack.com/apps → Your App
  - Go to: Event Subscriptions
  - Toggle "Enable Events" to ON

- [ ] **8. Set Webhook URL**
  - Paste Webhook URL in "Request URL" field
  - Wait for: ✅ "Verified"

- [ ] **9. Subscribe to Events**
  - Click "Add Bot User Event"
  - Add these 3 events:
    - ✅ `message.channels`
    - ✅ `message.im`
    - ✅ `message.groups`

- [ ] **10. Save & Reinstall**
  - Click "Save Changes"
  - Click "reinstall your app"
  - Click "Allow"

---

### Part D: Test Integration (1 minute)

- [ ] **11. Test in Slack**
  - Go to any Slack channel
  - Type: `/invite @YourBotName`
  - Send message: `Hello bot!`
  - Wait for bot response 🎉

- [ ] **12. Test Direct Message**
  - Click bot name → "Message"
  - Send: `What can you help me with?`
  - Verify bot responds

---

## ✅ Done! Your Slack Bot is Live!

### Quick Test Commands:
```
Hi bot!
What can you do?
Tell me about [your topic]
Help me with [your use case]
```

### View Activity:
BotSmith → Chatbot → Integrations → Slack → View Logs

---

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| Bot not responding | Check integration is enabled in BotSmith |
| "invalid_auth" | Re-copy bot token from Slack and update in BotSmith |
| Webhook not verified | Make sure BotSmith app is running |
| Bot not in channel | Invite with `/invite @YourBotName` |

---

**Total Time: ~10 minutes**
**Difficulty: Easy** ⭐⭐☆☆☆

Need detailed instructions? See: `SLACK_INTEGRATION_SETUP_GUIDE.md`
