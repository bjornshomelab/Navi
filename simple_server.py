#!/usr/bin/env python3
"""
JARVIS API Server - Simple Launcher
Fixes import issues and starts the server
"""

import sys
import os
from pathlib import Path

# Get project root and add to Python path
project_root = Path(__file__).parent.absolute()
api_dir = project_root / "api"

# Add paths for imports
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(api_dir))

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

def main():
    """Start JARVIS API server"""
    print("🤖 Starting JARVIS API Server...")
    
    # Change to API directory 
    os.chdir(api_dir)
    
    try:
        # Import the FastAPI app
        from main import app
        import uvicorn
        
        print("🚀 Server starting on http://localhost:8081")
        
        # Start server
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=8081,
            log_level="error",    # Minimal logging
            access_log=False      # No access logs
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
