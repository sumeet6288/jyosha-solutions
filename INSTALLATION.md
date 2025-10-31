# 🚀 BotSmith Installation Guide

Complete guide for installing and setting up the BotSmith AI Chatbot Builder application.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Yarn 1.22+** - Frontend package manager
- **MongoDB** - Database (local or cloud)
- **pip** - Python package manager

## 🎯 Quick Installation

### Option 1: Automated Installation (Recommended)

Use our master installation script that handles everything:

```bash
cd /app
bash install_all.sh
```

This script will:
- ✅ Install all backend Python dependencies
- ✅ Install all frontend Node.js dependencies
- ✅ Verify critical packages
- ✅ Handle errors automatically with retry logic
- ✅ Clean caches to prevent conflicts

### Option 2: Manual Installation

#### Backend Installation

```bash
cd /app/backend
bash install_dependencies.sh
```

Or manually:

```bash
cd /app/backend
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --force-reinstall --no-cache-dir
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

#### Frontend Installation

```bash
cd /app/frontend
bash install_dependencies.sh
```

Or manually:

```bash
cd /app/frontend
yarn cache clean
yarn install --frozen-lockfile
```

## 🔧 Common Installation Issues

### Issue 1: Corrupted Package Installation

**Error:** `OSError: [Errno 2] No such file or directory: '...INSTALLER*.tmp'`

**Solution:**
```bash
pip cache purge
pip install -r requirements.txt --force-reinstall --no-cache-dir
```

### Issue 2: Yarn Installation Fails

**Error:** `yarn install` hangs or fails

**Solution:**
```bash
rm -rf node_modules yarn.lock
yarn cache clean
yarn install
```

### Issue 3: Python Package Conflicts

**Error:** Version conflicts or import errors

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall --ignore-installed
```

### Issue 4: emergentintegrations Not Found

**Error:** `Could not find a version that satisfies emergentintegrations`

**Solution:**
```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

## ✅ Verification

### Verify Backend Installation

```bash
cd /app/backend
python -c "import fastapi, uvicorn, pymongo, motor, litellm, openai, anthropic"
echo "Backend packages verified!"
```

### Verify Frontend Installation

```bash
cd /app/frontend
ls node_modules/react node_modules/axios node_modules/recharts
echo "Frontend packages verified!"
```

### Check Installed Versions

```bash
# Backend
pip list | grep -E "(fastapi|uvicorn|pymongo|motor|litellm|openai|anthropic|google)"

# Frontend
yarn list --pattern "react|axios|recharts|lucide-react"
```

## 🏃 Running the Application

### Start All Services (Recommended)

```bash
sudo supervisorctl restart all
sudo supervisorctl status
```

### Start Backend Only

```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Start Frontend Only

```bash
cd /app/frontend
yarn start
```

## 📦 Dependencies Overview

### Backend Dependencies (requirements.txt)

**Core Framework:**
- fastapi==0.115.12 - Web framework
- uvicorn[standard]==0.34.0 - ASGI server
- pymongo==4.8.0 - MongoDB driver
- motor==3.5.1 - Async MongoDB driver

**AI/LLM Integration:**
- litellm==1.56.8 - Multi-provider LLM interface
- openai==1.99.9 - OpenAI API
- anthropic==0.42.0 - Claude API
- google-generativeai==0.8.4 - Gemini API
- emergentintegrations==0.1.0 - Universal LLM key support

**Document Processing:**
- pypdf==5.1.0 - PDF processing
- python-docx==1.1.2 - Word document processing
- openpyxl==3.1.5 - Excel processing
- beautifulsoup4==4.14.0 - HTML parsing
- lxml==5.3.0 - XML/HTML processing

**Authentication & Security:**
- pyjwt==2.10.1 - JWT tokens
- bcrypt==4.2.1 - Password hashing
- passlib==1.7.4 - Password utilities
- python-jose==3.3.0 - JWT/JWE implementation

**Data Processing:**
- pandas==2.2.3 - Data manipulation
- numpy==1.26.4 - Numerical computing

### Frontend Dependencies (package.json)

**Core Framework:**
- react==19.0.0 - UI library
- react-dom==19.0.0 - React DOM renderer
- react-router-dom==7.5.1 - Routing
- react-scripts==5.0.1 - Build tools

**UI Components:**
- @radix-ui/* - Accessible UI primitives
- lucide-react==0.511.0 - Icon library
- tailwindcss==3.4.17 - CSS framework
- recharts==3.3.0 - Charts library

**Forms & Validation:**
- react-hook-form==7.56.2 - Form management
- zod==3.24.4 - Schema validation
- @hookform/resolvers==5.1.0 - Form validators

**HTTP & State:**
- axios==1.8.4 - HTTP client
- react-hot-toast==2.6.0 - Notifications

## 🛠️ Troubleshooting

### Clear All Caches

```bash
# Python
pip cache purge
rm -rf ~/.cache/pip

# Yarn
yarn cache clean
rm -rf node_modules package-lock.json
```

### Reinstall Everything

```bash
# Backend
cd /app/backend
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --no-cache-dir

# Frontend
cd /app/frontend
rm -rf node_modules
yarn install
```

### Check Service Logs

```bash
# Backend logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
tail -f /var/log/supervisor/frontend.out.log
tail -f /var/log/supervisor/frontend.err.log
```

## 📝 Environment Variables

Make sure these files are properly configured:

### Backend (.env)
```bash
MONGO_URL=mongodb://localhost:27017/chatbase_db
EMERGENT_LLM_KEY=your_key_here  # Optional: For multi-provider LLM support
```

### Frontend (.env)
```bash
REACT_APP_BACKEND_URL=https://your-domain.com
```

## 🎉 Success!

If all installations succeed, you should see:
- ✅ Backend running on http://localhost:8001
- ✅ Frontend running on http://localhost:3000
- ✅ All services showing "RUNNING" status

## 📚 Additional Resources

- [Quick Start Guide](docs/QUICK_START.md)
- [Development Guide](docs/DEVELOPER_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)

## 🆘 Need Help?

If you encounter issues not covered here:

1. Check the logs: `sudo supervisorctl tail -f backend stderr`
2. Review test_result.md for known issues
3. Try the automated installation scripts
4. Clear all caches and reinstall

---

**Note:** The installation scripts include automatic retry logic and error recovery. If installation fails, the scripts will attempt up to 3 retries with different strategies before failing.
