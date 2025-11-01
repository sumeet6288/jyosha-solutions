# BotSmith - AI Chatbot Builder

**Complete chatbot builder application with multi-provider AI support, file uploads, website scraping, and real-time chat**

## 🚀 Quick Start (Fast Installation)

### ⚡ Super Fast Start (Recommended)
If dependencies are already installed, this will start immediately:
```bash
bash /app/fast_start.sh
```

### 📦 Quick Install
Fresh installation with optimized speed:
```bash
bash /app/quick_install.sh
sudo supervisorctl restart all
```

### 🛠️ Manual Installation
```bash
# Backend
cd /app/backend
pip install -q -r requirements.txt

# Frontend  
cd /app/frontend
yarn install --frozen-lockfile --prefer-offline

# Start services
sudo supervisorctl restart all
```

## ⏱️ Installation Time
- **Fast Start** (dependencies already installed): ~5 seconds
- **Quick Install** (fresh installation): ~2-3 minutes
- **Manual Install**: ~3-5 minutes

## 🌟 Features

### ✅ Fully Implemented
- **Multi-Provider AI**: OpenAI (GPT-4o-mini), Claude (3.5 Sonnet), Gemini (2.0 Flash)
- **Source Management**: File uploads (PDF, DOCX, TXT, XLSX, CSV), website scraping, text content
- **RAG System**: Text-based retrieval with MongoDB
- **Chat Interface**: Real-time AI chat with conversation history
- **Analytics Dashboard**: Response time trends, hourly activity, conversation stats
- **Integration Management**: Slack, Telegram, Discord, WhatsApp, WebChat, API, Twilio, Messenger
- **User Management**: Admin panel with role management and activity tracking
- **Visual Customization**: Color themes, branding, welcome messages, widget settings
- **Public Chat**: Shareable chat interface with custom branding
- **Mobile Responsive**: Fully responsive design

## 📦 Tech Stack

### Backend
- FastAPI 0.115.12
- MongoDB (motor 3.5.1)
- emergentintegrations, litellm 1.56.8
- OpenAI 1.99.9, Anthropic 0.42.0, Google Generative AI 0.8.4

### Frontend
- **React 18.2.0** (locked for compatibility - DO NOT upgrade to React 19)
- React Router DOM 7.5.1
- Radix UI components
- Tailwind CSS 3.4.17
- Recharts 3.3.0

## 🚨 Important Notes

### React Version Lock
The application uses **React 18.2.0** for compatibility with react-scripts 5.0.1:
- `react`: 18.2.0 (exact version)
- `react-dom`: 18.2.0 (exact version)
- **Resolutions added to prevent upgrades**

⚠️ **DO NOT upgrade to React 19** - it causes webpack compilation errors.

### Service Management
```bash
sudo supervisorctl status              # Check status
sudo supervisorctl restart all         # Restart all
sudo supervisorctl restart frontend    # Restart frontend only
sudo supervisorctl restart backend     # Restart backend only
```

## 🔧 Configuration

**Backend** (`/app/backend/.env`):
```env
MONGO_URL=mongodb://localhost:27017/chatbase_db
```

**Frontend** (`/app/frontend/.env`):
```env
REACT_APP_BACKEND_URL=<your-backend-url>
```

## 🐛 Troubleshooting

### Dependencies taking too long?
```bash
bash /app/fast_start.sh  # Only installs if needed
```

### Frontend webpack errors?
```bash
cd /app/frontend
yarn add react@18.2.0 react-dom@18.2.0 --exact
sudo supervisorctl restart frontend
```

### Check logs
```bash
tail -50 /var/log/supervisor/backend.out.log
tail -50 /var/log/supervisor/frontend.out.log
```

## 📊 API Endpoints

Full API documentation available at: http://localhost:8001/docs

### Key Endpoints
- Chatbots: `/api/chatbots` (GET, POST, PUT, DELETE)
- Sources: `/api/sources/{chatbot_id}/file` (file upload)
- Chat: `/api/chat` (send message)
- Analytics: `/api/analytics/dashboard` (statistics)
- Integrations: `/api/integrations/{chatbot_id}` (manage integrations)

## 📝 Development

1. Make code changes
2. Services auto-reload
3. For .env or dependency changes: `sudo supervisorctl restart all`

---

**Made with ❤️ for better conversations | © 2025 BotSmith**
