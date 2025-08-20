# 🚀 NAVI Quick Start Guide

## ✅ Ready to Go!

**NAVI is your privacy-first AI assistant!** Get started with our interactive installer.

### 🎯 What makes NAVI special:
- ✅ **100% Local Processing** - Your data stays private
- ✅ **Multi-Provider Support** - Ollama, OpenAI, Google Gemini
- ✅ **Smart Memory System** - RAG-powered context retention
- ✅ **5 Specialized Agents** - Each optimized for specific tasks
- ✅ **Zero Configuration** - Works out of the box

---

## 🚀 One-Command Installation

### 🎯 Interactive Setup (Recommended)

```bash
git clone https://github.com/bjornshomelab/Navi.git
cd Navi
chmod +x setup.sh
./setup.sh
```

**The installer guides you through:**
1. **AI Provider Selection** (Local/Cloud/Hybrid)
2. **RAG Database Setup** (Enhanced memory)
3. **Feature Configuration** (Voice, images, etc.)
4. **Shell Integration** (Convenient aliases)

---

## 🎮 Using NAVI

### 🎯 Main Commands

```bash
# Start NAVI (if you chose shell aliases)
navi

# Command-line interface
navi-cli

# Check system status
navi-status

# Get help
navi-help
```

### 🤖 Agent-Specific Tasks

```bash
# Programming help
navi -a coder "Write a Python function to sort a list"

# Research assistance  
navi -a researcher "Latest AI developments"

# Creative writing
navi -a creative "Write a short story"

# General chat
navi -a chat "Hello, how are you?"

# Image tasks (with compatible providers)
navi -a image "Generate a sunset"
```

### 💬 Interactive Mode

```bash
# Start interactive session
navi

# Then chat naturally:
> Hello NAVI!
> Can you help me with Python?
> What's the weather like?
> Write me a poem about AI
```

---

## 🔧 Configuration

### 🎯 Quick Config

```bash
# Edit main settings
nano config/settings.yaml

# Configure API keys
nano .env

# Check what's working
navi --status
```

### 🤖 AI Provider Setup

#### Local AI (Privacy-First)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama3.2
ollama pull codellama
```

#### Cloud AI
```bash
# Add to .env file
echo "OPENAI_API_KEY=your-key-here" >> .env
echo "GOOGLE_API_KEY=your-key-here" >> .env
```

---

## 🎯 Common Use Cases

### For Developers
```bash
navi -a coder "Explain async/await in Python"
navi -a coder "Review this code: [paste code]"
navi -a coder "Debug this error: [error message]"
```

### For Researchers  
```bash
navi -a researcher "Summarize this paper: [URL/text]"
navi -a researcher "Find trends in AI safety"
navi -a researcher "Compare these two approaches"
```

### For Daily Use
```bash
navi "Plan my day"
navi "Explain quantum computing simply"
navi "Help me write an email"
```

---

## 🆘 Troubleshooting

### Installation Issues
```bash
# Check Python version (needs 3.8+)
python3 --version

# Make script executable
chmod +x setup.sh

# Run with bash directly
bash setup.sh
```

### NAVI Won't Start
```bash
# Check status
navi --status

# Try manual start
python3 navi.py

# Check configuration
cat config/settings.yaml
```

### No AI Provider
```bash
# Install Ollama for local AI
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# Or add API key for cloud AI
echo "OPENAI_API_KEY=your-key" >> .env
```

---

## 🎉 Next Steps

1. **Try different agents** - Each specializes in different tasks
2. **Explore the RAG system** - It learns from your conversations  
3. **Customize settings** - Edit `config/settings.yaml`
4. **Join the community** - Check GitHub for updates and discussion

---

**Welcome to NAVI! 🤖✨**

*Your privacy-first AI assistant is ready to help!*

# Välj mellan olika GUI-designs
jarvis-design

# Direkt till modern GUI
jarvis-modern

# Direkt till klassisk GUI  
jarvis-classic
```

### 🎨 Vad händer när du kör `jarvis`?

1. **Automatisk server-start** - Kontrollerar och startar JARVIS API-server
2. **GUI-val** - Ger dig 5 sekunder att välja GUI (standard = modern)
3. **Intelligent uppstart** - Hanterar alla dependencies automatiskt

### 📊 GUI-alternativen

#### 🎨 Modern GUI (Standard)
- Discord/VS Code-inspirerat mörkt tema
- Professionell design med moderna komponenter
- Förbättrad användarupplevelse
- Real-time audio visualizer med bar chart
- Card-baserad layout med hover effects

#### 🏠 Klassisk GUI
- Original tkinter-design
- Enkel och funktionell
- Waveform audio visualizer
- Traditionell layout

### ⚡ Snabbkommandon

```bash
jarvis              # Start med auto GUI-val (5s timeout)
jarvis-modern       # Direkt till modern GUI
jarvis-classic      # Direkt till klassisk GUI
jarvis-design       # Interaktiv design-väljare
```

### 🎯 Tips

- **Standard val**: Tryck bara Enter eller vänta 5 sekunder för modern GUI
- **Snabb access**: Använd `jarvis-modern` för direkt start
- **Jämförelse**: Använd `jarvis-design` för att se skillnaderna
- **Gamla sättet**: `jarvis-classic` ger dig original-designen

### 🚀 Exempel

```bash
# Snabbaste sättet - bara kör jarvis
$ jarvis
🤖 JARVIS AI Assistant - Full Start
Startar server och GUI automatiskt...

📦 Aktiverar virtual environment...
✅ JARVIS server körs redan

🎨 Vilken GUI vill du använda?
1. Modern GUI (Rekommenderas)  
2. Klassisk GUI
3. Visa design-väljare
Enter = Modern GUI (standard)

Välj (1-3, eller Enter för standard): [Enter]

🎨 Startar Modern GUI...
```

---

**Pro tip**: Sätt `jarvis` som standardkommando och njut av den automatiska uppstarten! 🚀
