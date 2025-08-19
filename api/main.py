"""
JARVIS AI Agent - Main FastAPI Application
Iron Man style personal assistant with Google APIs and local system control
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes - use absolute imports to avoid relative import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.command import router as command_router
from routes.actions import router as actions_router
from routes.memory import router as memory_router
from routes.voice import router as voice_router

# Create FastAPI app
app = FastAPI(
    title="JARVIS AI Agent",
    description="Personal AI Assistant with Google APIs and Local System Control",
    version="1.0.0"
)

# Add CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(command_router, prefix="/api")
app.include_router(actions_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(voice_router, prefix="/api")

@app.get("/")
async def root():
    """Health check and welcome message"""
    return {
        "message": "JARVIS AI Agent is online, sir.",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/status")
async def status():
    """System status check"""
    return {
        "jarvis": "online",
        "ai_brain": "operational", 
        "google_apis": "connected",
        "local_agent": "standby",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8080)),
        reload=True
    )
