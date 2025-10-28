# 📘 BotSmith User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Creating Your First Chatbot](#creating-your-first-chatbot)
3. [Adding Knowledge Base](#adding-knowledge-base)
4. [Customizing Appearance](#customizing-appearance)
5. [Testing Your Chatbot](#testing-your-chatbot)
6. [Analytics & Insights](#analytics--insights)
7. [Sharing & Deployment](#sharing--deployment)
8. [Managing Subscriptions](#managing-subscriptions)
9. [Account Settings](#account-settings)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### 1. Sign Up

1. Navigate to the BotSmith homepage
2. Click **"Try for Free"** or **"Sign In"**
3. Create your account with email and password
4. You'll be automatically redirected to the dashboard

### 2. Dashboard Overview

Your dashboard shows:
- **Create New Agent**: Quick button to create chatbots
- **Total Conversations**: Number of chats across all bots
- **Total Messages**: Message count
- **Active Chatbots**: Currently active bots
- **Free Plan Usage**: Resource consumption (chatbots, messages, files, websites, text sources)
- **Your Chatbots**: List of all your created chatbots

---

## Creating Your First Chatbot

### Step 1: Create Chatbot

1. Click **"+ Create New"** button on dashboard
2. You'll be redirected to the Chatbot Builder
3. A new chatbot is automatically created

### Step 2: Configure Settings

1. Click the **"Settings"** tab
2. Configure basic settings:
   - **Name**: Give your chatbot a descriptive name (e.g., "Customer Support Bot")
   - **AI Provider**: Choose from:
     - **OpenAI**: GPT-4o, GPT-4o-mini (fast and cost-effective)
     - **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus (excellent reasoning)
     - **Google**: Gemini 2.0 Flash, Gemini 1.5 Pro (multimodal)
   - **System Message**: Define your chatbot's personality and behavior
     ```
     Example: "You are a friendly customer support agent for Acme Inc. 
     You help customers with product inquiries, order tracking, and 
     technical support. Always be polite and professional."
     ```

3. Click **"Save"** to apply changes

### Recommended Models by Use Case:

- **Customer Support**: GPT-4o-mini (fast, accurate)
- **Technical Documentation**: Claude 3.5 Sonnet (detailed explanations)
- **General Q&A**: Gemini 2.0 Flash (balanced performance)
- **Complex Reasoning**: Claude 3 Opus (advanced analysis)
- **Creative Content**: GPT-4o (versatile)

---

## Adding Knowledge Base

Your chatbot learns from the sources you provide. You can add three types of sources:

### Method 1: Upload Files

1. Go to **"Sources"** tab in Chatbot Builder
2. Click **"+ Add Source"** button
3. Select **"Upload File"**
4. Choose your file:
   - **Supported formats**: PDF, DOCX, TXT, XLSX, CSV
   - **Max size**: 100MB per file
   - **Examples**: Product manuals, FAQ documents, price lists
5. Click **"Upload"**
6. Wait for processing to complete (status changes to "Completed")

**Best Practices:**
- Use well-formatted documents
- Break large documents into smaller files
- Remove unnecessary content
- Use clear headings and structure

### Method 2: Scrape Website

1. Click **"+ Add Source"**
2. Select **"Add Website"**
3. Enter the website URL (e.g., `https://example.com/help`)
4. Click **"Scrape Website"**
5. The content will be extracted automatically

**Supported Websites:**
- Public documentation sites
- Help centers
- Blog posts
- Knowledge bases

**Note**: Private/password-protected pages are not accessible.

### Method 3: Add Text Content

1. Click **"+ Add Source"**
2. Select **"Add Text"**
3. Give your source a name
4. Paste or type your content (up to 50,000 characters)
5. Click **"Add Text Source"**

**Use Cases:**
- Company policies
- Product descriptions
- Quick FAQs
- Custom instructions

### Managing Sources

- **View Sources**: See all added sources in the Sources tab
- **Delete Source**: Click the trash icon next to any source
- **Status Indicators**:
  - 🔵 **Processing**: Content is being analyzed
  - ✅ **Completed**: Source is ready to use
  - ❌ **Failed**: Error occurred (hover for details)

---

## Customizing Appearance

### Branding Your Chatbot

1. Navigate to **"Appearance"** tab
2. Customize the following:

#### Color Theme
- **Primary Color**: Main chatbot color (buttons, headers)
- **Secondary Color**: Accent color (highlights, gradients)
- Click the color picker to choose custom colors
- Live preview shows changes in real-time

#### Branding Assets
- **Logo URL**: Your company logo (shown in chat header)
- **Avatar URL**: Chatbot avatar (shown next to messages)
- Use direct image URLs (HTTPS recommended)
- Recommended sizes:
  - Logo: 200x50px
  - Avatar: 100x100px (circular)

#### Welcome Message
- Customize the first message users see
- Keep it friendly and informative
- Examples:
  - "Hi! I'm here to help you with product questions. What can I assist you with?"
  - "Welcome to Acme Support! Ask me anything about our services."

#### Widget Settings
- **Position**: Choose where the chat widget appears:
  - Bottom-right (default)
  - Bottom-left
  - Top-right
  - Top-left
- **Theme**: Light, Dark, or Auto (follows system)

3. Click **"Save Appearance"**
4. Click **"View Live Preview"** to see changes immediately

---

## Testing Your Chatbot

### Preview Mode

1. Click **"Preview"** button (top-right of builder)
2. A chat window opens
3. Type test questions to interact with your bot
4. Check if responses are accurate and relevant

### Testing Checklist:

☐ Test basic questions from your knowledge base
☐ Ask questions not in your data (should respond appropriately)
☐ Check response tone and style
☐ Verify branding appears correctly
☐ Test on mobile view
☐ Verify response time is acceptable

### Tips for Better Results:

1. **Add Comprehensive Sources**: More context = better answers
2. **Clear System Message**: Define behavior and boundaries
3. **Test Edge Cases**: Ask unusual or off-topic questions
4. **Iterate**: Refine system message based on test results

---

## Analytics & Insights

### Overview Tab

View analytics for a specific chatbot:

1. Go to **"Analytics"** tab in Chatbot Builder
2. See key metrics:
   - **Total Conversations**: Number of chat sessions
   - **Total Messages**: User + bot messages
   - **Avg Response Time**: How fast your bot responds
   - **Active Users**: Unique users in selected period

### Insights Tab

Access advanced analytics:

1. Click **"Insights"** tab
2. Select time period (7, 30, or 90 days)
3. View powerful visualizations:

#### Message Volume Trend
- Line chart showing daily message count
- Identify busy periods and growth trends

#### Response Time Trend
- Track chatbot performance over time
- Optimize if response times increase

#### Hourly Activity Distribution
- Bar chart showing messages by hour (0-23)
- Identify peak hours
- Schedule maintenance during low-traffic times

#### Top Asked Questions
- Most frequent user queries
- Improve answers for common questions
- Identify missing documentation

#### Satisfaction Distribution
- Pie chart with 1-5 star ratings
- User feedback on chat quality
- Monitor satisfaction trends

### Chat Logs

1. Click **"Load Chat Logs"** in Analytics tab
2. View all conversations with:
   - User name and email
   - Conversation status (Active/Resolved/Escalated)
   - Message count
   - Timestamp
3. Click **"View Messages"** to expand full conversation
4. Review user-bot interactions
5. Use insights to:
   - Improve responses
   - Identify common issues
   - Train on new topics

---

## Sharing & Deployment

### Widget Tab

Configure and generate widget code:

1. Go to **"Widget"** tab
2. Customize widget settings (position, theme)
3. Toggle **"Enable Widget"** to activate

### Share Tab

Multiple deployment options:

#### 1. Public Chat Link
- Toggle **"Public Access"** ON
- Copy the public URL
- Share link via email, social media, or QR code
- Anyone with the link can chat

**Example URL:**
```
https://botsmith.ai/public-chat/your-chatbot-id
```

#### 2. Website Embed

**Step 1**: Copy embed code
```html
<iframe 
  src="https://botsmith.ai/embed/your-chatbot-id"
  width="400"
  height="600"
  frameborder="0"
></iframe>
```

**Step 2**: Paste into your website's HTML
- Before closing `</body>` tag for widget
- In specific page section for inline embed

**Step 3**: Publish your website

#### 3. Export Conversations

- Click **"Export Conversations"**
- Choose format: JSON or CSV
- Select date range
- Download file for analysis

#### 4. Webhooks

- Configure webhook URL for real-time notifications
- Receive events when:
  - New conversation starts
  - User sends message
  - Chatbot responds
  - Conversation ends

**Webhook payload example:**
```json
{
  "event": "message.received",
  "chatbot_id": "uuid",
  "conversation_id": "uuid",
  "message": "User message",
  "timestamp": "2025-01-28T10:30:00Z"
}
```

---

## Managing Subscriptions

### View Current Plan

1. Click **"Subscription"** in navigation
2. See your current plan details:
   - Plan name (Free, Starter, Professional, Enterprise)
   - Status (Active, Trial, Expired)
   - Usage statistics with progress bars

### Understanding Plans

#### Free Plan ($0/month)
- 1 chatbot
- 100 messages/month
- 5 file uploads
- 2 website sources
- 5 text sources
- Basic analytics
- Community support

#### Starter Plan ($150/month)
- 5 chatbots
- 10,000 messages/month
- Priority support
- Custom branding
- All AI models
- API access

#### Professional Plan ($499/month)
- 25 chatbots
- 100,000 messages/month
- 24/7 priority support
- Full API access
- All AI models
- Custom integrations
- Dedicated account manager

#### Enterprise Plan (Custom Pricing)
- Unlimited everything
- Custom analytics
- Dedicated 24/7 support
- White-label solution
- On-premise deployment
- Custom AI training
- SLA guarantee

### Upgrade Process

1. Click **"Upgrade Plan"** button
2. Select desired plan
3. Click **"Subscribe Now"**
4. Enter payment information (Secure via Stripe)
5. Confirm subscription
6. New limits apply immediately

### Downgrade or Cancel

1. Go to Subscription page
2. Click **"Manage Subscription"**
3. Select **"Change Plan"** or **"Cancel Subscription"**
4. Confirm action
5. Changes take effect at end of billing period

---

## Account Settings

### Update Profile

1. Click your profile icon (top-right)
2. Select **"Account Settings"**
3. Update information:
   - Name
   - Phone number
   - Company name
   - Job title
   - Bio
4. Click **"Update Profile"**

### Change Email

1. Go to Account Settings
2. Scroll to **"Email Settings"**
3. Enter new email
4. Click **"Update Email"**
5. Verify new email address

### Change Password

1. Go to Account Settings
2. Scroll to **"Security"**
3. Enter:
   - Current password
   - New password
   - Confirm new password
4. Click **"Change Password"**

### Delete Account

⚠️ **Warning**: This action is permanent!

1. Go to Account Settings
2. Scroll to bottom
3. Click **"Delete Account"**
4. Review what will be deleted:
   - All chatbots
   - All sources
   - All conversations
   - Profile information
5. Type your password to confirm
6. Click **"Delete My Account"**

---

## Troubleshooting

### Chatbot Not Responding

**Issue**: Chatbot doesn't reply or gives generic answers

**Solutions**:
1. Check if chatbot is active (toggle in Settings)
2. Verify API key is configured (check with support)
3. Ensure sources are fully processed (not stuck in "Processing")
4. Review system message for conflicts
5. Test with simple questions first

### Source Upload Failed

**Issue**: File upload shows "Failed" status

**Solutions**:
1. Check file size (must be under 100MB)
2. Verify file format (PDF, DOCX, TXT, XLSX, CSV only)
3. Ensure file is not corrupted
4. Try re-uploading
5. Check if file is password-protected (not supported)

### Website Scraping Not Working

**Issue**: Website source fails or returns empty

**Solutions**:
1. Verify URL is publicly accessible
2. Check if site blocks scrapers (robots.txt)
3. Try different pages from same domain
4. Use "Add Text" and paste content manually
5. Contact support for specific domains

### Slow Response Times

**Issue**: Chatbot takes too long to respond

**Solutions**:
1. Switch to faster model (GPT-4o-mini, Gemini 2.0 Flash)
2. Reduce number of sources (keep most relevant)
3. Check Analytics > Response Time Trend
4. Clear conversation history (start new session)
5. Upgrade plan for better performance

### Appearance Not Updating

**Issue**: Changes to colors/branding don't appear

**Solutions**:
1. Click **"Save Appearance"** after changes
2. Click **"View Live Preview"** to refresh
3. Clear browser cache (Ctrl+Shift+Delete)
4. Open public chat link in incognito mode
5. Wait 5 minutes for CDN cache to clear

### Analytics Not Showing Data

**Issue**: Analytics page shows zeros or "No data"

**Solutions**:
1. Ensure chatbot has received messages
2. Check selected date range includes activity
3. Refresh page
4. Wait 5-10 minutes for data processing
5. Create test conversations using Preview

### Subscription Issues

**Issue**: Plan limits not updated after upgrade

**Solutions**:
1. Sign out and sign back in
2. Check payment was successful (email confirmation)
3. Wait 5 minutes for sync
4. Contact support with transaction ID

### Contact Support

If issues persist:
- **Email**: support@botsmith.ai
- **Phone**: +1 (555) 123-4567
- **Live Chat**: Available 24/7 on dashboard
- **Help Center**: https://help.botsmith.ai

---

## Best Practices

### ✅ Do's

1. **Test Regularly**: Preview after every major change
2. **Update Sources**: Keep knowledge base current
3. **Monitor Analytics**: Check weekly for insights
4. **Iterate System Message**: Refine based on performance
5. **Use Clear Branding**: Professional logos and colors
6. **Add Multiple Sources**: Comprehensive coverage
7. **Review Chat Logs**: Learn from user interactions

### ❌ Don'ts

1. **Don't Ignore Errors**: Fix failed sources immediately
2. **Don't Overload**: Quality > quantity for sources
3. **Don't Neglect Testing**: Always preview before sharing
4. **Don't Use Generic Messages**: Customize for your brand
5. **Don't Ignore Feedback**: Act on user satisfaction ratings
6. **Don't Set Unrealistic Expectations**: Define chatbot limits clearly
7. **Don't Forget to Save**: Always save changes before exiting

---

## FAQs

**Q: How many languages does BotSmith support?**
A: All AI models support 50+ languages. Your chatbot responds in the language users write in.

**Q: Can I use my own API keys?**
A: Yes, contact support for custom API key integration (Professional plan and above).

**Q: Is my data secure?**
A: Yes, all data is encrypted in transit (TLS 1.3) and at rest (AES-256). We're SOC 2 compliant.

**Q: Can I transfer chatbots between accounts?**
A: Yes, contact support for chatbot transfers.

**Q: What happens if I exceed my plan limits?**
A: Chatbots pause automatically. Upgrade to resume service or wait for monthly reset.

**Q: Can I get a refund?**
A: Yes, within 30 days of purchase. Contact support for refund requests.

**Q: Do you offer white-label solutions?**
A: Yes, available with Enterprise plan. Contact sales for details.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Create New Chatbot | `Ctrl + N` |
| Open Preview | `Ctrl + P` |
| Save Changes | `Ctrl + S` |
| Search Chatbots | `Ctrl + F` |
| Open Settings | `Ctrl + ,` |
| Go to Dashboard | `Ctrl + H` |
| Go to Analytics | `Ctrl + A` |

---

**Need more help?** Visit our [Help Center](https://help.botsmith.ai) or contact support!