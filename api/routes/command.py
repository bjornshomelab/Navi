"""
JARVIS AI Agent - Command Router
Handles /command endpoint for processing user commands
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
import time
import uuid
import re
from datetime import datetime
import sys
import os

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import CommandRequest, CommandResponse, CommandType, ActionStatus
from services.gemini import GeminiService
from services.local_agent import LocalAgentService
from services.google_apis import GoogleAPIService
from services.automation import AutomationService
from services.research import ResearchService
from services.memory import AdvancedMemoryService
from services.self_improvement import SelfImprovementService
from services.session_manager import session_manager
from services.wake_word import create_wake_word_detector
from services.enhanced_voice import EnhancedVoiceService
from services.enhanced_local_agent import EnhancedLocalAgentService

router = APIRouter()

# Service instances
try:
    gemini_service = GeminiService()
    print("✅ Gemini service initialized")
except Exception as e:
    print(f"❌ Gemini service failed: {e}")
    gemini_service = None

local_agent = LocalAgentService()

# Enhanced local agent for advanced operations
try:
    enhanced_local_agent = EnhancedLocalAgentService()
    print("✅ Enhanced Local Agent service initialized")
except Exception as e:
    print(f"❌ Enhanced Local Agent service failed: {e}")
    enhanced_local_agent = None

try:
    google_service = GoogleAPIService()
    print("✅ Google API service initialized")
except Exception as e:
    print(f"❌ Google API service failed: {e}")
    google_service = None

try:
    automation_service = AutomationService()
    print("✅ Automation service initialized")
except Exception as e:
    print(f"❌ Automation service failed: {e}")
    automation_service = None

try:
    research_service = ResearchService()
    print("✅ Research service initialized")
except Exception as e:
    print(f"❌ Research service failed: {e}")
    research_service = None

try:
    memory_service = AdvancedMemoryService()
    print("✅ Advanced Memory service initialized")
except Exception as e:
    print(f"❌ Memory service failed: {e}")
    memory_service = None

try:
    self_improvement_service = SelfImprovementService()
    print("✅ Self-Improvement service initialized")
except Exception as e:
    print(f"❌ Self-Improvement service failed: {e}")
    self_improvement_service = None

# Initialize wake word detector
try:
    wake_word_detector = create_wake_word_detector()
    print("✅ Wake word detector initialized")
except Exception as e:
    print(f"❌ Wake word detector failed: {e}")
    wake_word_detector = None

# Initialize voice service
try:
    voice_service = EnhancedVoiceService()
    print("✅ Enhanced voice service initialized")
except Exception as e:
    print(f"❌ Voice service failed: {e}")
    voice_service = None

@router.post("/command", response_model=CommandResponse)
async def process_command(request: CommandRequest):
    """
    Main endpoint for processing user commands
    This is where the magic happens - JARVIS analyzes and executes commands
    """
    start_time = time.time()
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Update session activity (this resets the 5-minute timeout)
        session_manager.update_activity(session_id, request.user_id)
        
        # Get contextual memory for better AI responses
        contextual_memories = []
        if memory_service:
            contextual_memories = await memory_service.get_contextual_memory(request.message)
            if contextual_memories:
                # Add memory context to request
                if not request.context:
                    request.context = {}
                request.context["memories"] = contextual_memories
        
        # Use Gemini AI to understand the command
        if gemini_service:
            ai_response, command_type, actions = await gemini_service.process_command(
                request.message, 
                request.context
            )
        else:
            # Fallback without AI
            ai_response = f"JARVIS (No AI): I received your message '{request.message}' but AI is not available."
            command_type = "chat"
            actions = ["conversation"]
        
        # Execute actions based on command type
        actions_taken = []
        status = ActionStatus.COMPLETED
        
        if command_type == "system_action":
            # Execute local system actions with enhanced agent
            for action in actions:
                if enhanced_local_agent:
                    result = await enhanced_local_agent.execute_enhanced_action(action)
                    if result["success"]:
                        actions_taken.append(f"Enhanced Local: {result['message']}")
                    else:
                        actions_taken.append(f"Enhanced Local Error: {result['message']}")
                        status = ActionStatus.FAILED
                else:
                    # Fallback to basic local agent
                    result = await local_agent.execute_action(action)
                    actions_taken.append(f"Local: {result}")
                
        elif command_type == "google_api":
            # Execute Google API actions
            if google_service:
                for action in actions:
                    result = await google_service.execute_action(action)
                    actions_taken.append(f"Google: {result}")
            else:
                actions_taken.append("Google API: Service not available")
                
        elif command_type == "file_operation":
            # Execute file operations with enhanced agent
            for action in actions:
                if enhanced_local_agent:
                    result = await enhanced_local_agent.execute_enhanced_action(action)
                    if result["success"]:
                        actions_taken.append(f"Enhanced File: {result['message']}")
                        # Add detailed info if available
                        if "items" in result:
                            actions_taken.append(f"Details: Found {len(result['items'])} items")
                        elif "organized_files" in result:
                            actions_taken.append(f"Details: Organized {result['total_moved']} files")
                    else:
                        actions_taken.append(f"Enhanced File Error: {result['message']}")
                        status = ActionStatus.FAILED
                else:
                    # Fallback to basic file operations
                    result = await local_agent.execute_file_operation(action)
                    actions_taken.append(f"File: {result}")
                
        elif command_type == "web_action":
            # Execute web automation
            if automation_service:
                for action in actions:
                    result = await automation_service.execute_automation(action)
                    actions_taken.append(f"Web: {result}")
                    
                    # Track browser session for cleanup
                    session_manager.add_resource(session_id, 'browser_session', session_id)
            else:
                actions_taken.append("Web automation: Service not available")
                
        elif command_type == "desktop_action":
            # Execute desktop automation
            if automation_service:
                for action in actions:
                    result = await automation_service.execute_automation(action)
                    actions_taken.append(f"Desktop: {result}")
                    
                    # Track browser session for cleanup
                    session_manager.add_resource(session_id, 'browser_session', session_id)
            else:
                actions_taken.append("Desktop automation: Service not available")
                
        elif command_type == "research_action":
            # Execute interactive research workflow
            if research_service:
                for action in actions:
                    # Extract research topic from action
                    topic = action.replace("research: ", "")
                    
                    # Check if this is a follow-up to existing workflow
                    workflow_pattern = r"workflow[:\s]+(\w+)"
                    workflow_match = re.search(workflow_pattern, topic, re.IGNORECASE)
                    
                    choice_patterns = [
                        r"option\s*(\d+)", r"choose\s+for\s+me", r"auto", 
                        r"save\s+report", r"just\s+show\s+me"
                    ]
                    
                    is_choice = any(re.search(pattern, topic, re.IGNORECASE) for pattern in choice_patterns)
                    
                    if workflow_match:
                        # This is a workflow continuation
                        workflow_id = workflow_match.group(1)
                        choice = topic.replace(f"workflow {workflow_id}", "").strip()
                        if is_choice:
                            if "save" in choice.lower():
                                result = await research_service.save_research_report(workflow_id)
                            else:
                                result = await research_service.handle_user_choice(workflow_id, choice)
                        else:
                            result = await research_service.get_workflow_status(workflow_id)
                    elif is_choice and hasattr(research_service, 'active_workflows'):
                        # User responding to most recent workflow
                        if research_service.active_workflows:
                            latest_workflow_id = max(research_service.active_workflows.keys())
                            if "save" in topic.lower():
                                result = await research_service.save_research_report(latest_workflow_id)
                            else:
                                result = await research_service.handle_user_choice(latest_workflow_id, topic)
                        else:
                            result = {"error": "No active research workflow found"}
                    else:
                        # Start new interactive research workflow
                        result = await research_service.start_interactive_research(topic)
                        
                        # Track the research workflow in session
                        if isinstance(result, dict) and 'workflow_id' in result:
                            session_manager.add_resource(session_id, 'research_workflow', result['workflow_id'])
                    
                    actions_taken.append(f"Research: {result}")
            else:
                actions_taken.append("Research: Service not available")
                
        elif command_type == "memory_action":
            # Execute memory operations
            if memory_service:
                for action in actions:
                    # Extract memory operation from action
                    memory_query = action.replace("memory: ", "")
                    if "remember" in memory_query.lower():
                        # Store new memory
                        await memory_service.store_memory(
                            content=memory_query,
                            category="user_instruction",
                            importance=0.8,
                            tags=["user_command"]
                        )
                        result = "Memory stored successfully"
                    else:
                        # Retrieve memories
                        memories = await memory_service.retrieve_memories(memory_query)
                        result = f"Found {len(memories)} relevant memories"
                    actions_taken.append(f"Memory: {result}")
            else:
                actions_taken.append("Memory: Service not available")
                
        elif command_type == "self_improvement":
            # Execute self-improvement
            if self_improvement_service:
                for action in actions:
                    improvement_request = action.replace("improve: ", "")
                    if "analyze" in improvement_request.lower():
                        result = await self_improvement_service.analyze_codebase()
                        actions_taken.append(f"Self-Improvement: Analyzed {result.get('files_analyzed', 0)} files, found {len(result.get('improvements_found', []))} improvements")
                    else:
                        stats = await self_improvement_service.get_improvement_stats()
                        actions_taken.append(f"Self-Improvement: Code quality score: {stats.get('code_quality_score', 0):.1f}/100")
            else:
                actions_taken.append("Self-Improvement: Service not available")
            
        else:  # chat
            # Pure conversation - no actions needed
            actions_taken.append("Conversation")
        
        execution_time = time.time() - start_time
        
        # Learn from this interaction
        if memory_service:
            success = status == ActionStatus.COMPLETED
            await memory_service.learn_from_interaction(
                user_message=request.message,
                ai_response=ai_response,
                command_type=command_type,
                success=success,
                execution_time=execution_time
            )
        
        # Speak the response using TTS
        if voice_service and ai_response:
            try:
                # Clean response for TTS (remove markdown, excessive formatting)
                clean_response = _clean_text_for_tts(ai_response)
                voice_service.speak(clean_response)
            except Exception as e:
                print(f"❌ TTS error: {e}")
        
        return CommandResponse(
            response=ai_response,
            command_type=CommandType(command_type),
            actions_taken=actions_taken,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail=f"Command processing failed: {str(e)}"
        )

@router.get("/command/history")
async def get_command_history(limit: int = 10):
    """Get recent command history (future implementation with database)"""
    return {
        "message": "Command history feature coming soon",
        "limit": limit
    }

@router.post("/command/batch")
async def process_batch_commands(commands: list[CommandRequest]):
    """Process multiple commands in sequence"""
    results = []
    
    for cmd in commands:
        try:
            result = await process_command(cmd)
            results.append(result)
        except Exception as e:
            results.append({
                "error": str(e),
                "command": cmd.message
            })
    
    return {
        "batch_results": results,
        "total_commands": len(commands),
        "successful": len([r for r in results if "error" not in r])
    }

@router.get("/command/automation/info")
async def get_automation_info():
    """Get current automation system information"""
    if automation_service:
        info = await automation_service.get_system_info()
        return {
            "automation_available": True,
            "system_info": info
        }
    else:
        return {
            "automation_available": False,
            "error": "Automation service not available"
        }

@router.post("/command/automation/close-browser")
async def close_browser():
    """Close the automation browser"""
    if automation_service:
        automation_service.close_browser()
        return {"message": "Browser closed"}
    else:
        return {"error": "Automation service not available"}

@router.get("/command/research/status")
async def get_research_status():
    """Get status of all research sessions"""
    if research_service:
        status = await research_service.get_research_status()
        return {
            "research_available": True,
            "status": status
        }
    else:
        return {
            "research_available": False,
            "error": "Research service not available"
        }

@router.post("/command/research/close")
async def close_research_session(session_id: str = None):
    """Close research session and browser tabs"""
    if research_service:
        result = await research_service.close_research_session(session_id)
        return {"message": result}
    else:
        return {"error": "Research service not available"}

@router.post("/command/research/conduct")
async def conduct_research(topic: str, num_tabs: int = 3):
    """Manually trigger research on a topic"""
    if research_service:
        result = await research_service.conduct_research(topic, num_tabs=num_tabs)
        return result
    else:
        return {"error": "Research service not available"}

@router.post("/command/research/interactive")
async def start_interactive_research(topic: str):
    """Start an interactive research workflow"""
    if research_service:
        result = await research_service.start_interactive_research(topic)
        return result
    else:
        return {"error": "Research service not available"}

@router.post("/command/research/workflow/{workflow_id}/choice")
async def handle_workflow_choice(workflow_id: str, choice: str):
    """Handle user choice in research workflow"""
    if research_service:
        result = await research_service.handle_user_choice(workflow_id, choice)
        return result
    else:
        return {"error": "Research service not available"}

@router.post("/command/research/workflow/{workflow_id}/save")
async def save_research_report(workflow_id: str, save_location: str = "auto"):
    """Save research report to file"""
    if research_service:
        result = await research_service.save_research_report(workflow_id, save_location)
        return result
    else:
        return {"error": "Research service not available"}

@router.get("/command/research/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """Get status of research workflow"""
    if research_service:
        result = await research_service.get_workflow_status(workflow_id)
        return result
    else:
        return {"error": "Research service not available"}

@router.get("/command/research/workflows")
async def list_active_workflows():
    """List all active research workflows"""
    if research_service and hasattr(research_service, 'active_workflows'):
        workflows = []
        for wf_id, workflow in research_service.active_workflows.items():
            workflows.append({
                "workflow_id": wf_id,
                "topic": workflow.topic,
                "phase": workflow.phase,
                "created_at": workflow.created_at.isoformat()
            })
        return {"workflows": workflows}
    else:
        return {"workflows": []}

@router.get("/command/memory/stats")
async def get_memory_stats():
    """Get memory system statistics"""
    if memory_service:
        stats = await memory_service.get_memory_stats()
        return {
            "memory_available": True,
            "stats": stats
        }
    else:
        return {
            "memory_available": False,
            "error": "Memory service not available"
        }

@router.post("/command/memory/store")
async def store_memory(content: str, category: str = "user_input", importance: float = 0.5):
    """Manually store a memory"""
    if memory_service:
        memory_id = await memory_service.store_memory(content, category, importance)
        return {"message": f"Memory stored with ID: {memory_id}"}
    else:
        return {"error": "Memory service not available"}

@router.get("/command/memory/retrieve")
async def retrieve_memories(query: str, limit: int = 10):
    """Retrieve memories based on query"""
    if memory_service:
        memories = await memory_service.retrieve_memories(query, limit=limit)
        return {
            "memories": [
                {
                    "content": m.content,
                    "category": m.category,
                    "importance": m.importance,
                    "timestamp": m.timestamp.isoformat(),
                    "tags": m.tags
                }
                for m in memories
            ]
        }
    else:
        return {"error": "Memory service not available"}

@router.get("/command/improvement/analyze")
async def analyze_codebase():
    """Analyze codebase for improvements"""
    if self_improvement_service:
        analysis = await self_improvement_service.analyze_codebase()
        return analysis
    else:
        return {"error": "Self-improvement service not available"}

@router.get("/command/improvement/stats")
async def get_improvement_stats():
    """Get self-improvement statistics"""
    if self_improvement_service:
        stats = await self_improvement_service.get_improvement_stats()
        return {
            "improvement_available": True,
            "stats": stats
        }
    else:
        return {
            "improvement_available": False,
            "error": "Self-improvement service not available"
        }

@router.post("/command/improvement/suggest")
async def suggest_improvements(file_path: str):
    """Get improvement suggestions for a specific file"""
    if self_improvement_service:
        suggestions = await self_improvement_service.suggest_code_improvements(file_path)
        return suggestions
    else:
        return {"error": "Self-improvement service not available"}

@router.get("/command/sessions")
async def list_active_sessions():
    """Get information about all active sessions"""
    sessions = session_manager.get_all_sessions()
    return {
        "active_sessions": len(sessions),
        "sessions": sessions
    }

@router.get("/command/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a specific session"""
    session_info = session_manager.get_session_info(session_id)
    if session_info:
        return {
            "session_found": True,
            "session_info": session_info
        }
    else:
        return {
            "session_found": False,
            "error": "Session not found or expired"
        }

