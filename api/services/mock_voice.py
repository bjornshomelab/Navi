"""
JARVIS AI Agent -class EnhancedVoiceService:
    """Enhanced voice service with Google Cloud TTS and system fallback"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        self.use_google_tts = False
        self.google_client = None
        
        # Google TTS settings
        self.google_settings = {
            'language_code': 'sv-SE',
            'voice_name': 'sv-SE-Standard-A',  # Natural Swedish female voice
            'speaking_rate': 1.0,
            'pitch': 0.0,
            'volume_gain_db': 0.0
        }
        
        # Try to initialize Google TTS
        self._try_google_tts()
        
        # Initialize pygame for audio playback if using Google TTS
        if self.use_google_tts:
            self._init_pygame()
        
        # Start voice processing thread
        self._start_voice_thread()
        
        engine_name = "Google Cloud TTS (naturlig svenska)" if self.use_google_tts else "System TTS"
        print(f"🔊 Enhanced voice service initialized with {engine_name}")
    
    def _try_google_tts(self):
        """Try to initialize Google Cloud TTS"""
        if not GOOGLE_TTS_AVAILABLE:
            return
            
        try:
            # Check for credentials
            if not os.path.exists('credentials.json'):
                print("⚠️ credentials.json not found - using system TTS")
                return
            
            # Set credentials
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
            
            # Create client
            self.google_client = texttospeech.TextToSpeechClient()
            
            # Test with a quick synthesis
            self._test_google_tts()
            
            self.use_google_tts = True
            print("✅ Google Cloud TTS initialized - naturlig svenska röst aktiverad")
            
        except Exception as e:
            print(f"⚠️ Google TTS initialization failed: {e}")
            print("⚠️ Falling back to system TTS")
            self.use_google_tts = False
    
    def _test_google_tts(self):
        """Test Google TTS connectivity"""
        try:
            # Create a minimal test request
            text_input = texttospeech.SynthesisInput(text="Test")
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.google_settings['language_code'],
                name=self.google_settings['voice_name']
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.google_settings['speaking_rate']
            )
            
            # Test synthesis
            response = self.google_client.synthesize_speech(
                input=text_input,
                voice=voice,
                audio_config=audio_config
            )
            
            if not response.audio_content:
                raise Exception("Empty audio response")
                
        except Exception as e:
            print(f"❌ Google TTS test failed: {e}")
            raise
    
    def _init_pygame(self):
        """Initialize pygame mixer for audio playback"""
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("✅ Audio playback (pygame) initialized")
        except Exception as e:
            print(f"❌ Audio playback initialization failed: {e}")
            self.use_google_tts = Falseice Service
Provides natural Swedish voice using Google Cloud TTS with fallback to system TTS
"""
import threading
import queue
import time
import subprocess
import tempfile
import os

# Try to import Google Cloud TTS
try:
    from google.cloud import texttospeech
    import pygame
    GOOGLE_TTS_AVAILABLE = True
    print("✅ Google Cloud TTS available")
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    print("⚠️ Google Cloud TTS not available - falling back to system TTS")

class EnhancedVoiceService:
    """Mock voice service that just prints what would be spoken"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        
        # Start voice processing thread
        self._start_voice_thread()
        
        print("🔊 Mock voice service initialized")
    
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
        """Speak text using system TTS and print to console"""
        print(f"🔊 JARVIS says: '{text}'")
        
        # Try to use system TTS for actual audio output
        try:
            import subprocess
            # Use spd-say with Swedish voice if available
            subprocess.run([
                'spd-say', 
                '-l', 'sv',  # Swedish language
                '-r', '10',  # Slightly faster rate
                '-p', '10',  # Slightly higher pitch
                text
            ], timeout=30, capture_output=True)
        except Exception as e:
            # Fallback to just timing simulation
            print(f"⚠️ TTS audio failed: {e}")
            time.sleep(len(text) * 0.05)  # ~20 chars per second
    
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
        
        self.is_speaking = False
        print("🔇 Speech stopped")
    
    def get_status(self):
        """Get current voice service status"""
        return {
            'engine': 'mock_voice',
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'available': True
        }
    
    def get_available_voices(self):
        """Get available voices"""
        return [
            {'name': 'JARVIS-Mock', 'language': 'sv-SE', 'gender': 'neutral'}
        ]
    
    def set_voice_settings(self, **kwargs):
        """Update voice settings"""
        print(f"🎛️ Mock voice settings updated: {kwargs}")
    
    def shutdown(self):
        """Shutdown voice service"""
        self.stop_speaking()
        self.voice_queue.put((None, 0))
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
        print("🔇 Mock voice service shut down")

# Factory function
def create_voice_service():
    """Create mock voice service"""
    return MockVoiceService()
