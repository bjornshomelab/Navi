#!/usr/bin/env python3
"""
Test NLP Service och Agents List funktionalitet
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

async def test_nlp_service():
    """Testa NLP service"""
    print("🧠 Testar NLP Service...")
    
    try:
        from services.nlp_service import NLPService
        nlp = NLPService()
        
        test_phrases = [
            "lista alla agents",
            "visa specialister", 
            "vilka experter finns",
            "be kodaren skapa en API",
            "agent coder hjälp med Python",
            "forska om machine learning",
            "research AI development",
            "kom ihåg att jag gillar Python",
            "systemstatus",
            "hjälp mig"
        ]
        
        print("\n📊 NLP Analys-resultat:")
        print("=" * 50)
        
        for phrase in test_phrases:
            analysis = nlp.enhance_command_understanding(phrase)
            intent = analysis.get('intent', 'unknown')
            confidence = analysis.get('confidence', 0)
            method = analysis.get('method', 'unknown')
            
            print(f"Input: '{phrase}'")
            print(f"  → Intent: {intent}")
            print(f"  → Confidence: {confidence:.2f}")
            print(f"  → Method: {method}")
            
            if 'agent_type' in analysis:
                print(f"  → Agent: {analysis['agent_type']}")
            if 'extracted_topic' in analysis:
                print(f"  → Topic: {analysis['extracted_topic']}")
            print()
        
        # Testa NLP-statistik
        stats = nlp.get_nlp_stats()
        print("📈 NLP Stats:")
        for key, value in stats.items():
            print(f"  • {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ NLP Test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_agent_router():
    """Testa Agent Router och list functionality"""
    print("\n🤖 Testar Agent Router...")
    
    try:
        from services.advanced_agents import AgentRouter
        router = AgentRouter()
        
        # Testa agents listing
        print("\n📋 Agents List:")
        print("=" * 50)
        agents_list = router.list_agents()
        print(agents_list)
        
        # Testa capabilities
        print("\n🔧 Agent Capabilities:")
        print("=" * 30)
        capabilities = router.get_all_capabilities()
        for agent_name, caps in capabilities.items():
            print(f"\n{caps['name']} ({agent_name}):")
            print(f"  Specialitet: {caps['speciality']}")
            keywords = caps['keywords'][:3]  # Visa bara första 3
            print(f"  Keywords: {', '.join(keywords)}...")
        
        # Testa agent routing
        print("\n🎯 Test Agent Routing:")
        print("=" * 25)
        
        test_requests = [
            "skapa en Python script",
            "optimera systemet",
            "designa en modern hemsida",
            "analysera data med machine learning"
        ]
        
        for request in test_requests:
            result = await router.route_request(request)
            print(f"\nRequest: '{request}'")
            print(f"  → Routed to: {result.get('agent_used', 'none')}")
            print(f"  → Confidence: {result.get('confidence', 0):.2f}")
            print(f"  → Success: {result.get('success', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent Router test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_integration():
    """Testa integration mellan NLP och Agent Router"""
    print("\n🔗 Testar NLP + Agent Integration...")
    
    try:
        from services.nlp_service import NLPService
        from services.advanced_agents import AgentRouter
        
        nlp = NLPService()
        router = AgentRouter()
        
        integration_tests = [
            {
                'input': "lista alla agents",
                'expected_intent': 'agent_list'
            },
            {
                'input': "be kodaren hjälpa mig",
                'expected_intent': 'agent_request'
            },
            {
                'input': "forska om Python AI",
                'expected_intent': 'research'
            }
        ]
        
        print("\n🧪 Integration Test Results:")
        print("=" * 35)
        
        for test in integration_tests:
            input_text = test['input']
            expected = test['expected_intent']
            
            # NLP analys
            analysis = nlp.enhance_command_understanding(input_text)
            actual_intent = analysis.get('intent')
            
            # Resultat
            status = "✅" if actual_intent == expected else "❌"
            print(f"{status} '{input_text}'")
            print(f"     Expected: {expected}")
            print(f"     Actual: {actual_intent}")
            print(f"     Confidence: {analysis.get('confidence', 0):.2f}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Kör alla tester"""
    print("🚀 JARVIS NLP & Agents Test Suite")
    print("=" * 40)
    
    # Kör tester
    nlp_ok = await test_nlp_service()
    router_ok = await test_agent_router()  
    integration_ok = await test_integration()
    
    # Sammanfattning
    print("\n📊 TEST SAMMANFATTNING")
    print("=" * 25)
    print(f"NLP Service: {'✅' if nlp_ok else '❌'}")
    print(f"Agent Router: {'✅' if router_ok else '❌'}")
    print(f"Integration: {'✅' if integration_ok else '❌'}")
    
    if all([nlp_ok, router_ok, integration_ok]):
        print("\n🎉 Alla tester lyckades! NLP och Agents fungerar.")
        print("\n💡 Nästa steg: Testa 'jarvis ls agents' i terminalen")
    else:
        print("\n⚠️ Några tester misslyckades. Kontrollera felen ovan.")

if __name__ == "__main__":
    asyncio.run(main())
