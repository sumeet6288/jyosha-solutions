# \ud83d\udcda BotSmith Documentation

Welcome to the BotSmith documentation! This comprehensive guide will help you understand, use, and contribute to BotSmith.

## \ud83d\udccd Quick Navigation

### For Users
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[User Guide](USER_GUIDE.md)** - Complete feature walkthrough and tutorials
- **[FAQ](#frequently-asked-questions)** - Common questions and answers

### For Developers
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Setup, architecture, and development
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to BotSmith
- **[Changelog](../CHANGELOG.md)** - Version history and updates

### For DevOps
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[Security Guide](SECURITY.md)** - Security best practices and policies

---

## \ud83d\ude80 Getting Started

### 1. Installation

Choose your installation method:

**Local Development:**
```bash
git clone <repository-url>
cd botsmith
# Follow Quick Start Guide
```

**Docker:**
```bash
docker-compose up -d
```

**Cloud Deployment:**
- AWS, Google Cloud, Azure, DigitalOcean
- See [Deployment Guide](DEPLOYMENT_GUIDE.md)

### 2. Configuration

**Backend Configuration:**
```bash
cd backend
cp .env.example .env
# Edit .env with your settings
```

**Frontend Configuration:**
```bash
cd frontend
cp .env.example .env
# Edit .env with your settings
```

### 3. First Steps

1. Start the application
2. Create your first chatbot
3. Add knowledge base sources
4. Test with the preview
5. Share your chatbot!

**Detailed instructions:** [Quick Start Guide](QUICK_START.md)

---

## \ud83d\udcd6 Documentation Structure

### Core Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [README](../README.md) | Project overview and quick start | Everyone |
| [Quick Start](QUICK_START.md) | 5-minute setup guide | New users |
| [User Guide](USER_GUIDE.md) | Complete feature guide (50+ pages) | End users |
| [Developer Guide](DEVELOPER_GUIDE.md) | Development setup and architecture | Developers |
| [API Documentation](API_DOCUMENTATION.md) | Complete API reference | Developers |
| [Deployment Guide](DEPLOYMENT_GUIDE.md) | Production deployment | DevOps |
| [Security Guide](SECURITY.md) | Security policies and best practices | Everyone |

### Additional Resources

| Document | Description |
|----------|-------------|
| [Contributing](../CONTRIBUTING.md) | Contribution guidelines |
| [Changelog](../CHANGELOG.md) | Version history |
| [License](../LICENSE) | MIT License |

---

## \u2728 Features Overview

### \ud83e\udd16 AI & Chatbots

**Multi-Provider Support:**
- OpenAI (GPT-4o, GPT-4o-mini)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
- Google (Gemini 2.0 Flash, Gemini 1.5 Pro)

**Capabilities:**
- Natural language understanding
- Context-aware responses
- Knowledge base integration
- Conversation memory

**Learn more:** [User Guide - AI Integration](USER_GUIDE.md#creating-your-first-chatbot)

### \ud83d\udcda Knowledge Base

**Source Types:**
- **File Upload**: PDF, DOCX, TXT, XLSX, CSV (up to 100MB)
- **Website Scraping**: Extract content from any public URL
- **Text Content**: Direct text input

**Processing:**
- Async processing for large files
- Automatic text extraction
- Content indexing
- Smart context retrieval

**Learn more:** [User Guide - Knowledge Base](USER_GUIDE.md#adding-knowledge-base)

### \ud83c\udfa8 Customization

**Appearance:**
- Custom brand colors (primary & secondary)
- Logo and avatar URLs
- Welcome messages
- Widget positioning (4 locations)
- Theme options (light/dark/auto)

**Branding:**
- Fully branded public chat pages
- Custom domains (Enterprise)
- White-label options (Enterprise)

**Learn more:** [User Guide - Customization](USER_GUIDE.md#customizing-appearance)

### \ud83d\udcca Analytics & Insights

**Basic Analytics:**
- Total conversations
- Total messages
- Response times
- Active users

**Advanced Insights:**
- Message volume trends (line chart)
- Response time trends (line chart)
- Hourly activity distribution (bar chart)
- Top asked questions (bar chart)
- Satisfaction distribution (pie chart)

**Chat Logs:**
- Complete conversation history
- Expandable message threads
- User information
- Conversation status

**Learn more:** [User Guide - Analytics](USER_GUIDE.md#analytics--insights)

### \ud83d\udc65 User Management

**Account Features:**
- Profile management
- Email and password updates
- Usage statistics
- Subscription management

**Admin Features:**
- User CRUD operations
- Role management (user/moderator/admin)
- Status control (active/suspended/banned)
- Activity tracking
- Login history
- Bulk operations

**Learn more:** [User Guide - Admin](USER_GUIDE.md#account-settings)

### \ud83c\udf10 Sharing & Integration

**Sharing Options:**
- Public chat links
- Embed codes (iframe)
- Social media sharing

**Integrations:**
- Webhook support
- API access
- Export options (JSON/CSV)

**Learn more:** [User Guide - Sharing](USER_GUIDE.md#sharing--deployment)

---

## \ud83d\udee0\ufe0f Technical Architecture

### System Overview

```
┌─────────────────┐
│  React Frontend │ ──────┐
│   (Port 3000)   │       │
└─────────────────┘       │ HTTP/REST
                          │
┌─────────────────┐       │
│ FastAPI Backend │ ◄─────┘
│   (Port 8001)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────────┐
│MongoDB│ │ AI Providers│
└───────┘ └─────────────┘
```

### Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- MongoDB with Motor (async)
- emergentintegrations (AI)
- JWT authentication
- Async file processing

**Frontend:**
- React 18
- Tailwind CSS
- Recharts (analytics)
- Axios (HTTP)
- React Router v6

**Infrastructure:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- Supervisor (process management)
- MongoDB (database)

**Learn more:** [Developer Guide - Architecture](DEVELOPER_GUIDE.md#architecture-overview)

---

## \ud83d\udcda API Reference

### Quick Examples

**Create Chatbot:**
```bash
curl -X POST "http://localhost:8001/api/chatbots" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support Bot",
    "model": "gpt-4o-mini",
    "provider": "openai"
  }'
```

**Send Chat Message:**
```bash
curl -X POST "http://localhost:8001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chatbot_id": "CHATBOT_ID",
    "message": "Hello!",
    "session_id": "SESSION_ID"
  }'
```

**Get Analytics:**
```bash
curl -X GET "http://localhost:8001/api/analytics/dashboard" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Complete reference:** [API Documentation](API_DOCUMENTATION.md)

---

## \ud83d\udd12 Security

### Security Features

✅ JWT Authentication  
✅ Bcrypt Password Hashing  
✅ TLS/SSL Encryption  
✅ Input Validation  
✅ File Upload Security  
✅ CORS Protection  
✅ Rate Limiting  
✅ XSS Protection  
✅ CSRF Protection  

### Best Practices

**Production Checklist:**
- [ ] HTTPS enabled
- [ ] Strong passwords
- [ ] Firewall configured
- [ ] Rate limiting active
- [ ] Security headers set
- [ ] Regular backups
- [ ] Monitoring enabled

**Learn more:** [Security Guide](SECURITY.md)

---

## \ud83e\uddea Testing

### Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
yarn test
```

**Integration:**
```bash
# See Developer Guide for setup
```

### Test Coverage

- ✅ API endpoints (100% coverage)
- ✅ Authentication flows
- ✅ File processing
- ✅ AI integration
- ✅ Database operations

---

## \ud83d\udcb0 Pricing & Plans

### Free Plan
- 1 chatbot
- 100 messages/month
- Basic analytics
- Community support

### Starter Plan - $150/month
- 5 chatbots
- 10,000 messages/month
- Advanced analytics
- Priority support

### Professional Plan - $499/month
- 25 chatbots
- 100,000 messages/month
- Full API access
- 24/7 support

### Enterprise Plan - Custom
- Unlimited chatbots
- Unlimited messages
- White-label
- On-premise deployment

**Learn more:** [User Guide - Subscriptions](USER_GUIDE.md#managing-subscriptions)

---

## \ud83d\ude80 Deployment

### Deployment Options

**Docker Compose (Recommended):**
```bash
docker-compose up -d
```

**Cloud Platforms:**
- AWS (EC2, ECS, Elastic Beanstalk)
- Google Cloud (Cloud Run, GKE)
- Azure (App Service, AKS)
- DigitalOcean (Droplets, App Platform)

**Traditional VPS:**
- Ubuntu 22.04 LTS
- Manual installation

**Complete guide:** [Deployment Guide](DEPLOYMENT_GUIDE.md)

---

## \ud83e\udd1d Contributing

We welcome contributions! Here's how to get started:

### Ways to Contribute

1. **Report Bugs**: Create issues with detailed information
2. **Suggest Features**: Share your ideas
3. **Write Code**: Submit pull requests
4. **Improve Docs**: Help others understand BotSmith
5. **Answer Questions**: Help community members

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit pull request

**Complete guide:** [Contributing Guide](../CONTRIBUTING.md)

---

## \ud83c\udf93 Tutorials & Examples

### Tutorial Series

Coming soon:
- [ ] Building your first customer support bot
- [ ] Integrating with your website
- [ ] Advanced customization techniques
- [ ] Analyzing chatbot performance
- [ ] Multi-language support setup

### Example Projects

Coming soon:
- [ ] E-commerce support bot
- [ ] HR onboarding assistant
- [ ] Technical documentation bot
- [ ] FAQ automation
- [ ] Lead generation bot

---

## \u2753 Frequently Asked Questions

### General

**Q: What AI models does BotSmith support?**  
A: OpenAI (GPT-4o, GPT-4o-mini), Anthropic (Claude 3.5 Sonnet, Claude 3 Opus), and Google (Gemini 2.0 Flash, Gemini 1.5 Pro).

**Q: How many languages are supported?**  
A: All AI models support 50+ languages. Your chatbot responds in the language users write in.

**Q: Can I use my own API keys?**  
A: Yes, Professional and Enterprise plans support custom API keys.

### Technical

**Q: What databases are supported?**  
A: MongoDB 6.0+ is currently supported.

**Q: Can I self-host BotSmith?**  
A: Yes, full self-hosting documentation is provided.

**Q: What's the maximum file upload size?**  
A: 100MB per file (configurable).

### Pricing

**Q: Is there a free trial?**  
A: Yes, the Free plan is available forever with basic features.

**Q: Can I cancel anytime?**  
A: Yes, cancel anytime. No questions asked.

**Q: Do you offer refunds?**  
A: Yes, within 30 days of purchase.

---

## \ud83d\udcde Support

### Get Help

**Documentation:**
- Search this documentation
- Check the FAQ above
- Review troubleshooting guides

**Community:**
- GitHub Discussions
- Discord (coming soon)
- Stack Overflow tag: `botsmith`

**Direct Support:**
- **Email**: support@botsmith.ai
- **Phone**: +1 (555) 123-4567 (Pro/Enterprise)
- **Chat**: Live chat on website (24/7 for Pro/Enterprise)

### Report Issues

**Bug Reports:**
- GitHub Issues
- Include detailed reproduction steps
- Attach logs and screenshots

**Security Issues:**
- Email: security@botsmith.ai
- Use responsible disclosure
- See [Security Guide](SECURITY.md)

---

## \ud83d\udccd Roadmap

### Version 1.1 (Q2 2025)
- [ ] Voice message support
- [ ] Real-time typing indicators
- [ ] Message templates
- [ ] Advanced search
- [ ] Email notifications

### Version 1.2 (Q3 2025)
- [ ] WhatsApp integration
- [ ] Slack integration
- [ ] Multi-language UI
- [ ] Sentiment analysis
- [ ] A/B testing

### Version 2.0 (Q4 2025)
- [ ] Video chat support
- [ ] AI voice responses
- [ ] Advanced workflows
- [ ] Plugin system
- [ ] Marketplace

**Full roadmap:** [Changelog](../CHANGELOG.md#roadmap)

---

## \ud83d\udccb Changelog

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history.

---

## \ud83d\udce6 Downloads

**Latest Release:** v1.0.0

- [Source Code (.zip)](https://github.com/your-org/botsmith/archive/v1.0.0.zip)
- [Source Code (.tar.gz)](https://github.com/your-org/botsmith/archive/v1.0.0.tar.gz)
- [Docker Image](https://hub.docker.com/r/your-org/botsmith)

---

## \ud83d\udcc4 License

BotSmith is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

## \ud83d\udc4f Acknowledgments

### Contributors
Thank you to all contributors who have helped make BotSmith better!

### Technologies
- FastAPI
- React
- MongoDB
- OpenAI, Anthropic, Google AI
- And many more...

### Community
Thank you to our amazing community for feedback, bug reports, and support!

---

## \ud83d\udce7 Contact

**General Inquiries:** hello@botsmith.ai  
**Support:** support@botsmith.ai  
**Security:** security@botsmith.ai  
**Press:** press@botsmith.ai  
**Partnerships:** partners@botsmith.ai

**Website:** https://botsmith.ai  
**GitHub:** https://github.com/your-org/botsmith  
**Twitter:** @botsmith_ai  
**LinkedIn:** BotSmith

---

<div align=\"center\">
  <p>Made with ❤️ by Jyosha Solutions</p>
  <p>© 2025 BotSmith. All rights reserved.</p>
</div>
