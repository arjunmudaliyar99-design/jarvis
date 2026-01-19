"""
JARVIS Voice Module - Advanced Speech Recognition and Natural TTS
Handles voice input, language detection, and human-like speech output
"""
import logging
import speech_recognition as sr
import pyttsx3
import threading
from typing import Tuple, Optional
from deep_translator import GoogleTranslator
from langdetect import detect
from config import VOICE_CONFIG, USER_LANGUAGE

logger = logging.getLogger(__name__)


class JarvisVoiceSystem:
    """Advanced voice input/output system for JARVIS"""
    
    def __init__(self):
        """Initialize speech recognition and TTS with improved sensitivity"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configure recognizer with LOWER threshold for better sensitivity
        # Lower energy threshold = more sensitive to quiet speech
        self.recognizer.energy_threshold = 300  # Lowered from 3000 to 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = VOICE_CONFIG['pause_threshold']
        
        # Initialize TTS
        self.use_online_tts = VOICE_CONFIG['use_online_tts']
        if not self.use_online_tts:
            self._init_offline_tts()
        
        # Output language (Hindi by default)
        self.output_language = USER_LANGUAGE
        
        logger.info("✅ Voice system initialized")
        logger.info(f"🔊 TTS Mode: {'Online (gTTS)' if self.use_online_tts else 'Offline (pyttsx3)'}")
        logger.info(f"🌍 Output Language: {self.output_language}")
        logger.info(f"🎤 Energy Threshold: {self.recognizer.energy_threshold} (lower = more sensitive)")
    
    def _init_offline_tts(self):
        """Initialize pyttsx3 for offline TTS"""
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            
            # Select natural voice
            best_voice = None
            for voice in voices:
                if 'zira' in voice.name.lower() or 'david' in voice.name.lower():
                    best_voice = voice.id
                    break
            
            if best_voice:
                self.tts_engine.setProperty('voice', best_voice)
            elif len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            
            self.tts_engine.setProperty('rate', VOICE_CONFIG['rate'])
            self.tts_engine.setProperty('volume', VOICE_CONFIG['volume'])
            
            logger.info("✅ Offline TTS initialized")
        except Exception as e:
            logger.error(f"❌ TTS initialization failed: {e}")
            self.tts_engine = None
    
    def listen(self, timeout: int = 10) -> Tuple[Optional[str], Optional[str]]:
        """
        Listen to microphone and convert speech to text with improved error handling
        
        Args:
            timeout: Max time to wait for speech
            
        Returns:
            Tuple of (recognized_text, detected_language)
        """
        try:
            with self.microphone as source:
                logger.info("🎤 Listening for FULL sentence...")
                
                # Ambient noise adjustment - 1 second for better calibration
                logger.info("📊 Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                logger.info(f"🎚️ Energy threshold adjusted to: {self.recognizer.energy_threshold}")
                
                # Listen - capture full phrase
                logger.info("🎙️ Recording speech...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=VOICE_CONFIG['phrase_timeout']
                )
                
                logger.info("🔄 Processing speech...")
                
                # Recognize with multiple strategies
                text = None
                recognized_lang = None
                
                # Try English (India) first
                try:
                    text = self.recognizer.recognize_google(audio, language='en-IN')
                    recognized_lang = 'en'
                    logger.info(f"✅ RECOGNIZED [en-IN]: '{text}'")
                except sr.UnknownValueError:
                    logger.debug("❓ Not recognized as English (India)")
                except sr.RequestError as e:
                    logger.error(f"❌ Google API error (en-IN): {e}")
                except Exception as e:
                    logger.debug(f"en-IN recognition error: {e}")
                
                # Try Hindi if English failed
                if not text:
                    try:
                        text = self.recognizer.recognize_google(audio, language='hi-IN')
                        recognized_lang = 'hi'
                        logger.info(f"✅ RECOGNIZED [hi-IN]: '{text}'")
                    except sr.UnknownValueError:
                        logger.debug("❓ Not recognized as Hindi")
                    except sr.RequestError as e:
                        logger.error(f"❌ Google API error (hi-IN): {e}")
                    except Exception as e:
                        logger.debug(f"hi-IN recognition error: {e}")
                
                # Try English (US) as fallback
                if not text:
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        recognized_lang = 'en'
                        logger.info(f"✅ RECOGNIZED [en-US]: '{text}'")
                    except sr.UnknownValueError:
                        logger.warning("❓ Speech not understood in any language")
                    except sr.RequestError as e:
                        logger.error(f"❌ Google API error (en-US): {e}")
                    except Exception as e:
                        logger.debug(f"en-US recognition error: {e}")
                
                if not text:
                    logger.warning("⚠️ NO SPEECH RECOGNIZED - Try speaking louder and clearer")
                    return None, None
                
                # Detect language if not already set
                if not recognized_lang:
                    try:
                        recognized_lang = detect(text)
                    except:
                        recognized_lang = 'en'
                
                return text, recognized_lang
                
        except sr.WaitTimeoutError:
            logger.debug("⏰ No speech detected (timeout)")
            return None, None
        except sr.UnknownValueError:
            logger.warning("❓ Speech not understood - Try speaking more clearly")
            return None, None
        except Exception as e:
            logger.error(f"❌ Listen error: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def speak(self, text: str, language: Optional[str] = None, async_mode: bool = False):
        """
        Speak text with natural voice
        
        Args:
            text: Text to speak
            language: Language code (default: USER_LANGUAGE)
            async_mode: Speak in background thread
        """
        if not language:
            language = self.output_language
        
        logger.info(f"🔊 SPEAKING [{language}]: '{text[:100]}...'")
        
        if async_mode:
            thread = threading.Thread(
                target=self._speak_sync,
                args=(text, language)
            )
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text, language)
    
    def _speak_sync(self, text: str, language: str):
        """Internal synchronous speak method"""
        try:
            if self.use_online_tts:
                self._speak_online(text, language)
            else:
                self._speak_offline(text)
        except Exception as e:
            logger.error(f"❌ TTS error: {e}")
    
    def _speak_online(self, text: str, language: str):
        """Speak using gTTS (online, better quality)"""
        try:
            from gtts import gTTS
            import pygame
            import tempfile
            import os
            
            # Generate speech
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            tts.save(temp_path)
            
            # Play audio
            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Cleanup
            pygame.mixer.music.unload()
            os.unlink(temp_path)
            
            logger.info("✅ Speech completed")
            
        except ImportError:
            logger.error("❌ gTTS not installed. Run: pip install gtts")
            self._speak_offline(text)
        except Exception as e:
            logger.error(f"❌ Online TTS failed: {e}")
            self._speak_offline(text)
    
    def _speak_offline(self, text: str):
        """Speak using pyttsx3 (offline)"""
        try:
            if self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                logger.info("✅ Speech completed")
            else:
                logger.error("❌ TTS engine not available")
        except Exception as e:
            logger.error(f"❌ Offline TTS failed: {e}")
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if target_lang == 'en':
            return text
        
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated = translator.translate(text)
            logger.info(f"🌐 Translated to {target_lang}: {translated}")
            return translated
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return text
