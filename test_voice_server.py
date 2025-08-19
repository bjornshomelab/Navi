#!/usr/bin/env python3
"""
Simple JARVIS Voice Test Server
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="JARVIS Voice Test")

# Global voice service
voice_service = None

class SpeakRequest(BaseModel):
    text: str
    priority: int = 1

@app.on_event("startup")
async def startup():
    global voice_service
    try:
        from api.services.enhanced_voice import EnhancedVoiceService
        voice_service = EnhancedVoiceService()
        print("✅ Enhanced Voice Service initialiserad")
    except Exception as e:
        print(f"❌ Voice service fel: {e}")

@app.get("/")
async def root():
    return {"message": "JARVIS Voice Test Server", "status": "online"}

@app.post("/speak")
async def speak(request: SpeakRequest):
    try:
        if voice_service:
            voice_service.speak(request.text, request.priority)
            return {"status": "speaking", "text": request.text[:50]}
        else:
            return {"status": "error", "message": "Voice service not available"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/voices")
async def get_voices():
    try:
        if voice_service:
            voices = voice_service.get_voices()
            return {"voices": voices}
        else:
            return {"voices": []}
    except Exception as e:
        return {"error": str(e)}

@app.get("/status")
async def get_status():
    try:
        if voice_service:
            status = voice_service.get_status()
            return status
        else:
            return {"status": "Voice service not initialized"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8081, log_level="info")
