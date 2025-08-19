#!/usr/bin/env python3
"""
Test script för JARVIS Agent System
"""

import sys
import asyncio
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

from services.advanced_agents import AgentRouter

async def test_agents():
    """Testa alla agents"""
    print("🤖 Testing JARVIS Agent System...\n")
    
    # Initialize router
    router = AgentRouter()
    
    # Test 1: Lista alla agents
    print("📋 Test 1: Lista alla agents")
    agent_list = router.list_agents()
    print(agent_list)
    print("\n" + "="*80 + "\n")
    
    # Test 2: Testa coder agent
    print("💻 Test 2: Coder Agent")
    result = await router.direct_agent_request("coder", "skapa en enkel Python Flask API")
    print(f"Success: {result.get('success')}")
    if 'code' in result:
        print(f"Generated {result.get('language')} code:")
        print(result['code'][:200] + "..." if len(result['code']) > 200 else result['code'])
    print("\n" + "="*80 + "\n")
    
    # Test 3: Testa university tutor
    print("📚 Test 3: University Tutor Agent")
    result = await router.direct_agent_request("university_tutor", "förklara vad en derivata är")
    print(f"Success: {result.get('success')}")
    if 'explanation' in result:
        print("Generated explanation:")
        print(result['explanation'][:300] + "..." if len(result['explanation']) > 300 else result['explanation'])
    print("\n" + "="*80 + "\n")
    
    # Test 4: Testa study coach
    print("🎯 Test 4: Study Coach Agent")
    result = await router.direct_agent_request("study_coach", "jag prokrastinerar och behöver hjälp")
    print(f"Success: {result.get('success')}")
    if 'anti_procrastination_guide' in result:
        print("Generated coaching advice:")
        print(result['anti_procrastination_guide'][:300] + "..." if len(result['anti_procrastination_guide']) > 300 else result['anti_procrastination_guide'])
    print("\n" + "="*80 + "\n")
    
    # Test 5: Automatisk routing
    print("🔀 Test 5: Automatisk Agent Routing")
    queries = [
        "designa en modern CSS layout",
        "hur optimerar jag mitt Linux system?",
        "skapa en machine learning modell",
        "jag har ingen motivation att studera"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        result = await router.route_request(query)
        print(f"Routed to: {result.get('agent_name', 'None')} (confidence: {result.get('confidence', 0):.2f})")
        print(f"Success: {result.get('success')}")
    
    print("\n🎉 Agent testing complete!")

if __name__ == "__main__":
    asyncio.run(test_agents())
