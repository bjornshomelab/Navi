"""
JARVIS AI Agent - Text-to-Speech Service
Provides voice output for JARVIS responses
"""
import threading
import time
import os
import tempfile
from typing import Optional, Dict, Any
import queue

# TTS Engine priorities (in order of preference)
TTS_ENGINES = []

# Try different TTS engines in order of preference
# Try different TTS engines in order of preference
try:
    # Skip pyttsx3 for now as it may hang on some systems
    # import pyttsx3
    # TTS_ENGINES.append('pyttsx3')
    # print("✅ pyttsx3 TTS engine available")
    pass
except ImportError:
    pass

try:
    import gtts
    TTS_ENGINES.append('gtts')
    print("✅ Google TTS (gTTS) engine available")
except ImportError:
    pass

try:
    # Check for espeak system command
    import subprocess
    result = subprocess.run(['which', 'espeak'], capture_output=True)
    if result.returncode == 0:
        TTS_ENGINES.append('espeak')
        print("✅ espeak TTS engine available")
except:
    pass

try:
    # Check for festival system command
    import subprocess
    result = subprocess.run(['which', 'festival'], capture_output=True)
    if result.returncode == 0:
        TTS_ENGINES.append('festival')
        print("✅ festival TTS engine available")
except:
    pass

if not TTS_ENGINES:
    print("⚠️ No TTS engines available. Install: pip install pyttsx3 gtts")

