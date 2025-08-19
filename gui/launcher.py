#!/usr/bin/env python3
"""
JARVIS GUI Launcher
Start the JARVIS GUI application with fallback support
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main launcher with fallback"""
    try:
        # Try advanced GUI with audio visualization
        print("Starting JARVIS GUI with audio visualization...")
        from gui.main_window import main as main_gui
        main_gui()
    except ImportError as e:
        if 'pyaudio' in str(e) or 'matplotlib' in str(e):
            print(f"Advanced GUI dependencies not available: {e}")
            print("Falling back to simple GUI...")
            try:
                from gui.simple_gui import main as simple_gui
                simple_gui()
            except ImportError as e2:
                print(f"Simple GUI also failed: {e2}")
                print("Please install GUI dependencies:")
                print("pip install matplotlib numpy")
                print("sudo apt-get install python3-pyaudio")
                sys.exit(1)
        else:
            print(f"GUI startup error: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
