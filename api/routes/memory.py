"""
JARVIS AI Agent - Memory Router
Handles /memory endpoint for storing and retrieving memories
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import MemoryEntry

router = APIRouter()

# In-memory storage for now (replace with database later)
memory_storage: List[MemoryEntry] = []

@router.post("/memory", response_model=MemoryEntry)
async def store_memory(memory: MemoryEntry):
    """Store a new memory entry"""
    try:
        memory.id = str(len(memory_storage) + 1)
        memory.timestamp = datetime.now()
        memory_storage.append(memory)
        
        return memory
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory", response_model=List[MemoryEntry])
async def get_memories(category: str = None, limit: int = 10):
    """Retrieve memories, optionally filtered by category"""
    try:
        if category:
            filtered_memories = [m for m in memory_storage if m.category == category]
        else:
            filtered_memories = memory_storage
        
        # Return most recent memories first
        return sorted(filtered_memories, key=lambda x: x.timestamp, reverse=True)[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/search")
async def search_memories(query: str, limit: int = 5):
    """Search memories by content"""
    try:
        matching_memories = []
        query_lower = query.lower()
        
        for memory in memory_storage:
            if (query_lower in memory.content.lower() or 
                any(query_lower in tag.lower() for tag in memory.tags)):
                matching_memories.append(memory)
        
        # Sort by importance and recency
        matching_memories.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        
        return matching_memories[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a specific memory"""
    try:
        global memory_storage
        memory_storage = [m for m in memory_storage if m.id != memory_id]
        
        return {"message": f"Memory {memory_id} deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/stats")
async def get_memory_stats():
    """Get memory storage statistics"""
    try:
        categories = {}
        for memory in memory_storage:
            categories[memory.category] = categories.get(memory.category, 0) + 1
        
        return {
            "total_memories": len(memory_storage),
            "categories": categories,
            "oldest_memory": min(memory_storage, key=lambda x: x.timestamp).timestamp if memory_storage else None,
            "newest_memory": max(memory_storage, key=lambda x: x.timestamp).timestamp if memory_storage else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