class VoiceService:
    """Text-to-Speech service for JARVIS"""
    
    def __init__(self, engine_preference: Optional[str] = None):
        self.engine = None
        self.engine_name = None
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        
        # Voice settings
        self.settings = {
            'rate': 180,        # Words per minute
            'volume': 0.9,      # Volume (0.0 to 1.0)
            'voice_id': None,   # Specific voice ID
            'language': 'sv'    # Language code
        }
        
        # Initialize TTS engine
        self._initialize_engine(engine_preference)
        
        # Start voice processing thread
        self._start_voice_thread()
    
    def _initialize_engine(self, preferred_engine: Optional[str] = None):
        """Initialize the best available TTS engine"""
        engines_to_try = [preferred_engine] if preferred_engine else TTS_ENGINES
        
        for engine_name in engines_to_try:
            if engine_name not in TTS_ENGINES:
                continue
                
            try:
                if engine_name == 'pyttsx3':
                    self._init_pyttsx3()
                elif engine_name == 'gtts':
                    self._init_gtts()
                elif engine_name == 'espeak':
                    self._init_espeak()
                elif engine_name == 'festival':
                    self._init_festival()
                
                self.engine_name = engine_name
                print(f"🔊 Voice service initialized with {engine_name}")
                return
                
            except Exception as e:
                print(f"❌ Failed to initialize {engine_name}: {e}")
                continue
        
        print("❌ No TTS engine could be initialized")
        self.engine_name = 'none'
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine"""
        try:
            import pyttsx3
            import os
            import threading
            import time
            
            # Set display variable for headless systems
            if 'DISPLAY' not in os.environ:
                os.environ['DISPLAY'] = ':0'
            
            # Initialize in a separate thread to avoid hanging
            engine_container = {'engine': None, 'error': None}
            
            def init_engine():
                try:
                    engine_container['engine'] = pyttsx3.init(driverName='espeak')
                except:
                    try:
                        engine_container['engine'] = pyttsx3.init()
                    except Exception as e:
                        engine_container['error'] = str(e)
            
            thread = threading.Thread(target=init_engine)
            thread.daemon = True
            thread.start()
            thread.join(timeout=5)  # 5 second timeout
            
            if engine_container['error']:
                raise Exception(engine_container['error'])
            
            if not engine_container['engine']:
                raise Exception("pyttsx3 initialization timed out")
                
            self.engine = engine_container['engine']
            
            # Configure pyttsx3 settings
            self.engine.setProperty('rate', self.settings['rate'])
            self.engine.setProperty('volume', self.settings['volume'])
            
            # Try to find a Swedish voice
            voices = self.engine.getProperty('voices')
            if voices:
                swedish_voice = None
                
                for voice in voices:
                    if hasattr(voice, 'id') and voice.id:
                        voice_id = voice.id.lower()
                        if 'sv' in voice_id or 'swedish' in voice_id:
                            swedish_voice = voice.id
                            break
                        elif 'en' in voice_id and not swedish_voice:
                            # Fallback to English if no Swedish found
                            swedish_voice = voice.id
                
                if swedish_voice:
                    self.engine.setProperty('voice', swedish_voice)
                    print(f"🎤 Selected voice: {swedish_voice}")
            
        except Exception as e:
            print(f"❌ pyttsx3 initialization failed: {e}")
            raise
    
    def _init_gtts(self):
        """Initialize Google TTS"""
        # gTTS doesn't need initialization, just mark as available
        self.engine = 'gtts'
    
    def _init_espeak(self):
        """Initialize espeak"""
        self.engine = 'espeak'
    
    def _init_festival(self):
        """Initialize festival"""
        self.engine = 'festival'
    
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
        """Actually speak the text using the configured engine"""
        try:
            if self.engine_name == 'pyttsx3':
                self.engine.say(text)
                self.engine.runAndWait()
                
            elif self.engine_name == 'gtts':
                self._speak_with_gtts(text)
                
            elif self.engine_name == 'espeak':
                self._speak_with_espeak(text)
                
            elif self.engine_name == 'festival':
                self._speak_with_festival(text)
                
            else:
                print(f"🔊 JARVIS would say: '{text}'")
                
        except Exception as e:
            print(f"❌ Speech error: {e}")
            print(f"🔊 JARVIS would say: '{text}'")
    
    def _speak_with_gtts(self, text: str):
        """Speak using Google TTS"""
        try:
            from gtts import gTTS
            import pygame
            
            # Create temporary audio file
            tts = gTTS(text=text, lang=self.settings['language'], slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_filename = tmp_file.name
                tts.save(tmp_filename)
            
            # Play the audio file
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Cleanup
            pygame.mixer.quit()
            os.unlink(tmp_filename)
            
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            raise
    
    def _speak_with_espeak(self, text: str):
        """Speak using espeak"""
        import subprocess
        
        cmd = [
            'espeak', 
            '-s', str(self.settings['rate']),  # Speed
            '-v', f"{self.settings['language']}",  # Voice/language
            text
        ]
        
        subprocess.run(cmd, capture_output=True)
    
    def _speak_with_festival(self, text: str):
        """Speak using festival"""
        import subprocess
        
        # Festival expects text via stdin
        process = subprocess.Popen(
            ['festival', '--tts'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        process.communicate(input=text)
    
    def speak(self, text: str, priority: int = 1, interrupt: bool = False):
        """Add text to speech queue"""
        if not text.strip():
            return
        
        if interrupt:
            # Clear queue and stop current speech
            self.stop_speaking()
            
        # Add to queue
        self.voice_queue.put((text, priority))
        print(f"🔊 Queued for speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def speak_immediately(self, text: str):
        """Speak text immediately, interrupting current speech"""
        self.speak(text, priority=0, interrupt=True)
    
    def stop_speaking(self):
        """Stop current speech and clear queue"""
        # Clear the queue
        while not self.voice_queue.empty():
            try:
                self.voice_queue.get_nowait()
                self.voice_queue.task_done()
            except queue.Empty:
                break
        
        # Stop current speech if using pyttsx3
        if self.engine_name == 'pyttsx3' and self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        self.is_speaking = False
        print("🔇 Speech stopped")
    
    def set_voice_settings(self, **kwargs):
        """Update voice settings"""
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
                
                # Apply settings to pyttsx3 if active
                if self.engine_name == 'pyttsx3' and self.engine:
                    if key == 'rate':
                        self.engine.setProperty('rate', value)
                    elif key == 'volume':
                        self.engine.setProperty('volume', value)
                    elif key == 'voice_id':
                        self.engine.setProperty('voice', value)
        
        print(f"🎛️ Voice settings updated: {kwargs}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if self.engine_name == 'pyttsx3' and self.engine:
            voices = self.engine.getProperty('voices')
            return [{'id': v.id, 'name': v.name, 'language': getattr(v, 'languages', [])} for v in voices]
        
        return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current voice service status"""
        return {
            'engine': self.engine_name,
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'settings': self.settings.copy(),
            'available_engines': TTS_ENGINES
        }
    
    def shutdown(self):
        """Shutdown voice service"""
        self.stop_speaking()
        
        # Signal voice thread to stop
        self.voice_queue.put((None, 0))
        
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
        
        print("🔇 Voice service shut down")

# Global voice service instance
voice_service = VoiceService()
