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
            from services.advanced_agents import AgentRouter
            from services.nlp_service import NLPService
            
            self.research = EnhancedResearchService()
            self.memory = AdvancedMemoryService()
            self.self_improvement = SelfImprovementService()
            self.local_agent = EnhancedLocalAgentService()
            self.agent_router = AgentRouter()
            self.nlp = NLPService()
            
            print("✅ Core services initialized (inkl. NLP)")
            print(f"🤖 Advanced Agent System ready med {len(self.agent_router.agents)} specialister")
            
        except ImportError as e:
            print(f"⚠️ Some services not available: {e}")
            self.research = None
            self.memory = None
            self.self_improvement = None
            self.local_agent = None
            self.agent_router = None
    
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
        
        # NEW: Handle agents listing
        elif user_input.lower() in ['agents', 'agents list', 'ls agents', 'lista agents', 'visa agents']:
            return self.handle_agents_list()
        
        # Use NLP for enhanced command understanding
        elif self.nlp:
            return await self.handle_nlp_command(user_input)
        
        # Fallback to basic command parsing
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
        
        elif user_input.lower().startswith('agent '):
            # Agent system commands
            return await self.handle_agent_command(user_input)
        
        else:
            # General AI conversation (now with agent routing)
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
    
    async def handle_agent_command(self, command: str) -> str:
        """Handle agent system commands"""
        if not self.agent_router:
            return "❌ Agent system inte tillgängligt"
        
        parts = command.split(' ', 2)
        if len(parts) < 3:
            return "❌ Använd: agent <typ> <förfrågan>\n💡 Exempel: agent coder skapa en API"
        
        agent_type = parts[1].lower()
        request = parts[2]
        
        try:
            result = await self.agent_router.direct_agent_request(agent_type, request)
            
            if result.get('success'):
                response = f"🤖 **{result.get('agent_name', 'Agent')}** svarar:\n\n"
                
                # Handle different response types
                if 'code' in result:
                    response += f"💻 **Genererad kod ({result.get('language', 'text')}):**\n"
                    response += f"```{result.get('language', '')}\n{result['code']}\n```\n"
                    
                    if 'description' in result:
                        response += f"\n📝 **Beskrivning:** {result['description']}\n"
                    
                    if 'instructions' in result:
                        response += "\n📋 **Instruktioner:**\n"
                        for instruction in result['instructions']:
                            response += f"• {instruction}\n"
                
                elif 'template' in result:
                    response += f"📄 **{result.get('type', 'Template')}:**\n"
                    response += f"```\n{result['template']}\n```\n"
                    
                    if 'tips' in result:
                        response += "\n💡 **Tips:**\n"
                        for tip in result['tips']:
                            response += f"• {tip}\n"
                
                elif 'message' in result:
                    response += result['message']
                    
                    if 'capabilities' in result:
                        response += "\n\n🔧 **Kapaciteter:**\n"
                        for cap in result['capabilities']:
                            response += f"• {cap}\n"
                
                if 'next_steps' in result:
                    response += "\n🎯 **Nästa steg:**\n"
                    for step in result['next_steps']:
                        response += f"• {step}\n"
                
                return response
            else:
                error_msg = f"❌ {result.get('error', 'Agent-fel')}"
                if 'available_agents' in result:
                    error_msg += f"\n\n🤖 Tillgängliga agents: {', '.join(result['available_agents'])}"
                return error_msg
                
        except Exception as e:
            return f"❌ Agent system fel: {e}"
    
    def list_agents(self) -> str:
        """List all available agents"""
        if not self.agent_router:
            return "❌ Agent system inte tillgängligt"
        
        return self.agent_router.list_agents()
    
    def handle_agents_list(self) -> str:
        """Handle agents listing command"""
        if not self.agent_router:
            return "❌ Agent system inte tillgängligt"
        
        return self.agent_router.list_agents()
    
    async def handle_nlp_command(self, user_input: str) -> str:
        """Handle command using NLP analysis"""
        try:
            # Analysera input med NLP
            analysis = self.nlp.enhance_command_understanding(user_input)
            
            print(f"🧠 NLP Analysis - Intent: {analysis.get('intent', 'unknown')} "
                  f"(confidence: {analysis.get('confidence', 0):.2f})")
            
            intent = analysis.get('intent')
            confidence = analysis.get('confidence', 0)
            
            # Hög-confidence routing
            if confidence > 0.6:  # Sänk threshold lite
                
                if intent == 'direct_command':
                    command = analysis.get('command', '')
                    if command == 'agents':
                        return self.handle_agents_list()
                    elif command.startswith('research'):
                        topic = command.replace('research', '').strip()
                        return await self.handle_research(topic)
                    elif command.startswith('system'):
                        sys_cmd = command.replace('system', '').strip()
                        return await self.handle_system_command(sys_cmd)
                    else:
                        # Recursively process the command
                        return await self.process_command(command)
                
                elif intent == 'agent_list':
                    return self.handle_agents_list()
                
                elif intent == 'agent_request':
                    agent_type = analysis.get('agent_type')
                    request = analysis.get('request', user_input)
                    if agent_type and request:
                        return await self.handle_direct_agent_request(agent_type, request)
                
                elif intent == 'research':
                    topic = analysis.get('extracted_topic', user_input.replace('research', '').strip())
                    return await self.handle_research(topic)
                
                elif intent == 'memory':
                    query = user_input.replace('memory', '').replace('minne', '').strip()
                    return await self.handle_memory(query)
                
                elif intent == 'learn':
                    info = user_input.replace('learn', '').replace('lär', '').strip()
                    return await self.handle_learning(info)
                
                elif intent == 'system':
                    command = user_input.replace('system', '').strip()
                    return await self.handle_system_command(command)
                
                elif intent == 'help':
                    return self.get_help()
            
            # Medium-confidence: föreslå rättelser eller routing
            elif confidence > 0.3:
                suggestions = self.nlp.suggest_corrections(user_input)
                if suggestions:
                    response = f"🤔 Menade du kanske:\n"
                    for i, suggestion in enumerate(suggestions[:3], 1):
                        response += f"{i}. {suggestion}\n"
                    response += "\n💡 Eller använd agent-routing för komplex förfrågan..."
                    return response
            
            # Low confidence: använd agent routing som fallback
            return await self.handle_general_query(user_input)
            
        except Exception as e:
            print(f"⚠️ NLP-fel: {e}")
            # Fallback to basic processing
            return await self.handle_general_query(user_input)
    
    async def handle_direct_agent_request(self, agent_type: str, request: str) -> str:
        """Handle direct agent request extracted by NLP"""
        if not self.agent_router:
            return "❌ Agent system inte tillgängligt"
        
        try:
            result = await self.agent_router.direct_agent_request(agent_type, request)
            
            if result.get('success'):
                response = f"🤖 **{result.get('agent_name', 'Agent')}** svarar:\n\n"
                
                # Handle different response types
                if 'code' in result:
                    response += f"💻 **Genererad kod ({result.get('language', 'text')}):**\n"
                    response += f"```{result.get('language', '')}\n{result['code']}\n```\n"
                    
                    if 'description' in result:
                        response += f"\n📝 **Beskrivning:** {result['description']}\n"
                    
                    if 'instructions' in result:
                        response += "\n📋 **Instruktioner:**\n"
                        for instruction in result['instructions']:
                            response += f"• {instruction}\n"
                
                elif 'template' in result:
                    response += f"📄 **{result.get('type', 'Template')}:**\n"
                    response += f"```\n{result['template']}\n```\n"
                    
                    if 'tips' in result:
                        response += "\n💡 **Tips:**\n"
                        for tip in result['tips']:
                            response += f"• {tip}\n"
                
                elif 'message' in result:
                    response += result['message']
                    
                    if 'capabilities' in result:
                        response += "\n\n🔧 **Kapaciteter:**\n"
                        for cap in result['capabilities']:
                            response += f"• {cap}\n"
                
                return response
            else:
                return f"❌ Agent-fel: {result.get('error', 'Okänt fel')}"
                
        except Exception as e:
            return f"❌ Agent routing-fel: {e}"
    
    async def handle_general_query(self, query: str) -> str:
        """Handle general AI conversation with agent routing"""
        
        # Try agent routing first for specialized requests
        if self.agent_router:
            try:
                agent_result = await self.agent_router.route_request(query)
                
                if agent_result.get('success'):
                    response = f"🤖 **{agent_result.get('agent_name', 'Specialist')}** ({agent_result.get('confidence', 0):.0%} match):\n\n"
                    
                    # Handle different response types (samma logik som ovan)
                    if 'code' in agent_result:
                        response += f"💻 **Kod ({agent_result.get('language', 'text')}):**\n"
                        response += f"```{agent_result.get('language', '')}\n{agent_result['code']}\n```\n"
                        
                        if 'description' in agent_result:
                            response += f"\n📝 {agent_result['description']}\n"
                    
                    elif 'message' in agent_result:
                        response += agent_result['message']
                        
                        if 'capabilities' in agent_result:
                            response += "\n\n🔧 **Vad jag kan hjälpa med:**\n"
                            for cap in agent_result['capabilities'][:5]:  # Visa max 5
                                response += f"• {cap}\n"
                    
                    return response
                    
            except Exception as e:
                print(f"⚠️ Agent routing fel: {e}")
        
        # Fallback to general AI response
        
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

