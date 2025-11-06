# Complete Slack Integration Setup Guide

## Overview
This guide will help you connect your BotSmith chatbot to Slack, allowing your bot to receive and respond to messages in Slack channels and direct messages.

---

## Part 1: Create a Slack App

### Step 1: Go to Slack API Dashboard
1. Visit: **https://api.slack.com/apps**
2. Click the **"Create New App"** button (green button in top right)

### Step 2: Choose Creation Method
1. Select **"From scratch"**
2. Enter App Details:
   - **App Name**: Choose a name (e.g., "My AI Assistant" or "Support Bot")
   - **Pick a workspace**: Select your Slack workspace
3. Click **"Create App"**

---

## Part 2: Configure Bot Permissions

### Step 3: Add Bot Token Scopes
1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll down to **"Scopes"** section
3. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**
4. Add these scopes one by one:
   - `chat:write` - Allows bot to send messages
   - `chat:write.public` - Allows bot to send messages to channels without joining
   - `users:read` - Allows bot to read user information
   - `channels:history` - Allows bot to read channel messages
   - `im:history` - Allows bot to read direct messages
   - `groups:history` - Allows bot to read private channel messages

### Step 4: Install App to Workspace
1. Scroll up to **"OAuth Tokens for Your Workspace"** section
2. Click **"Install to Workspace"** button
3. Review permissions and click **"Allow"**
4. **IMPORTANT**: Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)
   - Save this token somewhere safe - you'll need it in the next steps

---

## Part 3: Configure BotSmith Chatbot

### Step 5: Access Your Chatbot
1. Go to your BotSmith dashboard: **https://dep-install-demo.preview.emergentagent.com**
2. Click on the chatbot you want to connect to Slack
3. Navigate to the **"Integrations"** tab

### Step 6: Add Slack Integration
1. Find the **Slack** card in the integrations list
2. Click **"Setup"** or **"Configure"** button
3. In the modal that appears:
   - **Bot Token**: Paste the token you copied (starts with `xoxb-`)
   - Toggle **"Enable Integration"** to ON
4. Click **"Save"** or **"Test Connection"**
5. You should see: ✅ **"Connection successful"**

### Step 7: Get Webhook URL
1. After saving, click the **"⚡ Setup Webhook"** button (lightning bolt icon)
2. Copy the webhook URL that appears
   - It will look like: `https://dep-install-demo.preview.emergentagent.com/api/slack/webhook/[your-chatbot-id]`
3. Keep this URL handy for the next steps

---

## Part 4: Configure Slack Event Subscriptions

### Step 8: Enable Event Subscriptions
1. Go back to **https://api.slack.com/apps**
2. Select your app
3. In the left sidebar, click **"Event Subscriptions"**
4. Toggle **"Enable Events"** to ON

### Step 9: Set Request URL
1. In the **"Request URL"** field, paste the webhook URL you copied in Step 7
2. Slack will verify the URL - you should see: ✅ **"Verified"**
   - If it fails, check that:
     - Your BotSmith app is running
     - The webhook URL is correct
     - Your chatbot ID is valid

### Step 10: Subscribe to Bot Events
1. Scroll down to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add these events one by one:
   - `message.channels` - Messages in public channels
   - `message.im` - Direct messages to the bot
   - `message.groups` - Messages in private channels

### Step 11: Save Changes
1. Scroll to bottom and click **"Save Changes"**
2. Slack will prompt: **"Reinstall your app"**
3. Click the **"reinstall your app"** link
4. Review permissions and click **"Allow"**

---

## Part 5: Testing Your Integration

### Step 12: Invite Bot to Channel
1. In your Slack workspace, go to any channel
2. Type: `/invite @YourBotName` (use the actual bot name)
3. Press Enter
4. The bot will join the channel

### Step 13: Test the Bot
1. In the channel, send a message: `Hello bot!`
2. Wait 2-3 seconds
3. Your bot should respond with an AI-generated message! 🎉

### Step 14: Test Direct Messages
1. Click on your bot's name in Slack
2. Click **"Message"** to start a DM
3. Send a message
4. Bot should respond

---

## Troubleshooting

### Bot doesn't respond?

**Check 1: Integration is enabled**
- In BotSmith → Integrations → Make sure Slack is toggled ON

**Check 2: Bot token is valid**
- Go to https://api.slack.com/apps → Your App → OAuth & Permissions
- Make sure token is still valid
- Re-copy and update in BotSmith if needed

**Check 3: Events are configured**
- https://api.slack.com/apps → Your App → Event Subscriptions
- Make sure it's enabled and events are subscribed

**Check 4: Bot has permission to read messages**
- Invite bot to the channel: `/invite @YourBotName`
- Bot needs to be in the channel to see messages

**Check 5: Check BotSmith Integration Logs**
- In BotSmith → Chatbot → Integrations
- Click on Slack integration
- View activity logs to see if messages are being received

### "invalid_auth" error?

This means the bot token is invalid or expired:
1. Go to https://api.slack.com/apps
2. Select your app → OAuth & Permissions
3. Copy the Bot User OAuth Token again
4. Update it in BotSmith → Integrations → Slack

### Webhook URL verification fails?

1. Make sure your BotSmith app is running
2. Check that the URL is exactly: `https://dep-install-demo.preview.emergentagent.com/api/slack/webhook/[chatbot-id]`
3. Try clicking "Retry" in Slack Event Subscriptions
4. Check backend logs for errors

---

## Features Included

✅ **Responds in channels** - Bot replies to mentions in public channels  
✅ **Direct messages** - Bot responds to DMs  
✅ **Thread support** - Responses appear in threads  
✅ **AI-powered** - Uses your configured AI provider (OpenAI/Claude/Gemini)  
✅ **Knowledge base** - Uses sources you've uploaded to the chatbot  
✅ **Conversation history** - Maintains context across messages  
✅ **Activity tracking** - All interactions logged in BotSmith  

---

## Quick Reference

| Task | Location |
|------|----------|
| Create Slack App | https://api.slack.com/apps |
| Get Bot Token | Slack API → Your App → OAuth & Permissions |
| Configure BotSmith | Dashboard → Chatbot → Integrations → Slack |
| Set Webhook URL | Slack API → Your App → Event Subscriptions |
| View Logs | BotSmith → Chatbot → Integrations → View Logs |

---

## Next Steps

After successful setup:
1. **Test thoroughly** - Send various messages to ensure bot responds correctly
2. **Configure AI** - Adjust chatbot settings (temperature, instructions, etc.)
3. **Add knowledge** - Upload documents/websites to improve bot responses
4. **Monitor usage** - Check activity logs and analytics
5. **Invite to more channels** - Use `/invite @YourBotName` in other channels

---

## Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review BotSmith integration logs
3. Check Slack App event logs
4. Ask for assistance with specific error messages

**Your Slack integration is ready to go! 🚀**