@router.post("/command/sessions/{session_id}/cleanup")
async def force_cleanup_session(session_id: str):
    """Manually force cleanup of a specific session"""
    try:
        success = await session_manager.force_cleanup_session(session_id)
        return {
            "success": success,
            "message": f"Session {session_id} cleaned up successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to cleanup session: {str(e)}"
        }

@router.post("/command/sessions/cleanup-expired")
async def cleanup_expired_sessions():
    """Manually trigger cleanup of all expired sessions"""
    try:
        session_manager._cleanup_expired_sessions_sync()
        return {
            "success": True,
            "message": "Expired sessions cleanup completed"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Cleanup failed: {str(e)}"
        }

@router.post("/command/wake-word/start")
async def start_wake_word_detection():
    """Start wake word detection"""
    if wake_word_detector:
        # Set callback to process wake word commands
        def handle_wake_word(command: str):
            # Create a command request and process it
            import asyncio
            asyncio.create_task(process_wake_word_command(command))
        
        wake_word_detector.set_callback(handle_wake_word)
        success = wake_word_detector.start_listening()
        
        return {
            "success": success,
            "message": "Wake word detection started" if success else "Failed to start wake word detection",
            "wake_words": ["hey jarvis", "hej jarvis", "god morgon jarvis", "god kväll jarvis"]
        }
    else:
        return {
            "success": False,
            "error": "Wake word detector not available"
        }