🤖 AGENT SYSTEM:
• agents              - Lista alla specialiserade agents
• agent [typ] [fråga] - Kontakta specifik specialist direkt
• [naturlig fråga]    - JARVIS routar automatiskt till bästa agent

💻 AGENT SPECIALISTER:
• coder              - Senior Developer (kod, arkitektur, DevOps)
• data_scientist     - Data analys, ML, AI, statistik
• designer           - UI/UX design, grafisk formgivning
• content_creator    - Innehållsskapande, copywriting, berättelser
• university_tutor   - Undervisning, akademiska ämnen
• study_coach        - Studieteknik, motivation, planering
• system_analyst     - Systemanalys, arkitektur, processoptimering
• image_generator    - AI-baserad bildgenerering och redigering

🧠 NLP FEATURES:
• Naturlig språkförståelse på svenska och engelska
• Automatisk intent-detection och kommando-routing
• Felrättningsförslag vid felstavning
• Kontextuell kommando-analys

💬 EXEMPEL PÅ NATURLIGT SPRÅK:
• "Forska om Machine Learning"
• "Visa alla specialists"
• "Be kodaren skapa en API"
• "Hjälp mig med systemstatus"
• "Kom ihåg att jag föredrar Python"

💡 TIPS:
• Skriv på svenska eller engelska - JARVIS förstår båda
• Var specifik för bästa resultat
• Använd 'help' för denna hjälp
• Skriv 'exit' för att avsluta
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
