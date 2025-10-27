# 🗺️ BotSmith Application - Visual Sitemap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          🏠 LANDING PAGE (/)                                 │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Pricing    │  │  Enterprise  │  │  Resources   │  │   Sign In    │   │
│  │  /pricing    │  │ /enterprise  │  │  /resources  │  │   /signin    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                              │
│  ┌──────────────┐                                                           │
│  │   Sign Up    │                                                           │
│  │   /signup    │                                                           │
│  └──────────────┘                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
                          Both redirect to Dashboard
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       📊 DASHBOARD (/dashboard)                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Navigation Bar                                                      │   │
│  │  • Chatbots  • Analytics  • Subscription  • Integrations            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  Stats Cards                                                      │      │
│  │  • Total Conversations  • Total Messages                          │      │
│  │  • Active Chatbots     • Total Chatbots                          │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  Free Plan Usage Monitor                                          │      │
│  │  • Chatbots: 1/1 (100%) ████████████████████                      │      │
│  │  • Messages: 0/100 (0%) ░░░░░░░░░░░░░░░░░░░░                      │      │
│  │  • Files: 0/5  • Websites: 0/2  • Text: 0/5                      │      │
│  │  [Upgrade Plan]                                                    │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  Your Chatbots                              [+ Create New]        │      │
│  │  ┌──────────────────────────────────────────────────────────┐    │      │
│  │  │ 🤖 New Chatbot          Active  gpt-4o-mini              │    │      │
│  │  │    0 conversations  |  0 messages    [Toggle] [Manage]   │    │      │
│  │  └──────────────────────────────────────────────────────────┘    │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                    │                    │
         ┌──────────┴──────────┬─────────┴─────────┬─────────┴──────────┐
         ↓                     ↓                   ↓                     ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   📈 ANALYTICS   │  │ 💳 SUBSCRIPTION   │  │ 🔌 INTEGRATIONS  │  │ ⚙️ ACCOUNT       │
│   /analytics     │  │  /subscription    │  │  /integrations   │  │   SETTINGS       │
│                  │  │                   │  │                  │  │  /account-       │
│ Global analytics │  │ • Current Plan    │  │ • Available      │  │   settings       │
│ across all bots  │  │ • Usage Stats     │  │   Integrations   │  │                  │
│                  │  │ • Plan Cards      │  │ • Connected      │  │ • Profile Update │
│ • Total Convs    │  │ • Upgrade Button  │  │   Services       │  │ • Email Change   │
│ • Total Messages │  │                   │  │ • API Keys       │  │ • Password       │
│ • Charts         │  │ Plans:            │  │                  │  │ • Delete Account │
│ • Date Filters   │  │ • Free ($0)       │  │                  │  │                  │
│                  │  │ • Starter ($150)  │  │                  │  │                  │
│                  │  │ • Pro ($499)      │  │                  │  │                  │
│                  │  │ • Enterprise      │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
         
                                      ↓ Click "Manage" on Chatbot
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🤖 CHATBOT BUILDER (/chatbot/:id)                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Tab Navigation                                                       │  │
│  │  📁Sources │ ⚙️Settings │ 🎨Appearance │ 💬Widget │ 📊Analytics │    │  │
│  │            │           │              │         │ 📈Insights  │ 🔗Share│  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
         │             │              │            │           │         │
         ↓             ↓              ↓            ↓           ↓         ↓

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 📁 SOURCES   │  │ ⚙️ SETTINGS  │  │ 🎨 APPEARANCE│  │ 💬 WIDGET    │
│              │  │              │  │              │  │              │
│ • File Upload│  │ • Name       │  │ • Primary    │  │ • Position   │
│ • Website    │  │ • Status     │  │   Color      │  │ • Theme      │
│ • Text       │  │ • Provider   │  │ • Secondary  │  │ • Size       │
│              │  │   - OpenAI   │  │   Color      │  │              │
│ Max 100MB    │  │   - Claude   │  │ • Logo URL   │  │ Installation │
│              │  │   - Gemini   │  │ • Avatar URL │  │ Instructions │
│ Source List: │  │ • Model      │  │ • Welcome    │  │              │
│ ┌──────────┐ │  │ • Temp 0-1   │  │   Message    │  │              │
│ │📄 doc.pdf│ │  │ • Instructions│ │              │  │              │
│ └──────────┘ │  │ • Welcome    │  │ [View Live   │  │              │
│              │  │   Message    │  │  Preview]    │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 📊 ANALYTICS │  │ 📈 INSIGHTS  │  │ 🔗 SHARE     │
│              │  │              │  │              │
│ • Total Convs│  │ • Response   │  │ • Public     │
│ • Total Msgs │  │   Time Trend │  │   Access     │
│ • Date Range │  │   (LineChart)│  │   Toggle     │
│              │  │ • Hourly     │  │              │
│ Charts:      │  │   Activity   │  │ • Public     │
│ • Convs/Time │  │   (BarChart) │  │   Chat Link  │
│ • Msgs/Time  │  │ • Top Qs     │  │   [Copy]     │
│              │  │   (BarChart) │  │              │
│ [Load Chat   │  │ • Satisfaction│ │ • Embed Code │
│  Logs]       │  │   (PieChart) │  │   Generator  │
│              │  │ • Stats Cards│  │   [Copy]     │
│ Conversations│  │              │  │              │
│ ┌──────────┐ │  │ Period:      │  │ • Export CSV │
│ │ User 1   │ │  │ • 7 days     │  │ • Export JSON│
│ │ [Expand] │ │  │ • 30 days    │  │              │
│ └──────────┘ │  │ • 90 days    │  │ • Webhook    │
│   Messages:  │  │              │  │   URL        │
│   • You: Hi  │  │              │  │   [Enable]   │
│   • Bot: Hey │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
                                              │
                                              ↓ View Live Preview
                                              ↓
                                    ┌──────────────────┐
                                    │ 💬 PUBLIC CHAT   │
                                    │ /public-chat/:id │
                                    │                  │
                                    │ • Custom Colors  │
                                    │ • Custom Logo    │
                                    │ • Custom Avatar  │
                                    │ • Chat Interface │
                                    │ • Real-time      │
                                    │   Messaging      │
                                    └──────────────────┘
                                              │
                                              ↓ Can also be embedded
                                              ↓
                                    ┌──────────────────┐
                                    │ 🔗 EMBED CHAT    │
                                    │   /embed/:id     │
                                    │                  │
                                    │ • Widget Mode    │
                                    │ • Iframe         │
                                    │ • Minimizable    │
                                    └──────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       👨‍💼 ADMIN DASHBOARD (/admin)                          │
