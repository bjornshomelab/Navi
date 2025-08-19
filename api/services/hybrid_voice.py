"""
JARVIS AI Agent - Hybrid Voice Service
Tries Google TTS first, falls back to simple TTS
"""
import threading
import queue
import subprocess

class HybridVoiceService:
    """Voice service that tries Google TTS, falls back to simple TTS"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        self.use_google = False
        self.google_service = None
        self.tts_command = None
        
        # Try to initialize Google TTS
        self._try_google_tts()
        
        # If Google TTS fails, find system TTS command
        if not self.use_google:
            self._find_system_tts()
        
        # Start voice processing thread
        self._start_voice_thread()
        
        engine_name = "Google Cloud TTS" if self.use_google else f"System TTS ({self.tts_command})"
        print(f"🔊 Hybrid voice service initialized with {engine_name}")
    
    def _try_google_tts(self):
        """Try to initialize Google TTS"""
        try:
            import os
            if not os.path.exists('credentials.json'):
                print("⚠️ credentials.json not found, skipping Google TTS")
                return
            
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
            
            # Import and test without hanging
            from google.cloud import texttospeech
            import pygame
            
            # Quick test without full initialization
            print("🎤 Testing Google TTS...")
            
            # For now, skip Google TTS to avoid hanging and use system TTS
            # self.google_service = GoogleTTSService()
            # self.use_google = True
            print("⚠️ Google TTS temporarily disabled to avoid hanging")
            
        except Exception as e:
            print(f"⚠️ Google TTS initialization failed: {e}")
    
    def _find_system_tts(self):
        """Find available system TTS command"""
        commands_to_test = ['spd-say', 'espeak', 'festival', 'say']
        
        for cmd in commands_to_test:
            try:
                result = subprocess.run(['which', cmd], capture_output=True, timeout=2)
                if result.returncode == 0:
                    self.tts_command = cmd
                    print(f"✅ Found system TTS command: {cmd}")
                    return
            except:
                continue
        
        print("❌ No system TTS command found")
    
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
                print(f"❌ Voice worker error: {e}")
                self.is_speaking = False
    
    def _speak_text(self, text: str):
        """Speak text using available TTS engine"""
        try:
            if self.use_google and self.google_service:
                self.google_service._speak_text(text)
            elif self.tts_command:
                self._speak_with_system(text)
            else:
                print(f"🔊 JARVIS would say: '{text}'")
        except Exception as e:
            print(f"❌ TTS error: {e}")
            print(f"🔊 JARVIS would say: '{text}'")
    
    def _speak_with_system(self, text: str):
        """Speak using system TTS command"""
        try:
            if self.tts_command == 'spd-say':
                subprocess.run(['spd-say', text], timeout=30)
            elif self.tts_command == 'espeak':
                subprocess.run(['espeak', '-s', '180', text], timeout=30)
            elif self.tts_command == 'say':  # macOS
                subprocess.run(['say', text], timeout=30)
            elif self.tts_command == 'festival':
                subprocess.run(['echo', text], stdout=subprocess.PIPE, text=True)
                subprocess.run(['festival', '--tts'], input=text, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            print("❌ TTS timeout")
        except Exception as e:
            print(f"❌ System TTS error: {e}")
    
    def speak(self, text: str, priority: int = 1, interrupt: bool = False):
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
        
        # Stop current speech
        if self.use_google and self.google_service:
            self.google_service.stop_speaking()
        else:
            # Kill system TTS processes
            try:
                subprocess.run(['pkill', '-f', 'spd-say'], timeout=2)
                subprocess.run(['pkill', '-f', 'espeak'], timeout=2)
            except:
                pass
        
        self.is_speaking = False
        print("🔇 Speech stopped")
    
    def get_status(self):
        """Get current voice service status"""
        return {
            'engine': 'google_tts' if self.use_google else 'system_tts',
            'command': self.tts_command if not self.use_google else None,
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'google_available': self.use_google,
            'system_available': self.tts_command is not None
        }
    
    def get_available_voices(self):
        """Get available voices"""
        if self.use_google and self.google_service:
            return self.google_service.get_available_voices()
        else:
            return []
    
    def set_voice_settings(self, **kwargs):
        """Update voice settings"""
        if self.use_google and self.google_service:
            self.google_service.set_voice_settings(**kwargs)
        else:
            print(f"🎛️ Voice settings not supported for system TTS")
    
    def shutdown(self):
        """Shutdown voice service"""
        self.stop_speaking()
        self.voice_queue.put((None, 0))
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
        
        if self.use_google and self.google_service:
            self.google_service.shutdown()
        
        print("🔇 Hybrid voice service shut down")

# Factory function
def create_voice_service():
    """Create hybrid voice service"""
    return HybridVoiceService()
