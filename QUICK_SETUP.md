# 🚀 NAVI Quick Setup Guide

Welcome to NAVI! This guide will get you up and running in just a few minutes.

## ⚡ Super Quick Start

```bash
git clone https://github.com/bjornshomelab/Navi.git
cd Navi
chmod +x setup.sh
./setup.sh
```

**That's it!** The interactive installer will handle everything.

## 🎯 What the Installer Does

### Step 1: System Check ✅
- Verifies Python 3.8+ is installed
- Checks for required system packages

### Step 2: Your Preferences 🎛️
The installer asks about your setup preferences:

#### AI Provider Choice
- **🏠 Local AI (Ollama)** - Complete privacy, no internet required
- **☁️ Cloud AI (OpenAI/Google)** - Most powerful models, needs API key
- **🔄 Hybrid** - Best of both worlds

#### Memory & Intelligence
- **🧠 RAG Database** - Enhanced memory system for smarter responses
- **🔍 Semantic Search** - AI-powered knowledge retrieval

#### Features & Integration
- **⚡ Optional Features** - Voice, image processing, advanced tools
- **🐚 Shell Aliases** - Convenient commands like `navi` and `navi-cli`

### Step 3: Automatic Setup 🤖
- Creates virtual environment (optional)
- Installs Python dependencies
- Downloads AI models (if local AI chosen)
- Configures API keys (if cloud AI chosen)
- Sets up RAG database
- Creates shell aliases

### Step 4: Ready to Go! 🎉
- Tests installation
- Shows you how to start NAVI
- Provides helpful next steps

## 🎮 Usage After Installation

### If you chose Shell Aliases:
```bash
navi              # Start NAVI
navi-cli          # Command-line mode
navi-status       # Check system status
navi-help         # Show help
```

### Manual commands:
```bash
# If you have virtual environment:
source navi_env/bin/activate
python3 navi.py

# Direct usage:
python3 navi.py
```

## 🔧 Common Installation Choices

### For Maximum Privacy:
1. Choose "Local AI (Ollama)"
2. Enable RAG database
3. Install optional features
4. Create shell aliases

### For Maximum Power:
1. Choose "Cloud AI"
2. Enter your OpenAI or Google API key
3. Enable RAG database
4. Install all features

### For Flexibility:
1. Choose "Hybrid"
2. Set up both local and cloud AI
3. Configure all features
4. Use local for privacy, cloud for power

## 🆘 Troubleshooting

### Python Issues
```bash
# Check Python version (needs 3.8+)
python3 --version

# Install Python on Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

### Permission Issues
```bash
# Make setup script executable
chmod +x setup.sh

# Run with explicit bash
bash setup.sh
```

### Network Issues
```bash
# For local-only setup (no internet required after initial clone)
./setup.sh
# Choose "Local AI" and skip model downloads
```

## 🎯 Quick Commands Reference

### Starting NAVI
```bash
# Interactive mode
navi

# Single question
navi "What's the weather like?"

# Specific agent
navi -a coder "Write a Python function"

# Check status
navi --status
```

### Configuration
```bash
# Edit main config
nano config/settings.yaml

# Edit API keys
nano .env

# View current setup
navi --status
```

## 🔄 What's Next?

After installation, you can:
1. **Start chatting** - Just run `navi` and ask anything
2. **Try different agents** - Use `-a coder` for programming help
3. **Explore features** - Check the main README for advanced usage
4. **Customize** - Edit `config/settings.yaml` for your preferences

## 💡 Pro Tips

- **Use RAG database** - It makes NAVI much smarter over time
- **Try hybrid setup** - Local for privacy, cloud for heavy tasks
- **Explore agents** - Each agent is optimized for different tasks
- **Check status regularly** - `navi --status` shows what's working
- **Read the docs** - The main README has tons of examples

---

**Welcome to NAVI! 🤖✨**

*Your privacy-first AI assistant is ready to help!*
