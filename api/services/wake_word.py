"""
JARVIS AI Agent - Wake Word Detection Service
Listens for wake words like "hey jarvis", "god morgon jarvis", etc.
"""
import threading
import time
import re
from typing import List, Callable, Optional
import queue

try:
    import speech_recognition as sr
    import pyaudio
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ Speech recognition not available. Install: pip install SpeechRecognition pyaudio")

class WakeWordDetector:
    """Detects wake words and triggers JARVIS activation"""
    
    def __init__(self):
        self.wake_words = [
            r"hey\s+jarvis",
            r"hej\s+jarvis", 
            r"god\s+morgon\s+jarvis",
            r"god\s+kväll\s+jarvis",
            r"jarvis\s+wake\s+up",
            r"aktivera\s+jarvis",
            r"starta\s+jarvis"
        ]
        
        self.is_listening = False
        self.listen_thread = None
        self.callback = None
        self.recognizer = None
        self.microphone = None
        self.audio_queue = queue.Queue()
        
        if SPEECH_AVAILABLE:
            self.setup_audio()
        
    def setup_audio(self):
        """Setup audio input for wake word detection"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("🎤 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Microphone calibrated")
            
        except Exception as e:
            print(f"❌ Audio setup failed: {e}")
            self.recognizer = None
            self.microphone = None
    
    def set_callback(self, callback: Callable[[str], None]):
        """Set callback function to trigger when wake word is detected"""
        self.callback = callback
    
    def detect_wake_word(self, text: str) -> Optional[str]:
        """Check if text contains a wake word"""
        text_lower = text.lower()
        
        for pattern in self.wake_words:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return pattern
        return None
    
    def start_listening(self):
        """Start listening for wake words"""
        if not SPEECH_AVAILABLE:
            print("❌ Cannot start wake word detection: Speech recognition not available")
            return False
            
        if not self.recognizer or not self.microphone:
            print("❌ Cannot start wake word detection: Audio not properly setup")
            return False
            
        if self.is_listening:
            return True
            
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        print("👂 Wake word detection started. Say 'Hey Jarvis' to activate!")
        return True
    
    def stop_listening(self):
        """Stop listening for wake words"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("🔇 Wake word detection stopped")
    
    def _listen_loop(self):
        """Main listening loop"""
        while self.is_listening:
            try:
                # Listen for audio
                with self.microphone as source:
                    # Listen for 1 second, then process
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Process audio in background
                threading.Thread(
                    target=self._process_audio, 
                    args=(audio,), 
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
            except Exception as e:
                print(f"⚠️ Wake word detection error: {e}")
                time.sleep(1)
    
    def _process_audio(self, audio):
        """Process audio to detect wake words"""
        try:
            # Use Google Speech Recognition (free tier)
            text = self.recognizer.recognize_google(audio, language='sv-SE')
            print(f"🎤 Heard: '{text}'")
            
            # Check for wake word
            wake_word = self.detect_wake_word(text)
            if wake_word:
                print(f"🎯 Wake word detected: '{wake_word}'")
                
                # Extract command after wake word
                command = self._extract_command(text, wake_word)
                
                if self.callback:
                    self.callback(command)
                    
        except sr.UnknownValueError:
            # Speech not understood, ignore
            pass
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
    
    def _extract_command(self, text: str, wake_pattern: str) -> str:
        """Extract command text after wake word"""
        text_lower = text.lower()
        
        # Remove wake word from beginning
        for pattern in self.wake_words:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                # Get text after the wake word
                command = text[match.end():].strip()
                
                # If no command after wake word, use default greeting
                if not command:
                    return "Hej! Vad kan jag hjälpa dig med?"
                
                return command
        
        return text

# Mock wake word detector for systems without speech recognition
class MockWakeWordDetector:
    """Mock detector for testing without audio hardware"""
    
    def __init__(self):
        self.callback = None
        self.is_listening = False
        
    def set_callback(self, callback):
        self.callback = callback
        
    def start_listening(self):
        print("🎤 Mock wake word detector started")
        print("💡 Type 'hey jarvis [command]' to simulate wake word")
        self.is_listening = True
        return True
        
    def stop_listening(self):
        print("🔇 Mock wake word detector stopped") 
        self.is_listening = False
        
    def simulate_wake_word(self, text: str):
        """Simulate wake word detection for testing"""
        if self.callback and "jarvis" in text.lower():
            command = text.replace("hey jarvis", "").replace("hej jarvis", "").strip()
            if not command:
                command = "Hej! Vad kan jag hjälpa dig med?"
            self.callback(command)

# Factory function to create appropriate detector
def create_wake_word_detector() -> WakeWordDetector:
    """Create wake word detector based on available hardware"""
    if SPEECH_AVAILABLE:
        return WakeWordDetector()
    else:
        return MockWakeWordDetector()
