# NAVI - Your Local-First AI Assistant
# Package initialization

__version__ = "2.0.0"
__author__ = "NAVI Team"
__description__ = "Local-first AI assistant with multi-provider support"

from .core import NaviCore, NaviCLI
from .providers import ProviderManager, setup_providers
from .memory import MemoryManager, ConversationMemory
from .agents import AgentManager

__all__ = [
    "NaviCore",
    "NaviCLI", 
    "ProviderManager",
    "setup_providers",
    "MemoryManager", 
    "ConversationMemory",
    "AgentManager"
]
