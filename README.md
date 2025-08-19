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

## ⚡ Quick Start

### 🔧 Installation

1. **Clone och setup:**
   ```bash
   git clone [your-repo]
   cd Jarvis
   python3 -m venv jarvis
   source jarvis/bin/activate
   pip install -r requirements.txt
   ```

2. **Starta JARVIS Core:**
   ```bash
   # Aktivera alias (lägg till i ~/.bashrc)
   alias jarvis='cd /path/to/Jarvis && python3 jarvis_core.py'
   
   # Starta direkt
   python3 jarvis_core.py
   ```

### 💬 Användning

```bash
🤖 JARVIS Core - Terminal AI Agent
🎯 Fokuserad på intelligens och automation

💬 Du: help
🤖 JARVIS: [visar alla kommandon och agents]

💬 Du: agents
🤖 JARVIS: [listar alla specialiserade agents]

💬 Du: agent coder "skapa en Flask API"
🤖 Senior Developer: [genererar komplett Python Flask kod]

💬 Du: research "Python AI trends 2025"
🤖 JARVIS: [startar djup forskning och analys]

💬 Du: learn "Björn gillar att jobba på kvällar"
🤖 JARVIS: [sparar i personligt minne]

💬 Du: system "installera docker"
🤖 JARVIS: [kör sudo-kommandon säkert med lösenordsprompt]
```

### 📚 Core Kommandon

| Kommando | Beskrivning | Exempel |
|----------|-------------|---------|
| `help` | Visa alla kommandon | `help` |
| `agents` | Lista specialiserade agents | `agents` |
| `agent <typ> <fråga>` | Kontakta specifik agent | `agent coder "skapa en API"` |
| `research <ämne>` | Starta forskning | `research "Linux automation"` |
| `learn <fakta>` | Lär JARVIS något | `learn "favoritspråk är Python"` |
| `memory <sök>` | Sök i minne | `memory "Python"` |
| `system <kommando>` | Kör systemoperationer | `system "status"` |
| **Naturliga frågor** | Automatisk routing | `"hur optimerar jag min kod?"` |

### 🔐 Säker Sudo Integration

JARVIS Core inkluderar säker sudo-användning med:
- **Lösenordsprompt** för alla sudo-operationer
- **Whitelist** av tillåtna kommandon
- **Fullständig logging** av alla sudo-aktiviteter
- **Security violation detection**

```bash
💬 Du: system "installera nginx"
🔐 Sudo-rättigheter krävs för: apt install nginx
Ange ditt lösenord: [secure input]
✅ nginx installation klar!
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

# JARVIS Core - Terminal AI Agent 🤖⚡

> **Terminal-focused AI assistant with specialized agents and advanced automation**

JARVIS Core är den senaste evolutionen av JARVIS AI - en kraftfull terminal-baserad assistent fokuserad på **intelligens över interface**. Systemet inkluderar specialiserade AI-agents för utveckling, utbildning, design och systemautomation.

![JARVIS Status](https://img.shields.io/badge/status-operational-brightgreen)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![Terminal](https://img.shields.io/badge/interface-terminal-blue)
![Agents](https://img.shields.io/badge/agents-7-purple)

## 🎯 Core Philosophy: Intelligence Over Interface

**Från GUI till Core Intelligence:**
- ✅ **Terminal interface** - Ren kommandorad-interaktion
- ✅ **7 Specialiserade Agents** - Expert AI inom olika områden  
- ✅ **Säker sudo integration** - System automation med lösenordsprompt
- ✅ **Research & Memory** - All intelligens bevarad och förbättrad
- ✅ **Local automation** - Kraftfull systemintegration

---

## 🤖 Specialiserade Agent System

### 💻 **Senior Developer Agent** (`coder`)
- **Specialitet**: Full-stack utveckling och arkitektur
- **Kapaciteter**: 
  - Kod-generering i 10+ språk (Python, JavaScript, Go, Rust, etc.)
  - DevOps automation (Docker, CI/CD pipelines)
  - Code review och optimering
  - Environment setup med sudo-rättigheter
- **Exempel**: `agent coder "skapa en REST API i Python"`

### 🔧 **System Analyst Agent** (`system_analyst`)
- **Specialitet**: System optimering och infrastruktur
- **Kapaciteter**:
  - Automatiska backup-lösningar
  - Säkerhetskonfiguration (firewall, SSH)
  - Performance monitoring och tuning
  - Service management och automation
- **Exempel**: `agent system_analyst "optimera mitt Linux system"`

### 📊 **Data Scientist Agent** (`data_scientist`)
- **Specialitet**: Dataanalys, ML och AI
- **Kapaciteter**:
  - Komplett ML pipelines med scikit-learn
  - Exploratory Data Analysis (EDA)
  - Data visualization och reporting
  - Feature engineering och model selection
- **Exempel**: `agent data_scientist "analysera min CSV fil"`

### 🎨 **UI/UX Designer Agent** (`designer`)
- **Specialitet**: Grafisk design och användarupplevelse
- **Kapaciteter**:
  - Modern CSS frameworks och design systems
  - Responsiv design och accessibility
  - Färgscheman och typografi
  - Component libraries
- **Exempel**: `agent designer "skapa modern CSS för min hemsida"`

### ✍️ **Content Creator Agent** (`content_creator`)
- **Specialitet**: Innehållsskapande och copywriting
- **Kapaciteter**:
  - SEO-optimerade blog posts
  - Social media content strategier
  - Marketing copy och sales pages
  - Technical writing och dokumentation
- **Exempel**: `agent content_creator "skriv en bloggpost om AI"`

### 📚 **University Tutor Agent** (`university_tutor`)
- **Specialitet**: Akademisk vägledning och utbildning
- **Kapaciteter**:
  - Konceptförklaringar (matematik, fysik, datalogi)
  - Personliga studieplaner och scheman
  - Tentamensförberedelser
  - Uppsats- och forskningshjälp
- **Exempel**: `agent university_tutor "förklara vad en derivata är"`

### 🎯 **Study Coach Agent** (`study_coach`)
- **Specialitet**: Motivation och produktivitetscoaching
- **Kapaciteter**:
  - Anti-prokrastinering strategier
  - Motivation boosting tekniker
  - Stress management och mental hälsa
  - Goal setting och habit tracking
- **Exempel**: `agent study_coach "jag prokrastinerar och behöver hjälp"`

---

## 🚀 Intelligent Agent Routing

JARVIS Core inkluderar **automatisk agent routing** - bara ställ din fråga naturligt så väljer systemet rätt specialist:

```bash
💬 Du: "hur bygger jag en webapp?"
🤖 Agent routing - Bästa match: coder (confidence: 0.85)
🤖 Senior Developer svarar: [detaljerad webapp guide]

💬 Du: "jag har ingen motivation att studera" 
🤖 Agent routing - Bästa match: study_coach (confidence: 0.78)
🤖 Study Coach svarar: [motivation boost strategier]

💬 Du: "designa en logo för mitt företag"
🤖 Agent routing - Bästa match: designer (confidence: 0.71)
🤖 UI/UX Designer svarar: [design process och tools]
```

---
