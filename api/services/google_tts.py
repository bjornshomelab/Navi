"""
JARVIS AI Agent - Google Cloud Text-to-Speech Service
High-quality voice synthesis using Google Cloud TTS
"""
import threading
import queue
import time
import tempfile
import os
from typing import Optional, Dict, Any

try:
    from google.cloud import texttospeech
    import pygame
    GOOGLE_TTS_AVAILABLE = True
    print("✅ Google Cloud Text-to-Speech available")
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    print("❌ Google Cloud Text-to-Speech not available")

class GoogleTTSService:
    """Text-to-Speech service using Google Cloud"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        self.client = None
        
        # Voice settings
        self.settings = {
            'language_code': 'sv-SE',  # Swedish
            'voice_name': 'sv-SE-Standard-A',  # Female Swedish voice
            'speaking_rate': 1.0,      # Normal speed
            'pitch': 0.0,              # Normal pitch
            'volume_gain_db': 0.0      # Normal volume
        }
        
        # Initialize Google TTS client
        self._initialize_client()
        
        # Initialize pygame mixer for audio playback
        self._initialize_audio()
        
        # Start voice processing thread
        self._start_voice_thread()
        
        if self.client:
            print("🔊 Google TTS service initialized successfully")
        else:
            print("❌ Google TTS service initialization failed")
    
    def _initialize_client(self):
        """Initialize Google Cloud TTS client"""
        if not GOOGLE_TTS_AVAILABLE:
            return
            
        try:
            # Check if credentials are available
            if os.path.exists("credentials.json"):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
            
            self.client = texttospeech.TextToSpeechClient()
            
            # Test the client with a simple request to verify it works
            self._test_client()
            
        except Exception as e:
            print(f"❌ Failed to initialize Google TTS client: {e}")
            self.client = None
    
    def _test_client(self):
        """Test Google TTS client connectivity"""
        try:
            # Create a simple test request
            text_input = texttospeech.SynthesisInput(text="Test")
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.settings['language_code'],
                name=self.settings['voice_name']
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            # Make a test request (don't actually play it)
            response = self.client.synthesize_speech(
                input=text_input,
                voice=voice,
                audio_config=audio_config
            )
            
            if response.audio_content:
                print("✅ Google TTS client test successful")
            else:
                raise Exception("Empty response from Google TTS")
                
        except Exception as e:
            print(f"❌ Google TTS client test failed: {e}")
            raise
    
    def _initialize_audio(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("✅ Audio playback initialized")
        except Exception as e:
            print(f"❌ Audio playback initialization failed: {e}")
    
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
        """Synthesize and play text using Google Cloud TTS"""
        try:
            if not self.client:
                print(f"🔊 JARVIS would say: '{text}'")
                return
            
            # Create synthesis input
            text_input = texttospeech.SynthesisInput(text=text)
            
            # Set voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.settings['language_code'],
                name=self.settings['voice_name']
            )
            
            # Set audio configuration
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.settings['speaking_rate'],
                pitch=self.settings['pitch'],
                volume_gain_db=self.settings['volume_gain_db']
            )
            
            # Make the TTS request
            response = self.client.synthesize_speech(
                input=text_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Play the audio
            self._play_audio(response.audio_content)
            
        except Exception as e:
            print(f"❌ TTS synthesis error: {e}")
            print(f"🔊 JARVIS would say: '{text}'")
    
    def _play_audio(self, audio_content: bytes):
        """Play audio content using pygame"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file.write(audio_content)
                tmp_file_path = tmp_file.name
            
            # Load and play audio
            pygame.mixer.music.load(tmp_file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
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
        
        # Stop pygame music
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        self.is_speaking = False
        print("🔇 Speech stopped")
    
    def set_voice_settings(self, **kwargs):
        """Update voice settings"""
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
        
        print(f"🎛️ Voice settings updated: {kwargs}")
    
    def get_available_voices(self) -> list:
        """Get list of available Swedish voices"""
        if not self.client:
            return []
        
        try:
            # Get list of voices
            voices = self.client.list_voices()
            
            # Filter for Swedish voices
            swedish_voices = []
            for voice in voices.voices:
                for lang_code in voice.language_codes:
                    if lang_code.startswith('sv'):
                        swedish_voices.append({
                            'name': voice.name,
                            'language_codes': list(voice.language_codes),
                            'ssml_gender': voice.ssml_gender.name
                        })
                        break
            
            return swedish_voices
            
        except Exception as e:
            print(f"❌ Failed to get voices: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current voice service status"""
        return {
            'engine': 'google_cloud_tts',
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'settings': self.settings.copy(),
            'client_available': self.client is not None,
            'audio_available': pygame.mixer.get_init() is not None
        }
    
    def shutdown(self):
        """Shutdown voice service"""
        self.stop_speaking()
        
        # Signal voice thread to stop
        self.voice_queue.put((None, 0))
        
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
        
        # Cleanup pygame
        try:
            pygame.mixer.quit()
        except:
            pass
        
        print("🔇 Google TTS service shut down")

# Factory function
def create_voice_service():
    """Create Google TTS voice service instance"""
    return GoogleTTSService()

# Fallback to simple TTS if Google TTS fails
def create_voice_service_with_fallback():
    """Create voice service with fallback to simple TTS"""
    try:
        service = GoogleTTSService()
        if service.client:
            return service
        else:
            print("⚠️ Google TTS failed, falling back to simple TTS")
            from .simple_tts import create_voice_service as create_simple
            return create_simple()
    except Exception as e:
        print(f"⚠️ Google TTS error ({e}), falling back to simple TTS")
        from .simple_tts import create_voice_service as create_simple
        return create_simple()
