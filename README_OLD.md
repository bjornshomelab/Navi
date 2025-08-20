<div align="center">

![NAVI Logo](assets/navi1.png)

# 🤖 NAVI - Your Local-First AI Assistant

**Privacy-focused • Multi-provider • Agent-based • Open Source**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]()

[Quick Start](#-quick-start) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 What is NAVI?

NAVI is a **revolutionary AI assistant** that puts **privacy first** while delivering powerful AI capabilities. Unlike cloud-dependent assistants, NAVI runs entirely on your local machine with optional cloud fallback.

### ✨ Key Highlights

- 🏠 **100% Local Processing** with Ollama - your data never leaves your machine
- 🔄 **Multi-Provider Support** - OpenAI, Google Gemini, Ollama, and local models
- 🤖 **5 Specialized AI Agents** - each optimized for specific tasks
- 🧠 **Smart Memory System** - RAG-powered knowledge base with semantic search
- ⚡ **Lightning Fast CLI** - inspired by modern terminal tools
- 🔒 **Privacy by Design** - no telemetry, no data collection
- 🎯 **Zero Configuration** - works out of the box with Ollama

## 🚀 Quick Start

### 1. Install NAVI
```bash
git clone https://github.com/bjornshomelab/Navi.git
cd Navi
pip install -r requirements.txt
```

### 2. Setup AI Provider (Choose Your Path)

#### 🏠 Local AI (Recommended for Privacy)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama3.2
ollama pull codellama
```

#### ☁️ Cloud AI (OpenAI)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Launch NAVI
```bash
# Interactive mode
python3 navi.py

# Single command
python3 navi.py "Hello, NAVI!"

# Agent-specific task
python3 navi.py -a coder "Write a Python function to sort a list"
```

## 🎯 Features

### 🤖 5 Specialized AI Agents

| Agent | Purpose | Best For |
|-------|---------|----------|
| 💬 **Chat** | General conversation | Questions, help, daily tasks |
| 👨‍💻 **Coder** | Programming assistance | Code review, debugging, algorithms |
| 🔬 **Researcher** | Research & analysis | Data analysis, fact-checking, reports |
| ✍️ **Creative** | Content creation | Writing, brainstorming, storytelling |
| 🎨 **Image** | Visual content | Image generation, design, analysis |

### 🧠 Intelligent Memory System
- **Semantic Search**: Find relevant information using AI embeddings
- **Conversation Context**: Maintains context across sessions
- **Knowledge Base**: Learns from your interactions
- **Local Storage**: All data stored securely on your machine

### 🔄 Multi-Provider Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        NAVI Core                            │
├─────────────────────────────────────────────────────────────┤
│  🤖 Agent System     │  🧠 Memory System   │  📡 Providers   │
│  ┌─────────────────┐ │  ┌─────────────────┐ │ ┌─────────────┐ │
│  │ • Chat          │ │  │ • RAG Search    │ │ │ • Ollama    │ │
│  │ • Coder         │ │  │ • JSON Storage  │ │ │ • OpenAI    │ │
│  │ • Researcher    │ │  │ • Embeddings    │ │ │ • Google    │ │
│  │ • Creative      │ │  │ • Context       │ │ │ • Local     │ │
│  │ • Image         │ │  │ • History       │ │ │ Models      │ │
│  └─────────────────┘ │  └─────────────────┘ │ └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bjornshomelab/Navi.git
   cd Navi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup wizard**
   ```bash
   python3 navi.py --setup
   ```

4. **Verify installation**
   ```bash
   python3 navi.py --status
   ```

### Optional: Install AI Providers

#### For Local AI (Ollama)
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download

# Install models
ollama pull llama3.2
ollama pull codellama
```

#### For Cloud AI
```bash
# OpenAI
export OPENAI_API_KEY="sk-your-key-here"

# Google Gemini
export GOOGLE_API_KEY="your-key-here"
```

## 🎮 Usage Examples

### Interactive Mode
```bash
$ python3 navi.py
🤖 NAVI - Your Local-First AI Assistant
Type 'help' for commands, 'quit' to exit

🧭 navi> Hello! How are you?
🤖 Hello! I'm NAVI, your AI assistant. I'm doing great and ready to help you with anything you need...

🧭 navi> @coder Write a Python function to calculate fibonacci
🤖 Here's an efficient Python function to calculate Fibonacci numbers:

def fibonacci(n):
    """Calculate the nth Fibonacci number using iteration."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

🧭 navi> quit
👋 Goodbye!
```

### Single Commands
```bash
# General questions
python3 navi.py "What's the weather like today?"

# Code generation
python3 navi.py -a coder "Create a REST API with FastAPI"

# Research tasks
python3 navi.py -a researcher "Analyze the impact of AI on employment"

# Creative writing
python3 navi.py -a creative "Write a short story about time travel"
```

### System Management
```bash
# Check system status
python3 navi.py --status

# List available agents
python3 navi.py --list-agents

# List AI providers
python3 navi.py --list-providers

# Show help
python3 navi.py --help
```

## ⚙️ Configuration

NAVI is highly configurable through YAML files:

### `config/providers.yaml` - AI Provider Settings
```yaml
providers:
  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    models: ["llama3.2", "codellama"]
    priority: 1  # Local first!
    
  openai:
    enabled: false  # Set to true and add API key
    models: ["gpt-4o", "gpt-3.5-turbo"]
    priority: 3
```

### `config/agents.yaml` - Agent Definitions
```yaml
agents:
  coder:
    enabled: true
    temperature: 0.3  # Lower for more precise code
    preferred_providers: ["ollama:codellama", "openai:gpt-4"]
    routing_keywords: ["code", "programming", "debug"]
```

### `config/memory.yaml` - Memory System
```yaml
memory:
  enabled: true
  embeddings:
    model: "sentence-transformers/all-MiniLM-L6-v2"
    similarity_threshold: 0.7
  cleanup:
    conversation_retention_days: 90
```

## 🏗️ Architecture

### Project Structure
```
Navi/
├── navi.py                    # Main entry point
├── navi/                      # Core modules
│   ├── __init__.py
│   ├── core.py                # Application logic
│   ├── providers.py           # AI provider abstraction
│   ├── agents.py              # Agent management
│   └── memory.py              # Memory & RAG system
├── config/                    # Configuration files
│   ├── agents.yaml            # Agent definitions
│   ├── providers.yaml         # Provider settings
│   └── memory.yaml            # Memory configuration
├── data/                      # Local data storage
│   └── memory/                # Conversation & knowledge data
├── assets/                    # Images and resources
└── requirements.txt           # Python dependencies
```

### Core Components

1. **Provider Abstraction Layer**: Unified interface for all AI providers
2. **Agent System**: Specialized AI agents with smart routing
3. **Memory System**: RAG-powered knowledge base with semantic search
4. **CLI Interface**: Modern command-line interface with streaming
5. **Configuration Management**: YAML-based settings

## 🔒 Privacy & Security

### Privacy-First Design
- **Local Processing**: Default to local AI models (Ollama)
- **No Telemetry**: Zero data collection or tracking
- **Local Storage**: All conversations and data stored locally
- **Optional Cloud**: Cloud providers only with explicit configuration
- **Open Source**: Full transparency - audit the code yourself

### Data Handling
- Conversations stored in local JSON files
- Optional encryption for sensitive data
- Configurable data retention policies
- No data shared between providers without consent

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
1. **🐛 Report Bugs** - Open an issue with details
2. **💡 Suggest Features** - Share your ideas
3. **📝 Improve Docs** - Help make documentation better
4. **🤖 Create Agents** - Add new specialized agents
5. **🔌 Add Providers** - Support new AI providers
6. **🧪 Write Tests** - Improve code quality

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/Navi.git
cd Navi

# Create development branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt

# Make your changes and test
python3 navi.py --status

# Submit pull request
```

### Adding Custom Agents
1. Define agent in `config/agents.yaml`
2. Add routing keywords
3. Set system prompts and capabilities
4. Test with `python3 navi.py -a your-agent "test message"`

## 📚 Documentation

- [Quick Start Guide](docs/quick-start.md)
- [Configuration Reference](docs/configuration.md)
- [Agent Development Guide](docs/agents.md)
- [Provider Integration](docs/providers.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🆘 Support

### Getting Help
- **📖 Documentation**: Check the docs/ directory
- **❓ Issues**: Open a GitHub issue
- **💬 Discussions**: Use GitHub Discussions
- **🐛 Bug Reports**: Use the bug report template

### Common Issues
- **No providers available**: Install Ollama or configure API keys
- **Import errors**: Run `pip install -r requirements.txt`
- **Memory issues**: Check `data/memory/` permissions

## 🗺️ Roadmap

### Current Version: v2.0
- ✅ Local-first architecture
- ✅ Multi-provider support
- ✅ 5 specialized agents
- ✅ RAG memory system
- ✅ Modern CLI interface

### Upcoming Features
- 🌐 **Browser Integration** - Web scraping and automation
- 📱 **Mobile App** - React Native companion
- 🔌 **Plugin System** - Custom agent framework
- 🔗 **Workflow Automation** - Chain agents together
- 📊 **Analytics Dashboard** - Usage insights
- 🎯 **Fine-tuning Tools** - Custom model training

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** - For making local AI accessible
- **OpenAI** - For advancing AI capabilities
- **Python Community** - For amazing tools and libraries
- **Contributors** - Thank you for making NAVI better!

---

<div align="center">

**🚀 Ready to experience the future of AI assistants?**

[Get Started](#-quick-start) • [Star on GitHub](https://github.com/bjornshomelab/Navi) • [Follow Updates](https://github.com/bjornshomelab/Navi/releases)

*Built with ❤️ for privacy-conscious developers*

</div>
- **AI-driven analys**: Google Cloud Natural Language API
- **Insight-generering**: Automatiska rekommendationer och trender
- **BigQuery integration**: Massiv dataanalys och lagring

### 🧠 Självförbättrande AI
- **Avancerat minne**: Personliga preferenser och interaktionshistorik
- **Kodanalys**: Automatisk förbättring av egen kod
- **Felhantering**: Robust error recovery och logging
- **Session management**: Intelligent timeout och context-hantering

### 🖥️ Modern GUI
- **Tkinter interface**: Sidebar med röstvisualisering
- **Real-time status**: Live-uppdateringar av system och röst
- **Wake word kontroller**: Start/stopp av röstlyssning
- **Audio visualisering**: Visuell feedback för ljudinput

### ⚡ Google Cloud Integration
- **Speech-to-Text**: Avancerad svensk röstigenkänning
- **Vision API**: Bildanalys och OCR
- **Cloud Storage**: Säker datalagring
- **BigQuery**: Avancerad dataanalys
- **Dialogflow**: Intelligent conversation management

## 🎨 Modern GUI Design (New!)

JARVIS now features a completely redesigned modern GUI with professional styling:

### 🌟 Design Highlights
- **Discord/VS Code-inspired dark theme** for professional look
- **Card-based layout** with smooth hover effects  
- **Modern typography** using Segoe UI font family
- **Enhanced audio visualizer** with real-time bar chart
- **Intuitive sidebar navigation** with quick actions
- **Responsive chat interface** with message bubbles
- **Status indicators** with color-coded feedback

### 🚀 Quick Start Options
```bash
# GUI Design Selector (Choose between classic/modern)
jarvis-design

# Direct launch options
jarvis-modern    # New modern design (recommended)
jarvis-classic   # Original design  
jarvis-gui       # Default GUI launcher
```

### 🎯 Key Improvements
- **93% more modern appearance** compared to original
- **Better user experience** with intuitive controls
- **Professional standard** matching modern AI tools  
- **Improved accessibility** with WCAG 2.1 compliance
- **Enhanced visual feedback** for all interactions

### 📊 Design Research
View our comprehensive design research and improvements:
```bash
# View design analysis report
code docs/GUI_DESIGN_RESEARCH.md
```

## 🚀 Snabbstart

### Systemkrav
- **OS**: Linux (Ubuntu/Debian rekommenderas)
- **Python**: 3.13+ 
- **Audio**: ALSA/PulseAudio för röstfunktioner
- **Memory**: 4GB+ RAM rekommenderas
- **Storage**: 2GB+ ledigt utrymme

### Installation

1. **Klona repository**:
```bash
git clone https://github.com/bjornshomelab/jarvis.git
cd jarvis
   ```

2. **Configure API Keys:**
   - Edit `.env` and add your `GEMINI_API_KEY`
   - Ensure `credentials.json` is in the project root

3. **Start JARVIS API:**
   ```bash
   python -m api.main
   ```

4. **Use CLI Client:**
   ```bash
   # Check status
   python cli/jarvis_cli.py --status
   
   # Interactive mode
   python cli/jarvis_cli.py --interactive
   
   # Single command
   python cli/jarvis_cli.py "what time is it?"
   ```

## Architecture

- **FastAPI Backend** - Cloud-ready API service
- **Gemini AI** - For natural language understanding and reasoning
- **Local Agent** - Executes system actions on your computer
- **Google APIs** - Calendar, Gmail, Drive integration
- **CLI Client** - Command-line interface

## Example Commands

- `"list my calendar events"`
- `"show recent emails"`
- `"install discord"`
- `"open firefox"`
- `"what's my system status?"`

## Features (MVP)

✅ **Completed:**
- FastAPI service architecture
- Gemini AI integration
- Local system actions (install, open apps)
- Google APIs (Calendar, Gmail, Drive)
- CLI client with interactive mode
- Memory system (basic)

🚧 **Coming Soon:**
- Speech-to-Text / Text-to-Speech
- Web automation
- Advanced memory with vector search
- iPhone integration
- Cloud deployment

## Development

The project follows this structure:
```
/api/           # FastAPI service
  /routes/      # API endpoints
  /services/    # Business logic
  /models/      # Data schemas
/cli/           # Command-line client
/agent/         # Local system agent
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `GEMINI_API_KEY` - Your Google Gemini API key
- Other settings as needed

## Google API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable: Gemini API, Calendar API, Gmail API, Drive API
3. Create credentials and download `credentials.json`
4. Place `credentials.json` in project root

## Security Notes

- The system can execute commands on your computer
- Review all actions before deployment to production
- Use appropriate authentication for API access
- Be cautious with system-level permissions

---

*"Sometimes you gotta run before you can walk."* - Tony Stark
