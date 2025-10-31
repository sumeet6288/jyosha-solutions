#!/bin/bash

# Master Installation Script
# Installs both backend and frontend dependencies

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════╗"
echo "║     BotSmith - Complete Dependency Installer       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

print_info "Installation directory: $SCRIPT_DIR"
echo ""

# Install Backend Dependencies
echo "═══════════════════════════════════════════════════"
echo "1. BACKEND DEPENDENCIES"
echo "═══════════════════════════════════════════════════"

if [ -f "$SCRIPT_DIR/backend/install_dependencies.sh" ]; then
    chmod +x "$SCRIPT_DIR/backend/install_dependencies.sh"
    bash "$SCRIPT_DIR/backend/install_dependencies.sh"
    print_success "Backend installation completed"
else
    print_warning "Backend installation script not found, using fallback method"
    cd "$SCRIPT_DIR/backend"
    pip install --upgrade pip
    pip install -r requirements.txt --force-reinstall --no-cache-dir
    pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
    print_success "Backend fallback installation completed"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "2. FRONTEND DEPENDENCIES"
echo "═══════════════════════════════════════════════════"

if [ -f "$SCRIPT_DIR/frontend/install_dependencies.sh" ]; then
    chmod +x "$SCRIPT_DIR/frontend/install_dependencies.sh"
    bash "$SCRIPT_DIR/frontend/install_dependencies.sh"
    print_success "Frontend installation completed"
else
    print_warning "Frontend installation script not found, using fallback method"
    cd "$SCRIPT_DIR/frontend"
    yarn install
    print_success "Frontend fallback installation completed"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "3. VERIFICATION"
echo "═══════════════════════════════════════════════════"

# Verify backend
print_info "Checking backend installation..."
cd "$SCRIPT_DIR/backend"
if python -c "import fastapi, uvicorn, pymongo, motor, litellm" 2>/dev/null; then
    print_success "Backend core packages verified"
else
    print_error "Some backend packages may be missing"
fi

# Verify frontend
print_info "Checking frontend installation..."
cd "$SCRIPT_DIR/frontend"
if [ -d "node_modules/react" ] && [ -d "node_modules/axios" ]; then
    print_success "Frontend core packages verified"
else
    print_error "Some frontend packages may be missing"
fi

echo ""
echo "╔════════════════════════════════════════════════════╗"
print_success "     Installation Complete!                         "
echo "╚════════════════════════════════════════════════════╝"
echo ""
print_info "Next steps:"
echo "  1. Start backend:  cd backend && uvicorn server:app --host 0.0.0.0 --port 8001"
echo "  2. Start frontend: cd frontend && yarn start"
echo "  3. Or use:         sudo supervisorctl restart all"
echo ""
