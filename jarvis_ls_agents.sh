#!/bin/bash
"""
JARVIS Agents Lister - Snabb kommando för att lista alla agents
"""

# Använd detta script för: jarvis ls agents

cd /home/bjorn/Skrivbord/Jarvis
source jarvis/bin/activate

# Kör Python kommando för att lista agents
python3 -c "
import sys
sys.path.insert(0, 'api')

try:
    from services.advanced_agents import AgentRouter
    router = AgentRouter()
    print(router.list_agents())
except ImportError as e:
    print('❌ Kunde inte ladda Agent Router:', e)
    print('💡 Kör först: source jarvis/bin/activate')
except Exception as e:
    print('❌ Fel:', e)
"
