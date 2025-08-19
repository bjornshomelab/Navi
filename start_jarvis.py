#!/usr/bin/env python3
"""
JARVIS AI Agent - Server Launcher
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    print("🛰️  Starting JARVIS AI Agent...")
    print("📡 API will be available at: http://localhost:8081")
    print("📚 API docs at: http://localhost:8081/docs")
    print("🔍 Status check: http://localhost:8081/status")
    print()
    
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8081,
        reload=True
    )
