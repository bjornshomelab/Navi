#!/usr/bin/env python3
"""
Test Enhanced Voice Service for JARVIS
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_voice_service():
    print("🎤 Testar Enhanced Voice Service...")
    
    try:
        from api.services.enhanced_voice import EnhancedVoiceService
        print("✅ Import lyckades")
        
        # Initialize service
        voice = EnhancedVoiceService()
        print("✅ Voice service initialiserad")
        
        # Get status
        status = voice.get_status()
        print(f"📊 {len(status['engines'])} TTS-motorer tillgängliga:")
        
        for i, engine in enumerate(status['engines']):
            marker = "🎯" if i == 0 else "  "
            print(f"{marker} {engine['name']}: {engine['description']} ({engine['quality']} kvalitet)")
            print(f"    Röster: {', '.join(engine['voices'])}")
        
        if status['engines']:
            print(f"\n🔊 Testar primär motor: {status['engines'][0]['name']}")
            voice.speak("Hej! Jag är JARVIS med en förbättrad naturlig svensk röst.")
            
            import time
            print("⏳ Väntar på att rösten ska spela...")
            time.sleep(6)
            print("✅ Test slutförd!")
        else:
            print("❌ Inga TTS-motorer tillgängliga")
            
    except Exception as e:
        print(f"❌ Fel: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voice_service()
