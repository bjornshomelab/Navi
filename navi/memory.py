# NAVI Memory Management
# Local-first memory system with RAG and JSON storage

import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class MemoryItem:
    """Individual memory item"""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON storage"""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "embedding": self.embedding
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            content=data["content"],
            metadata=data["metadata"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            embedding=data.get("embedding")
        )

class ConversationMemory:
    """Manages conversation context and history"""
    
    def __init__(self, session_id: str, max_history: int = 50):
        self.session_id = session_id
        self.max_history = max_history
        self.messages: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        
        # Keep only last N messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_recent_context(self, num_messages: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation context"""
        return self.messages[-num_messages:] if self.messages else []
    
    def set_context(self, key: str, value: Any):
        """Set context variable"""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context variable"""
        return self.context.get(key, default)

class LocalEmbeddings:
    """Local embeddings using sentence transformers"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        
    async def initialize(self):
        """Initialize the embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✅ Initialized local embeddings: {self.model_name}")
        except ImportError:
            logger.warning("⚠️  sentence-transformers not installed. Embeddings disabled.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize embeddings: {e}")
    
    async def encode(self, texts: List[str]) -> List[List[float]]:
        """Encode texts to embeddings"""
        if not self.model:
            return []
        
        try:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Encoding error: {e}")
            return []
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            import numpy as np
            
            a = np.array(vec1)
            b = np.array(vec2)
            
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        except ImportError:
            # Fallback without numpy
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm_a = sum(a * a for a in vec1) ** 0.5
            norm_b = sum(b * b for b in vec2) ** 0.5
            
            if norm_a == 0 or norm_b == 0:
                return 0
            
            return dot_product / (norm_a * norm_b)

class MemoryManager:
    """Main memory management system"""
    
    def __init__(self, data_dir: str = "data/memory"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.conversations_file = self.data_dir / "conversations.json"
        self.knowledge_file = self.data_dir / "knowledge.json"
        self.embeddings_file = self.data_dir / "embeddings.json"
        
        self.conversations: Dict[str, List[Dict]] = {}
        self.knowledge: List[MemoryItem] = []
        self.embeddings = LocalEmbeddings()
        
        self.active_conversations: Dict[str, ConversationMemory] = {}
    
    async def initialize(self):
        """Initialize memory system"""
        logger.info("🧠 Initializing memory system...")
        
        # Initialize embeddings
        await self.embeddings.initialize()
        
        # Load existing data
        await self.load_conversations()
        await self.load_knowledge()
        
        logger.info("✅ Memory system initialized")
    
    async def load_conversations(self):
        """Load conversation history"""
        if self.conversations_file.exists():
            try:
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
                logger.info(f"📚 Loaded {len(self.conversations)} conversation sessions")
            except Exception as e:
                logger.error(f"Failed to load conversations: {e}")
    
    async def save_conversations(self):
        """Save conversation history"""
        try:
            # Include active conversations
            all_conversations = self.conversations.copy()
            for session_id, conv in self.active_conversations.items():
                all_conversations[session_id] = conv.messages
            
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(all_conversations, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save conversations: {e}")
    
    async def load_knowledge(self):
        """Load knowledge base"""
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge = [MemoryItem.from_dict(item) for item in data]
                logger.info(f"📖 Loaded {len(self.knowledge)} knowledge items")
            except Exception as e:
                logger.error(f"Failed to load knowledge: {e}")
    
    async def save_knowledge(self):
        """Save knowledge base"""
        try:
            data = [item.to_dict() for item in self.knowledge]
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save knowledge: {e}")
    
    def get_conversation(self, session_id: str) -> ConversationMemory:
        """Get or create conversation memory"""
        if session_id not in self.active_conversations:
            conv = ConversationMemory(session_id)
            
            # Load existing messages
            if session_id in self.conversations:
                for msg in self.conversations[session_id]:
                    conv.messages.append(msg)
            
            self.active_conversations[session_id] = conv
        
        return self.active_conversations[session_id]
    
    async def save_interaction(self, user_message: str, assistant_response: str, 
                             context: Optional[Dict] = None):
        """Save an interaction to memory"""
        session_id = context.get('session_id', 'default') if context else 'default'
        conv = self.get_conversation(session_id)
        
        # Add messages to conversation
        conv.add_message("user", user_message, context)
        conv.add_message("assistant", assistant_response)
        
        # Save to persistent storage
        await self.save_conversations()
        
        # Add to knowledge base if significant
        await self.add_to_knowledge(user_message, assistant_response, context)
    
    async def add_to_knowledge(self, user_message: str, assistant_response: str, 
                             context: Optional[Dict] = None):
        """Add interaction to knowledge base"""
        # Create a knowledge item
        content = f"Q: {user_message}\nA: {assistant_response}"
        
        # Generate ID
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check if already exists
        if any(item.id == content_hash for item in self.knowledge):
            return
        
        metadata = {
            "type": "qa_pair",
            "user_message": user_message,
            "assistant_response": assistant_response,
            "context": context or {}
        }
        
        # Create memory item
        memory_item = MemoryItem(
            id=content_hash,
            content=content,
            metadata=metadata,
            timestamp=datetime.now()
        )
        
        # Generate embedding if available
        if self.embeddings.model:
            embeddings = await self.embeddings.encode([content])
            if embeddings:
                memory_item.embedding = embeddings[0]
        
        # Add to knowledge
        self.knowledge.append(memory_item)
        
        # Save to disk
        await self.save_knowledge()
    
    async def search_knowledge(self, query: str, max_results: int = 5) -> List[MemoryItem]:
        """Search knowledge base using semantic similarity"""
        if not self.knowledge:
            return []
        
        if not self.embeddings.model:
            # Fallback to simple text search
            results = []
            query_lower = query.lower()
            for item in self.knowledge:
                if query_lower in item.content.lower():
                    results.append(item)
            return results[:max_results]
        
        # Semantic search using embeddings
        query_embedding = await self.embeddings.encode([query])
        if not query_embedding:
            return []
        
        query_vec = query_embedding[0]
        similarities = []
        
        for item in self.knowledge:
            if item.embedding:
                similarity = self.embeddings.cosine_similarity(query_vec, item.embedding)
                similarities.append((similarity, item))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in similarities[:max_results]]
    
    async def get_relevant_context(self, query: str, session_id: str, 
                                 max_items: int = 3) -> Dict[str, Any]:
        """Get relevant context for a query"""
        context = {
            "conversation_history": [],
            "relevant_knowledge": [],
            "session_context": {}
        }
        
        # Get conversation history
        conv = self.get_conversation(session_id)
        context["conversation_history"] = conv.get_recent_context(5)
        context["session_context"] = conv.context
        
        # Search knowledge base
        relevant_items = await self.search_knowledge(query, max_items)
        context["relevant_knowledge"] = [
            {
                "content": item.content,
                "timestamp": item.timestamp.isoformat(),
                "metadata": item.metadata
            }
            for item in relevant_items
        ]
        
        return context
    
    async def cleanup_old_data(self, days: int = 30):
        """Clean up old memory data"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Clean knowledge base
        original_count = len(self.knowledge)
        self.knowledge = [
            item for item in self.knowledge
            if item.timestamp > cutoff_date
        ]
        
        removed_count = original_count - len(self.knowledge)
        if removed_count > 0:
            logger.info(f"🧹 Cleaned up {removed_count} old knowledge items")
            await self.save_knowledge()
        
        # Clean old conversations
        old_sessions = []
        for session_id, messages in self.conversations.items():
            if messages:
                last_message_time = datetime.fromisoformat(messages[-1]["timestamp"])
                if last_message_time < cutoff_date:
                    old_sessions.append(session_id)
        
        for session_id in old_sessions:
            del self.conversations[session_id]
        
        if old_sessions:
            logger.info(f"🧹 Cleaned up {len(old_sessions)} old conversation sessions")
            await self.save_conversations()

# Example usage
if __name__ == "__main__":
    async def test_memory():
        memory = MemoryManager()
        await memory.initialize()
        
        # Test conversation
        await memory.save_interaction(
            "What is Python?",
            "Python is a high-level programming language known for its simplicity and readability.",
            {"session_id": "test_session"}
        )
        
        # Test search
        results = await memory.search_knowledge("programming language")
        print(f"Found {len(results)} relevant items")
        
        for item in results:
            print(f"- {item.content[:100]}...")
    
    asyncio.run(test_memory())
