# Discord Integration Setup Guide

## ⚠️ CRITICAL: Enable Required Intents

Discord bots require **Privileged Gateway Intents** to read message content. You MUST enable these in the Discord Developer Portal.

## Step-by-Step Setup Instructions

### 1. Create Discord Application & Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "BotSmith ChatBot")
4. Click **"Create"**

### 2. Create Bot User
1. In your application, go to **"Bot"** section (left sidebar)
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Copy the **Bot Token** (you'll need this later)
   - Click **"Reset Token"** if you need to generate a new one
   - ⚠️ Keep this token secret!

### 3. ✅ Enable Privileged Gateway Intents (CRITICAL!)
In the Bot section, scroll down to **"Privileged Gateway Intents"**:

**REQUIRED INTENTS:**
- ☑️ **MESSAGE CONTENT INTENT** - Enable this! (Required to read message content)
- ☑️ **SERVER MEMBERS INTENT** - Optional but recommended
- ☑️ **PRESENCE INTENT** - Optional

**Without MESSAGE CONTENT INTENT enabled, your bot WILL NOT work!**

### 4. Configure Bot Permissions
1. Go to **"OAuth2"** → **"URL Generator"** (left sidebar)
2. Under **Scopes**, select:
   - ☑️ `bot`
   - ☑️ `applications.commands`
3. Under **Bot Permissions**, select:
   - ☑️ Send Messages
   - ☑️ Read Messages/View Channels
   - ☑️ Read Message History
   - ☑️ Add Reactions (optional)
   - ☑️ Attach Files (optional)

### 5. Invite Bot to Your Server
1. Copy the generated **OAuth2 URL** at the bottom
2. Paste it in your browser
3. Select your Discord server from dropdown
4. Click **"Authorize"**
5. Complete the CAPTCHA
6. Your bot will now appear in your server (offline initially)

### 6. Configure in BotSmith
1. In BotSmith, go to your Chatbot → **Integrations** tab
2. Find **Discord** integration
3. Click **"Setup"**
4. Paste your **Bot Token**
5. (Optional) Add Client ID and Server ID
6. Click **"Save"**
7. Enable the integration using the toggle switch
8. Click the **⚡ Start Bot** button (green button with lightning icon)
9. Your bot should now be **ONLINE** in Discord!

### 7. Test Your Bot
1. Go to your Discord server
2. Send a message in any channel where the bot has access
3. The bot should reply with an AI-generated response!

## Troubleshooting

### Bot appears offline
- Check if you clicked the **⚡ Start Bot** button in BotSmith
- Verify your bot token is correct
- Check backend logs for errors

### Bot doesn't respond to messages
**Most Common Issue:** MESSAGE CONTENT INTENT not enabled
- Go to Discord Developer Portal → Your Application → Bot
- Scroll to "Privileged Gateway Intents"
- Enable **MESSAGE CONTENT INTENT**
- Click **⚡ Start Bot** again in BotSmith

### "Privileged intents" error
This means you haven't enabled MESSAGE CONTENT INTENT in Discord Developer Portal:
1. Go to https://discord.com/developers/applications
2. Select your application
3. Go to "Bot" section
4. Enable "MESSAGE CONTENT INTENT" under Privileged Gateway Intents
5. Save changes
6. Restart bot in BotSmith (Stop → Start)

### Bot responds but with generic messages
- Check your chatbot's instructions/system message in Settings tab
- Verify knowledge base sources are uploaded in Sources tab

## Architecture Notes

- Discord bots use **WebSocket Gateway** connection (not webhooks like Slack)
- The bot must be running continuously to receive messages
- When you restart the backend, all Discord bots auto-start if integration is enabled
- Bot runs in background using discord.py library

## Useful Links

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Intents Guide](https://discord.com/developers/docs/topics/gateway#gateway-intents)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)
