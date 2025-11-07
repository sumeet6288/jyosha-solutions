# Discord Integration - Quick Start Checklist ✅

## 📋 Complete This Checklist in Order

### Part A: Discord Bot Setup (7 minutes)

- [ ] **1. Create Discord Application**
  - Go to: https://discord.com/developers/applications
  - Click "New Application"
  - Name your bot and create

- [ ] **2. Add Bot to Application**
  - Go to: Bot section (left sidebar)
  - Click "Add Bot"
  - Customize name and avatar (optional)

- [ ] **3. Get Bot Token**
  - Click "Reset Token"
  - **Copy the token immediately**
  - 📝 Save it: `_______________________________`
  - ⚠️ You'll only see it once!

- [ ] **4. Enable MESSAGE CONTENT INTENT** ⚠️ **CRITICAL!**
  - Scroll to "Privileged Gateway Intents"
  - Enable these:
    - ✅ MESSAGE CONTENT INTENT (REQUIRED!)
    - ✅ SERVER MEMBERS INTENT (optional)
    - ✅ PRESENCE INTENT (optional)
  - Click "Save Changes"

---

### Part B: BotSmith Configuration (2 minutes)

- [ ] **5. Open BotSmith Dashboard**
  - URL: https://setup-preview-4.preview.emergentagent.com

- [ ] **6. Configure Discord Integration**
  - Go to: Dashboard → Your Chatbot → Integrations
  - Click "Setup" on Discord card
  - Paste Bot Token: `MT...`
  - Click "Test Connection"
  - Verify: ✅ "Connected as [BotName]"
  - Enable integration
  - Click "Save"

---

### Part C: Invite Bot to Server (3 minutes)

- [ ] **7. Generate Invite URL**
  - Back to: https://discord.com/developers/applications
  - Your App → OAuth2 → URL Generator

- [ ] **8. Select Scopes**
  - Check these scopes:
    - ✅ `bot`
    - ✅ `applications.commands` (optional)

- [ ] **9. Select Bot Permissions**
  - Check these permissions:
    - ✅ Send Messages (required)
    - ✅ Read Messages/View Channels (required)
    - ✅ Read Message History (recommended)
    - ✅ Send Messages in Threads (recommended)
    - ✅ Embed Links (optional)

- [ ] **10. Invite Bot**
  - Copy the Generated URL
  - Open in browser
  - Select your Discord server
  - Click "Authorize"
  - Complete CAPTCHA

---

### Part D: Test Integration (1 minute)

- [ ] **11. Verify Bot is Online**
  - Open Discord server
  - Look for bot in member list
  - Should show green "Online" status

- [ ] **12. Test Bot Response**
  - Go to any text channel
  - Send: `@YourBotName Hello!`
  - Wait for bot response 🎉

- [ ] **13. Test Direct Message**
  - Click bot name → "Message"
  - Send: `Hi bot!`
  - Verify bot responds

---

## ✅ Done! Your Discord Bot is Live!

### Quick Test Commands:
```
@YourBot Hello!
@YourBot What can you help me with?
@YourBot Tell me about [your topic]
Help me with [your use case]
```

### View Activity:
BotSmith → Chatbot → Integrations → Discord → View Logs

---

## 🚨 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Bot not responding | ⚠️ Enable MESSAGE CONTENT INTENT in Developer Portal |
| "Invalid bot token" | Reset token in Developer Portal and update in BotSmith |
| Bot appears offline | Check token is correct and integration is enabled |
| Bot can't see messages | MESSAGE CONTENT INTENT must be enabled! |
| Permission denied | Invite bot again with correct permissions |

---

## ⚠️ CRITICAL: MESSAGE CONTENT INTENT

**Most Common Issue:**
- Bot won't respond if MESSAGE CONTENT INTENT is not enabled
- This is a privileged intent that must be explicitly enabled
- Location: Developer Portal → Bot → Privileged Gateway Intents
- Make sure to click "Save Changes"!

---

## 📍 Key URLs

1. **Discord Developer Portal**: https://discord.com/developers/applications
2. **BotSmith Dashboard**: https://setup-preview-4.preview.emergentagent.com
3. **Webhook URL**: Generated automatically in BotSmith

---

## 🎯 Bot Token Security

- ✅ Keep your token secret
- ✅ Never share it publicly
- ✅ Never commit it to GitHub
- ✅ Rotate immediately if compromised
- ✅ Store securely (BotSmith encrypts it)

---

## 📊 Verification Checklist

After setup, verify:
- [ ] Bot token is correct (test connection passes)
- [ ] MESSAGE CONTENT INTENT is enabled
- [ ] Bot has Send Messages permission
- [ ] Bot appears online in server
- [ ] Bot responds to messages/mentions
- [ ] Integration is enabled in BotSmith
- [ ] Logs show message activity

---

**Total Time: ~12 minutes**
**Difficulty: Easy** ⭐⭐☆☆☆

**Critical Step:** Don't forget MESSAGE CONTENT INTENT! 🔑

Need detailed instructions? See: `DISCORD_INTEGRATION_SETUP_GUIDE.md`
