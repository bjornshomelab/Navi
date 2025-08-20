# NAVI Agent System Integration
# Integrates with existing agent system and provider abstraction

import asyncio
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from navi.providers import ProviderManager, Message, ChatResponse
from navi.memory import MemoryManager, ConversationMemory

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str
    enabled: bool
    agent_type: str
    description: str
    system_prompt: str
    temperature: float = 0.7
    max_context_length: int = 4000
    capabilities: List[str] = None
    routing_keywords: List[str] = None
    preferred_providers: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.routing_keywords is None:
            self.routing_keywords = []
        if self.preferred_providers is None:
            self.preferred_providers = []

class AgentManager:
    """Manages AI agents with provider abstraction"""
    
    def __init__(self, provider_manager: ProviderManager, memory_manager: MemoryManager):
        self.provider_manager = provider_manager
        self.memory_manager = memory_manager
        self.agents: Dict[str, AgentConfig] = {}
        self.agent_routing: Dict[str, str] = {}
        
    async def initialize(self):
        """Initialize agent system"""
        logger.info("🤖 Initializing agent system...")
        
        # Load agent configuration
        await self.load_agent_config()
        
        # Setup routing
        self.setup_routing()
        
        logger.info(f"✅ Initialized {len(self.agents)} agents")
    
    async def load_agent_config(self):
        """Load agent configuration from YAML"""
        config_path = Path("config/agents.yaml")
        if not config_path.exists():
            logger.warning("⚠️  Agent config not found, using defaults")
            self.setup_default_agents()
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            agents_config = config.get('agents', {})
            
            for agent_name, agent_data in agents_config.items():
                if agent_data.get('enabled', True):
                    agent_config = AgentConfig(
                        name=agent_name,
                        enabled=True,
                        agent_type=agent_data.get('type', 'general'),
                        description=agent_data.get('description', ''),
                        system_prompt=agent_data.get('system_prompt', ''),
                        temperature=agent_data.get('temperature', 0.7),
                        max_context_length=agent_data.get('max_context_length', 4000),
                        capabilities=agent_data.get('capabilities', []),
                        routing_keywords=agent_data.get('routing_keywords', []),
                        preferred_providers=agent_data.get('preferred_providers', [])
                    )
                    
                    self.agents[agent_name] = agent_config
                    logger.info(f"📝 Loaded agent: {agent_name}")
        
        except Exception as e:
            logger.error(f"❌ Failed to load agent config: {e}")
            self.setup_default_agents()
    
    def setup_default_agents(self):
        """Setup default agents if config is missing"""
        default_agents = {
            "chat": AgentConfig(
                name="chat",
                enabled=True,
                agent_type="general",
                description="General purpose chat assistant",
                system_prompt="You are NAVI, a helpful AI assistant. Be friendly, concise, and accurate.",
                capabilities=["conversation", "general_knowledge"],
                routing_keywords=["help", "question", "what", "how", "why"]
            ),
            "coder": AgentConfig(
                name="coder",
                enabled=True,
                agent_type="specialist",
                description="Programming and code assistant",
                system_prompt="You are a senior software engineer. Provide clean, efficient code with explanations.",
                temperature=0.3,
                capabilities=["code_generation", "debugging", "code_review"],
                routing_keywords=["code", "programming", "function", "debug", "script"],
                preferred_providers=["ollama:codellama", "openai:gpt-4"]
            )
        }
        
        self.agents = default_agents
        logger.info("🔧 Using default agent configuration")
    
    def setup_routing(self):
        """Setup keyword-based routing"""
        self.agent_routing = {}
        
        for agent_name, agent in self.agents.items():
            for keyword in agent.routing_keywords:
                if keyword not in self.agent_routing:
                    self.agent_routing[keyword] = []
                self.agent_routing[keyword].append(agent_name)
    
    def route_message(self, message: str) -> Optional[str]:
        """Route message to appropriate agent based on keywords"""
        message_lower = message.lower()
        
        # Count keyword matches for each agent
        agent_scores = {}
        
        for keyword, agents in self.agent_routing.items():
            if keyword.lower() in message_lower:
                for agent in agents:
                    agent_scores[agent] = agent_scores.get(agent, 0) + 1
        
        # Return agent with highest score
        if agent_scores:
            best_agent = max(agent_scores.items(), key=lambda x: x[1])
            return best_agent[0]
        
        # Default to chat agent
        return "chat"
    
    def get_best_provider(self, agent_name: str) -> Optional[str]:
        """Get best available provider for an agent"""
        if agent_name not in self.agents:
            return None
        
        agent = self.agents[agent_name]
        
        # Check preferred providers first
        available_providers = self.provider_manager.list_available_providers()
        
        for preferred in agent.preferred_providers:
            if preferred in available_providers:
                return preferred
        
        # Fallback to any available provider
        if available_providers:
            return available_providers[0]
        
        return None
    
    async def process_message(self, message: str, conversation: ConversationMemory) -> ChatResponse:
        """Process message with automatic agent routing"""
        # Route to appropriate agent
        agent_name = self.route_message(message)
        
        return await self.process_agent_request(agent_name, message, conversation)
    
    async def process_agent_request(self, agent_name: str, message: str, 
                                  conversation: ConversationMemory) -> ChatResponse:
        """Process message with specific agent"""
        if agent_name not in self.agents:
            return ChatResponse(
                content=f"Agent '{agent_name}' not found. Available agents: {', '.join(self.list_agents())}",
                model="error",
                provider="navi"
            )
        
        agent = self.agents[agent_name]
        
        # Get best provider
        provider_name = self.get_best_provider(agent_name)
        if not provider_name:
            return ChatResponse(
                content="No AI providers available. Please configure OpenAI API key or install Ollama.",
                model="error",
                provider="navi"
            )
        
        provider = self.provider_manager.get_provider(provider_name)
        if not provider:
            return ChatResponse(
                content=f"Provider '{provider_name}' not available.",
                model="error",
                provider="navi"
            )
        
        try:
            # Get relevant context from memory
            context = await self.memory_manager.get_relevant_context(
                message, conversation.session_id
            )
            
            # Build message list
            messages = []
            
            # System prompt
            messages.append(Message(role="system", content=agent.system_prompt))
            
            # Add relevant knowledge if available
            if context["relevant_knowledge"]:
                knowledge_content = "Relevant information from memory:\n"
                for item in context["relevant_knowledge"]:
                    knowledge_content += f"- {item['content']}\n"
                
                messages.append(Message(role="system", content=knowledge_content))
            
            # Add recent conversation history
            for hist_msg in context["conversation_history"][-5:]:  # Last 5 messages
                messages.append(Message(
                    role=hist_msg["role"],
                    content=hist_msg["content"]
                ))
            
            # Current user message
            messages.append(Message(role="user", content=message))
            
            # Send to provider
            response = await provider.chat(
                messages,
                temperature=agent.temperature,
                max_tokens=agent.max_context_length
            )
            
            # Update response metadata
            response.metadata = {
                "agent": agent_name,
                "agent_type": agent.agent_type,
                "capabilities": agent.capabilities
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Agent '{agent_name}' processing error: {e}")
            return ChatResponse(
                content=f"I encountered an error while processing your request: {str(e)}",
                model="error",
                provider="navi"
            )
    
    async def stream_response(self, message: str, agent_name: Optional[str], 
                            conversation: ConversationMemory):
        """Stream response from agent"""
        # Route agent if not specified
        if not agent_name:
            agent_name = self.route_message(message)
        
        if agent_name not in self.agents:
            yield f"Agent '{agent_name}' not found."
            return
        
        agent = self.agents[agent_name]
        
        # Get provider
        provider_name = self.get_best_provider(agent_name)
        if not provider_name:
            yield "No AI providers available."
            return
        
        provider = self.provider_manager.get_provider(provider_name)
        if not provider:
            yield f"Provider '{provider_name}' not available."
            return
        
        try:
            # Get context and build messages (same as process_agent_request)
            context = await self.memory_manager.get_relevant_context(
                message, conversation.session_id
            )
            
            messages = []
            messages.append(Message(role="system", content=agent.system_prompt))
            
            if context["relevant_knowledge"]:
                knowledge_content = "Relevant information from memory:\n"
                for item in context["relevant_knowledge"]:
                    knowledge_content += f"- {item['content']}\n"
                messages.append(Message(role="system", content=knowledge_content))
            
            for hist_msg in context["conversation_history"][-5:]:
                messages.append(Message(
                    role=hist_msg["role"],
                    content=hist_msg["content"]
                ))
            
            messages.append(Message(role="user", content=message))
            
            # Stream response
            full_response = ""
            async for chunk in provider.stream_chat(
                messages,
                temperature=agent.temperature,
                max_tokens=agent.max_context_length
            ):
                full_response += chunk
                yield chunk
            
            # Save to memory
            conversation.add_message("user", message)
            conversation.add_message("assistant", full_response)
            
        except Exception as e:
            logger.error(f"Stream error for agent '{agent_name}': {e}")
            yield f"Error: {str(e)}"
    
    def list_agents(self) -> List[str]:
        """List available agent names"""
        return list(self.agents.keys())
    
    def get_agent_info(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get information about an agent"""
        if agent_name not in self.agents:
            return None
        
        agent = self.agents[agent_name]
        return {
            "name": agent.name,
            "type": agent.agent_type,
            "description": agent.description,
            "capabilities": agent.capabilities,
            "routing_keywords": agent.routing_keywords,
            "preferred_providers": agent.preferred_providers
        }
    
    def get_all_agents_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents"""
        return {
            name: self.get_agent_info(name)
            for name in self.agents.keys()
        }

# Example usage
if __name__ == "__main__":
    async def test_agents():
        from navi.providers import setup_providers
        from navi.memory import MemoryManager
        
        # Setup components
        provider_manager = setup_providers()
        memory_manager = MemoryManager()
        await memory_manager.initialize()
        
        # Initialize agent manager
        agent_manager = AgentManager(provider_manager, memory_manager)
        await agent_manager.initialize()
        
        # Test routing
        print("Testing agent routing:")
        test_messages = [
            "Hello, how are you?",
            "Write a Python function to calculate fibonacci",
            "What is machine learning?",
            "Debug this code please"
        ]
        
        for msg in test_messages:
            agent = agent_manager.route_message(msg)
            print(f"'{msg}' -> {agent}")
        
        # Test processing
        conversation = ConversationMemory("test_session")
        response = await agent_manager.process_message("Hello!", conversation)
        print(f"\nResponse: {response.content}")
    
    asyncio.run(test_agents())
