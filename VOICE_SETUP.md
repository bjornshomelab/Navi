# JARVIS Röstförbättringar - Setup Guide

## Översikt
JARVIS har nu en kraftigt förbättrad röstservice med stöd för flera högkvalitativa svenska TTS-motorer.

## Tillgängliga Röstmotorer (i prioritetsordning)

### 1. Microsoft Edge TTS (Rekommenderas!)
- **Kvalitet**: Mycket hög, naturlig svensk röst
- **Kostnad**: Gratis
- **Installation**: Automatisk
- **Svenska röster**: 
  - `sv-SE-MattiasNeural` (Manlig, modern) **← JARVIS standard**
  - `sv-SE-SofieNeural` (Kvinnlig, modern)

### 2. Google Cloud Text-to-Speech
- **Kvalitet**: Högsta kvalitet
- **Kostnad**: Betaltjänst (första 1 miljon tecken gratis/månad)
- **Installation**: Kräver service account setup

### 3. eSpeak
- **Kvalitet**: Medium
- **Kostnad**: Gratis
- **Installation**: `sudo apt install espeak`

### 4. Speech Dispatcher
- **Kvalitet**: Medium
- **Kostnad**: Gratis
- **Installation**: `sudo apt install speech-dispatcher`

## Google Cloud TTS Setup (Valfritt för högsta kvalitet)

1. **Skapa Service Account**:
   ```bash
   # Gå till Google Cloud Console
   # Välj projekt "bjornshomelab"
   # IAM & Admin > Service Accounts
   # Create Service Account
   ```

2. **Ge behörigheter**:
   - Cloud Text-to-Speech API User

3. **Ladda ner nyckelfil**:
   - Döp till `service-account.json`
   - Placera i `/home/bjorn/Skrivbord/Jarvis/`

4. **Aktivera API**:
   ```bash
   # I Google Cloud Console:
   # APIs & Services > Library
   # Sök "Cloud Text-to-Speech API"
   # Enable
   ```

## Testning

### 1. Testa Edge TTS med manlig röst (Standard)
```bash
cd /home/bjorn/Skrivbord/Jarvis
source jarvis/bin/activate
python -c "
from api.services.enhanced_voice import EnhancedVoiceService
voice = EnhancedVoiceService()
voice.speak('Hej! Jag är JARVIS med en manlig svensk röst.')
import time
time.sleep(5)
"
```

### 2. Testa via API
```bash
# Starta JARVIS server
cd /home/bjorn/Skrivbord/Jarvis
source jarvis/bin/activate
python -m api.main

# I en annan terminal:
curl -X POST "http://localhost:8080/api/voice/speak" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hej! Nu har jag en mycket bättre svensk röst. Vad tycker du?", "priority": 1}'
```

### 3. Kontrollera tillgängliga röster
```bash
curl http://localhost:8080/api/voice/voices
```

## Röstinställningar

Du kan ändra röst via API:
```bash
# Byta till kvinnlig röst
curl -X POST "http://localhost:8080/api/voice/settings" \
     -H "Content-Type: application/json" \
     -d '{
       "voice_name": "sv-SE-SofieNeural",
       "language": "sv-SE",
       "rate": 180,
       "volume": 0.9
     }'

# Tillbaka till manlig röst (standard)
curl -X POST "http://localhost:8080/api/voice/settings" \
     -H "Content-Type: application/json" \
     -d '{
       "voice_name": "sv-SE-MattiasNeural",
       "language": "sv-SE",
       "rate": 180,
       "volume": 0.9
     }'
```

## Felsökning

### Inget ljud
1. Kontrollera att högtalare fungerar: `speaker-test`
2. Kontrollera systemets TTS: `spd-say "test"`
3. Kontrollera Edge TTS installation: `edge-tts --list-voices | grep sv-SE`

### Edge TTS installation
Om Edge TTS inte installeras automatiskt:
```bash
cd /home/bjorn/Skrivbord/Jarvis
source jarvis/bin/activate
pip install edge-tts
```

### Pygame audio-problem
```bash
sudo apt update
sudo apt install python3-pygame libsdl2-mixer-2.0-0
```

## Kommando för snabbstart

Lägg till i din `.bashrc`:
```bash
alias jarvis-voice-test='cd /home/bjorn/Skrivbord/Jarvis && source jarvis/bin/activate && python -c "from api.services.enhanced_voice import EnhancedVoiceService; voice = EnhancedVoiceService(); voice.speak(\"JARVIS är nu redo med manlig svensk röst\")"'
```

Sedan kan du testa med: `jarvis-voice-test`
