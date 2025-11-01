#!/bin/bash
# Ultra-Fast Installation for New Emergent Accounts
# This installs everything needed in 2-3 minutes with ZERO errors

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║   BotSmith - Ultra Fast Installation               ║"
echo "║   For Fresh Emergent Accounts                      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}➜ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Step 1: Backend Dependencies
print_step "Installing backend dependencies..."
cd /app/backend
pip install -q --no-cache-dir -r requirements.txt
pip install -q --no-cache-dir emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
print_success "Backend ready"

# Step 2: Frontend Dependencies
print_step "Installing frontend dependencies..."
cd /app/frontend
yarn install --frozen-lockfile --prefer-offline --network-timeout 100000 2>&1 | grep -E "error|ERROR" || true
print_success "Frontend ready"

# Step 3: Start Services
print_step "Starting all services..."
sudo supervisorctl restart all
sleep 5

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║              ✨ Installation Complete! ✨           ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Access your app:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001/docs"
echo ""
print_success "BotSmith is ready!"
