# Complete Discord Integration Setup Guide

## Overview
This guide will help you connect your BotSmith chatbot to Discord, allowing your bot to receive and respond to messages in Discord servers and direct messages.

---

## Part 1: Create a Discord Bot

### Step 1: Go to Discord Developer Portal
1. Visit: **https://discord.com/developers/applications**
2. Log in with your Discord account
3. Click the **"New Application"** button (top right)

### Step 2: Create Your Application
1. Enter an **Application Name** (e.g., "My AI Assistant" or "Support Bot")
2. Read and accept Discord's Terms of Service
3. Click **"Create"**

### Step 3: Configure Bot Settings
1. In the left sidebar, click **"Bot"**
2. Click **"Add Bot"** button
3. Click **"Yes, do it!"** to confirm
4. **Customize Your Bot:**
   - Upload a bot avatar/icon (optional)
   - Set a username for your bot
   - Add a description

### Step 4: Get Bot Token
1. Under **"TOKEN"** section, click **"Reset Token"**
2. Click **"Yes, do it!"** to confirm
3. **IMPORTANT**: Copy the token immediately (you'll only see it once!)
   - It looks like: `MTExxx...xxxxx.Gyyy...yyyy.Zzzz-zzzz_zzzz`
4. 📝 Save this token securely - you'll need it in the next steps

### Step 5: Enable Privileged Gateway Intents (CRITICAL!)
1. Scroll down to **"Privileged Gateway Intents"** section
2. Enable these intents:
   - ✅ **PRESENCE INTENT** (optional)
   - ✅ **SERVER MEMBERS INTENT** (optional)
   - ✅ **MESSAGE CONTENT INTENT** ⚠️ **REQUIRED!**
3. Click **"Save Changes"**

**Note:** Without MESSAGE CONTENT INTENT, your bot cannot read message content!

---

## Part 2: Configure BotSmith Chatbot

### Step 6: Access Your Chatbot
1. Go to your BotSmith dashboard: **https://setup-display.preview.emergentagent.com**
2. Click on the chatbot you want to connect to Discord
3. Navigate to the **"Integrations"** tab

### Step 7: Add Discord Integration
1. Find the **Discord** card in the integrations list
2. Click **"Setup"** or **"Configure"** button
3. In the modal that appears:
   - **Bot Token**: Paste the token you copied (starts with `MT...`)
   - Toggle **"Enable Integration"** to ON
4. Click **"Test Connection"**
   - You should see: ✅ **"Connected as [YourBotName]"**
5. Click **"Save"**

### Step 8: Note Your Setup (Optional)
- The webhook URL will be generated automatically
- Discord bots work best with real-time Gateway connections
- This integration uses a hybrid approach for simplicity

---

## Part 3: Invite Bot to Your Discord Server

### Step 9: Generate Invite Link
1. Go back to **https://discord.com/developers/applications**
2. Select your application
3. In the left sidebar, click **"OAuth2"** → **"URL Generator"**

### Step 10: Select Permissions
1. Under **"SCOPES"**, check:
   - ✅ `bot`
   - ✅ `applications.commands` (optional, for slash commands)

2. Under **"BOT PERMISSIONS"**, check:
   - ✅ **Send Messages** (required)
   - ✅ **Send Messages in Threads** (recommended)
   - ✅ **Read Messages/View Channels** (required)
   - ✅ **Read Message History** (recommended)
   - ✅ **Add Reactions** (optional)
   - ✅ **Embed Links** (optional)
   - ✅ **Attach Files** (optional)

### Step 11: Copy and Use Invite Link
1. Scroll down and copy the **"GENERATED URL"**
2. Open the URL in a new browser tab
3. Select the Discord server where you want to add the bot
4. Click **"Authorize"**
5. Complete the CAPTCHA verification
6. Your bot will now appear in your server! 🎉

---

## Part 4: Testing Your Integration

### Step 12: Find Your Bot in Server
1. Open your Discord server
2. Look for your bot in the member list (right sidebar)
3. The bot should show as "Online" with a green status

### Step 13: Test in a Channel
1. Go to any text channel in your server
2. Send a message: `Hello bot!`
3. **Important**: For the current implementation, you need to mention the bot
   - Type: `@YourBotName Hello!`
4. Wait 2-3 seconds
5. Your bot should respond with an AI-generated message! 🎉

### Step 14: Test Direct Messages
1. Click on your bot's name in the member list
2. Click **"Message"** to start a DM
3. Send a message
4. Bot should respond

---

## Important Notes About Discord Integration

### Discord Bot Architecture
Discord bots can work in two ways:
1. **Gateway/WebSocket (Recommended for Production)**
   - Real-time connection
   - Receives events instantly
   - More reliable
   - Requires discord.py library

2. **Webhook/HTTP (Current Implementation)**
   - Simpler to implement
   - Works for interactions and slash commands
   - May have slight delays

### Current Limitations
- This integration uses a simplified approach
- For full production use with high message volume, consider implementing Discord Gateway
- Messages may need bot mentions depending on configuration

---

## Troubleshooting

### Bot doesn't respond?

**Check 1: MESSAGE CONTENT INTENT**
- Go to Developer Portal → Your App → Bot
- Make sure MESSAGE CONTENT INTENT is enabled
- Click "Save Changes"

**Check 2: Bot token is valid**
- In BotSmith → Integrations → Discord
- Click "Test Connection"
- Should show "Connected as [BotName]"

**Check 3: Bot has permissions**
- Make sure bot has "Send Messages" permission
- Check channel permissions (bot must be able to read and send)

**Check 4: Integration is enabled**
- In BotSmith → Integrations
- Make sure Discord toggle is ON

**Check 5: Bot is in the server**
- Bot should appear in member list
- Status should be "Online" (green dot)

### "Invalid bot token" error?

1. Go to Developer Portal
2. Select your app → Bot
3. Reset the token and copy the new one
4. Update in BotSmith → Integrations → Discord

### Bot appears offline?

- Check if bot token is correct
- Make sure integration is enabled in BotSmith
- Try regenerating the token

### Bot doesn't see messages?

- **MESSAGE CONTENT INTENT must be enabled!**
- This is the most common issue
- Go to Bot settings and enable it

---

## Features Included

✅ **Responds in channels** - Bot replies to messages/mentions  
✅ **Direct messages** - Bot responds to DMs  
✅ **Message replies** - Responses reference original message  
✅ **AI-powered** - Uses your configured AI provider (OpenAI/Claude/Gemini)  
✅ **Knowledge base** - Uses sources you've uploaded to the chatbot  
✅ **Conversation history** - Maintains context across messages  
✅ **Activity tracking** - All interactions logged in BotSmith  

---

## Discord Bot Best Practices

1. **Set a clear bot status**
   - Go to Bot settings → Status
   - Set to "Online" and choose an activity

2. **Add bot description**
   - Help users understand what your bot does
   - Add it in the General Information section

3. **Use rate limiting**
   - Discord has rate limits for bot API calls
   - BotSmith handles this automatically

4. **Monitor bot usage**
   - Check BotSmith → Integrations → View Logs
   - Monitor for errors or issues

5. **Privacy and Security**
   - Never share your bot token
   - Keep it secure like a password
   - Rotate token if compromised

---

## Quick Reference

| Task | Location |
|------|----------|
| Create Discord Bot | https://discord.com/developers/applications |
| Get Bot Token | Developer Portal → Your App → Bot → Token |
| Enable Intents | Developer Portal → Bot → Privileged Gateway Intents |
| Generate Invite Link | Developer Portal → OAuth2 → URL Generator |
| Configure BotSmith | Dashboard → Chatbot → Integrations → Discord |
| View Logs | BotSmith → Chatbot → Integrations → View Logs |

---

## Advanced: Slash Commands (Optional)

To add slash commands to your bot:

1. Go to Developer Portal → Your App → Bot
2. Click "applications.commands" scope when generating invite URL
3. Use Discord's API to register commands
4. Commands will trigger the webhook with interaction events

---

## Next Steps

After successful setup:
1. **Test thoroughly** - Send various messages to ensure bot responds correctly
2. **Configure AI** - Adjust chatbot settings (temperature, instructions, etc.)
3. **Add knowledge** - Upload documents/websites to improve bot responses
4. **Monitor usage** - Check activity logs and analytics
5. **Customize permissions** - Fine-tune what your bot can do in channels

---

## Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review BotSmith integration logs
3. Check Discord Developer Portal for API errors
4. Verify MESSAGE CONTENT INTENT is enabled
5. Ask for assistance with specific error messages

**Your Discord bot is ready to chat! 🤖**