│                    (Accessible from User Profile Dropdown)                   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Tab Navigation                                                       │  │
│  │  📊 Overview │ 👥 Users │ ⚙️ Settings │ 📈 Analytics                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Users Management (EnhancedUsersManagement)                          │  │
│  │                                                                        │  │
│  │  Search: [_____________]  Status: [All▾]  Role: [All▾]  Sort: [▾]   │  │
│  │                                                                        │  │
│  │  [ ] Select All                               [Bulk Actions ▾]       │  │
│  │                                                                        │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │ [ ] 👤 John Doe (john@example.com)       👤user  🟢active     │  │  │
│  │  │     Created: Oct 1, 2025  |  Last login: 2 hours ago          │  │  │
│  │  │                                                                 │  │  │
│  │  │     [✏️Edit] [📊Stats] [📋Activity] [🔒Login] [🔑Reset] [🗑️Del]│  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                        │  │
│  │  Pagination: [1] 2 3 ... 10                                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Action Modals:                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ ✏️ Edit User │  │ 📊 View Stats│  │ 📋 Activity  │  │ 🔒 Login     │   │
│  │              │  │              │  │    Logs      │  │   History    │   │
│  │ • Name/Email │  │ • Chatbots   │  │              │  │              │   │
│  │ • Role       │  │ • Messages   │  │ • Actions    │  │ • Timestamp  │   │
│  │ • Status     │  │ • Sources    │  │ • Resources  │  │ • IP Address │   │
│  │ • Profile    │  │ • Activity   │  │ • Timestamps │  │ • User Agent │   │
│  │ • Limits     │  │ • Charts     │  │              │  │ • Success    │   │
│  │ • Notes      │  │              │  │              │  │   /Fail      │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐                                         │
│  │ 🔑 Password  │  │ 📦 Bulk      │                                         │
│  │    Reset     │  │   Actions    │                                         │
│  │              │  │              │                                         │
│  │ • New Pass   │  │ • Delete     │                                         │
│  │ • Confirm    │  │ • Change Role│                                         │
│  │ • Generate   │  │ • Change Stat│                                         │
│  │   Random     │  │ • Export CSV │                                         │
│  └──────────────┘  └──────────────┘                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         🔧 UTILITY PAGES                                     │
│                                                                              │
│  ┌──────────────────┐       ┌──────────────────┐                           │
│  │ 💬 CHAT PAGE     │       │ 🚫 404 NOT FOUND │                           │
│  │   /chat/:id      │       │     /* (all)     │                           │
│  │                  │       │                  │                           │
│  │ Internal testing │       │ Error page for   │                           │
│  │ interface for    │       │ undefined routes │                           │
│  │ chatbot owners   │       │                  │                           │
│  │                  │       │ [Go Home]        │                           │
│  │ • Debug mode     │       │                  │                           │
│  │ • Performance    │       │                  │                           │
│  │ • Testing        │       │                  │                           │
│  └──────────────────┘       └──────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      🎯 USER FLOW EXAMPLES                                   │
│                                                                              │
│  Example 1: Create & Customize a Chatbot                                   │
│  ──────────────────────────────────────────────────────────────────────     │
│  Landing → Sign Up → Dashboard → Create New → Chatbot Builder              │
│    ↓                                                                         │
│  Sources Tab → Upload Files/Add Website                                     │
│    ↓                                                                         │
│  Settings Tab → Choose GPT-4 → Set Temperature → Add Instructions          │
│    ↓                                                                         │
│  Appearance Tab → Pick Colors → Add Logo → Customize Welcome               │
│    ↓                                                                         │
│  Share Tab → Enable Public Access → Copy Link → Done!                      │
│                                                                              │
│  Example 2: Upgrade Subscription                                            │
│  ──────────────────────────────────────────────────────────────────────     │
│  Dashboard → Upgrade Plan Button → Subscription Page                        │
│    ↓                                                                         │
│  Select Plan (Starter/Pro/Enterprise) → Upgrade Button                     │
│    ↓                                                                         │
│  Payment Flow (LemonSqueezy) → Success → Updated Plan                      │
│                                                                              │
│  Example 3: Admin Manages User                                              │
│  ──────────────────────────────────────────────────────────────────────     │
│  Admin Dashboard → Users Tab → Search User                                  │
│    ↓                                                                         │
│  Click Edit → Update Role to Moderator → Set Custom Limits                 │
│    ↓                                                                         │
│  Add Admin Notes → Save Changes → User Updated                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 DATABASE COLLECTIONS                                  │
│                                                                              │
│  Database: chatbase_db                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │   users      │  │  chatbots    │  │   sources    │                     │
│  │   (26 flds)  │  │  (35+ flds)  │  │   (11 flds)  │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │conversations │  │  messages    │  │  analytics   │                     │
│  │   (10 flds)  │  │   (7 flds)   │  │   (9 flds)   │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │conversation_ │  │login_history │  │activity_logs │                     │
│  │   ratings    │  │   (8 flds)   │  │   (9 flds)   │                     │
│  │   (6 flds)   │  │              │  │              │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  Database: botsmith                                                         │
│  ┌──────────────┐  ┌──────────────┐                                        │
│  │    plans     │  │subscriptions │                                        │
│  │  (10+ flds)  │  │  (9+ flds)   │                                        │
│  └──────────────┘  └──────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      📱 RESPONSIVE DESIGN                                    │
│                                                                              │
│  Mobile (< 640px)      Tablet (640-768px)    Desktop (> 768px)             │
│  ┌──────────────┐     ┌──────────────┐      ┌──────────────┐              │
│  │ ☰ Hamburger  │     │ Split Layout │      │  Full Layout │              │
│  │              │     │              │      │              │              │
│  │ Stacked      │     │ 2-Column     │      │  3-Column    │              │
│  │ Single Col   │     │ Grid         │      │  Grid        │              │
│  │              │     │              │      │              │              │
│  │ Touch UI     │     │ Hybrid       │      │  Mouse/Keys  │              │
│  └──────────────┘     └──────────────┘      └──────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Page Hierarchy

```
├── Public (7 pages)
│   ├── Landing Page
│   ├── Pricing
│   ├── Enterprise
│   ├── Resources
│   ├── Public Chat
│   ├── Embed Chat
│   └── 404 Not Found
│
├── Authentication (2 pages - bypassed)
│   ├── Sign In (→ Dashboard)
│   └── Sign Up (→ Dashboard)
│
├── Main App (7 pages)
│   ├── Dashboard
│   ├── Chatbot Builder (7 tabs)
│   │   ├── Sources
│   │   ├── Settings
│   │   ├── Appearance
│   │   ├── Widget
│   │   ├── Analytics
│   │   ├── Insights
│   │   └── Share
│   ├── Analytics
│   ├── Subscription
│   ├── Integrations
│   ├── Account Settings
│   └── Chat Page
│
└── Admin (1 page)
    └── Admin Dashboard
        ├── Overview Tab
        ├── Users Tab
        ├── Settings Tab
        └── Analytics Tab
```

---

## 🎨 Visual Components Legend

| Symbol | Meaning |
|--------|---------|
| 🏠 | Homepage/Landing |
| 📊 | Dashboard/Analytics |
| 🤖 | Chatbot |
| 👥 | Users |
| ⚙️ | Settings |
| 📁 | Files/Sources |
| 💬 | Chat/Messages |
| 🎨 | Design/Appearance |
| 🔗 | Links/Sharing |
| 💳 | Subscription/Payment |
| 🔌 | Integrations |
| 👨‍💼 | Admin |
| 🔐 | Authentication |
| 📈 | Insights/Graphs |
| 🚫 | Error/Not Found |
| ✏️ | Edit |
| 🗑️ | Delete |
| 📋 | Logs |
| 🔒 | Security |

---

**Sitemap Version:** 1.0  
**Last Updated:** October 27, 2025  
**Total Pages:** 19  
**Total Routes:** 17 active
