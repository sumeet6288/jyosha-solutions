#!/bin/bash

# BotSmith - Fast Setup Script
# Optimized for quick installation when loading repo in new Emergent account

set -e

echo "🚀 BotSmith Fast Setup"
echo "======================="
echo ""

# Function to check if a command succeeded
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Backend Dependencies
echo "📦 Installing backend dependencies..."
cd /app/backend
pip install -q -r requirements.txt > /tmp/backend_install.log 2>&1 &
BACKEND_PID=$!

# Frontend Dependencies
echo "📦 Installing frontend dependencies..."
cd /app/frontend
yarn install --frozen-lockfile --silent > /tmp/frontend_install.log 2>&1 &
FRONTEND_PID=$!

# Wait for both installations
echo "⏳ Installing dependencies in parallel..."
wait $BACKEND_PID
check_success "Backend dependencies installed"

wait $FRONTEND_PID
check_success "Frontend dependencies installed"

# Install emergentintegrations (for AI providers)
echo "📦 Installing emergentintegrations..."
pip install -q emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/ > /dev/null 2>&1
check_success "Emergentintegrations installed"

# Restart services
echo ""
echo "🔄 Starting services..."
sudo supervisorctl restart all > /dev/null 2>&1
sleep 5

# Check services status
echo ""
echo "📊 Service Status:"
sudo supervisorctl status | grep -E "(backend|frontend|mongodb)" | while read line; do
    if echo "$line" | grep -q "RUNNING"; then
        echo "  ✅ $(echo $line | awk '{print $1}')"
    else
        echo "  ❌ $(echo $line | awk '{print $1}')"
    fi
done

echo ""
echo "✨ BotSmith is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8001/docs"
echo ""
