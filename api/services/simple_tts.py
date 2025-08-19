"""
JARVIS AI Agent - Simple TTS Service
Simple text-to-speech using system commands
"""
import subprocess
import threading
import queue
import time

class SimpleTTSService:
    """Simple TTS service using system commands"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        self.engine_name = 'simple'
        
        # Test available TTS commands
        self.tts_command = self._find_tts_command()
        
        # Start voice processing thread
        self._start_voice_thread()
        
        print(f"🔊 Simple TTS service initialized with {self.tts_command}")
    
    def _find_tts_command(self):
        """Find available TTS command"""
        commands_to_test = [
            ['espeak', '--version'],
            ['festival', '--version'],  
            ['say', '--version'],  # macOS
            ['spd-say', '--version']  # speech-dispatcher
        ]
        
        for cmd_test in commands_to_test:
            try:
                result = subprocess.run(cmd_test, capture_output=True, timeout=5)
                if result.returncode == 0:
                    cmd_name = cmd_test[0]
                    print(f"✅ Found TTS command: {cmd_name}")
                    return cmd_name
            except:
                continue
        
        print("❌ No TTS command found")
        return None
    
    def _start_voice_thread(self):
        """Start background thread for voice processing"""
        self.speak_thread = threading.Thread(target=self._voice_worker, daemon=True)
        self.speak_thread.start()
    
    def _voice_worker(self):
        """Background worker for processing voice requests"""
        while True:
            try:
                text, priority = self.voice_queue.get(timeout=1)
                if text is None:  # Shutdown signal
                    break
                
                self.is_speaking = True
                self._speak_text(text)
                self.is_speaking = False
                self.voice_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ TTS worker error: {e}")
                self.is_speaking = False
    
    def _speak_text(self, text):
        """Actually speak the text using system command"""
        try:
            if not self.tts_command:
                print(f"🔊 JARVIS would say: '{text}'")
                return
            
            if self.tts_command == 'espeak':
                subprocess.run(['espeak', '-s', '180', text], timeout=30)
            elif self.tts_command == 'festival':
                subprocess.run(['echo', text], stdout=subprocess.PIPE, text=True)
                subprocess.run(['festival', '--tts'], input=text, text=True, timeout=30)
            elif self.tts_command == 'say':  # macOS
                subprocess.run(['say', text], timeout=30)
            elif self.tts_command == 'spd-say':
                subprocess.run(['spd-say', text], timeout=30)
            else:
                print(f"🔊 JARVIS would say: '{text}'")
                
        except subprocess.TimeoutExpired:
            print("❌ TTS timeout")
        except Exception as e:
            print(f"❌ TTS error: {e}")
            print(f"🔊 JARVIS would say: '{text}'")
    
    def speak(self, text, priority=1, interrupt=False):
        """Add text to speech queue"""
        if not text.strip():
            return
        
        if interrupt:
            self.stop_speaking()
            
        self.voice_queue.put((text, priority))
        print(f"🔊 Queued for speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def stop_speaking(self):
        """Stop current speech and clear queue"""
        # Clear the queue
        while not self.voice_queue.empty():
            try:
                self.voice_queue.get_nowait()
                self.voice_queue.task_done()
            except queue.Empty:
                break
        
        # Kill any running TTS processes
        try:
            subprocess.run(['pkill', '-f', 'espeak'], timeout=2)
            subprocess.run(['pkill', '-f', 'festival'], timeout=2)
        except:
            pass
        
        self.is_speaking = False
        print("🔇 Speech stopped")
    
    def get_status(self):
        """Get current voice service status"""
        return {
            'engine': 'simple_tts',
            'command': self.tts_command,
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'available': self.tts_command is not None
        }
    
    def shutdown(self):
        """Shutdown voice service"""
        self.stop_speaking()
        self.voice_queue.put((None, 0))
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
        print("🔇 Simple TTS service shut down")

# Create global instance
def create_voice_service():
    """Create voice service instance"""
    return SimpleTTSService()
