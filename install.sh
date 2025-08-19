#!/bin/bash

# JARVIS AI Agent - Installation Script
# Automated setup for Ubuntu/Debian systems

set -e

echo "🤖 JARVIS AI Agent - Installation Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running on supported OS
print_step "Checking operating system..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_status "Linux detected"
    if command -v apt-get &> /dev/null; then
        PACKAGE_MANAGER="apt"
        print_status "Using apt package manager"
    elif command -v dnf &> /dev/null; then
        PACKAGE_MANAGER="dnf"
        print_status "Using dnf package manager"
    else
        print_error "Unsupported package manager. Please install manually."
        exit 1
    fi
else
    print_error "Unsupported operating system. Linux required."
    exit 1
fi

# Check Python version
print_step "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
    
    # Check if version is 3.11+
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
        print_status "Python version is compatible"
    else
        print_warning "Python 3.11+ recommended for best compatibility"
    fi
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Install system dependencies
print_step "Installing system dependencies..."
if [[ "$PACKAGE_MANAGER" == "apt" ]]; then
    sudo apt update
    sudo apt install -y \
        python3-pip \
        python3-venv \
        python3-dev \
        espeak \
        espeak-data \
        espeak-data-sv \
        speech-dispatcher \
        speech-dispatcher-swedish \
        alsa-utils \
        pulseaudio \
        python3-pygame \
        ffmpeg \
        curl \
        git \
        build-essential \
        portaudio19-dev \
        libasound2-dev
elif [[ "$PACKAGE_MANAGER" == "dnf" ]]; then
    sudo dnf install -y \
        python3-pip \
        python3-virtualenv \
        python3-devel \
        espeak \
        speech-dispatcher \
        alsa-utils \
        pulseaudio \
        python3-pygame \
        ffmpeg \
        curl \
        git \
        gcc \
        gcc-c++ \
        portaudio-devel \
        alsa-lib-devel
fi

print_status "System dependencies installed"

# Create virtual environment
print_step "Creating Python virtual environment..."
if [[ ! -d "jarvis" ]]; then
    python3 -m venv jarvis
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source jarvis/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_step "Installing Python dependencies..."
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    print_status "Python dependencies installed from requirements.txt"
else
    print_warning "requirements.txt not found, installing core dependencies..."
    pip install \
        fastapi \
        uvicorn \
        edge-tts \
        pygame \
        SpeechRecognition \
        pyaudio \
        requests \
        python-multipart \
        pydantic \
        google-cloud-speech \
        google-cloud-texttospeech \
        google-cloud-vision \
        google-cloud-storage \
        google-cloud-bigquery \
        google-cloud-logging \
        gtts \
        python-dotenv \
        matplotlib \
        numpy
fi

# Test voice system
print_step "Testing voice system..."
if command -v spd-say &> /dev/null; then
    print_status "Testing speech-dispatcher..."
    echo "Testar JARVIS röst" | spd-say -l sv || print_warning "Speech-dispatcher test failed"
fi

if jarvis/bin/edge-tts --list-voices | grep -q "sv-SE"; then
    print_status "Edge TTS Swedish voices available"
else
    print_warning "Edge TTS may not have Swedish voices installed"
fi

# Create startup scripts
print_step "Creating startup scripts..."

# JARVIS server startup script
cat > start_jarvis.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting JARVIS AI Agent..."
cd "$(dirname "$0")"
source jarvis/bin/activate
python -m api.main
EOF

# JARVIS GUI startup script
cat > start_gui.sh << 'EOF'
#!/bin/bash
echo "🖥️ Starting JARVIS GUI..."
cd "$(dirname "$0")"
source jarvis/bin/activate
python gui/main_window.py
EOF

# Voice test script
cat > test_voice.sh << 'EOF'
#!/bin/bash
echo "🎤 Testing JARVIS voice..."
cd "$(dirname "$0")"
source jarvis/bin/activate
python test_voice.py
EOF

# Stop all JARVIS processes
cat > stop_jarvis.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping JARVIS processes..."
pkill -f "python -m api.main" 2>/dev/null || true
pkill -f "gui/main_window.py" 2>/dev/null || true
echo "✅ JARVIS stopped"
EOF

# Make scripts executable
chmod +x start_jarvis.sh start_gui.sh test_voice.sh stop_jarvis.sh
print_status "Startup scripts created"

# Create bash aliases
print_step "Creating bash aliases..."
ALIASES_FILE="$HOME/.jarvis_aliases"
cat > "$ALIASES_FILE" << EOF
# JARVIS AI Agent Aliases
alias jarvis-start='cd $(pwd) && ./start_jarvis.sh'
alias jarvis-gui='cd $(pwd) && ./start_gui.sh'
alias jarvis-voice='cd $(pwd) && ./test_voice.sh'
alias jarvis-stop='cd $(pwd) && ./stop_jarvis.sh'
alias jarvis-cd='cd $(pwd)'
EOF

# Add to .bashrc if not already present
if ! grep -q "jarvis_aliases" "$HOME/.bashrc"; then
    echo "" >> "$HOME/.bashrc"
    echo "# JARVIS AI Agent Aliases" >> "$HOME/.bashrc"
    echo "source $ALIASES_FILE" >> "$HOME/.bashrc"
    print_status "Aliases added to .bashrc"
else
    print_status "Aliases already in .bashrc"
fi

# Test installation
print_step "Testing JARVIS installation..."
if python -c "from api.services.enhanced_voice import EnhancedVoiceService; print('✅ Voice service import successful')" 2>/dev/null; then
    print_status "JARVIS core modules working"
else
    print_warning "Some JARVIS modules may have issues"
fi

# Final instructions
echo ""
echo "🎉 JARVIS AI Agent installation completed!"
echo "========================================"
echo ""
echo "📋 Next steps:"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. Test voice: jarvis-voice"
echo "3. Start JARVIS: jarvis-start"
echo "4. Start GUI: jarvis-gui"
echo ""
echo "🎤 Voice commands:"
echo "- 'Hej JARVIS' - Wake word"
echo "- 'God morgon JARVIS' - Morning greeting"
echo "- 'JARVIS, vad är klockan?' - Ask time"
echo ""
echo "🌐 API available at: http://localhost:8080"
echo "📖 Documentation: http://localhost:8080/docs"
echo ""
echo "🔧 Useful commands:"
echo "- jarvis-start  # Start JARVIS server"
echo "- jarvis-gui    # Start GUI interface"
echo "- jarvis-voice  # Test voice system"
echo "- jarvis-stop   # Stop all JARVIS processes"
echo "- jarvis-cd     # Go to JARVIS directory"
echo ""
print_status "Installation complete! Welcome to JARVIS AI Agent 🤖"
