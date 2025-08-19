"""
JARVIS AI Agent - Advanced Memory & Learning Service
Handles long-term memory, context retention, and self-improvement capabilities
"""
import json
import sqlite3
import asyncio
import os
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import hashlib
import pickle
from pathlib import Path

@dataclass
class MemoryEntry:
    """Represents a memory entry in JARVIS brain"""
    id: str
    content: str
    category: str
    importance: float  # 0.0 to 1.0
    timestamp: datetime
    context: Dict[str, Any]
    access_count: int
    last_accessed: datetime
    tags: List[str]
    related_entries: List[str]

@dataclass
class LearningPattern:
    """Represents a learned pattern or improvement"""
    pattern_id: str
    pattern_type: str  # "command_optimization", "user_preference", "error_resolution"
    pattern_data: Dict[str, Any]
    confidence: float
    usage_count: int
    success_rate: float
    created_at: datetime
    last_used: datetime

class AdvancedMemoryService:
    """Advanced memory system for JARVIS with learning capabilities"""
    
    def __init__(self, memory_dir: str = "jarvis_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize databases
        self.db_path = self.memory_dir / "jarvis_brain.db"
        self.learning_db_path = self.memory_dir / "jarvis_learning.db"
        
        # Initialize memory systems
        self._init_databases()
        
        # Memory configuration
        self.max_memory_entries = 10000
        self.memory_retention_days = 365
        self.importance_threshold = 0.3
        
        # Learning system
        self.learning_enabled = True
        self.auto_optimize = True
        
        print("🧠 Advanced Memory System initialized")
    
    def _init_databases(self):
        """Initialize SQLite databases for memory and learning"""
        # Memory database
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                importance REAL NOT NULL,
                timestamp TEXT NOT NULL,
                context TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                tags TEXT,
                related_entries TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                command_type TEXT,
                success BOOLEAN,
                timestamp TEXT NOT NULL,
                execution_time REAL,
                user_satisfaction REAL
            )
        ''')
        
        conn.close()
        
        # Learning database
        conn = sqlite3.connect(self.learning_db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                confidence REAL NOT NULL,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                last_used TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS optimizations (
                id TEXT PRIMARY KEY,
                optimization_type TEXT NOT NULL,
                original_code TEXT,
                optimized_code TEXT,
                improvement_metric TEXT,
                improvement_value REAL,
                applied BOOLEAN DEFAULT FALSE,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.close()
    
    async def store_memory(self, content: str, category: str, importance: float = 0.5, 
                          context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Store a new memory entry"""
        try:
            memory_id = hashlib.md5(f"{content}_{time.time()}".encode()).hexdigest()[:16]
            
            memory = MemoryEntry(
                id=memory_id,
                content=content,
                category=category,
                importance=max(0.0, min(1.0, importance)),
                timestamp=datetime.now(),
                context=context or {},
                access_count=0,
                last_accessed=datetime.now(),
                tags=tags or [],
                related_entries=[]
            )
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            conn.execute('''
                INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory.id, memory.content, memory.category, memory.importance,
                memory.timestamp.isoformat(), json.dumps(memory.context),
                memory.access_count, memory.last_accessed.isoformat(),
                json.dumps(memory.tags), json.dumps(memory.related_entries)
            ))
            conn.commit()
            conn.close()
            
            # Auto-relate to similar memories
            await self._find_and_link_related_memories(memory_id)
            
            return memory_id
            
        except Exception as e:
            print(f"❌ Memory storage error: {e}")
            return ""
    
    async def retrieve_memories(self, query: str, category: str = None, 
                               limit: int = 10, min_importance: float = 0.0) -> List[MemoryEntry]:
        """Retrieve relevant memories based on query"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Build query
            sql = "SELECT * FROM memories WHERE importance >= ?"
            params = [min_importance]
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            if query:
                sql += " AND (content LIKE ? OR tags LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            sql += " ORDER BY importance DESC, last_accessed DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to MemoryEntry objects
            memories = []
            for row in rows:
                memory = MemoryEntry(
                    id=row[0],
                    content=row[1],
                    category=row[2],
                    importance=row[3],
                    timestamp=datetime.fromisoformat(row[4]),
                    context=json.loads(row[5]) if row[5] else {},
                    access_count=row[6],
                    last_accessed=datetime.fromisoformat(row[7]) if row[7] else datetime.now(),
                    tags=json.loads(row[8]) if row[8] else [],
                    related_entries=json.loads(row[9]) if row[9] else []
                )
                memories.append(memory)
                
                # Update access count
                await self._update_memory_access(memory.id)
            
            return memories
            
        except Exception as e:
            print(f"❌ Memory retrieval error: {e}")
            return []
    
    async def learn_from_interaction(self, user_message: str, ai_response: str, 
                                   command_type: str, success: bool, execution_time: float):
        """Learn from user interactions to improve future responses"""
        try:
            # Store conversation
            conv_id = hashlib.md5(f"{user_message}_{time.time()}".encode()).hexdigest()[:16]
            
            conn = sqlite3.connect(self.db_path)
            conn.execute('''
                INSERT INTO conversations VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                conv_id, user_message, ai_response, command_type, success,
                datetime.now().isoformat(), execution_time, None
            ))
            conn.commit()
            conn.close()
            
            # Extract learning patterns
            if self.learning_enabled:
                await self._extract_learning_patterns(user_message, ai_response, command_type, success)
            
            # Store as memory if important
            importance = 0.7 if success else 0.4
            await self.store_memory(
                content=f"User: {user_message} | Response: {ai_response[:100]}...",
                category="conversation",
                importance=importance,
                context={
                    "command_type": command_type,
                    "success": success,
                    "execution_time": execution_time
                },
                tags=[command_type, "interaction"]
            )
            
        except Exception as e:
            print(f"❌ Learning error: {e}")
    
    async def _extract_learning_patterns(self, user_message: str, ai_response: str, 
                                       command_type: str, success: bool):
        """Extract patterns from interactions for future optimization"""
        try:
            # Pattern 1: Command optimization
            if not success and command_type in ["system_action", "web_action", "desktop_action"]:
                pattern_id = hashlib.md5(f"cmd_opt_{user_message}".encode()).hexdigest()[:16]
                pattern_data = {
                    "original_command": user_message,
                    "failed_response": ai_response,
                    "command_type": command_type,
                    "failure_reason": "execution_failed"
                }
                await self._store_learning_pattern(pattern_id, "command_optimization", pattern_data, 0.6)
            
            # Pattern 2: User preferences
            if success:
                preference_keywords = self._extract_preference_keywords(user_message)
                if preference_keywords:
                    pattern_id = hashlib.md5(f"pref_{user_message}".encode()).hexdigest()[:16]
                    pattern_data = {
                        "user_input": user_message,
                        "successful_response": ai_response,
                        "preferences": preference_keywords,
                        "command_type": command_type
                    }
                    await self._store_learning_pattern(pattern_id, "user_preference", pattern_data, 0.8)
            
        except Exception as e:
            print(f"❌ Pattern extraction error: {e}")
    
    def _extract_preference_keywords(self, message: str) -> List[str]:
        """Extract user preference keywords from messages"""
        preference_indicators = ["i like", "i prefer", "i want", "i need", "always", "never", "usually"]
        keywords = []
        
        message_lower = message.lower()
        for indicator in preference_indicators:
            if indicator in message_lower:
                # Extract context around the preference
                start = message_lower.find(indicator)
                context = message_lower[start:start+50]
                keywords.append(context)
        
        return keywords
    
    async def _store_learning_pattern(self, pattern_id: str, pattern_type: str, 
                                    pattern_data: Dict[str, Any], confidence: float):
        """Store a learning pattern"""
        try:
            conn = sqlite3.connect(self.learning_db_path)
            
            # Check if pattern exists
            cursor = conn.execute("SELECT * FROM learning_patterns WHERE pattern_id = ?", (pattern_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing pattern
                conn.execute('''
                    UPDATE learning_patterns 
                    SET usage_count = usage_count + 1, last_used = ?
                    WHERE pattern_id = ?
                ''', (datetime.now().isoformat(), pattern_id))
            else:
                # Insert new pattern
                conn.execute('''
                    INSERT INTO learning_patterns VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pattern_id, pattern_type, json.dumps(pattern_data), confidence,
                    1, 0.0, datetime.now().isoformat(), datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Pattern storage error: {e}")
    
    async def get_contextual_memory(self, user_message: str, max_entries: int = 5) -> List[Dict[str, Any]]:
        """Get relevant contextual memories for current conversation"""
        try:
            # Get recent conversations
            recent_memories = await self.retrieve_memories(
                query=user_message,
                category="conversation",
                limit=max_entries,
                min_importance=0.4
            )
            
            # Get related knowledge
            knowledge_memories = await self.retrieve_memories(
                query=user_message,
                category="knowledge",
                limit=3,
                min_importance=0.6
            )
            
            all_memories = recent_memories + knowledge_memories
            
            return [
                {
                    "content": memory.content,
                    "category": memory.category,
                    "importance": memory.importance,
                    "timestamp": memory.timestamp.isoformat(),
                    "tags": memory.tags
                }
                for memory in all_memories[:max_entries]
            ]
            
        except Exception as e:
            print(f"❌ Contextual memory error: {e}")
            return []
    
    async def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """Suggest code optimizations based on learned patterns"""
        try:
            conn = sqlite3.connect(self.learning_db_path)
            
            # Find patterns that could lead to optimizations
            cursor = conn.execute('''
                SELECT * FROM learning_patterns 
                WHERE pattern_type = 'command_optimization' AND usage_count > 2
                ORDER BY confidence DESC LIMIT 10
            ''')
            patterns = cursor.fetchall()
            conn.close()
            
            suggestions = []
            for pattern in patterns:
                pattern_data = json.loads(pattern[2])
                suggestion = {
                    "type": "command_improvement",
                    "issue": pattern_data.get("failure_reason", "unknown"),
                    "original_command": pattern_data.get("original_command", ""),
                    "confidence": pattern[3],
                    "usage_count": pattern[4],
                    "suggested_fix": self._generate_fix_suggestion(pattern_data)
                }
                suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            print(f"❌ Optimization suggestion error: {e}")
            return []
    
    def _generate_fix_suggestion(self, pattern_data: Dict[str, Any]) -> str:
        """Generate a fix suggestion based on failure pattern"""
        command_type = pattern_data.get("command_type", "")
        failure_reason = pattern_data.get("failure_reason", "")
        
        if command_type == "system_action" and failure_reason == "execution_failed":
            return "Add better error handling and alternative command paths"
        elif command_type == "web_action":
            return "Implement more robust browser initialization and fallback methods"
        elif command_type == "desktop_action":
            return "Add platform-specific automation methods"
        else:
            return "Improve command parsing and execution logic"
    
    async def _find_and_link_related_memories(self, memory_id: str):
        """Find and link related memories"""
        # Implementation for memory linking based on content similarity
        pass
    
    async def _update_memory_access(self, memory_id: str):
        """Update memory access statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute('''
                UPDATE memories 
                SET access_count = access_count + 1, last_accessed = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), memory_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Memory access update error: {e}")
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Memory stats
            cursor = conn.execute("SELECT COUNT(*) FROM memories")
            total_memories = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT category, COUNT(*) FROM memories GROUP BY category")
            categories = dict(cursor.fetchall())
            
            cursor = conn.execute("SELECT AVG(importance) FROM memories")
            avg_importance = cursor.fetchone()[0] or 0.0
            
            # Conversation stats
            cursor = conn.execute("SELECT COUNT(*) FROM conversations WHERE success = 1")
            successful_interactions = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM conversations")
            total_interactions = cursor.fetchone()[0]
            
            conn.close()
            
            # Learning stats
            conn = sqlite3.connect(self.learning_db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM learning_patterns")
            learning_patterns = cursor.fetchone()[0]
            conn.close()
            
            success_rate = (successful_interactions / total_interactions * 100) if total_interactions > 0 else 0
            
            return {
                "total_memories": total_memories,
                "memory_categories": categories,
                "average_importance": round(avg_importance, 2),
                "total_interactions": total_interactions,
                "successful_interactions": successful_interactions,
                "success_rate": round(success_rate, 1),
                "learning_patterns": learning_patterns,
                "memory_system_health": "excellent" if success_rate > 80 else "good" if success_rate > 60 else "needs_improvement"
            }
            
        except Exception as e:
            print(f"❌ Memory stats error: {e}")
            return {"error": str(e)}
