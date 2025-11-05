# 🎯 WHERE TO FIND THE DISCORD "START BOT" BUTTON

## Step-by-Step Visual Guide

### 1️⃣ Go to Dashboard
- Navigate to: `http://localhost:3000/dashboard`
- You'll see your chatbot(s) listed under "Your Chatbots"

### 2️⃣ Click "Manage" on Your Chatbot
- Click the **"Manage"** button next to your chatbot
- This opens the Chatbot Builder

### 3️⃣ Click the "Integrations" Tab
- At the top of the Chatbot Builder, you'll see tabs:
  ```
  [Sources] [Settings] [Appearance] [Widget] [Analytics] [Insights] [Integrations] ← CLICK HERE
  ```

### 4️⃣ Find Your Discord Integration Card
- Scroll down to find the **Discord** card
- It should show: "Discord" with logo and "Configured" badge (if you've already set up the bot token)

### 5️⃣ Locate the Buttons Row
Inside the Discord card, you'll see a row of buttons:

```
┌─────────────────────────────────────────────────────────────────┐
│  Discord Integration Card                                        │
│                                                                   │
│  [🔧 Setup]  [🔄]  [⚡]  [🗑️]                                     │
│   PURPLE    BLUE  GREEN  RED                                     │
│   Button    Test  START  Delete                                  │
│            Button  BOT   Button                                  │
│                   BUTTON                                         │
│                    ↑↑↑                                           │
│              CLICK THIS!!                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 6️⃣ Click the GREEN ⚡ (Lightning Bolt) Button
- **This is the "Start Bot" button!**
- Tooltip says: "Start Discord Bot (Required for Messages)"
- It's the **third button** from the left
- Has a **green border** with a **lightning bolt icon (⚡)**

### 7️⃣ Success!
After clicking, you should see a toast notification:
```
✅ Discord Bot Started
Your Discord bot is now online and listening for messages!
```

---

## Button Details:

| Button | Color | Icon | Position | Purpose |
|--------|-------|------|----------|---------|
| Setup | Purple | 🔧 Settings | 1st | Configure bot token |
| Test | Blue | 🔄 Refresh | 2nd | Test Discord API connection |
| **START BOT** | **GREEN** | **⚡ Zap** | **3rd** | **Start the Discord bot (CLICK THIS!)** |
| Delete | Red | 🗑️ Trash | 4th | Remove integration |

---

## What Happens When You Click "Start Bot"?

1. **Starts Discord Bot Process**: Launches the Discord bot using discord.py library
2. **Connects to Gateway**: Connects to Discord's real-time messaging gateway  
3. **Listens for Messages**: Bot starts listening for messages in your Discord server
4. **Processes Messages**: When users send messages, the bot:
   - Receives the message
   - Generates AI response using your configured AI provider (OpenAI/Claude/Gemini)
   - Sends the response back to Discord
   - Saves conversation history in database

---

## ⚠️ IMPORTANT PREREQUISITES

### Before Clicking Start Bot:

1. **Enable MESSAGE CONTENT INTENT in Discord Developer Portal**:
   ```
   1. Go to https://discord.com/developers/applications
   2. Select your application
   3. Click "Bot" in left sidebar
   4. Scroll to "Privileged Gateway Intents"
   5. Toggle ON "MESSAGE CONTENT INTENT"
   6. Click "Save Changes"
   ```

2. **Ensure EMERGENT_LLM_KEY is Set**:
   - Check backend `.env` file
   - Should have: `EMERGENT_LLM_KEY=your-key-here`
   - This is needed for AI response generation

3. **Verify Your Chatbot Has AI Configuration**:
   - Go to Settings tab
   - Check that AI Provider is set (OpenAI/Claude/Gemini)
   - Check that Model is selected (e.g., gpt-4o-mini)

---

## 🐛 Troubleshooting

### If you still get "error processing message" after clicking Start Bot:

1. **Check Backend Logs**:
   ```bash
   tail -50 /var/log/supervisor/backend.err.log
   ```
   Look for errors like:
   - "Error generating AI response"
   - "Missing API key"
   - "Invalid model"

2. **Verify Bot Status**:
   - Bot should show as "online" in your Discord server
   - Check server member list

3. **Test AI Configuration**:
   - Try sending a test message in the Chat Preview (in Widget tab)
   - If preview works but Discord doesn't, it's a Discord-specific issue
   - If preview also fails, it's an AI configuration issue

4. **Check EMERGENT_LLM_KEY**:
   ```bash
   cd /app/backend && grep EMERGENT_LLM_KEY .env
   ```

---

## 📍 Exact File Locations (For Reference)

- **Frontend Component**: `/app/frontend/src/components/ChatbotIntegrations.jsx` (line 700-710)
- **Backend Handler**: `/app/backend/routers/discord.py` `/start-bot` endpoint (line 458-515)
- **Bot Manager**: `/app/backend/services/discord_bot_manager.py`
- **Message Processor**: `discord_bot_manager.py` `process_message()` (line 102-261)

---

## 💡 Quick Test

After clicking Start Bot, send a test message in your Discord server:
```
User: Hello bot!
Bot: [Should reply with AI-generated response]
```

If you get an error, check the backend logs immediately!
