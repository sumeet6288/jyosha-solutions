# 📋 BotSmith - Quick Reference Guide

## 🚀 Quick Navigation

### For End Users
- **Homepage**: https://quickinstall-2.preview.emergentagent.com/
- **Start Building**: https://quickinstall-2.preview.emergentagent.com/dashboard
- **Pricing**: https://quickinstall-2.preview.emergentagent.com/pricing
- **Help**: https://quickinstall-2.preview.emergentagent.com/resources

### For Administrators
- **Admin Panel**: https://quickinstall-2.preview.emergentagent.com/admin
- **User Management**: Admin Dashboard → Users Tab
- **System Settings**: Admin Dashboard → Settings Tab

---

## 📱 All Pages at a Glance

### 🌐 Public Pages (7)
| # | Page | Route | Purpose |
|---|------|-------|---------|
| 1 | Landing Page | `/` | Product homepage |
| 2 | Pricing | `/pricing` | Plans & pricing |
| 3 | Enterprise | `/enterprise` | Enterprise solutions |
| 4 | Resources | `/resources` | Documentation |
| 5 | Public Chat | `/public-chat/:id` | Chat interface |
| 6 | Embed Chat | `/embed/:id` | Embeddable widget |
| 7 | 404 Page | `*` | Error page |

### 🏠 Main App Pages (7)
| # | Page | Route | Key Features |
|---|------|-------|--------------|
| 1 | Dashboard | `/dashboard` | Overview, stats, chatbot list |
| 2 | Chatbot Builder | `/chatbot/:id` | **7 tabs**: Sources, Settings, Appearance, Widget, Analytics, Insights, Share |
| 3 | Analytics | `/analytics` | Global analytics |
| 4 | Subscription | `/subscription` | Plans & usage |
| 5 | Integrations | `/integrations` | Third-party apps |
| 6 | Account Settings | `/account-settings` | Profile management |
| 7 | Chat Page | `/chat/:id` | Testing interface |

### 👨‍💼 Admin Pages (1)
| # | Page | Route | Key Features |
|---|------|-------|--------------|
| 1 | Admin Dashboard | `/admin` | User management, system settings |

---

## 🎯 Feature Quick Lookup

### Chatbot Builder - 7 Tabs Overview

#### 1️⃣ Sources Tab
- Upload files (PDF, DOCX, TXT, XLSX, CSV)
- Add websites
- Add text content
- Max file size: 100MB

#### 2️⃣ Settings Tab
- Choose AI provider: OpenAI, Claude, Gemini
- Select model
- Adjust temperature
- Set instructions & welcome message

#### 3️⃣ Appearance Tab
- Customize colors (primary, secondary, accent)
- Add logo & avatar
- Edit welcome message
- Widget positioning

#### 4️⃣ Widget Tab
- Configure widget position
- Choose theme (light/dark/auto)
- Widget size options

#### 5️⃣ Analytics Tab
- View conversations & messages
- See chat logs
- User interactions
- Performance metrics

#### 6️⃣ Insights Tab
- Response time trends
- Hourly activity distribution
- Top questions
- Satisfaction ratings (1-5 stars)

#### 7️⃣ Share Tab
- Public access toggle
- Get public chat link
- Generate embed code
- Export conversations (JSON/CSV)
- Webhook setup

---

## 🤖 AI Models Available

### OpenAI
- `gpt-4o-mini` (default)
- `gpt-4o`
- `gpt-4-turbo`

### Anthropic (Claude)
- `claude-3.5-sonnet`
- `claude-3-opus`

### Google (Gemini)
- `gemini-2.0-flash-exp`
- `gemini-1.5-pro`

---

## 💳 Subscription Plans

| Plan | Price | Chatbots | Messages/Month | Features |
|------|-------|----------|----------------|----------|
| **Free** | $0 | 1 | 100 | Basic analytics, community support |
| **Starter** | $150 | 5 | 5,000 | Multi-provider AI, advanced analytics |
| **Professional** | $499 | 20 | 50,000 | All providers, webhooks, white-label |
| **Enterprise** | Custom | ∞ | ∞ | Dedicated support, SLA, custom integrations |

---

## 👥 Admin Panel - User Management

### User Actions (6 buttons per user)
1. **Edit** - Update profile, role, status, limits
2. **View Stats** - Usage metrics & analytics
3. **Activity Logs** - Action history
4. **Login History** - Login tracking with IPs
5. **Password Reset** - Admin password reset
6. **Delete** - Remove user & data

### Bulk Operations
- ✅ Bulk delete users
- ✅ Bulk role assignment
- ✅ Bulk status change
- ✅ Bulk export to CSV

### User Filters
- Search by name/email
- Filter by status (active/suspended/banned)
- Filter by role (user/moderator/admin)
- Sort by date, activity, name

---

## 🎨 Branding Elements

