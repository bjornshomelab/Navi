#!/usr/bin/env python3
"""
JARVIS API Server Launcher
Handles import path issues and starts the FastAPI server
"""

import sys
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
API_DIR = PROJECT_ROOT / "api"

# Add directories to Python path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(API_DIR))

# Change to API directory for relative file access
os.chdir(API_DIR)

# Suppress audio warnings and errors
import warnings
warnings.filterwarnings('ignore')

os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['ALSA_PCM_CARD'] = 'default'
os.environ['ALSA_PCM_DEVICE'] = '0'

# Redirect ALSA errors to /dev/null (Linux only)
try:
    import ctypes
    from ctypes import cdll
    libc = cdll.LoadLibrary("libc.so.6")
    
    # Disable ALSA error output
    def alsa_error_handler(filename, line, func, err, fmt, *args):
        pass
    
    # Try to set ALSA error handler
    try:
        import alsaaudio
        libasound = cdll.LoadLibrary("libasound.so.2")
        error_handler_func = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
        libasound.snd_lib_error_set_handler(error_handler_func(alsa_error_handler))
    except:
        pass
except:
    pass

def main():
    """Start the JARVIS API server"""
    try:
        print("🤖 JARVIS API Server Starting...")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🐍 Python path: {sys.path[:3]}...")
        
        # Import and run the FastAPI app
        from main import app
        import uvicorn
        
        print("🚀 Starting server on http://localhost:8081")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8081,
            log_level="warning",  # Reduce noise
            access_log=False      # Disable access logs
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
