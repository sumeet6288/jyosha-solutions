#!/bin/bash

# Quick Installation Script for BotSmith
# This script installs dependencies efficiently without unnecessary steps

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════╗"
echo "║     BotSmith - Quick Dependency Installer          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ========================================
# BACKEND DEPENDENCIES
# ========================================
echo "═══════════════════════════════════════════════════"
echo "1. INSTALLING BACKEND DEPENDENCIES"
echo "═══════════════════════════════════════════════════"

cd /app/backend

if [ -f "requirements.txt" ]; then
    print_status "Installing Python packages..."
    
    # Install all dependencies at once without upgrade
    pip install -q -r requirements.txt 2>&1 | grep -v "already satisfied" || true
    
    # Install emergentintegrations from custom index
    pip install -q emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/ 2>&1 | grep -v "already satisfied" || true
    
    print_success "Backend dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# ========================================
# FRONTEND DEPENDENCIES
# ========================================
echo ""
echo "═══════════════════════════════════════════════════"
echo "2. INSTALLING FRONTEND DEPENDENCIES"
echo "═══════════════════════════════════════════════════"

cd /app/frontend

if [ -f "package.json" ]; then
    print_status "Installing Node.js packages with Yarn..."
    
    # Check if node_modules exists and is recent
    if [ -d "node_modules" ] && [ -f "node_modules/.yarn-integrity" ]; then
        print_warning "node_modules exists, checking if update needed..."
        
        # Quick check if package.json is newer than node_modules
        if [ "package.json" -nt "node_modules" ] || [ "yarn.lock" -nt "node_modules" ]; then
            print_status "Dependencies need update, installing..."
            yarn install --frozen-lockfile --silent 2>&1 | grep -E "(error|ERROR|warning)" || true
        else
            print_success "Dependencies are up to date, skipping installation"
        fi
    else
        print_status "Fresh installation..."
        yarn install --frozen-lockfile --prefer-offline --silent 2>&1 | grep -E "(error|ERROR)" || true
    fi
    
    print_success "Frontend dependencies installed"
else
    print_error "package.json not found"
    exit 1
fi

# ========================================
# VERIFICATION
# ========================================
echo ""
echo "═══════════════════════════════════════════════════"
echo "3. VERIFYING INSTALLATION"
echo "═══════════════════════════════════════════════════"

# Check critical backend packages
print_status "Checking backend packages..."
python3 -c "import fastapi, pymongo, litellm" 2>/dev/null && print_success "Backend packages verified" || print_error "Backend verification failed"

# Check critical frontend packages
print_status "Checking frontend packages..."
[ -d "/app/frontend/node_modules/react" ] && print_success "Frontend packages verified" || print_error "Frontend verification failed"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║          ✅ Installation Complete!                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
print_status "Starting services with: sudo supervisorctl restart all"
echo ""
