"""
JARVIS AI Agent - Actions Router
Handles /actions endpoint for coordinating local and cloud actions
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime
import sys
import os

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import ActionRequest, ActionResponse, ActionStatus
from services.local_agent import LocalAgentService

router = APIRouter()
local_agent = LocalAgentService()

@router.post("/actions", response_model=ActionResponse)
async def execute_action(request: ActionRequest):
    """Execute a specific action (local or cloud)"""
    action_id = str(uuid.uuid4())
    
    try:
        if request.target == "local" or not request.target:
            # Execute local action
            result = await local_agent.execute_action(
                f"{request.action_type}: {request.parameters}"
            )
            
            return ActionResponse(
                action_id=action_id,
                status=ActionStatus.COMPLETED,
                result={"output": result},
                timestamp=datetime.now()
            )
        
        else:
            return ActionResponse(
                action_id=action_id,
                status=ActionStatus.FAILED,
                error="Cloud actions not yet implemented",
                timestamp=datetime.now()
            )
            
    except Exception as e:
        return ActionResponse(
            action_id=action_id,
            status=ActionStatus.FAILED,
            error=str(e),
            timestamp=datetime.now()
        )

@router.get("/actions/status/{action_id}")
async def get_action_status(action_id: str):
    """Get status of a specific action"""
    # This would typically query a database
    return {
        "action_id": action_id,
        "status": "completed",
        "message": "Action status tracking coming soon"
    }

@router.get("/system/status")
async def get_system_status():
    """Get local system status"""
    try:
        status = local_agent.get_system_status()
        return {
            "status": "operational",
            "system": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
