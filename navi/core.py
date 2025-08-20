# NAVI - Local-First AI Assistant Core
# Main NAVI application with provider abstraction

import asyncio
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from navi.providers import setup_providers, provider_manager, Message, ChatResponse
from navi.memory import MemoryManager, ConversationMemory
from navi.agents import AgentManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NaviCore:
    """Main NAVI application class"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.provider_manager = None
        self.memory_manager = None
        self.agent_manager = None
        self.config = {}
        
    async def initialize(self):
        """Initialize NAVI with all components"""
        logger.info("🚀 Initializing NAVI...")
        
        # Load configuration
        await self.load_config()
        
        # Setup providers
        self.provider_manager = setup_providers()
        
        # Initialize memory
        self.memory_manager = MemoryManager()
        await self.memory_manager.initialize()
        
        # Initialize agents
        self.agent_manager = AgentManager(
            provider_manager=self.provider_manager,
            memory_manager=self.memory_manager
        )
        await self.agent_manager.initialize()
        
        logger.info("✅ NAVI initialized successfully!")
        
        # Show available providers
        available = self.provider_manager.list_available_providers()
        if available:
            logger.info(f"📡 Available providers: {', '.join(available)}")
        else:
            logger.warning("⚠️  No AI providers available. Please configure OpenAI API key or install Ollama.")
    
    async def load_config(self):
        """Load configuration from files"""
        config_files = [
            "providers.yaml",
            "agents.yaml", 
            "memory.yaml"
        ]
        
        for config_file in config_files:
            config_path = self.config_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        self.config[config_file.replace('.yaml', '')] = config_data
                        logger.info(f"📁 Loaded config: {config_file}")
                except Exception as e:
                    logger.error(f"❌ Failed to load {config_file}: {e}")
            else:
                logger.warning(f"⚠️  Config file not found: {config_file}")
    
    async def chat(self, message: str, agent: Optional[str] = None, 
                   context: Optional[Dict] = None) -> ChatResponse:
        """Send a chat message to NAVI"""
        try:
            # Create conversation context
            conversation = ConversationMemory(session_id=context.get('session_id', 'default') if context else 'default')
            
            # Route to appropriate agent
            if agent:
                response = await self.agent_manager.process_agent_request(agent, message, conversation)
            else:
                response = await self.agent_manager.process_message(message, conversation)
            
            # Save to memory
            await self.memory_manager.save_interaction(message, response.content, context)
            
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return ChatResponse(
                content=f"Sorry, I encountered an error: {str(e)}",
                model="error",
                provider="navi"
            )
    
    async def stream_chat(self, message: str, agent: Optional[str] = None,
                         context: Optional[Dict] = None):
        """Stream a chat response from NAVI"""
        try:
            conversation = ConversationMemory(session_id=context.get('session_id', 'default') if context else 'default')
            
            async for chunk in self.agent_manager.stream_response(message, agent, conversation):
                yield chunk
                
        except Exception as e:
            logger.error(f"Stream chat error: {e}")
            yield f"Error: {str(e)}"
    
    def get_agent_list(self) -> List[str]:
        """Get list of available agents"""
        if self.agent_manager:
            return self.agent_manager.list_agents()
        return []
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        if not self.provider_manager:
            return {}
        
        status = {}
        for provider_name in self.provider_manager.list_providers():
            provider = self.provider_manager.get_provider(provider_name)
            status[provider_name] = {
                "available": provider.is_available() if provider else False,
                "models": provider.get_models() if provider and provider.is_available() else []
            }
        
        return status

class NaviCLI:
    """Command-line interface for NAVI"""
    
    def __init__(self):
        self.navi = NaviCore()
        self.session_id = "cli_session"
        
    async def run_interactive(self):
        """Run interactive CLI session"""
        await self.navi.initialize()
        
        print("🤖 NAVI - Your Local-First AI Assistant")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🧭 navi> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                elif user_input.lower() == 'status':
                    await self.print_status()
                    continue
                elif user_input.startswith('@'):
                    # Agent command
                    parts = user_input[1:].split(' ', 1)
                    agent = parts[0]
                    message = parts[1] if len(parts) > 1 else ""
                    
                    if not message:
                        print(f"Usage: @{agent} <message>")
                        continue
                        
                    response = await self.navi.chat(
                        message, 
                        agent=agent, 
                        context={'session_id': self.session_id}
                    )
                    print(f"\n🤖 {response.content}")
                else:
                    # Regular chat
                    response = await self.navi.chat(
                        user_input, 
                        context={'session_id': self.session_id}
                    )
                    print(f"\n🤖 {response.content}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def print_help(self):
        """Print help information"""
        help_text = """
NAVI Commands:
  help          - Show this help
  status        - Show provider and agent status
  quit/exit/q   - Exit NAVI
  @agent <msg>  - Send message to specific agent
  
Available agents: """ + ", ".join(self.navi.get_agent_list()) + """

Examples:
  Hello, how are you?
  @coder Write a Python function to sort a list
  @researcher What is artificial intelligence?
        """
        print(help_text)
    
    async def print_status(self):
        """Print system status"""
        print("\n📊 NAVI Status:")
        
        # Provider status
        provider_status = self.navi.get_provider_status()
        print("\n📡 Providers:")
        for name, status in provider_status.items():
            status_icon = "✅" if status["available"] else "❌"
            print(f"  {status_icon} {name}")
            if status["models"]:
                print(f"    Models: {', '.join(status['models'][:3])}{'...' if len(status['models']) > 3 else ''}")
        
        # Agent status
        agents = self.navi.get_agent_list()
        print(f"\n🤖 Agents: {len(agents)} available")
        for agent in agents:
            print(f"  • {agent}")

async def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        command = " ".join(sys.argv[1:])
        navi = NaviCore()
        await navi.initialize()
        
        response = await navi.chat(command)
        print(response.content)
    else:
        # Interactive mode
        cli = NaviCLI()
        await cli.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())
