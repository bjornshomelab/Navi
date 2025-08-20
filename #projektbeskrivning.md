🛰 Projekt: NAVI – Din Personliga AI-Agent
🎯 Vision

Bygga en AI-agent som bor i ditt system och lever i molnet, men kan nås via dator, iPhone och röst.
NAVI ska kunna förstå dig, utföra handlingar, växa över tid och alltid minnas din kontext.

⚙️ Arkitektur
            [ Du / Siri / Terminal ]
                       │
            (Röst/Text Input)
                       │
                 ┌───────────┐
                 │   Client  │
   (CLI på datorn, iPhone Shortcut, Web-App)
                 └─────┬─────┘
                       │ REST/WebSocket
                       ▼
                ┌─────────────┐
                │  NAVI API │   (hostad i Cloud Run)
                └──────┬──────┘
                       │
         ┌─────────────┼───────────────────────────────┐
         │             │                               │
 [Google API]     [Lokalt på datorn]           [Minne/Databas]
 - Gemini         - CLI actions                - Firestore (struktur)
 - Calendar       - Skärmstyrning              - Vector DB (semantik)
 - Gmail          - Filsystem                  - Logs (BigQuery ev.)
 - Drive          - Terminal
 - STT / TTS      - Web automation
 - Vision

🔑 Huvudmoduler
1. NAVI API (Cloud Run)

Backend i Python (FastAPI)

Pratar med:

Gemini API för resonemang

STT/TTS API för röst

Gmail/Calendar/Drive API för produktivitet

Exponerar endpoints:

/command – ta emot röst/text-kommandon

/memory – lagra/hämta minne

/actions – koordinera lokala eller cloud actions

2. Minne

Långtidsminne: Firestore + VectorDB (Chroma/Weaviate)

Korttidsminne: session i Gemini API

Loggar allt i BigQuery för analys.

3. Lokala actions (på datorn)

En liten agent-client i Python som:

Tar kommandon från NAVI API.

Kan: klicka (pyautogui/ydotool), skriva, öppna appar, läsa filer.

Returnerar resultat tillbaka till molnet.

4. iPhone-integration

Snabbaste vägen: Siri Shortcut → skickar text/röst till NAVI API.

Nästa steg: liten Web-App (PWA) med chatt + röst.

Slutmål: dedikerad iOS-app (Flutter/Swift).

5. Gränssnitt

Terminal CLI:

navi "öppna senaste mejlet från Anna"



Voice (på datorn):

Hotword “Hey Navi”

Mikrofon → STT → NAVI API → TTS tillbaka.

iPhone:

Siri Shortcut eller app.

📅 Roadmap (MVP → Jarvis 1.0)
🚀 Steg 1 – MVP (2–3 veckor)

Cloud Run service (FastAPI)

Gemini API integrerat

Terminal CLI på datorn

Jarvis kan: svara på frågor, läsa kalender, hämta mejl

🌐 Steg 2 – Multi-interface (månad 2)

Lägg till STT/TTS via Google API

Siri Shortcut till Cloud Run

Jarvis svarar via röst både på dator och iPhone

🤖 Steg 3 – Kropp (månad 3–4)

Agent-client på datorn: kan klicka, öppna appar, läsa filer

Jarvis kan “bo” i datorn och interagera med UI

🧬 Steg 4 – Minne & Växande (månad 4–6)

Firestore + VectorDB för långtidsminne

Dagbok/loggfunktion

Jarvis lär sig preferenser och förbättrar beteende

✨ Steg 5 – Jarvis 1.0

En enhetlig assistent: samma minne och hjärna

Tillgänglig via CLI, voice, iPhone-app

Kan resonera, minnas, agera både i molnet och lokalt

NAVI är nästa generations AI-assistent, byggd för lokal integritet och kraftfull AI.