@router.post("/command/wake-word/stop")
async def stop_wake_word_detection():
    """Stop wake word detection"""
    if wake_word_detector:
        wake_word_detector.stop_listening()
        return {
            "success": True,
            "message": "Wake word detection stopped"
        }
    else:
        return {
            "success": False,
            "error": "Wake word detector not available"
        }

@router.get("/command/wake-word/status")
async def get_wake_word_status():
    """Get wake word detection status"""
    if wake_word_detector:
        return {
            "available": True,
            "listening": getattr(wake_word_detector, 'is_listening', False),
            "wake_words": ["hey jarvis", "hej jarvis", "god morgon jarvis", "god kväll jarvis"]
        }
    else:
        return {
            "available": False,
            "listening": False,
            "error": "Wake word detector not available"
        }

@router.post("/command/wake-word/simulate")
async def simulate_wake_word(text: str):
    """Simulate wake word for testing (only works with mock detector)"""
    if wake_word_detector and hasattr(wake_word_detector, 'simulate_wake_word'):
        wake_word_detector.simulate_wake_word(text)
        return {
            "success": True,
            "message": f"Simulated wake word: '{text}'"
        }
    else:
        return {
            "success": False,
            "error": "Wake word simulation not available"
        }

@router.post("/enhanced-local")
async def enhanced_local_action(
    action: str,
    path: Optional[str] = None,
    content: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None
):
    """
    Execute enhanced local computer operations
    
    Supports:
    - Advanced file operations (list, read, write, organize, backup)
    - Application management 
    - System monitoring
    - File search and organization
    """
    try:
        if not enhanced_local_agent:
            return {
                "success": False,
                "message": "Enhanced Local Agent is not available",
                "error": "Service not initialized"
            }
        
        # Prepare parameters
        kwargs = {}
        if path:
            kwargs['path'] = path
        if content:
            kwargs['content'] = content
        if parameters:
            kwargs.update(parameters)
        
        # Execute action
        result = await enhanced_local_agent.execute_enhanced_action(action, **kwargs)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Enhanced local action failed: {str(e)}",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/enhanced-local/capabilities")
