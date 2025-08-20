# NAVI - Provider Abstraction Layer
# Unified interface for multiple AI providers

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    name: str
    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    context_window: int = 8000
    cost_per_token: float = 0.0
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = ["chat"]

@dataclass
class Message:
    """Standardized message format"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ChatResponse:
    """Standardized response format"""
    content: str
    model: str
    provider: str
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.name = config.provider
        
    @abstractmethod
    async def chat(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Send chat messages and get response"""
        pass
    
    @abstractmethod
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat response"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available and configured"""
        pass
    
    @abstractmethod
    def get_models(self) -> List[str]:
        """Get list of available models"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_key = config.api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
    
    async def chat(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Send chat to OpenAI"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            response = await client.chat.completions.create(
                model=self.config.name,
                messages=openai_messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens)
            )
            
            return ChatResponse(
                content=response.choices[0].message.content,
                model=self.config.name,
                provider="openai",
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except ImportError:
            raise RuntimeError("OpenAI package not installed. Install with: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise
    
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat response from OpenAI"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            stream = await client.chat.completions.create(
                model=self.config.name,
                messages=openai_messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except ImportError:
            raise RuntimeError("OpenAI package not installed. Install with: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        try:
            import openai
            return bool(self.api_key)
        except ImportError:
            return False
    
    def get_models(self) -> List[str]:
        """Get OpenAI models"""
        return [
            "gpt-4o",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]

class OllamaProvider(AIProvider):
    """Ollama local AI provider"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"
    
    async def chat(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Send chat to Ollama"""
        try:
            import aiohttp
            
            # Convert messages to Ollama format
            prompt = self._messages_to_prompt(messages)
            
            payload = {
                "model": self.config.name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status != 200:
                        raise RuntimeError(f"Ollama API error: {response.status}")
                    
                    data = await response.json()
                    
                    return ChatResponse(
                        content=data["response"],
                        model=self.config.name,
                        provider="ollama"
                    )
                    
        except ImportError:
            raise RuntimeError("aiohttp package not installed. Install with: pip install aiohttp")
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            raise
    
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat response from Ollama"""
        try:
            import aiohttp
            import json
            
            prompt = self._messages_to_prompt(messages)
            
            payload = {
                "model": self.config.name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status != 200:
                        raise RuntimeError(f"Ollama API error: {response.status}")
                    
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                if "response" in data:
                                    yield data["response"]
                                if data.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except ImportError:
            raise RuntimeError("aiohttp package not installed. Install with: pip install aiohttp")
        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            raise
    
    def _messages_to_prompt(self, messages: List[Message]) -> str:
        """Convert messages to Ollama prompt format"""
        prompt_parts = []
        
        for msg in messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")
        
        return "\n\n".join(prompt_parts) + "\n\nAssistant:"
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            import aiohttp
            import asyncio
            
            async def check():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{self.base_url}/api/tags", timeout=2) as response:
                            return response.status == 200
                except:
                    return False
            
            # Run async check
            try:
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(check())
            except RuntimeError:
                # No event loop running
                return asyncio.run(check())
        except ImportError:
            return False
    
    def get_models(self) -> List[str]:
        """Get available Ollama models"""
        try:
            import aiohttp
            import asyncio
            
            async def get_models():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{self.base_url}/api/tags") as response:
                            if response.status == 200:
                                data = await response.json()
                                return [model["name"] for model in data.get("models", [])]
                except:
                    pass
                return []
            
            try:
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(get_models())
            except RuntimeError:
                return asyncio.run(get_models())
        except ImportError:
            return []

class ProviderManager:
    """Manages multiple AI providers"""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self.default_provider: Optional[str] = None
        
    def register_provider(self, name: str, provider: AIProvider):
        """Register a new provider"""
        self.providers[name] = provider
        logger.info(f"Registered provider: {name}")
        
        # Set as default if first available provider
        if not self.default_provider and provider.is_available():
            self.default_provider = name
            logger.info(f"Set default provider: {name}")
    
    def get_provider(self, name: Optional[str] = None) -> Optional[AIProvider]:
        """Get provider by name or default"""
        if name and name in self.providers:
            return self.providers[name]
        elif self.default_provider:
            return self.providers[self.default_provider]
        return None
    
    def list_providers(self) -> List[str]:
        """List all registered providers"""
        return list(self.providers.keys())
    
    def list_available_providers(self) -> List[str]:
        """List only available providers"""
        return [
            name for name, provider in self.providers.items()
            if provider.is_available()
        ]
    
    def get_all_models(self) -> Dict[str, List[str]]:
        """Get all models from all providers"""
        models = {}
        for name, provider in self.providers.items():
            if provider.is_available():
                models[name] = provider.get_models()
        return models

# Global provider manager instance
provider_manager = ProviderManager()

def setup_providers(config_path: Optional[str] = None) -> ProviderManager:
    """Setup providers from configuration"""
    # Default configurations
    default_configs = [
        ModelConfig(
            name="gpt-4o",
            provider="openai",
            capabilities=["chat", "code", "analysis"]
        ),
        ModelConfig(
            name="llama3.2",
            provider="ollama",
            base_url="http://localhost:11434",
            capabilities=["chat", "code"]
        ),
        ModelConfig(
            name="codellama",
            provider="ollama",
            base_url="http://localhost:11434",
            capabilities=["code", "programming"]
        )
    ]
    
    # Register providers
    for config in default_configs:
        if config.provider == "openai":
            provider = OpenAIProvider(config)
        elif config.provider == "ollama":
            provider = OllamaProvider(config)
        else:
            continue
            
        provider_manager.register_provider(f"{config.provider}:{config.name}", provider)
    
    return provider_manager

if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def test_providers():
        manager = setup_providers()
        
        print("Available providers:", manager.list_available_providers())
        print("All models:", manager.get_all_models())
        
        # Test chat
        provider = manager.get_provider()
        if provider:
            messages = [Message(role="user", content="Hello! How are you?")]
            response = await provider.chat(messages)
            print(f"Response from {response.provider}: {response.content}")
    
    asyncio.run(test_providers())
