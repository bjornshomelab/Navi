# JARVIS Installation Guide 🚀

## Snabbinstallation (Rekommenderat)

### För Ubuntu/Debian-system:

```bash
# 1. Klona JARVIS
git clone https://github.com/bjornshomelab/jarvis.git
cd jarvis

# 2. Kör installationsskriptet
chmod +x install.sh
./install.sh

# 3. Starta om terminalen eller ladda aliases
source ~/.bashrc

# 4. Testa installationen
jarvis-voice

# 5. Starta JARVIS
jarvis-start
```

Det är allt! 🎉

---

## Manuell installation

### Systemkrav
- **OS**: Linux (Ubuntu 20.04+ / Debian 11+ rekommenderas)
- **Python**: 3.11+ (3.13+ för bästa prestanda)
- **RAM**: 4GB+ (8GB+ rekommenderat)
- **Disk**: 2GB+ ledigt utrymme
- **Audio**: ALSA/PulseAudio för röstfunktioner

### Steg 1: Klona repository
```bash
git clone https://github.com/bjornshomelab/jarvis.git
cd jarvis
```

### Steg 2: Installera systemdependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y \
    python3-pip python3-venv python3-dev \
    espeak espeak-data espeak-data-sv \
    speech-dispatcher speech-dispatcher-swedish \
    alsa-utils pulseaudio \
    python3-pygame ffmpeg \
    build-essential portaudio19-dev libasound2-dev
```

**Fedora/CentOS:**
```bash
sudo dnf install -y \
    python3-pip python3-virtualenv python3-devel \
    espeak speech-dispatcher \
    alsa-utils pulseaudio \
    python3-pygame ffmpeg \
    gcc gcc-c++ portaudio-devel alsa-lib-devel
```

### Steg 3: Skapa Python virtual environment
```bash
python3 -m venv jarvis
source jarvis/bin/activate
```

### Steg 4: Installera Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Steg 5: Testa installationen
```bash
# Testa röstfunktioner
python test_voice.py

# Testa grundläggande funktioner
python -c "from api.services.enhanced_voice import EnhancedVoiceService; print('✅ JARVIS ready!')"
```

### Steg 6: Skapa startskript (valfritt)
```bash
# Gör skript körbara
chmod +x start_jarvis.sh start_gui.sh test_voice.sh stop_jarvis.sh

# Lägg till aliases i ~/.bashrc
echo 'alias jarvis-start="cd $(pwd) && ./start_jarvis.sh"' >> ~/.bashrc
echo 'alias jarvis-gui="cd $(pwd) && ./start_gui.sh"' >> ~/.bashrc
echo 'alias jarvis-voice="cd $(pwd) && ./test_voice.sh"' >> ~/.bashrc
echo 'alias jarvis-stop="cd $(pwd) && ./stop_jarvis.sh"' >> ~/.bashrc

# Ladda aliases
source ~/.bashrc
```

---

## Användning

### Starta JARVIS Server
```bash
# Med alias (rekommenderat)
jarvis-start

# Eller manuellt
cd jarvis
source jarvis/bin/activate
python -m api.main
```

Server startar på: http://localhost:8080

### Starta GUI
```bash
# Med alias
jarvis-gui

# Eller manuellt
python gui/main_window.py
```

### Testa röstfunktioner
```bash
# Med alias
jarvis-voice

# Eller manuellt
python test_voice.py
```

### Använd API:et
```bash
# Skicka kommando
curl -X POST "http://localhost:8080/api/command" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hej JARVIS, vad är klockan?", "command_type": "query"}'

# Be JARVIS prata
curl -X POST "http://localhost:8080/api/voice/speak" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hej! Jag är JARVIS, din AI-assistent."}'
```

---

## Google Cloud Setup (Valfritt)

För avancerade funktioner som Speech-to-Text och BigQuery:

### 1. Skapa Google Cloud projekt
1. Gå till [Google Cloud Console](https://console.cloud.google.com)
2. Skapa nytt projekt eller välj befintligt
3. Aktivera följande APIs:
   - Cloud Speech-to-Text API
   - Cloud Vision API  
   - Cloud Storage API
   - BigQuery API
   - Cloud Natural Language API

### 2. Skapa Service Account
1. IAM & Admin → Service Accounts
2. Create Service Account
3. Ge roller:
   - Cloud Speech Client
   - Cloud Vision Client
   - BigQuery User
   - Storage Object Viewer

### 3. Ladda ner nyckelfil
1. Klicka på service account
2. Keys → Add Key → Create new key
3. Välj JSON format
4. Spara som `service-account.json` i JARVIS-mappen

### 4. Sätt miljövariabel
```bash
export GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
# Lägg till i ~/.bashrc för permanent:
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/jarvis/service-account.json"' >> ~/.bashrc
```

---

## Felsökning

### Vanliga problem och lösningar

**Problem: Inget ljud från TTS**
```bash
# Testa systemljud
speaker-test -c2

# Testa speech-dispatcher
echo "test" | spd-say

# Kontrollera Edge TTS
source jarvis/bin/activate
edge-tts --list-voices | grep sv-SE
```

**Problem: Mikrofon fungerar inte**
```bash
# Testa inspelning
arecord -f cd -t wav -d 3 test.wav && aplay test.wav

# Kontrollera audio-enheter
arecord -l
aplay -l
```

**Problem: Python import-fel**
```bash
# Kontrollera virtual environment
which python
pip list | grep fastapi

# Installera om dependencies
pip install --force-reinstall -r requirements.txt
```

**Problem: Port 8080 upptagen**
```bash
# Hitta process som använder porten
lsof -i :8080

# Döda process om nödvändigt
sudo kill -9 $(lsof -t -i:8080)
```

**Problem: Permission denied**
```bash
# Fixa rättigheter för skript
chmod +x *.sh

# Fixa rättigheter för audio (Ubuntu)
sudo usermod -a -G audio $USER
# Logga ut och in igen
```

---

## Uppdatering

För att uppdatera JARVIS till senaste versionen:

```bash
cd jarvis
git pull origin main
source jarvis/bin/activate
pip install --upgrade -r requirements.txt
```

---

## Systemkrav för olika användningsfall

### Grundläggande användning (TTS + API)
- **RAM**: 2GB
- **CPU**: 2 kärnor
- **Disk**: 1GB

### Fullständig funktionalitet (GUI + Voice + Research)
- **RAM**: 4GB+
- **CPU**: 4 kärnor+
- **Disk**: 2GB+
- **Nätverk**: Bredband för research-funktioner

### Avancerad användning (Google Cloud + BigQuery)
- **RAM**: 8GB+
- **CPU**: 8 kärnor+
- **Disk**: 5GB+
- **Nätverk**: Snabb bredband

---

## Support

- **GitHub Issues**: [github.com/bjornshomelab/jarvis/issues](https://github.com/bjornshomelab/jarvis/issues)
- **Dokumentation**: Se README.md och wiki
- **Email**: bjornshomelab@gmail.com

---

**"Sometimes you gotta run before you can walk"** - Tony Stark

Välkommen till framtiden med JARVIS! 🤖✨
