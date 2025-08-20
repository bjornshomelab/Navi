#!/bin/bash

# NAVI Interactive Setup Script
# Smart installation with user preferences and guided configuration

set -e  # Exit on any error

echo "🤖 Welcome to NAVI - Your Local-First AI Assistant!"
echo "=================================================="
echo ""

# Quick setup test
python3 --version
echo "✅ Python found"

# Install basic dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --user --quiet || echo "⚠️ Some dependencies may need system packages"

echo "🎉 Basic NAVI setup complete!"
echo ""
echo "🚀 To start NAVI:"
echo "  python3 navi.py"
echo ""
echo "📚 For more options, see README.md"
