# JARVIS AI Agent 🤖

> **Iron Man style personal AI assistant with advanced Swedish voice capabilities**

JARVIS är en avancerad AI-assistent byggd med Python, FastAPI och Google Cloud APIs. Den kombinerar kraftfull forskning, dataanalys, röstinteraktion och automation för att skapa en verkligt intelligent personlig assistent.

![JARVIS Status](https://img.shields.io/badge/status-operational-brightgreen)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Funktioner

### 🎤 Avancerad Röstinteraktion
- **Wake Word Detection**: "Hej JARVIS", "God morgon JARVIS"
- **Naturlig svensk röst**: Microsoft Edge TTS med neural voices
- **Röstkommandon**: Fullständig röststyrning på svenska
- **Fallback-system**: Automatisk återgång vid audio-problem

### 🔬 Intelligent Forskning & Analys
- **Multi-source forskning**: Webb, akademiska källor, nyheter, myndighetdata
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
