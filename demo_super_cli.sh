#!/bin/bash
"""
🚀 JARVIS SUPER CLI DEMO
Demo av alla YAI-inspirerade funktioner med JARVIS superkrafter
"""

echo "🚀 JARVIS SUPER CLI DEMO"
echo "======================="
echo "En superdopad version av YAI med specialiserade AI-agents!"
echo

# Set up aliases
JARVIS="python /home/bjorn/Skrivbord/Jarvis/jarvis_cli.py"

echo "📋 DEMO 1: YAI-Style Exec Mode - Command Generation"
echo "=================================================="
echo "💻 Kommando: jarvis -e 'list all docker containers'"
$JARVIS -e "list all docker containers"
echo
echo "💻 Kommando: jarvis -e 'find large files in home directory'"  
$JARVIS -e "find large files in home directory"
echo
echo "💻 Kommando: jarvis -e 'show git status and recent commits'"
$JARVIS -e "show git status and recent commits"
echo

echo "📋 DEMO 2: Enhanced Chat Mode - AI Conversation"
echo "=============================================="
echo "💬 Kommando: jarvis -c 'hello'"
$JARVIS -c "hello"
echo
echo "💬 Kommando: jarvis -c 'explain machine learning in simple terms'"
$JARVIS -c "explain machine learning in simple terms"
echo

echo "📋 DEMO 3: Specialized Agent Mode - AI Superpowers"
echo "================================================="
echo "🤖 Kommando: jarvis -a coder 'create a simple Python function'"
$JARVIS -a coder "create a simple Python function"
echo
echo "🤖 Kommando: jarvis -a tutor 'explain derivatives in calculus'"
$JARVIS -a tutor "explain derivatives in calculus"
echo
echo "🤖 Kommando: jarvis -a coach 'help me stop procrastinating'"
$JARVIS -a coach "help me stop procrastinating"
echo

echo "📋 DEMO 4: YAI-Style Piping Support"
echo "=================================="
echo "🔧 Kommando: echo 'some error data' | jarvis -c 'analyze this'"
echo "some error data" | $JARVIS -c "analyze this"
echo
echo "🔧 Kommando: ps aux | head -5 | jarvis -c 'explain these processes'"
ps aux | head -5 | $JARVIS -c "explain these processes"
echo

echo "📋 DEMO 5: JSON Output för Scripting"
echo "===================================="
echo "📊 Kommando: jarvis -e 'list files' --json"
$JARVIS -e "list files" --json
echo

echo "📋 DEMO 6: Agent Capabilities Overview"
echo "===================================="
echo "🤖 Tillgängliga specialiserade agents:"
echo
echo "💻 Coder Agent - Programmering och utveckling"
echo "🔧 System Agent - Systemadministration"  
echo "📊 Data Scientist - Dataanalys och ML"
echo "🎨 Designer - UI/UX och grafik"
echo "✍️ Content Creator - Skrivande och marknadsföring"
echo "📚 University Tutor - Akademisk hjälp"
echo "🎯 Study Coach - Motivation och produktivitet"
echo "📖 Document Analyst - PDF-analys och studieplaner"
echo

echo "🎉 DEMO SLUTFÖRD!"
echo "================"
echo "JARVIS SUPER CLI kombinerar:"
echo "✅ YAI:s eleganta kommando-generering"
echo "✅ Kraftfulla specialiserade AI-agents"  
echo "✅ Avancerad dokumentanalys"
echo "✅ Piping och scripting support"
echo "✅ Interaktiv REPL-mode"
echo
echo "🚀 Nästa steg: Starta REPL med 'jarvis --repl'"
echo "💡 Fullständig dokumentation: JARVIS_SUPER_CLI.md"
