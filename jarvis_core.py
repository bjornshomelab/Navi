#!/usr/bin/env python3
"""
JARVIS Core - Terminal AI Agent
Simplified, powerful AI assistant focused on intelligence, not interface
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

class JarvisCore:
    """Core JARVIS Terminal AI Agent"""
    
    def __init__(self):
        self.session_id = f"core_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_id = "bjorn"
        self.conversation_history = []
        
        # Initialize services (without voice/GUI)
        self.setup_services()
        
        print("🤖 JARVIS Core - Terminal AI Agent")
        print("🎯 Fokuserad på intelligens och automation")
        print("💬 Skriv 'help' för kommandon, 'exit' för att avsluta\n")
    
    def setup_services(self):
        """Initialize core services without voice/GUI"""
        try:
            # Import core services
            from services.enhanced_research import EnhancedResearchService
            from services.memory import AdvancedMemoryService
            from services.self_improvement import SelfImprovementService
            from services.enhanced_local_agent import EnhancedLocalAgentService
            
            self.research = EnhancedResearchService()
            self.memory = AdvancedMemoryService()
            self.self_improvement = SelfImprovementService()
            self.local_agent = EnhancedLocalAgentService()
            
            print("✅ Core services initialized")
            
        except ImportError as e:
            print(f"⚠️ Some services not available: {e}")
            self.research = None
            self.memory = None
            self.self_improvement = None
            self.local_agent = None
    
    async def process_command(self, user_input: str) -> str:
        """Process user command and return response"""
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'type': 'user_input'
        })
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit', 'bye']:
            return "👋 Hej då! JARVIS Core avslutas."
        
        elif user_input.lower() in ['help', 'hjälp']:
            return self.get_help()
        
        elif user_input.lower().startswith('research ') or user_input.lower().startswith('forskning '):
            topic = user_input.split(' ', 1)[1] if ' ' in user_input else ""
            return await self.handle_research(topic)
        
        elif user_input.lower().startswith('memory ') or user_input.lower().startswith('minne '):
            query = user_input.split(' ', 1)[1] if ' ' in user_input else ""
            return await self.handle_memory(query)
        
        elif user_input.lower().startswith('learn ') or user_input.lower().startswith('lär '):
            info = user_input.split(' ', 1)[1] if ' ' in user_input else ""
            return await self.handle_learning(info)
        
        elif user_input.lower().startswith('system ') or user_input.lower().startswith('local '):
            command = user_input.split(' ', 1)[1] if ' ' in user_input else ""
            return await self.handle_system_command(command)
        
        else:
            # General AI conversation
            return await self.handle_general_query(user_input)
    
    async def handle_research(self, topic: str) -> str:
        """Handle research requests"""
        if not self.research:
            return "❌ Research service inte tillgänglig"
        
        if not topic:
            return "🔬 Vad vill du att jag ska forska om?"
        
        print(f"🔬 Startar research om: {topic}")
        
        try:
            results = await self.research.comprehensive_research(topic, depth='medium')
            
            response = f"🔬 Research om '{topic}' klar!\n\n"
            
            if 'insights' in results:
                response += "💡 Viktiga insikter:\n"
                for insight in results['insights'][:3]:
                    response += f"• {insight.get('description', 'N/A')}\n"
            
            if 'recommendations' in results:
                response += "\n🎯 Rekommendationer:\n"
                for rec in results['recommendations'][:3]:
                    response += f"• {rec.get('description', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Research-fel: {e}"
    
    async def handle_memory(self, query: str) -> str:
        """Handle memory queries"""
        if not self.memory:
            return "❌ Memory service inte tillgänglig"
        
        if not query:
            recent = self.memory.get_recent_memories(limit=5)
            if recent:
                response = "🧠 Senaste minnen:\n"
                for memory in recent:
                    response += f"• {memory.get('content', 'N/A')}\n"
                return response
            else:
                return "🧠 Inga minnen sparade än"
        
        # Search memories
        results = self.memory.search_memories(query)
        if results:
            response = f"🧠 Hittade {len(results)} minnen om '{query}':\n"
            for memory in results[:5]:
                response += f"• {memory.get('content', 'N/A')}\n"
            return response
        else:
            return f"🧠 Inga minnen hittades om '{query}'"
    
    async def handle_learning(self, info: str) -> str:
        """Handle learning new information"""
        if not self.memory:
            return "❌ Memory service inte tillgänglig"
        
        if not info:
            return "🧠 Vad vill du att jag ska lära mig?"
        
        try:
            self.memory.add_memory(
                content=info,
                memory_type="personal_fact",
                user_id=self.user_id,
                metadata={"source": "user_input", "session": self.session_id}
            )
            return f"🧠 Lärt mig: {info}\n💡 Jag kommer komma ihåg detta!"
            
        except Exception as e:
            return f"❌ Kunde inte spara minne: {e}"
    
    async def handle_system_command(self, command: str) -> str:
        """Handle local system commands"""
        if not self.local_agent:
            return "❌ Local agent service inte tillgänglig"
        
        if not command:
            return "⚙️ Vad vill du att jag ska göra på systemet?"
        
        try:
            print(f"⚙️ Kör system-kommando: {command}")
            result = await self.local_agent.execute_enhanced_command(command)
            
            if result.get('success'):
                response = f"✅ {result.get('message', 'Kommando utfört')}"
                if result.get('data'):
                    response += f"\n📊 Data: {result['data']}"
                return response
            else:
                return f"❌ {result.get('error', 'Kommando misslyckades')}"
                
        except Exception as e:
            return f"❌ System-fel: {e}"
    
    async def handle_general_query(self, query: str) -> str:
        """Handle general AI conversation"""
        
        # Simple AI response for now - can be enhanced with actual AI model
        response = f"🤖 Du frågade: '{query}'\n\n"
        response += "💭 Jag analyserar din fråga... \n"
        
        # Add some intelligence based on keywords
        keywords = query.lower().split()
        
        if any(word in keywords for word in ['tid', 'klocka', 'datum']):
            response += f"🕒 Aktuell tid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        elif any(word in keywords for word in ['väder', 'weather']):
            response += "🌤️ För väderinformation, kör: research väder Stockholm"
        
        elif any(word in keywords for word in ['status', 'system']):
            response += "💻 För systemstatus, kör: system status"
        
        else:
            response += "💡 Prova att använda specifika kommandon som:\n"
            response += "• research [ämne] - för forskning\n"
            response += "• learn [fakta] - för att lära mig något\n"
            response += "• memory [sök] - för att söka minnen\n"
            response += "• system [kommando] - för systemoperationer"
        
        return response
    
    def get_help(self) -> str:
        """Return help information"""
        help_text = """