async def get_enhanced_local_capabilities():
    """Get capabilities of enhanced local agent"""
    try:
        if not enhanced_local_agent:
            return {
                "success": False,
                "message": "Enhanced Local Agent is not available"
            }
        
        capabilities = enhanced_local_agent.get_capabilities()
        
        return {
            "success": True,
            "capabilities": capabilities,
            "examples": {
                "file_operations": [
                    "lista filer i /home/bjorn/Desktop",
                    "läs filen ~/documents/notes.txt", 
                    "organisera filer på skrivbordet",
                    "skapa backup av mina projekt"
                ],
                "application_operations": [
                    "öppna firefox",
                    "starta vscode",
                    "kör terminal"
                ],
                "system_operations": [
                    "visa systemstatus",
                    "systeminfo"
                ]
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to get capabilities: {str(e)}"
        }

def _clean_text_for_tts(text: str) -> str:
    """Clean text for TTS by removing markdown, code blocks, and excessive formatting"""
    if not text:
        return ""
    
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'#{1,6}\s*(.*)', r'\1', text)  # Headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    
    # Remove bullet points and lists
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Limit length for TTS (avoid very long responses)
    if len(text) > 500:
        text = text[:497] + "..."
    
    return text.strip()

async def process_wake_word_command(command: str):
    """Process command triggered by wake word"""
    try:
        # Create a command request
        from models.schemas import CommandRequest
        
        request = CommandRequest(
            message=command,
            session_id="wake_word_session",
            user_id="voice_user"
        )
        
        # Process the command
        response = await process_command(request)
        print(f"🎤 Wake word command processed: {command}")
        print(f"🤖 JARVIS response: {response.response}")
        
        # Speak the response using TTS for voice commands
        if voice_service and response.response:
            try:
                clean_response = _clean_text_for_tts(response.response)
                voice_service.speak(clean_response, priority=0, interrupt=True)
            except Exception as e:
                print(f"❌ Wake word TTS error: {e}")
        
        return response
        
    except Exception as e:
        print(f"❌ Wake word command processing failed: {e}")
