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

NAVI is a **revolutionary AI assistant** that puts **privacy first** while delivering powerful AI capabilities. Unlike cloud-dependent assistants, NAVI runs entirely on your local machine with optional cloud fallback, ensuring your data stays private and secure.

### ✨ Why Choose NAVI?

- 🏠 **100% Local Processing** - Your data never leaves your machine
- 🔄 **Multi-Provider Support** - OpenAI, Google Gemini, Ollama, and local models
- 🤖 **5 Specialized AI Agents** - Each optimized for specific tasks
- 🧠 **Smart Memory System** - RAG-powered knowledge base with semantic search
- ⚡ **Lightning Fast CLI** - Modern terminal-first experience
- 🔒 **Privacy by Design** - No telemetry, no data collection, completely open source
- 🎯 **Zero Configuration** - Works out of the box with local models

## 🚀 Quick Start

### Option 1: Local AI (Recommended for Privacy)
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download a model
ollama pull llama3.2

# 3. Clone and run NAVI
git clone https://github.com/bjornshomelab/Navi.git
cd Navi
pip install -r requirements.txt
python3 navi.py
```

### Option 2: Cloud AI (OpenAI)
```bash
# 1. Clone repository
git clone https://github.com/bjornshomelab/Navi.git
cd Navi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
export OPENAI_API_KEY="your-api-key-here"

# 4. Run NAVI
python3 navi.py
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

## 💡 Usage Examples

### Basic Commands
```bash
# Interactive mode
python3 navi.py

# Single command
python3 navi.py "Hello, NAVI!"

# Agent-specific task
python3 navi.py -a coder "Write a Python function to sort a list"

# Status check
python3 navi.py --status
```

### Agent Commands
```bash
# Programming help
python3 navi.py -a coder "Explain async/await in Python"

# Research assistance
python3 navi.py -a researcher "Latest developments in AI safety"

# Creative writing
python3 navi.py -a creative "Write a short story about AI"

# Image generation (with compatible providers)
python3 navi.py -a image "Generate a sunset over mountains"
```

## 🛠 Installation

### System Requirements
- **OS**: Linux (Ubuntu/Debian recommended), macOS, Windows WSL
- **Python**: 3.8+ (3.11+ recommended)
- **Memory**: 4GB+ RAM recommended
- **Storage**: 2GB+ free space

### Automated Installation (Linux)
```bash
git clone https://github.com/bjornshomelab/Navi.git
cd Navi
chmod +x install.sh
./install.sh
```

### Manual Installation
```bash
# 1. Clone repository
git clone https://github.com/bjornshomelab/Navi.git
cd Navi

# 2. Create virtual environment
python3 -m venv navi_env
source navi_env/bin/activate  # Linux/macOS
# or
navi_env\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure (optional)
cp config/settings.yaml.example config/settings.yaml
# Edit config/settings.yaml with your preferences

# 5. Run NAVI
python3 navi.py
```

## 🔧 Configuration

### Provider Setup

#### Ollama (Local AI)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama3.2          # General purpose
ollama pull codellama         # Code-focused
ollama pull llava             # Vision capabilities
```

#### OpenAI
```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-api-key-here"

# Or add to .env file
echo "OPENAI_API_KEY=sk-your-api-key-here" >> .env
```

#### Google Gemini
```bash
# Set environment variable
export GOOGLE_API_KEY="your-google-api-key"

# Or add to .env file
echo "GOOGLE_API_KEY=your-google-api-key" >> .env
```

### Configuration File
```yaml
# config/settings.yaml
providers:
  preferred: "ollama"  # ollama, openai, google
  fallback: ["openai", "google"]

agents:
  default: "chat"
  
memory:
  enabled: true
  max_entries: 1000
  
interface:
  streaming: true
  color: true
