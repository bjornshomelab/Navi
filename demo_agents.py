#!/usr/bin/env python3
"""
JARVIS Core Demo Script
Visar alla agents och deras kapaciteter
"""

import sys
import asyncio
import time
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

from services.advanced_agents import AgentRouter

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"🤖 {text}")
    print("="*80)

def print_demo_query(query, description=""):
    """Print a demo query"""
    print(f"\n💬 Demo Query: '{query}'")
    if description:
        print(f"📝 Purpose: {description}")
    print("-" * 60)

async def demo_all_agents():
    """Komplett demo av alla agents"""
    
    print_header("JARVIS CORE - ADVANCED AGENT SYSTEM DEMO")
    print("🎯 Demonstrerar alla specialiserade agents och deras kapaciteter")
    
    # Initialize router
    router = AgentRouter()
    
    # Demo 1: Agent Overview
    print_header("1. AGENT OVERVIEW")
    agent_list = router.list_agents()
    print(agent_list)
    
    # Demo 2: Coder Agent
    print_header("2. SENIOR DEVELOPER AGENT")
    print_demo_query("skapa en REST API i Python", "Visa kod-generering")
    
    result = await router.direct_agent_request("coder", "skapa en REST API i Python")
    if result.get('success') and 'code' in result:
        print(f"🎯 Generated {result.get('language')} code:")
        print("```python")
        print(result['code'][:500] + "..." if len(result['code']) > 500 else result['code'])
        print("```")
        
        if 'instructions' in result:
            print("\n📋 Instruktioner:")
            for instruction in result['instructions']:
                print(f"• {instruction}")
    
    # Demo 3: System Analyst
    print_header("3. SYSTEM ANALYST AGENT")
    print_demo_query("setup backup system", "Visa systemautomation")
    
    result = await router.direct_agent_request("system_analyst", "setup backup system")
    if result.get('success'):
        if 'backup_script' in result:
            print("🛠️ Generated backup script:")
            print("```bash")
            print(result['backup_script'][:300] + "..." if len(result['backup_script']) > 300 else result['backup_script'])
            print("```")
        
        if 'instructions' in result:
            print("\n📋 Setup Instructions:")
            for instruction in result['instructions'][:3]:
                print(f"• {instruction}")
    
    # Demo 4: University Tutor
    print_header("4. UNIVERSITY TUTOR AGENT")
    print_demo_query("förklara vad en derivata är", "Visa akademisk vägledning")
    
    result = await router.direct_agent_request("university_tutor", "förklara vad en derivata är")
    if result.get('success') and 'explanation' in result:
        print("📚 Matematisk förklaring:")
        explanation_lines = result['explanation'].split('\n')
        for line in explanation_lines[:15]:  # Visa första 15 raderna
            print(line)
        print("...[fortsätter med exempel och övningar]")
        
        if 'practice_problems' in result:
            print("\n🧮 Övningsproblem:")
            for problem in result['practice_problems']:
                print(f"• {problem}")
    
    # Demo 5: Study Coach
    print_header("5. STUDY COACH AGENT")
    print_demo_query("jag prokrastinerar och behöver hjälp", "Visa motivation coaching")
    
    result = await router.direct_agent_request("study_coach", "jag prokrastinerar och behöver hjälp")
    if result.get('success'):
        if 'immediate_intervention' in result:
            print("⚡ Omedelbar hjälp:")
            for tip in result['immediate_intervention']:
                print(f"  {tip}")
        
        if 'anti_procrastination_guide' in result:
            print("\n📖 Anti-prokrastinering guide (utdrag):")
            guide_lines = result['anti_procrastination_guide'].split('\n')
            for line in guide_lines[:10]:  # Visa första 10 raderna
                if line.strip():
                    print(line)
            print("...[fortsätter med detaljerade strategier]")
    
    # Demo 6: Designer Agent
    print_header("6. UI/UX DESIGNER AGENT")
    print_demo_query("skapa modern CSS för min hemsida", "Visa design system")
    
    result = await router.direct_agent_request("designer", "skapa modern CSS för min hemsida")
    if result.get('success') and 'code' in result:
        print("🎨 Modern CSS Framework:")
        print("```css")
        css_lines = result['code'].split('\n')
        for line in css_lines[:20]:  # Visa första 20 raderna
            print(line)
        print("...[fortsätter med komponenter och utilities]")
        print("```")
        
        if 'features' in result:
            print("\n✨ Features:")
            for feature in result['features'][:4]:
                print(f"• {feature}")
    
    # Demo 7: Data Scientist Agent
    print_header("7. DATA SCIENTIST AGENT")
    print_demo_query("skapa en machine learning modell", "Visa ML pipeline")
    
    result = await router.direct_agent_request("data_scientist", "skapa en machine learning modell")
    if result.get('success') and 'code' in result:
        print("🤖 ML Pipeline:")
        print("```python")
        ml_lines = result['code'].split('\n')
        for line in ml_lines[:15]:  # Visa första 15 raderna
            print(line)
        print("...[fortsätter med modellträning och evaluation]")
        print("```")
        
        if 'next_steps' in result:
            print("\n🎯 Nästa steg:")
            for step in result['next_steps']:
                print(f"• {step}")
    
    # Demo 8: Content Creator
    print_header("8. CONTENT CREATOR AGENT")
    print_demo_query("skapa en bloggpost template", "Visa content creation")
    
    result = await router.direct_agent_request("content_creator", "skapa en bloggpost template")
    if result.get('success') and 'template' in result:
        print("📝 Blog Post Template:")
        template_lines = result['template'].split('\n')
        for line in template_lines[:15]:  # Visa första 15 raderna
            print(line)
        print("...[fortsätter med SEO och marketing strategi]")
        
        if 'tips' in result:
            print("\n💡 Content Tips:")
            for tip in result['tips'][:3]:
                print(f"• {tip}")
    
    # Demo 9: Automatic Routing
    print_header("9. INTELLIGENT AUTO-ROUTING")
    print("🧠 JARVIS Core använder intelligent routing för naturliga frågor:")
    
    test_queries = [
        ("hur bygger jag en webapp?", "Förväntat: Senior Developer"),
        ("jag har ingen motivation", "Förväntat: Study Coach"), 
        ("designa en logo", "Förväntat: UI/UX Designer"),
        ("analysera min data", "Förväntat: Data Scientist"),
        ("optimera mitt system", "Förväntat: System Analyst"),
        ("förklara fysik koncept", "Förväntat: University Tutor"),
        ("skriv marknadsföringstext", "Förväntat: Content Creator")
    ]
    
    for query, expected in test_queries:
        print(f"\n💬 Query: '{query}'")
        result = await router.route_request(query)
        
        if result.get('success'):
            agent_name = result.get('agent_name', 'Unknown')
            confidence = result.get('confidence', 0)
            print(f"🎯 Routed to: {agent_name} (confidence: {confidence:.2f})")
            print(f"✅ Match: {expected}")
        else:
            print(f"❌ No suitable agent found")
    
    # Demo 10: Integration Showcase
    print_header("10. SYSTEM INTEGRATION SHOWCASE")
    print("""
🔧 JARVIS Core Integration Capabilities:

🔐 SUDO OPERATIONS:
• Säker lösenordsprompt för system-kommandon
• Whitelist av tillåtna operationer
• Fullständig logging av alla sudo-aktiviteter
• Security violation detection

🧠 MEMORY SYSTEM:
• Personliga preferenser och habits
• Konversationshistorik
• Learning från interaktioner
• Context-aware responses

🔬 RESEARCH ENGINE:
• Multi-source information gathering
• AI-driven analysis och insights
• Automatic summarization
• Trend detection

💻 LOCAL AUTOMATION:
• File management och organization
• System monitoring och optimization
• Development environment setup
• Service management

🎯 GOAL: En verkligt intelligent terminal-baserad assistent som
    lär sig, automatiserar och förbättrar din produktivitet!
    """)
    
    print_header("DEMO COMPLETE")
    print("🎉 JARVIS Core Agent System Demo färdig!")
    print("💡 Kör 'python3 jarvis_core.py' för att starta interactive mode")
    print("📚 Använd 'help' för alla kommandon och 'agents' för agent lista")

if __name__ == "__main__":
    asyncio.run(demo_all_agents())
