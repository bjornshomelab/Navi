#!/bin/bash
# JARVIS AI Agent - Installation and Setup Script

echo "🛰️  JARVIS AI Agent Setup"
echo "=========================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected."
    echo "It's recommended to use a virtual environment."
    echo "Creating one for you..."
    
    python3 -m venv jarvis
    source jarvis/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install requirements
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🔧 Setting up configuration..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Check for Google credentials
if [ ! -f credentials.json ]; then
    echo "⚠️  credentials.json not found"
    echo "Please download it from Google Cloud Console and place it in this directory"
else
    echo "✅ Google credentials found"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Ensure credentials.json is in place"
echo "3. Start JARVIS: python -m api.main"
echo "4. Or use CLI: python cli/jarvis_cli.py --status"
echo ""
echo "For interactive mode: python cli/jarvis_cli.py --interactive"
