# 🤖 BotSmith - AI Chatbot Builder Platform

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
</div>

## 📖 Overview

BotSmith is a comprehensive AI-powered chatbot builder platform that enables users to create, customize, and deploy intelligent chatbots with multiple AI provider support. Build context-aware chatbots trained on your own data through file uploads, website scraping, or text content.

## ✨ Key Features

### 🤖 Multi-Provider AI Support
- **OpenAI**: GPT-4o, GPT-4o-mini
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus
- **Google**: Gemini 2.0 Flash, Gemini 1.5 Pro

### 📚 Knowledge Base Management
- **File Uploads**: PDF, DOCX, TXT, XLSX, CSV (up to 100MB)
- **Website Scraping**: Extract content from any public URL
- **Text Content**: Direct text input for quick training
- Async processing for optimal performance

### 🎨 Customization Options
- **Appearance**: Custom brand colors, logos, avatars
- **Widget Settings**: Positioning (4 locations), theme (light/dark/auto)
- **Welcome Messages**: Personalized greetings
- **Chat Interface**: Fully branded public chat pages

### 📊 Advanced Analytics
- **Dashboard Metrics**: Conversations, messages, active chatbots
- **Response Time Trends**: Performance tracking over time
- **Hourly Activity**: Peak usage identification
- **Top Questions**: Most asked queries analysis
- **Satisfaction Ratings**: User feedback with 1-5 star system
- **Chat Logs**: Complete conversation history with user details

### 🔧 Admin Features
- **User Management**: Comprehensive admin panel
- **Activity Tracking**: Login history and user actions
- **Custom Limits**: Per-user resource allocation
- **Bulk Operations**: Mass user management tools

### 🌐 Sharing & Integration
- **Public Chat Links**: Shareable URLs for each chatbot
- **Embed Codes**: iframe integration for websites
- **Export Options**: Download conversations (JSON/CSV)
- **Webhook Support**: Real-time notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB 6.0+
- Yarn package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd botsmith
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
yarn install
```

4. **Set up environment variables**

Backend `.env` file:
```env
MONGO_URL=mongodb://localhost:27017/botsmith
EMERGENT_LLM_KEY=your_key_here
SECRET_KEY=your_secret_key
```

Frontend `.env` file:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

5. **Start the services**

Backend:
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

Frontend:
```bash
cd frontend
yarn start
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 📁 Project Structure

```
botsmith/
├── backend/
│   ├── routers/
│   │   ├── chatbots.py          # Chatbot CRUD operations
│   │   ├── sources.py           # Knowledge base management
│   │   ├── chat.py              # Chat endpoints
│   │   ├── analytics.py         # Analytics endpoints
│   │   ├── advanced_analytics.py # Advanced insights
│   │   ├── admin_users.py       # Admin user management
│   │   └── public_chat.py       # Public chat API
│   ├── services/
│   │   ├── chat_service.py      # AI integration service
│   │   ├── document_processor.py # File processing
│   │   └── website_scraper.py   # Web scraping
│   ├── models.py                # MongoDB models
│   ├── auth.py                  # Authentication
│   └── server.py                # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ChatbotBuilder.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Subscription.jsx
│   │   │   └── AccountSettings.jsx
│   │   ├── components/
│   │   │   ├── AddSourceModal.jsx
│   │   │   ├── ChatPreviewModal.jsx
│   │   │   └── admin/
│   │   └── utils/
│   │       └── api.js            # API client
│   └── package.json
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   └── DEPLOYMENT_GUIDE.md
└── README.md
```

## 🔑 API Key Configuration

### Emergent LLM Key (Recommended)
BotSmith supports the Emergent Universal LLM Key which works with:
- OpenAI (GPT-4o, GPT-4o-mini)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
- Google (Gemini 2.0 Flash, Gemini 1.5 Pro)

```bash
EMERGENT_LLM_KEY=your_emergent_key_here
```

### Individual Provider Keys (Alternative)
You can also use individual API keys:
```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

## 📚 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[User Guide](docs/USER_GUIDE.md)** - Step-by-step usage instructions
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Development setup and architecture
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: MongoDB with Motor (async driver)
- **AI Integration**: emergentintegrations library
- **File Processing**: pypdf, python-docx, openpyxl
- **Web Scraping**: BeautifulSoup4, lxml

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Routing**: React Router v6

### Infrastructure
- **Process Management**: Supervisor
- **Web Server**: Nginx
- **Container**: Docker support

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
yarn test
```

## 📊 Database Schema

### Collections
- `users` - User accounts and profiles
- `chatbots` - Chatbot configurations
- `sources` - Knowledge base sources
- `conversations` - Chat conversations
- `messages` - Individual chat messages
- `activity_logs` - User activity tracking
- `login_history` - Authentication logs

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation and sanitization
- Rate limiting support
- Secure file upload handling

## 🌟 Subscription Plans

### Free Plan
- 1 chatbot
- 100 messages/month
- Basic analytics
- Community support
- Standard AI models

### Starter Plan ($150/month)
- 5 chatbots
- 10,000 messages/month
- Advanced analytics
- Priority support
- Custom branding
- All AI models

### Professional Plan ($499/month)
- 25 chatbots
- 100,000 messages/month
- Advanced analytics
- 24/7 priority support
- Custom branding
- Full API access
- All AI models
- Custom integrations

### Enterprise Plan (Custom)
- Unlimited chatbots
- Unlimited messages
- Custom analytics
- Dedicated 24/7 support
- White-label solution
- Custom AI model training
- On-premise deployment
- SLA guarantee

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more details.

## 📝 License

This project is licensed under the MIT License.

## 💬 Support

- **Email**: support@botsmith.ai
- **Phone**: +1 (555) 123-4567
- **Documentation**: [docs.botsmith.ai](https://docs.botsmith.ai)
- **Community**: [community.botsmith.ai](https://community.botsmith.ai)

## 🎯 Roadmap

- [ ] Voice message support
- [ ] Video chat integration
- [ ] Advanced NLP preprocessing
- [ ] Multi-language support
- [ ] WhatsApp/Telegram integration
- [ ] Sentiment analysis
- [ ] A/B testing for responses
- [ ] Advanced workflow automation

---

<div align="center">
  Made with ❤️ by Jyosha Solutions
</div>