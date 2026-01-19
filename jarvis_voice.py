"""
JARVIS Voice Module - Multilingual Speech Recognition and Text-to-Speech
Handles voice input, language detection, translation, and speech output
"""

import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import os
import threading
import logging
from constants import VOICE

# Make language detection deterministic
DetectorFactory.seed = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JarvisVoice:
    """Multilingual voice assistant for speech recognition and TTS"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize pyttsx3 for natural human-like voice TTS
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS with natural voice (prefer female for better quality)
        voices = self.tts_engine.getProperty('voices')
        logger.info(f"🔊 Available voices: {len(voices)}")
        
        # Try to find best natural voice (prefer Zira - female, or David - male)
        best_voice = None
        for voice in voices:
            logger.info(f"  - {voice.name}")
            # Prefer Zira (natural female) or David (natural male)
            if 'zira' in voice.name.lower() or 'david' in voice.name.lower():
                best_voice = voice.id
                logger.info(f"✅ Selected voice: {voice.name}")
                break
        
        if not best_voice and len(voices) > 1:
            best_voice = voices[1].id  # Usually second voice is better quality
            logger.info(f"✅ Using second voice: {voices[1].name}")
        elif not best_voice and len(voices) > 0:
            best_voice = voices[0].id
            logger.info(f"✅ Using default voice: {voices[0].name}")
        
        if best_voice:
            self.tts_engine.setProperty('voice', best_voice)
        
        # Set speech rate (170 is natural conversational pace) and volume
        self.tts_engine.setProperty('rate', 165)  # Slightly slower for clarity
        self.tts_engine.setProperty('volume', 1.0)  # Max volume for clear output
        
        # Configure recognizer for better accuracy - using constants
        self.recognizer.energy_threshold = VOICE.get('energy_threshold', 3000)
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = VOICE.get('pause_threshold', 0.8)
        
        # Supported languages (ISO 639-1 codes) - Indian languages priority
        self.supported_languages = {
            'ta': 'Tamil',  # Priority language
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'or': 'Odia',
            'as': 'Assamese',
            'ur': 'Urdu',
            'hi': 'Hindi',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh-cn': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'ru': 'Russian',
            'pt': 'Portuguese',
            'it': 'Italian'
        }
        
        # User personalization
        self.user_name = 'Arjun'
        self.wake_word = 'jarvis'
        self.is_listening_continuous = False
        self.default_output_language = 'hi'  # Hindi - JARVIS speaks in Hindi
        
        logger.info("✅ JARVIS Voice Module Initialized")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen to microphone and convert speech to text
        
        Args:
            timeout: Time to wait for speech to start
            phrase_time_limit: Maximum time for phrase
            
        Returns:
            tuple: (text, detected_language) or (None, None) on failure
        """
        try:
            with self.microphone as source:
                logger.info("🎤 Listening for your voice...")
                
                # Adjust for ambient noise (important for noise reduction)
                logger.info("🔧 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                logger.info(f"🎯 Microphone energy threshold: {self.recognizer.energy_threshold}")
                logger.info("✅ Ready! Speak now...")
                
                # Listen for audio with proper timeouts
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("🔄 Processing speech... Please wait...")
                
                # Try to recognize speech with Indian languages support
                text = None
                recognized_with = None
                
                # Try multiple recognition strategies
                try:
                    # Strategy 1: Indian English (best for Indian accent)
                    text = self.recognizer.recognize_google(audio, language='en-IN')
                    recognized_with = 'en-IN (Indian English)'
                except Exception as e:
                    logger.warning(f"Indian English recognition failed: {e}")
                    try:
                        # Strategy 2: US English
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        recognized_with = 'en-US (US English)'
                    except Exception as e2:
                        logger.warning(f"US English recognition failed: {e2}")
                        try:
                            # Strategy 3: Auto-detect
                            text = self.recognizer.recognize_google(audio)
                            recognized_with = 'auto-detect'
                        except Exception as e3:
                            logger.error(f"All recognition strategies failed: {e3}")
                            raise
                
                if not text:
                    logger.error("❌ No text recognized")
                    return None, None
                
                # Detect language from recognized text
                try:
                    detected_lang = detect(text)
                    # Force English if detection is unreliable
                    if detected_lang not in ['en', 'hi', 'ta', 'te', 'ml', 'kn', 'bn', 'mr', 'gu', 'pa']:
                        detected_lang = 'en'
                except:
                    detected_lang = 'en'
                
                logger.info(f"✅ RECOGNIZED [{detected_lang}] via {recognized_with}: '{text}'")
                return text, detected_lang
                
        except sr.WaitTimeoutError:
            logger.warning("⏰ No speech detected within timeout")
            return None, None
            
        except sr.UnknownValueError:
            logger.warning("❌ Could not understand speech")
            return None, None
            
        except sr.RequestError as e:
            logger.error(f"❌ Speech recognition service error: {e}")
            return None, None
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in listen(): {e}")
            return None, None
    
    def translate_to_english(self, text, source_lang):
        """
        Translate text to English for internal processing
        
        Args:
            text: Text to translate
            source_lang: Source language code
            
        Returns:
            str: Translated English text
        """
        if source_lang == 'en':
            return text
        
        try:
            translated = GoogleTranslator(source=source_lang, target='en').translate(text)
            logger.info(f"🌐 Translated to English: {translated}")
            return translated
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return text  # Return original if translation fails
    
    def translate_from_english(self, text, target_lang):
        """
        Translate English response back to target language
        
        Args:
            text: English text to translate
            target_lang: Target language code
            
        Returns:
            str: Translated text
        """
        if target_lang == 'en':
            return text
        
        try:
            translated = GoogleTranslator(source='en', target=target_lang).translate(text)
            logger.info(f"🌐 Translated to {target_lang}: {translated}")
            return translated
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return text
    
    def speak(self, text, lang='en', async_mode=False):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            lang: Language code (ISO 639-1)
            async_mode: If True, speak in background thread (default False for reliability)
        """
        logger.info(f"🔊 SPEAKING [{lang}]: '{text}'")
        
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text, lang))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text, lang)
            logger.info("✅ Speech completed")
    
    def _speak_sync(self, text, lang):
        """Internal synchronous speak method using pyttsx3"""
        try:
            
            # Always use English male voice for best quality
            # pyttsx3 has excellent English male voices
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"❌ TTS error: {e}")
                # Retry once
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except:
                    pass
                
        except Exception as e:
            logger.error(f"❌ TTS error: {e}")
    
    def process_multilingual_command(self, callback=None):
        """
        Complete multilingual voice processing pipeline:
        1. Listen to user speech
        2. Detect language
        3. Translate to English for processing
        4. Get response (from callback)
        5. Translate response back to user's language
        6. Speak response
        
        Args:
            callback: Function to process English command and return response
                      Should accept (english_text) and return response_text
                      
        Returns:
            dict: {
                'user_text': original text,
                'user_lang': detected language,
                'english_text': translated to English,
                'response_english': response in English,
                'response_user_lang': response in user's language,
                'success': bool
            }
        """
        result = {
            'user_text': None,
            'user_lang': None,
            'english_text': None,
            'response_english': None,
            'response_user_lang': None,
            'success': False
        }
        
        # Step 1: Listen
        user_text, user_lang = self.listen()
        if not user_text:
            return result
        
        result['user_text'] = user_text
        result['user_lang'] = user_lang
        
        # Step 2: Translate to English
        english_text = self.translate_to_english(user_text, user_lang)
        result['english_text'] = english_text
        
        # Step 3: Process command
        if callback:
            try:
                response = callback(english_text)
                
                # Handle dict response (for exit flags, etc.)
                if isinstance(response, dict):
                    response_english = response.get('response', 'Command processed.')
                    # Pass through any flags like exit_requested
                    for key, value in response.items():
                        if key != 'response':
                            result[key] = value
                else:
                    response_english = response
                    
            except Exception as e:
                logger.error(f"❌ Callback error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                response_english = "I encountered an error processing your request."
        else:
            response_english = "Command received successfully."
        
        result['response_english'] = response_english
        
        # Step 4: Translate response to Hindi (JARVIS always speaks Hindi)
        response_hindi = self.translate_from_english(response_english, 'hi')
        result['response_user_lang'] = response_hindi
        result['response_hindi'] = response_hindi
        
        # Step 5: Speak response in Hindi
        self.speak(response_hindi, lang='hi', async_mode=False)
        
        result['success'] = True
        return result
    
    def get_language_name(self, lang_code):
        """Get human-readable language name"""
        return self.supported_languages.get(lang_code, lang_code.upper())
    
    def detect_wake_word(self, text):
        """Check if wake word 'jarvis' is in the text"""
        if not text:
            return False
        text_lower = text.lower()
        wake_words = ['jarvis', 'jarvis', 'hello jarvis', 'hey jarvis', 'hi jarvis']
        return any(word in text_lower for word in wake_words)
    
    def listen_for_wake_word(self, timeout=3):
        """Listen specifically for wake word with better logging"""
        try:
            logger.info("👂 Waiting for wake word...")
            
            with self.microphone as source:
                # Quick ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
                
                try:
                    # Try Indian English first
                    text = self.recognizer.recognize_google(audio, language='en-IN')
                    logger.info(f"🔍 Heard: '{text}'")
                    
                    if self.detect_wake_word(text):
                        logger.info(f"🎯 WAKE WORD DETECTED: '{text}'")
                        return True
                    else:
                        logger.info(f"ℹ️ Not a wake word: '{text}'")
                        
                except sr.UnknownValueError:
                    logger.debug("Could not understand audio")
                    pass
                except sr.RequestError as e:
                    logger.error(f"Recognition service error: {e}")
                    pass
                except Exception as e:
                    logger.debug(f"Recognition error: {e}")
                    pass
                    
        except sr.WaitTimeoutError:
            logger.debug("No speech detected in timeout")
            pass
        except Exception as e:
            logger.debug(f"Wake word detection cycle: {e}")
            pass
            
        return False
    
    def greet_user(self, lang='hi'):
        """Greet the user by name - Default Hindi"""
        greetings = {
            'hi': f"नमस्ते {self.user_name}, मैं ऑनलाइन हूं और आपकी सहायता के लिए तैयार हूं।",
            'en': f"Hello {self.user_name}, I'm online and ready to assist you.",
            'hi': f"नमस्ते {self.user_name}, मैं ऑनलाइन हूं और आपकी सहायता के लिए तैयार हूं।",
            'ta': f"வணக்கம் {self.user_name}, நான் ஆன்லைனில் உள்ளேன், உங்களுக்கு உதவ தயாராக இருக்கிறேன்.",
            'te': f"నమస్కారం {self.user_name}, నేను ఆన్‌లైన్‌లో ఉన్నాను మరియు మీకు సహాయం చేయడానికి సిద్ధంగా ఉన్నాను.",
            'ml': f"നമസ്കാരം {self.user_name}, ഞാൻ ഓൺലൈനിൽ ആണ്, നിങ്ങളെ സഹായിക്കാൻ തയ്യാറാണ്.",
            'kn': f"ನಮಸ್ಕಾರ {self.user_name}, ನಾನು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿದ್ದೇನೆ ಮತ್ತು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಸಿದ್ಧವಾಗಿದ್ದೇನೆ.",
        }
        greeting = greetings.get(lang, greetings['en'])
        self.speak(greeting, lang=lang, async_mode=False)
        return greeting


# Standalone test function
def test_jarvis_voice():
    """Test the voice module"""
    print("=" * 60)
    print("JARVIS Voice Module Test")
    print("=" * 60)
    
    jarvis = JarvisVoice()
    
    def simple_callback(english_text):
        """Simple echo callback for testing"""
        return f"You said: {english_text}"
    
    print("\n🎤 Say something in any language...")
    print("(The system will detect your language and respond in the same language)\n")
    
    result = jarvis.process_multilingual_command(callback=simple_callback)
    
    if result['success']:
        print("\n" + "=" * 60)
        print("📊 Result:")
        print(f"Your Language: {jarvis.get_language_name(result['user_lang'])}")
        print(f"You Said: {result['user_text']}")
        print(f"English: {result['english_text']}")
        print(f"Response: {result['response_user_lang']}")
        print("=" * 60)
    else:
        print("❌ Voice recognition failed. Please try again.")


if __name__ == "__main__":
    test_jarvis_voice()
