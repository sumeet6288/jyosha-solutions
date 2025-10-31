#!/bin/bash

# Frontend Dependencies Installation Script
# This script ensures robust installation of Node.js dependencies using Yarn

set -e  # Exit on error

echo "🚀 Starting frontend dependency installation..."
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

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_error "package.json not found!"
    exit 1
fi

print_success "Found package.json"

# Check if yarn is installed
if ! command -v yarn &> /dev/null; then
    print_error "Yarn is not installed. Please install yarn first."
    exit 1
fi

print_success "Yarn is installed: $(yarn --version)"

# Clean yarn cache
echo "🧹 Cleaning yarn cache..."
yarn cache clean --silent 2>/dev/null || true
print_success "Yarn cache cleaned"

# Remove node_modules and lock file if installation fails
if [ -d "node_modules" ]; then
    echo "📦 node_modules directory exists"
fi

# Install dependencies with retry logic
echo "📥 Installing dependencies with yarn..."
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if yarn install --frozen-lockfile 2>&1; then
        print_success "All dependencies installed successfully!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            print_warning "Installation failed. Retrying ($RETRY_COUNT/$MAX_RETRIES)..."
            # Remove node_modules and try again
            rm -rf node_modules
            yarn install 2>&1 | tail -20
        else
            print_error "Installation failed after $MAX_RETRIES attempts"
            print_warning "Trying yarn install without frozen lockfile..."
            yarn install || exit 1
        fi
    fi
done

# Verify critical packages
echo "🔍 Verifying critical packages..."
CRITICAL_PACKAGES=("react" "react-dom" "react-router-dom" "axios" "recharts" "lucide-react")

for package in "${CRITICAL_PACKAGES[@]}"; do
    if [ -d "node_modules/$package" ]; then
        print_success "$package verified"
    else
        print_warning "$package might be missing"
    fi
done

echo "================================================"
print_success "Frontend dependency installation completed!"
echo "📝 Key packages installed:"
ls -la node_modules | grep -E "(react|axios|recharts)" | head -10 || true
echo ""