🤖 JARVIS Core - Kommandon

📚 CORE KOMMANDON:
• research [ämne]     - Starta djup forskning om ett ämne
• learn [fakta]       - Lär JARVIS något nytt om dig/systemet  
• memory [sök]        - Sök i JARVIS minne eller visa senaste
• system [kommando]   - Kör lokala system-operationer

💬 CONVERSATION:
• Ställ frågor naturligt på svenska
• JARVIS kommer ihåg konversationshistorik
• Använd 'exit' för att avsluta

🔧 SYSTEM EXEMPEL:
• system status       - Visa systemstatus
• system backup       - Backup viktiga filer
• system organize     - Organisera filer automatiskt

🧠 LEARNING EXEMPEL:  
• learn "Björn jobbar bäst på kvällar"
• learn "Favoritprogrammering språk är Python"
• learn "Projektmapp finns i ~/kod/"

🔬 RESEARCH EXEMPEL:
• research "Python AI development 2025"
• research "Linux automation tools"
• research "Productivity tips for developers"

💡 Tips: JARVIS lär sig av varje interaktion och blir smartare över tid!
        """
        return help_text.strip()
    
    def run(self):
        """Main conversation loop"""
        try:
            while True:
                # Get user input
                try:
                    user_input = input("💬 Du: ").strip()
                except KeyboardInterrupt:
                    print("\n👋 JARVIS Core avslutas...")
                    break
                
                if not user_input:
                    continue
                
                # Process command
                try:
                    response = asyncio.run(self.process_command(user_input))
                    print(f"\n🤖 JARVIS: {response}\n")
                    
                    # Add response to history
                    self.conversation_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'assistant': response,
                        'type': 'assistant_response'
                    })
                    
                    # Exit if requested
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        break
                        
                except Exception as e:
                    print(f"\n❌ Fel: {e}\n")
                    
        except Exception as e:
            print(f"❌ Kritiskt fel: {e}")

def main():
    """Entry point"""
    try:
        # Change to project directory
        os.chdir(Path(__file__).parent)
        
        # Start JARVIS Core
        jarvis = JarvisCore()
        jarvis.run()
        
    except KeyboardInterrupt:
        print("\n👋 JARVIS Core avslutas...")
    except Exception as e:
        print(f"❌ Startup fel: {e}")

if __name__ == "__main__":
    main()
