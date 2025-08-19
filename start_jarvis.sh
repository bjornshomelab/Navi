#!/bin/bash
# JARVIS Startup Script
# Starts API server and optionally GUI with wake word detection

echo "🛰️  Starting JARVIS AI Agent..."

# Change to JARVIS directory
cd ~/Skrivbord/Jarvis

# Activate virtual environment
source jarvis/bin/activate

# Check if GUI flag is provided
if [ "$1" = "--gui" ] || [ "$1" = "-g" ]; then
    echo "🖥️  Starting with GUI..."
    
    # Start API server in background
    echo "📡 Starting API server..."
    python start_jarvis.py &
    API_PID=$!
    
    # Wait for API to start
    sleep 3
    
    # Start GUI
    echo "🎨 Starting GUI..."
    python gui/launcher.py
    
    # Kill API server when GUI closes
    kill $API_PID 2>/dev/null
    
elif [ "$1" = "--wake-word" ] || [ "$1" = "-w" ]; then
    echo "👂 Starting with wake word detection..."
    
    # Start API server in background
    echo "📡 Starting API server..."
    python start_jarvis.py &
    API_PID=$!
    
    # Wait for API to start
    sleep 3
    
    # Start wake word detection
    echo "🎤 Starting wake word detection..."
    curl -X POST "http://localhost:8081/api/command/wake-word/start" >/dev/null 2>&1
    
    echo "✅ JARVIS is ready! Say 'Hey Jarvis' to activate."
    echo "💡 Press Ctrl+C to stop"
    
    # Keep script running
    trap 'echo "🛑 Stopping JARVIS..."; curl -X POST "http://localhost:8081/api/command/wake-word/stop" >/dev/null 2>&1; kill $API_PID 2>/dev/null; exit' INT
    wait $API_PID
    
else
    echo "📡 Starting API server only..."
    python start_jarvis.py
fi