```

## 🌍 Use Cases

### For Developers
- **Code Review**: Get instant feedback on your code
- **Debugging**: AI-powered problem solving
- **Documentation**: Generate docs and comments
- **Learning**: Understand complex programming concepts

### For Researchers
- **Data Analysis**: Process and interpret data
- **Literature Review**: Summarize research papers
- **Report Generation**: Create comprehensive reports
- **Fact Checking**: Verify information quickly

### For Content Creators
- **Writing Assistance**: Overcome writer's block
- **Brainstorming**: Generate creative ideas
- **Editing**: Improve and refine content
- **Social Media**: Create engaging posts

### For Daily Use
- **Question Answering**: Get instant answers
- **Task Planning**: Organize your day
- **Learning**: Explore new topics
- **Problem Solving**: Work through challenges

## 🔒 Privacy & Security

### Privacy Features
- **Local Processing**: Core functionality works offline
- **No Telemetry**: Zero data collection or tracking
- **Open Source**: Full transparency of code
- **Data Control**: You own and control all your data

### Security Measures
- **Sandboxed Execution**: Runs in isolated environment
- **Secure Storage**: Local encryption for sensitive data
- **API Key Safety**: Secure handling of credentials
- **Regular Updates**: Security patches and improvements

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Quick Start
```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/yourusername/Navi.git
cd Navi

# 3. Create a feature branch
git checkout -b feature/amazing-feature

# 4. Make your changes and test
python3 -m pytest tests/

# 5. Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# 6. Create a Pull Request
```

### Areas for Contribution
- 🐛 **Bug Fixes**: Help us squash bugs
- ✨ **New Features**: Add exciting capabilities
- 📚 **Documentation**: Improve guides and examples
- 🧪 **Testing**: Increase test coverage
- 🌐 **Translations**: Support more languages
- 🎨 **UI/UX**: Enhance user experience

## 📚 Documentation

- 📖 [User Guide](docs/user-guide.md)
- 🔧 [Developer Guide](docs/developer-guide.md)
- 📋 [API Reference](docs/api-reference.md)
- 🚀 [Advanced Usage](docs/advanced-usage.md)
- ❓ [FAQ](docs/faq.md)

## 🐛 Troubleshooting

### Common Issues

**NAVI won't start?**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check configuration
python3 navi.py --status
```

**No AI provider available?**
```bash
# Install Ollama for local AI
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# Or set OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

**Memory issues?**
```bash
# Clear memory database
rm -rf data/memory/

# Or reduce memory usage in config
echo "memory: { max_entries: 100 }" >> config/settings.yaml
```

## 🏗 Architecture

NAVI uses a modular architecture designed for extensibility and maintainability:

```
navi/
├── core.py          # Main application logic
├── providers.py     # AI provider abstractions
├── agents.py        # Specialized AI agents
├── memory.py        # Memory and context management
└── __init__.py

config/
├── settings.yaml    # Main configuration
├── agents.yaml      # Agent configurations
├── providers.yaml   # Provider settings
└── memory.yaml      # Memory settings

cli/
└── navi_cli.py      # Command-line interface

data/
└── memory/          # Local memory storage
```

## 🛣 Roadmap

### v2.1 - Enhanced Intelligence
- [ ] Advanced reasoning capabilities
- [ ] Multi-modal input support
- [ ] Improved context understanding
- [ ] Custom agent creation

### v2.2 - Ecosystem Integration
- [ ] Plugin system
- [ ] VS Code extension
- [ ] Browser integration
- [ ] Mobile companion app

### v2.3 - Enterprise Features
- [ ] Team collaboration
- [ ] Access controls
- [ ] Audit logging
- [ ] Backup/sync options

## 📊 Performance

### Benchmarks
- **Startup Time**: < 3 seconds
- **Response Time**: < 500ms (local models)
- **Memory Usage**: 200-800MB
- **CPU Usage**: Low impact on system

### Optimization
- Lazy loading of AI models
- Efficient memory management
- Streaming responses
- Asynchronous processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Community

- 🐙 **GitHub**: [Issues](https://github.com/bjornshomelab/Navi/issues) • [Discussions](https://github.com/bjornshomelab/Navi/discussions)
- 📧 **Email**: bjornshomelab@gmail.com
- 💬 **Discord**: [Join our community](https://discord.gg/navi-ai) *(coming soon)*

## 🙏 Acknowledgments

- **OpenAI** for advancing AI accessibility
- **Ollama** for making local AI simple
- **The Open Source Community** for inspiration and support
- **Contributors** who make NAVI better every day

---

<div align="center">

**"The best AI assistant is the one that respects your privacy"**

*Building the future of local-first AI, one conversation at a time* 🤖✨

[⭐ Star this project](https://github.com/bjornshomelab/Navi) • [🍴 Fork it](https://github.com/bjornshomelab/Navi/fork) • [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20NAVI%20-%20Your%20Local-First%20AI%20Assistant!%20https://github.com/bjornshomelab/Navi)

</div>
