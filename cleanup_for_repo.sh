#!/bin/bash

# Cleanup script to remove files that cause installation issues
# Run this before pushing to repo

echo "🧹 Cleaning up troublesome files for fresh installation..."

# Delete frontend build artifacts and dependencies
echo "Removing frontend build artifacts..."
rm -rf /app/frontend/node_modules
rm -rf /app/frontend/build
rm -rf /app/frontend/.cache
rm -rf /app/frontend/node_modules/.cache
rm -f /app/frontend/yarn-error.log
rm -f /app/frontend/package-lock.json

# Delete backend cache and compiled files
echo "Removing backend cache..."
rm -rf /app/backend/__pycache__
rm -rf /app/backend/**/__pycache__
rm -rf /app/backend/.pytest_cache
rm -rf /app/backend/*.pyc
rm -rf /app/backend/**/*.pyc

# Delete Python cache
echo "Removing Python cache..."
find /app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /app -type f -name "*.pyc" -delete 2>/dev/null || true

# Delete log files
echo "Removing log files..."
rm -f /app/backend/*.log
rm -f /app/frontend/*.log
rm -f /tmp/*.log

# Keep important files
echo ""
echo "✅ Cleanup complete! Repo is ready for fresh installation"
echo ""
echo "Files kept:"
echo "  ✓ package.json (with React 18.2.0 locked)"
echo "  ✓ yarn.lock"
echo "  ✓ requirements.txt"
echo "  ✓ Source code"
echo "  ✓ Fast installation scripts"
echo ""
echo "Files removed:"
echo "  ✗ node_modules (will be installed fresh)"
echo "  ✗ Build artifacts"
echo "  ✗ Cache files"
echo "  ✗ Python bytecode"
echo ""
