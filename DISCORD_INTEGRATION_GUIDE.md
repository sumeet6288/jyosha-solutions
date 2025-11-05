# Discord Integration Guide - Start Bot Button Location

## Issue
Discord messages are returning error: "I apologize, but I encountered an error processing your message."

## Root Cause
The Discord bot needs to be **manually started** after configuration. The bot doesn't start automatically.

## Solution: Click the ⚡ Start Bot Button

### Step-by-Step Instructions:

1. **Navigate to Chatbot Builder**
   - Go to Dashboard
   - Click on your chatbot to open the Chatbot Builder

2. **Go to Integrations Section**
   - Look for the "Integrations" tab in the navigation menu
   - OR navigate directly to: `http://localhost:3000/chatbot/{your-chatbot-id}/integrations`

3. **Find Your Discord Integration**
   - Scroll down to find the Discord integration card
   - It should show as "Configured" if you've already added your bot token

4. **Locate the Start Bot Button**
   - You'll see several buttons next to your Discord integration:
     - 🔧 **Setup/Reconfigure** (purple) - Configure bot token
     - 🔄 **Test Connection** (blue) - Test Discord API connection
     - ⚡ **Start Bot** (green) - **THIS IS THE BUTTON YOU NEED!**
     - 🗑️ **Delete** (red) - Remove integration

5. **Click the Green Lightning Bolt (⚡) Button**
   - This button has a tooltip: "Start Discord Bot (Required for Messages)"
   - When clicked, it will:
     - Start the Discord bot process
     - Connect to Discord Gateway
     - Begin listening for messages
     - Show a success toast: "Discord Bot Started - Your Discord bot is now online and listening for messages!"

6. **Verify Bot is Running**
   - After clicking, the bot should be online in Discord
   - You can send a test message to verify it's working

## Important Notes:

### Prerequisites (MUST DO FIRST):
1. **Enable MESSAGE CONTENT INTENT** in Discord Developer Portal:
   - Go to https://discord.com/developers/applications
   - Select your application
   - Go to "Bot" section
   - Under "Privileged Gateway Intents", enable "MESSAGE CONTENT INTENT"
   - Save changes

2. **Ensure EMERGENT_LLM_KEY is set**:
   - The bot needs this to generate AI responses
   - Check backend `.env` file for `EMERGENT_LLM_KEY`

### If Bot Still Shows Errors After Starting:
1. Check backend logs: `tail -50 /var/log/supervisor/backend.err.log`
2. Look for "Error generating AI response" messages
3. Verify your chatbot has a valid AI provider configured (OpenAI, Claude, or Gemini)
4. Ensure EMERGENT_LLM_KEY is properly set in backend environment

### Button Location in UI:
```
Discord Integration Card
├── 🔧 Setup (purple button)
├── 🔄 Test (blue circular button) 
├── ⚡ Start Bot (GREEN CIRCULAR BUTTON WITH LIGHTNING BOLT) ← CLICK THIS!
└── 🗑️ Delete (red circular button)
```

## Technical Details:
- API Endpoint: `POST /api/discord/{chatbot_id}/start-bot`
- Handler: `handleStartDiscordBot()` in ChatbotIntegrations.jsx
- Backend: Discord bot uses discord.py library with Gateway connection
- The bot manager (`discord_bot_manager.py`) handles message processing
