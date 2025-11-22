# 🚀 BotSmith AI - Quick Start Guide

## ✅ Setup Complete - Application Ready!

### 📊 System Status

**All services are running successfully:**

- ✅ **Backend API** - Running on port 8001
- ✅ **Frontend App** - Running on port 3000  
- ✅ **MongoDB** - Running on port 27017
- ✅ **Database** - `chatbase_db` initialized with data

---

## 🌐 Access the Application

### **Live Application URL**
```
https://rapid-stack-launch.preview.emergentagent.com
```

### **API Documentation**
```
https://rapid-stack-launch.preview.emergentagent.com/docs
```

---

## 🔑 Default Admin Credentials

**Email:** `admin@botsmith.com`  
**Password:** `admin123`

> ⚠️ **Important:** Change the default password after first login for security

---

## 📦 Installed Dependencies

### Backend (Python - FastAPI)
- ✅ All packages from `requirements.txt` installed
- ✅ FastAPI and Uvicorn
- ✅ MongoDB drivers (motor, pymongo)
- ✅ AI Libraries (OpenAI, Anthropic, Google GenAI)
- ✅ emergentintegrations
- ✅ Document processing (pypdf, python-docx, openpyxl, beautifulsoup4)
- ✅ Total: 47+ packages

### Frontend (React)
- ✅ All packages from `package.json` installed via Yarn
- ✅ React 18.x
- ✅ React Router DOM
- ✅ Tailwind CSS
- ✅ Recharts for analytics
- ✅ Axios for API calls
- ✅ Total: 944+ packages

---

## 🗄️ Database Configuration

**MongoDB Database:** `chatbase_db`

**Collections Initialized:**
- ✅ `users` (1 admin user)
- ✅ `plans` (4 subscription plans: Free, Starter, Professional, Enterprise)

**Database Connection:**
```
MONGO_URL: mongodb://localhost:27017
DB_NAME: chatbase_db
```

---

## 🎯 Key Features Available

### 1. **AI Chatbot Builder**
   - Multi-provider support (OpenAI, Claude, Gemini)
   - Real-time chat with AI responses
   - Knowledge base integration

### 2. **Source Management**
   - File uploads (PDF, DOCX, TXT, XLSX, CSV)
   - Website scraping
   - Text content management

### 3. **Integration Management**
   - Slack, Telegram, Discord
   - WhatsApp, Messenger, Instagram
   - WebChat widget
   - REST API

### 4. **Admin Panel**
   - User management system
   - Analytics dashboard
   - Subscription management
   - System settings
   - Tech management (API keys, webhooks, logs)

### 5. **Analytics & Reporting**
   - Conversation analytics
   - Message statistics
   - Response time tracking
   - Hourly activity distribution
   - Provider usage statistics

### 6. **Subscription System**
   - 4 tier plans (Free, Starter, Professional, Enterprise)
   - Usage tracking and limits
   - Upgrade/downgrade functionality
   - Monthly billing cycle

---

## 🔧 Service Management

### Check Service Status
```bash
sudo supervisorctl status
```

### Restart Services
```bash
# Restart all services
sudo supervisorctl restart all

# Restart individual services
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart mongodb
```

### View Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
tail -f /var/log/supervisor/frontend.out.log
```

---

## 📝 Environment Variables

### Frontend (`/app/frontend/.env`)
```env
REACT_APP_BACKEND_URL=https://rapid-stack-launch.preview.emergentagent.com
WDS_SOCKET_PORT=443
REACT_APP_ENABLE_VISUAL_EDITS=true
ENABLE_HEALTH_CHECK=false
```

### Backend (`/app/backend/.env`)
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="chatbase_db"
CORS_ORIGINS="*"
SECRET_KEY="chatbase-secret-key-change-in-production-2024"
EMERGENT_LLM_KEY=sk-emergent-919922434748629944
```

---

## 🏗️ Project Structure

```
/app/
├── backend/              # FastAPI backend
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── models/          # Database models
│   ├── middleware/      # Custom middleware
│   ├── utils/           # Utility functions
│   ├── server.py        # Main server file
│   └── requirements.txt # Python dependencies
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Page components
│   │   ├── components/ # Reusable components
│   │   ├── App.js      # Main app component
│   │   └── index.js    # Entry point
│   ├── public/         # Static assets
│   └── package.json    # Node dependencies
│
└── test_result.md      # Testing documentation

```

---

## 🎨 Tech Stack

**Backend:**
- FastAPI (Python)
- MongoDB (Database)
- Motor (Async MongoDB driver)
- Pydantic (Data validation)

**Frontend:**
- React 18
- Tailwind CSS
- React Router DOM
- Axios
- Recharts

**AI Integration:**
- OpenAI GPT models
- Anthropic Claude
- Google Gemini
- emergentintegrations library

---

## 🚦 Next Steps

1. **Login to Admin Panel**
   - Visit the application URL
   - Click "Sign In"
   - Use admin credentials above

2. **Explore the Dashboard**
   - View statistics and analytics
   - Check existing chatbots
   - Review subscription plans

3. **Create Your First Chatbot**
   - Navigate to Dashboard
   - Click "Create Chatbot"
   - Configure AI provider and settings
   - Add knowledge base sources

4. **Set Up Integrations**
   - Go to Chatbot Builder → Integrations
   - Connect Slack, Telegram, or Discord
   - Test webhook connections

5. **Customize Settings**
   - Admin Panel → System Settings
   - Configure payment gateways
   - Set up email notifications
   - Manage API keys

---

## 🆘 Troubleshooting

### Services Not Starting
```bash
# Check logs for errors
tail -100 /var/log/supervisor/backend.err.log
tail -100 /var/log/supervisor/frontend.out.log

# Restart all services
sudo supervisorctl restart all
```

### Database Connection Issues
```bash
# Check MongoDB status
sudo supervisorctl status mongodb

# Test connection
mongosh --eval "db.adminCommand('ping')"
```

### Frontend Not Loading
```bash
# Check compilation status
tail -50 /var/log/supervisor/frontend.out.log | grep -i "compiled"

# Restart frontend
sudo supervisorctl restart frontend
```

---

## 📚 Additional Resources

- **API Documentation:** `/docs` endpoint
- **Testing Data:** `/app/test_result.md`
- **Setup Details:** `/app/SETUP_COMPLETE.md`
- **Provider Statistics:** `/app/PROVIDER_STATISTICS_FIX.md`

---

## ✨ Features Highlights

- **Multi-Provider AI Support** - OpenAI, Claude, Gemini
- **Real-Time Chat** - WebSocket support for instant messaging
- **RAG System** - Text-based retrieval with MongoDB
- **Document Processing** - Support for multiple file formats
- **Website Scraping** - Extract content from URLs
- **Integration Management** - Connect to 9+ platforms
- **Advanced Analytics** - Comprehensive reporting and insights
- **Subscription Management** - Tiered plans with usage tracking
- **Admin Panel** - Complete control over users and system
- **Responsive Design** - Beautiful UI with Tailwind CSS
- **Security Features** - Authentication, authorization, and encryption

---

## 🎉 Ready to Build!

Your BotSmith AI application is fully set up and ready to use. Login with the admin credentials and start building amazing AI-powered chatbots!

**Application URL:** https://rapid-stack-launch.preview.emergentagent.com

---

**Last Updated:** $(date)
**Setup Status:** ✅ Complete
**All Services:** ✅ Running
