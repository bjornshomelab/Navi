"""
JARVIS AI Agent - Data Models
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class CommandType(str, Enum):
    """Types of commands JARVIS can execute"""
    CHAT = "chat"
    SYSTEM_ACTION = "system_action"
    WEB_ACTION = "web_action"
    DESKTOP_ACTION = "desktop_action"
    RESEARCH_ACTION = "research_action"
    MEMORY_ACTION = "memory_action"
    SELF_IMPROVEMENT = "self_improvement"
    GOOGLE_API = "google_api"
    FILE_OPERATION = "file_operation"

class ActionStatus(str, Enum):
    """Status of action execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class CommandRequest(BaseModel):
    """Request model for /command endpoint"""
    message: str = Field(..., description="User command or message")
    user_id: Optional[str] = Field(None, description="User identifier for context")
    session_id: Optional[str] = Field(None, description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class CommandResponse(BaseModel):
    """Response model for /command endpoint"""
    response: str = Field(..., description="JARVIS response")
    command_type: CommandType = Field(..., description="Type of command processed")
    actions_taken: List[str] = Field(default_factory=list, description="Actions executed")
    status: ActionStatus = Field(..., description="Execution status")
    execution_time: float = Field(..., description="Time taken to process (seconds)")
    timestamp: datetime = Field(default_factory=datetime.now)

class ActionRequest(BaseModel):
    """Request model for /actions endpoint"""
    action_type: str = Field(..., description="Type of action to execute")
    parameters: Dict[str, Any] = Field(..., description="Action parameters")
    target: Optional[str] = Field(None, description="Target system (local/cloud)")

class ActionResponse(BaseModel):
    """Response model for /actions endpoint"""
    action_id: str = Field(..., description="Unique action identifier")
    status: ActionStatus = Field(..., description="Action status")
    result: Optional[Dict[str, Any]] = Field(None, description="Action result")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now)

class MemoryEntry(BaseModel):
    """Model for memory storage"""
    id: Optional[str] = Field(None, description="Memory entry ID")
    content: str = Field(..., description="Memory content")
    category: str = Field(..., description="Memory category")
    importance: float = Field(default=1.0, description="Importance score 0-1")
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list, description="Memory tags")

class SystemInfo(BaseModel):
    """System information model"""
    os: str
    architecture: str
    python_version: str
    memory_gb: float
    disk_space_gb: float
    cpu_cores: int
