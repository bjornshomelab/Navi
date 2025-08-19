"""
JARVIS AI Agent - Enhanced Voice Service
High-quality Swedish Text-to-Speech with multiple fallback options
"""
import threading
import queue
import time
import os
import tempfile
import subprocess
import json
from typing import Optional, Dict, Any, List
from urllib.parse import quote

class EnhancedVoiceService:
    """Enhanced Text-to-Speech service with high-quality Swedish voices"""
    
    def __init__(self):
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.speak_thread = None
        self.current_engine = None
        
        # Voice settings
        self.settings = {
            'language': 'sv-SE',
            'rate': 180,           # Words per minute
            'volume': 0.9,         # Volume (0.0 to 1.0)
            'pitch': 0,            # Pitch adjustment
            'voice_name': 'sv-SE-MattiasNeural',    # Manlig svensk röst
            'quality': 'high'      # high, medium, low
        }
        
        # Available TTS engines in order of preference for Swedish
        self.engines = []
        
        # Initialize TTS engines
        self._detect_engines()
        
        # Start voice processing thread
        self._start_voice_thread()
        
        if self.engines:
            print(f"🔊 Enhanced voice service initialized with {len(self.engines)} engines")
            print(f"🎤 Primary engine: {self.engines[0]['name']}")
        else:
            print("❌ No TTS engines available")
    
    def _detect_engines(self):
        """Detect and rank available TTS engines for Swedish"""
        
        # 1. Try Google Cloud TTS (highest quality for Swedish)
        if self._test_google_cloud_tts():
            self.engines.append({
                'name': 'google_cloud',
                'description': 'Google Cloud Text-to-Speech (Premium)',
                'quality': 'highest',
                'voices': ['sv-SE-Wavenet-C', 'sv-SE-Standard-C', 'sv-SE-Wavenet-A']  # Manliga röster först
            })
        
        # 2. Try Bing/Edge TTS (very good quality, free)
        if self._test_edge_tts():
            self.engines.append({
                'name': 'edge_tts',
                'description': 'Microsoft Edge Text-to-Speech',
                'quality': 'high',
                'voices': ['sv-SE-MattiasNeural', 'sv-SE-SofieNeural']  # Manlig först
            })
        
        # 3. Try Festival with Swedish voice
        if self._test_festival_swedish():
            self.engines.append({
                'name': 'festival_sv',
                'description': 'Festival with Swedish voice',
                'quality': 'medium',
                'voices': ['swedish']
            })
        
        # 4. Try espeak with Swedish
        if self._test_espeak():
            self.engines.append({
                'name': 'espeak',
                'description': 'eSpeak Swedish',
                'quality': 'medium',
                'voices': ['sv', 'sv+f3', 'sv+m3']
            })
        
        # 5. Try speech-dispatcher
        if self._test_speech_dispatcher():
            self.engines.append({
                'name': 'spd_say',
                'description': 'Speech Dispatcher',
                'quality': 'medium',
                'voices': ['swedish']
            })
        
        # 6. Try gTTS (Google Translate TTS) - requires internet
        if self._test_gtts():
            self.engines.append({
                'name': 'gtts',
                'description': 'Google Translate TTS',
                'quality': 'medium',
                'voices': ['sv']
            })
    
    def _test_google_cloud_tts(self) -> bool:
        """Test Google Cloud TTS availability"""
        try:
            # Check for service account credentials file
            cred_files = ['service-account.json', 'google-credentials.json', 'tts-credentials.json']
            cred_file = None
            
            for file in cred_files:
                if os.path.exists(file):
                    cred_file = file
                    break
            
            if not cred_file:
                print("ℹ️ Google Cloud TTS: No service account credentials found")
                return False
            
            # Try to import Google Cloud TTS
            from google.cloud import texttospeech
            
            # Set credentials
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_file
            
            # Quick test (don't actually make API call yet)
            client = texttospeech.TextToSpeechClient()
            print("✅ Google Cloud TTS available")
            return True
            
        except ImportError:
            print("ℹ️ Google Cloud TTS: Library not installed (pip install google-cloud-texttospeech)")
            return False
        except Exception as e:
            print(f"ℹ️ Google Cloud TTS: {e}")
            return False
    
    def _test_edge_tts(self) -> bool:
        """Test Microsoft Edge TTS availability"""
        try:
            import edge_tts
            print("✅ Microsoft Edge TTS available")
            return True
        except ImportError:
            # Try to install it
            try:
                subprocess.run(['pip', 'install', 'edge-tts'], 
                             capture_output=True, check=True, timeout=30)
                import edge_tts
                print("✅ Microsoft Edge TTS installed and available")
                return True
            except:
                print("ℹ️ Microsoft Edge TTS: Not available (pip install edge-tts)")
                return False
        except Exception as e:
            print(f"ℹ️ Microsoft Edge TTS: {e}")
            return False
    
    def _test_festival_swedish(self) -> bool:
        """Test Festival with Swedish voice"""
        try:
            # Check if festival is installed
            result = subprocess.run(['which', 'festival'], 
                                  capture_output=True, timeout=2)
            if result.returncode != 0:
                return False
            
            # Check for Swedish voice
            # Festival Swedish voices are usually in /usr/share/festival/voices/
            swedish_voice_paths = [
                '/usr/share/festival/voices/swedish/',
                '/usr/local/share/festival/voices/swedish/'
            ]
            
            for path in swedish_voice_paths:
                if os.path.exists(path):
                    print("✅ Festival with Swedish voice available")
                    return True
            
            print("ℹ️ Festival: No Swedish voice found")
            return False
            
        except Exception:
            return False
    
    def _test_espeak(self) -> bool:
        """Test espeak availability"""
        try:
            result = subprocess.run(['which', 'espeak'], 
                                  capture_output=True, timeout=2)
            if result.returncode == 0:
                print("✅ eSpeak available")
                return True
        except:
            pass
        return False
    
    def _test_speech_dispatcher(self) -> bool:
        """Test speech-dispatcher availability"""
        try:
            result = subprocess.run(['which', 'spd-say'], 
                                  capture_output=True, timeout=2)
            if result.returncode == 0:
                print("✅ Speech Dispatcher available")
                return True
        except:
            pass
        return False
    
    def _test_gtts(self) -> bool:
        """Test Google Translate TTS availability"""
        try:
            import gtts
            print("✅ Google Translate TTS available")
            return True
        except ImportError:
            return False
    
    def _start_voice_thread(self):
        """Start background thread for voice processing"""
        self.speak_thread = threading.Thread(target=self._voice_worker, daemon=True)
        self.speak_thread.start()
    
    def _voice_worker(self):
        """Background worker for processing voice requests"""
        while True:
            try:
                item = self.voice_queue.get(timeout=1)
                if item is None:  # Shutdown signal
                    break
                
                text, priority = item
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
        """Speak text using the best available engine"""
        if not text.strip():
            return
        
        # Try engines in order of preference
        for engine in self.engines:
            try:
                if self._speak_with_engine(text, engine):
                    return
            except Exception as e:
                print(f"❌ Engine {engine['name']} failed: {e}")
                continue
        
        print("❌ All TTS engines failed")
    
    def _speak_with_engine(self, text: str, engine: Dict) -> bool:
        """Speak text using a specific engine"""
        engine_name = engine['name']
        
        if engine_name == 'google_cloud':
            return self._speak_google_cloud(text, engine)
        elif engine_name == 'edge_tts':
            return self._speak_edge_tts(text, engine)
        elif engine_name == 'festival_sv':
            return self._speak_festival(text, engine)
        elif engine_name == 'espeak':
            return self._speak_espeak(text, engine)
        elif engine_name == 'spd_say':
            return self._speak_speech_dispatcher(text, engine)
        elif engine_name == 'gtts':
            return self._speak_gtts(text, engine)
        
        return False
    
    def _speak_google_cloud(self, text: str, engine: Dict) -> bool:
        """Speak using Google Cloud TTS"""
        try:
            from google.cloud import texttospeech
            import pygame
            
            client = texttospeech.TextToSpeechClient()
            
            # Configure voice
            voice_name = self.settings.get('voice_name') or engine['voices'][0]
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.settings['language'],
                name=voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.settings['rate'] / 180.0,  # Convert to rate (0.25-4.0)
                pitch=self.settings['pitch'],
                volume_gain_db=(self.settings['volume'] - 0.5) * 20  # Convert to dB
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Play audio using pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                f.write(response.audio_content)
                temp_file = f.name
            
            try:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                return True
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            print(f"❌ Google Cloud TTS error: {e}")
            return False
    
    def _speak_edge_tts(self, text: str, engine: Dict) -> bool:
        """Speak using Microsoft Edge TTS"""
        try:
            import edge_tts
            import asyncio
            import pygame
            
            voice_name = self.settings.get('voice_name') or engine['voices'][0]
            
            async def synthesize():
                communicate = edge_tts.Communicate(text, voice_name)
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    temp_file = f.name
                
                await communicate.save(temp_file)
                return temp_file
            
            # Run async synthesis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            temp_file = loop.run_until_complete(synthesize())
            loop.close()
            
            # Play audio
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            try:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                return True
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return False
    
    def _speak_festival(self, text: str, engine: Dict) -> bool:
        """Speak using Festival"""
        try:
            # Create Festival script
            script = f'(voice_cmu_us_slt_arctic_hts)\n(SayText "{text}")'
            
            result = subprocess.run(['festival', '--batch'], 
                                  input=script, text=True, 
                                  capture_output=True, timeout=10)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Festival error: {e}")
            return False
    
    def _speak_espeak(self, text: str, engine: Dict) -> bool:
        """Speak using eSpeak"""
        try:
            voice = self.settings.get('voice_name') or 'sv'
            rate = self.settings['rate']
            
            cmd = ['espeak', '-v', voice, '-s', str(rate), text]
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ eSpeak error: {e}")
            return False
    
    def _speak_speech_dispatcher(self, text: str, engine: Dict) -> bool:
        """Speak using Speech Dispatcher"""
        try:
            cmd = ['spd-say', '-l', 'sv', text]
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Speech Dispatcher error: {e}")
            return False
    
    def _speak_gtts(self, text: str, engine: Dict) -> bool:
        """Speak using Google Translate TTS"""
        try:
            from gtts import gTTS
            import pygame
            
            tts = gTTS(text=text, lang='sv', slow=False)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_file = f.name
            
            tts.save(temp_file)
            
            # Play audio
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            try:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                return True
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            return False
    
    def speak(self, text: str, priority: int = 1):
        """Add text to voice queue"""
        if text and text.strip():
            self.voice_queue.put((text.strip(), priority))
    
    def stop(self):
        """Stop current speech and clear queue"""
        # Clear queue
        while not self.voice_queue.empty():
            try:
                self.voice_queue.get_nowait()
            except queue.Empty:
                break
        
        # Stop pygame if playing
        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except:
            pass
        
        self.is_speaking = False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current voice service status"""
        return {
            'is_speaking': self.is_speaking,
            'queue_size': self.voice_queue.qsize(),
            'engines': [
                {
                    'name': engine['name'],
                    'description': engine['description'],
                    'quality': engine['quality'],
                    'voices': engine['voices']
                }
                for engine in self.engines
            ],
            'current_engine': self.engines[0]['name'] if self.engines else None,
            'settings': self.settings
        }
    
    def get_voices(self) -> List[Dict[str, Any]]:
        """Get available voices"""
        voices = []
        for engine in self.engines:
            for voice in engine['voices']:
                voices.append({
                    'name': voice,
                    'engine': engine['name'],
                    'description': engine['description'],
                    'quality': engine['quality'],
                    'language': 'sv-SE'
                })
        return voices
    
    def set_voice(self, voice_name: str):
        """Set specific voice"""
        self.settings['voice_name'] = voice_name
    
    def set_settings(self, **kwargs):
        """Update voice settings"""
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
    
    def shutdown(self):
        """Shutdown voice service"""
        self.voice_queue.put(None)  # Shutdown signal
        if self.speak_thread:
            self.speak_thread.join(timeout=2)
