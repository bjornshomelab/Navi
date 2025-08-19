"""
JARVIS AI Agent - Voice API Routes
Provides endpoints for controlling TTS voice output
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

router = APIRouter()

# Voice service instance - initialize lazily to avoid circular imports
voice_service = None

def get_voice_service():
    """Get voice service instance with lazy initialization"""
    global voice_service
    if voice_service is None:
        import sys
        import os
        # Add parent directory to path for absolute imports
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from services.enhanced_voice import EnhancedVoiceService
        voice_service = EnhancedVoiceService()
    return voice_service

class SpeakRequest(BaseModel):
    text: str
    priority: int = 1
    interrupt: bool = False

class VoiceSettings(BaseModel):
    language_code: str = None
    voice_name: str = None  
    speaking_rate: float = None
    pitch: float = None
    volume_gain_db: float = None

@router.post("/voice/speak")
async def speak_text(request: SpeakRequest):
    """Speak text using TTS"""
    try:
        service = get_voice_service()
        
        # Handle interrupt by stopping current speech first
        if request.interrupt:
            service.stop()
        
        service.speak(
            text=request.text,
            priority=request.priority
        )
        return {
            "status": "queued",
            "text": request.text[:50] + ("..." if len(request.text) > 50 else ""),
            "queue_size": service.voice_queue.qsize()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech failed: {str(e)}")

@router.post("/voice/stop")
async def stop_speaking():
    """Stop current speech and clear queue"""
    try:
        service = get_voice_service()
        service.stop()
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stop failed: {str(e)}")

@router.get("/voice/status")
async def get_voice_status():
    """Get voice service status"""
    try:
        service = get_voice_service()
        status = service.get_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.get("/voice/voices")
async def get_available_voices():
    """Get list of available voices"""
    try:
        service = get_voice_service()
        voices = service.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice list failed: {str(e)}")

@router.post("/voice/settings")
async def update_voice_settings(settings: VoiceSettings):
    """Update voice settings"""
    try:
        service = get_voice_service()
        # Filter out None values
        update_dict = {k: v for k, v in settings.dict().items() if v is not None}
        
        service.set_voice_settings(**update_dict)
        
        return {
            "status": "updated",
            "settings": service.settings if hasattr(service, 'settings') else {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings update failed: {str(e)}")

@router.get("/voice/settings")
async def get_voice_settings():
    """Get current voice settings"""
    try:
        service = get_voice_service()
        return {"settings": service.settings if hasattr(service, 'settings') else {}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings retrieval failed: {str(e)}")
