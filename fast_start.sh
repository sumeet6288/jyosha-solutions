#!/bin/bash

# Super Fast Startup Script for BotSmith
# Only installs if needed, otherwise starts immediately

set -e

echo "🚀 BotSmith Quick Start"
echo ""

# Check if backend dependencies are installed
if python3 -c "import fastapi, pymongo, litellm, motor" 2>/dev/null; then
    echo "✅ Backend dependencies already installed"
    BACKEND_OK=1
else
    echo "📦 Installing backend dependencies..."
    cd /app/backend
    pip install -q -r requirements.txt
    pip install -q emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
    echo "✅ Backend dependencies installed"
    BACKEND_OK=1
fi

# Check if frontend dependencies are installed
if [ -d "/app/frontend/node_modules/react" ] && [ -f "/app/frontend/node_modules/.yarn-integrity" ]; then
    echo "✅ Frontend dependencies already installed"
    FRONTEND_OK=1
else
    echo "📦 Installing frontend dependencies..."
    cd /app/frontend
    yarn install --frozen-lockfile --prefer-offline --silent
    echo "✅ Frontend dependencies installed"
    FRONTEND_OK=1
fi

if [ "$BACKEND_OK" = "1" ] && [ "$FRONTEND_OK" = "1" ]; then
    echo ""
    echo "✅ All dependencies ready!"
    echo "🔄 Restarting services..."
    sudo supervisorctl restart all
    echo ""
    echo "✨ BotSmith is ready at http://localhost:3000"
fi
