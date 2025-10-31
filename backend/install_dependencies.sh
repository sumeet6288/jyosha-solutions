#!/bin/bash

# Backend Dependencies Installation Script
# This script ensures robust installation of Python dependencies

set -e  # Exit on error

echo "🚀 Starting backend dependency installation..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found!"
    exit 1
fi

print_success "Found requirements.txt"

# Upgrade pip, setuptools, and wheel first
echo "📦 Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel --quiet
print_success "Core tools upgraded"

# Clean up any corrupted installations
echo "🧹 Cleaning up potentially corrupted packages..."
pip cache purge 2>/dev/null || true
print_success "Cache cleaned"

# Install dependencies with retry logic
echo "📥 Installing dependencies from requirements.txt..."
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if pip install -r requirements.txt --no-cache-dir; then
        print_success "All dependencies installed successfully!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            print_warning "Installation failed. Retrying ($RETRY_COUNT/$MAX_RETRIES)..."
            # Force reinstall on retry
            pip install -r requirements.txt --force-reinstall --no-cache-dir 2>&1 | tail -20
        else
            print_error "Installation failed after $MAX_RETRIES attempts"
            exit 1
        fi
    fi
done

# Install emergentintegrations with custom index
echo "🔧 Installing emergentintegrations from custom index..."
if pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/ --quiet; then
    print_success "emergentintegrations installed"
else
    print_warning "emergentintegrations installation failed, but continuing..."
fi

# Verify critical packages
echo "🔍 Verifying critical packages..."
CRITICAL_PACKAGES=("fastapi" "uvicorn" "pymongo" "motor" "litellm" "openai" "anthropic" "google-generativeai")

for package in "${CRITICAL_PACKAGES[@]}"; do
    if python -c "import $package" 2>/dev/null; then
        print_success "$package verified"
    else
        print_warning "$package might have issues"
    fi
done

echo "================================================"
print_success "Backend dependency installation completed!"
echo "📝 Installed packages:"
pip list | grep -E "(fastapi|uvicorn|pymongo|motor|litellm|openai|anthropic|google)" || true
echo ""
