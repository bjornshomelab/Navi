#!/usr/bin/env python3
"""
JARVIS Röstdemo - Visar skillnaden mellan manlig och kvinnlig svensk röst
"""
import time
import sys
import os

# Lägg till projektets root till Python path
sys.path.append('/home/bjorn/Skrivbord/Jarvis')

from api.services.enhanced_voice import EnhancedVoiceService

def demo_voices():
    """Demonstrera olika svenska röster"""
    print("🎤 JARVIS Röstdemo - Svenska röster")
    print("=" * 50)
    
    # Skapa röstservice
    voice = EnhancedVoiceService()
    
    # Visa tillgängliga röster
    print("\n📋 Tillgängliga röster:")
    voices = voice.get_voices()
    for i, v in enumerate(voices[:5], 1):  # Visa bara de första 5
        print(f"  {i}. {v['name']} ({v['engine']}) - {v['quality']} kvalitet")
    
    # Test 1: Manlig röst (standard)
    print(f"\n🎯 Test 1: Manlig röst (Standard)")
    voice.set_voice('sv-SE-MattiasNeural')
    voice.speak("Hej! Jag är JARVIS med en djup manlig svensk röst. Jag låter professionell och tydlig.")
    print("🔊 Spelar manlig röst...")
    time.sleep(6)
    
    # Test 2: Kvinnlig röst
    print(f"\n🎯 Test 2: Kvinnlig röst")
    voice.set_voice('sv-SE-SofieNeural')
    voice.speak("Hej! Nu talar jag med en mjuk kvinnlig svensk röst. Vilken röst föredrar du?")
    print("🔊 Spelar kvinnlig röst...")
    time.sleep(6)
    
    # Test 3: Tillbaka till manlig
    print(f"\n🎯 Test 3: Tillbaka till manlig röst")
    voice.set_voice('sv-SE-MattiasNeural')
    voice.speak("Nu är jag tillbaka med den manliga rösten. Denna är nu standardinställningen för JARVIS.")
    print("🔊 Spelar manlig röst igen...")
    time.sleep(6)
    
    # Avsluta
    voice.shutdown()
    print("\n✅ Röstdemo slutförd!")
    print("💡 För att ändra röst permanent, uppdatera enhanced_voice.py")

if __name__ == "__main__":
    try:
        demo_voices()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo avbruten av användare")
    except Exception as e:
        print(f"\n❌ Fel under demo: {e}")
