# 🚀 BotSmith - Quick Start Guide

## 5-Minute Setup

Get BotSmith running locally in just 5 minutes!

### Prerequisites

Make sure you have these installed:
```bash
python --version  # 3.11 or higher
node --version    # 18 or higher
yarn --version    # 1.22 or higher
mongod --version  # 6.0 or higher
```

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone <repository-url>
cd botsmith

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
yarn install
cd ..
```

### Step 2: Configure Environment

**Backend (.env):**
```bash
cd backend
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017/botsmith
EMERGENT_LLM_KEY=your_key_here
SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
EOF
cd ..
```

**Frontend (.env):**
```bash
cd frontend
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=true
EOF
cd ..
```

### Step 3: Start MongoDB

```bash
# Start MongoDB
mongod --dbpath /data/db

# Or with Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

### Step 4: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

### Step 5: Access the App

- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8001
- 📖 **API Docs**: http://localhost:8001/docs

---

## Quick Tutorial

### 1. Create Your First Chatbot

1. Click "Try for Free" on the landing page
2. You'll be auto-signed in (development mode)
3. Click "+ Create New" on the dashboard
4. A chatbot is created automatically!

### 2. Add Knowledge Base

1. Click "+ Add Source" button
2. Choose one:
   - **Upload File**: PDF, DOCX, TXT, XLSX, CSV
   - **Add Website**: Paste any public URL
   - **Add Text**: Paste content directly
3. Wait for processing to complete

### 3. Customize Appearance

1. Go to **"Appearance"** tab
2. Pick your brand colors
3. Add logo and avatar URLs
4. Customize welcome message
5. Click **"Save Appearance"**
6. Click **"View Live Preview"**

### 4. Test Your Bot

1. Click **"Preview"** button (top-right)
2. Ask questions about your content
3. Check if responses are accurate
4. Iterate and improve!

### 5. Share Your Bot

1. Go to **"Share"** tab
2. Toggle **"Public Access"** ON
3. Copy the public chat link
4. Share with anyone!

---

## Common Tasks

### Get API Key

**Emergent LLM Key** (Recommended):
1. Go to your profile
2. Click "Universal Key"
3. Copy and paste in backend/.env

**Or use individual keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/app/apikey

### Change AI Model

1. Go to **"Settings"** tab
2. Select **Provider**: OpenAI, Anthropic, or Google
3. Select **Model**: 
   - Fast & cheap: GPT-4o-mini, Gemini 2.0 Flash
   - Best quality: Claude 3.5 Sonnet, GPT-4o
4. Click **"Save"**

### View Analytics

1. Go to **"Analytics"** tab (in chatbot builder)
2. See conversations, messages, response time
3. Go to **"Insights"** tab for advanced charts
4. Click **"Load Chat Logs"** to see conversations

### Upgrade Plan

1. Click **"Subscription"** in navigation
2. View current usage
3. Click **"Upgrade Plan"**
4. Choose a plan
5. Enter payment details

---

## Troubleshooting

### Backend won't start

```bash
# Check if MongoDB is running
mongod --version

# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start

```bash
# Clear cache
rm -rf node_modules yarn.lock
yarn install

# Check Node version
node --version
```

### Chatbot not responding

1. Check if EMERGENT_LLM_KEY is set in backend/.env
2. Verify API key is valid
3. Check backend logs for errors
4. Make sure sources are fully processed

### "Connection refused" error

1. Make sure MongoDB is running: `mongod`
2. Check MONGO_URL in backend/.env
3. Test connection: `mongo --eval "db.version()"`

---

## Next Steps

📖 **Read the Docs:**
- [User Guide](docs/USER_GUIDE.md) - Complete feature guide
- [API Documentation](docs/API_DOCUMENTATION.md) - API reference
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Architecture and development

🚀 **Deploy to Production:**
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment

🤝 **Get Involved:**
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

---

## Support

Need help?
- 📧 Email: support@botsmith.ai
- 📝 Docs: https://docs.botsmith.ai
- 🐛 Issues: GitHub Issues

---

**Happy building!** 🤖✨