### Logo Design
- **Type**: Animated robot icon
- **Colors**: Purple (#7c3aed) → Fuchsia (#d946ef) → Pink (#ec4899)
- **Effects**: Sparkles, glow, pulse animations
- **Badge**: "AI" badge in purple

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Purple | #7c3aed | Primary brand |
| Fuchsia | #d946ef | Gradients |
| Pink | #ec4899 | Accents |
| Yellow | #fbbf24 | Sparkles |
| Cyan | #22d3ee | Highlights |

---

## 📊 Analytics Features

### Dashboard Analytics
- Total conversations
- Total messages  
- Active chatbots
- Total chatbots

### Chatbot Analytics
- Conversations over time
- Messages over time
- Chat logs with full threads
- Date range filters (7/30/90 days)

### Advanced Insights
- Response time trends (LineChart)
- Hourly activity (BarChart)
- Top questions (BarChart)
- Satisfaction distribution (PieChart)
- Performance metrics

---

## 🔗 Public Chat Features

### Customization
- Custom colors (primary, secondary)
- Custom logo display
- Custom avatar
- Custom welcome message
- Theme selector (light/dark/auto)

### Functionality
- Real-time messaging
- Session management
- Conversation history
- Knowledge base integration
- User info capture (name, email)

### Live Preview
- View changes instantly
- Cache-busting support
- Appearance tab → "View Live Preview" button

---

## 📁 Source Management

### Supported File Types
- **Documents**: PDF, DOCX, TXT
- **Spreadsheets**: XLSX, CSV
- **Max Size**: 100MB

### Source Types
1. **Files** - Upload documents
2. **Website** - Scrape URLs
3. **Text** - Direct content input

### Processing
- Automatic content extraction
- Status tracking (processing/processed/failed)
- Error handling with messages

---

## 🔐 User Roles

| Role | Access Level | Permissions |
|------|--------------|-------------|
| **User** | Standard | Create chatbots, manage own data |
| **Moderator** | Enhanced | User permissions + content moderation |
| **Admin** | Full | All permissions + user management |

---

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640-768px
- **Desktop**: 768-1024px
- **Large**: > 1024px

### Mobile Features
- Hamburger menu
- Touch-friendly (44x44px minimum)
- Stacked layouts
- Bottom sheet modals
- Simplified tables

---

## ⚡ Quick Commands

### Create New Chatbot
1. Dashboard → "Create New" button
2. Enter chatbot name
3. Select AI provider & model
4. Add sources (optional)
5. Customize appearance
6. Publish & share

### Edit Existing Chatbot
1. Dashboard → Find chatbot → "Manage"
2. Navigate to desired tab
3. Make changes
4. Click "Save Changes"

### Upgrade Plan
1. Dashboard → "Upgrade Plan" button
   OR
2. Subscription → Select plan → "Upgrade"

### View Analytics
1. Dashboard → "Analytics" tab
   OR
2. Chatbot Builder → "Analytics" or "Insights" tab

### Manage Users (Admin)
1. Admin Dashboard → "Users" tab
2. Search/filter users
3. Click action buttons
4. Make changes in modals

---

## 🔧 Technical Info

### Stack
- **Frontend**: React 18 + Tailwind CSS
- **Backend**: FastAPI + MongoDB
- **AI**: LiteLLM + EmergentIntegrations
- **Charts**: Recharts
- **Icons**: Lucide React

### Ports
- **Frontend**: 3000
- **Backend**: 8001
- **MongoDB**: 27017

### API Base URL
- Development: `http://localhost:8001`
- Production: `https://quickinstall-2.preview.emergentagent.com`

---

## 📞 Support & Resources

### Documentation
- **Full Docs**: `/app/PAGES_DOCUMENTATION.md`
- **Branding Guide**: `/app/BRANDING_ENHANCEMENT_DOCS.md`
- **Database Schema**: `/app/DATABASE_STRUCTURE.md`
- **Quick Reference**: `/app/QUICK_REFERENCE.md` (this file)

### Contact
- **Email**: support@botsmith.ai
- **Website**: https://quickinstall-2.preview.emergentagent.com
- **Resources**: https://quickinstall-2.preview.emergentagent.com/resources

---

## 🐛 Common Issues & Solutions

### Issue: Changes not reflecting
**Solution**: Hard refresh (Ctrl+F5 / Cmd+Shift+R)

### Issue: Chatbot not responding
**Solution**: Check AI provider settings & API configuration

### Issue: File upload fails
**Solution**: Ensure file is < 100MB and supported format

### Issue: Admin panel shows no users
**Solution**: Expected in dev mode (mocked authentication)

### Issue: Live preview not updating
**Solution**: Click "View Live Preview" button after saving

---

## ✅ Pre-Deployment Checklist

- [ ] Test all AI providers (OpenAI, Claude, Gemini)
- [ ] Verify file uploads work
- [ ] Check public chat customization
- [ ] Test embed code generation
- [ ] Verify webhook functionality
- [ ] Test mobile responsiveness
- [ ] Check all navigation links
- [ ] Verify analytics charts render
- [ ] Test subscription upgrade flow
- [ ] Review admin panel features
- [ ] Implement real authentication
- [ ] Configure production API keys
- [ ] Set up monitoring & logging
- [ ] Configure SSL certificates
- [ ] Set up backup strategy

---

**Quick Reference Version:** 1.0  
**Last Updated:** October 27, 2025  
**Status:** ✅ Complete
