"""
JARVIS Brain Module - Dual-Brain Architecture (ACTION + KNOWLEDGE)
Handles system automation AND educational explanations
WITH SECURITY: Input sanitization to prevent command injection
"""
import logging
import re
from typing import Dict, List, Optional, Tuple
from config import AI_CONFIG, AI_PROVIDER, GEMINI_API_KEY, OPENAI_API_KEY

# Import new dual-brain components
from intent_detector import IntentDetector
from knowledge_engine import KnowledgeEngine

# Import security module
try:
    from input_sanitizer import get_input_sanitizer
    INPUT_SANITIZER_AVAILABLE = True
except ImportError:
    INPUT_SANITIZER_AVAILABLE = False

logger = logging.getLogger(__name__)


class JarvisBrain:
    """
    DUAL-BRAIN ARCHITECTURE WITH SECURITY
    
    Brain 1: ACTION BRAIN (Priority 1)
    - Handles system control and automation
    - Bypasses AI for direct execution
    - Validates input for security
    
    Brain 2: KNOWLEDGE BRAIN (Priority 2)
    - Explains concepts like a teacher
    - Uses AI for educational responses
    - Sanitizes input before processing
    """
    
    def __init__(self, memory_manager):
        """
        Initialize dual-brain system
        
        Args:
            memory_manager: ConversationMemory instance
        """
        self.memory = memory_manager
        
        # Initialize security module
        if INPUT_SANITIZER_AVAILABLE:
            self.sanitizer = get_input_sanitizer()
            logger.info("✅ Input sanitizer initialized")
        else:
            self.sanitizer = None
            logger.warning("⚠️ Input sanitizer not available")
        
        # Initialize Intent Detector
        self.intent_detector = IntentDetector()
        logger.info("✅ Intent Detector initialized")
        
        # Initialize Knowledge Engine (Educational AI) - ALWAYS with API key
        from config import AI_CONFIG
        self.knowledge_engine = KnowledgeEngine(
            api_key=GEMINI_API_KEY,
            model_name=AI_CONFIG['model']
        )
        logger.info("✅ Knowledge Engine initialized with Gemini")
        
        # Legacy settings
        self.ai_provider = AI_PROVIDER
        self.system_prompt = AI_CONFIG['system_prompt']
        
        logger.info(f"✅ JARVIS DUAL-BRAIN initialized (Provider: {self.ai_provider})")
    
    def _init_gemini(self):
        """Initialize Google Gemini API"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            self.ai_client = genai.GenerativeModel(AI_CONFIG['model'])
            logger.info("✅ Gemini AI initialized")
        except ImportError:
            logger.error("❌ google-generativeai not installed. Run: pip install google-generativeai")
            self.ai_client = None
        except Exception as e:
            logger.error(f"❌ Gemini initialization failed: {e}")
            self.ai_client = None
    
    def _init_openai(self):
        """Initialize OpenAI API"""
        try:
            import openai
            
            if OPENAI_API_KEY == 'YOUR_OPENAI_API_KEY_HERE':
                logger.warning("⚠️ OpenAI API key not configured")
                self.ai_client = None
                return
            
            openai.api_key = OPENAI_API_KEY
            self.ai_client = openai
            logger.info("✅ OpenAI initialized")
        except ImportError:
            logger.error("❌ openai not installed. Run: pip install openai")
            self.ai_client = None
        except Exception as e:
            logger.error(f"❌ OpenAI initialization failed: {e}")
            self.ai_client = None
    
    def process_input(self, user_text: str, detected_lang: str = 'en') -> Dict:
        """
        DUAL-BRAIN PROCESSING WITH SECURITY:
        1. SANITIZE INPUT (prevent command injection)
        2. CLASSIFY INTENT (ACTION, INFORMATION, CONVERSATION, EXIT)
        3. Route to appropriate brain
        
        Args:
            user_text: User's speech input
            detected_lang: Detected language code
            
        Returns:
            Dict with: intent, response, action, confidence, entities
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🧠 JARVIS DUAL-BRAIN PROCESSING")
        logger.info(f"📝 RAW INPUT: '{user_text}'")
        logger.info(f"🌐 LANGUAGE: {detected_lang}")
        logger.info(f"{'='*60}")
        
        # SECURITY: Sanitize input first
        if self.sanitizer:
            is_safe, sanitized_text, warning = self.sanitizer.sanitize_text(user_text)
            
            if not is_safe:
                logger.error(f"🚨 SECURITY ALERT: Blocked dangerous input")
                return {
                    'intent': 'BLOCKED',
                    'response': 'I cannot process that request for security reasons.',
                    'action': None,
                    'confidence': 1.0,
                    'entities': {},
                    'warning': warning
                }
            
            if warning:
                logger.warning(f"⚠️ {warning}")
            
            user_text = sanitized_text
            logger.info(f"🔒 SANITIZED INPUT: '{user_text}'")
        
        # STEP 1: CLASSIFY INTENT
        primary_intent, confidence, details = self.intent_detector.classify_intent(user_text)
        
        logger.info(f"\n🎯 PRIMARY INTENT: {primary_intent} (confidence: {confidence:.2f})")
        
        # Add to memory with intent
        self.memory.add_user_message(
            user_text, 
            detected_lang, 
            intent=primary_intent,
            topic=details.get('type')
        )
        
        # ROUTE TO APPROPRIATE BRAIN
        
        # ========== ACTION BRAIN (PRIORITY 1) ==========
        if primary_intent == 'ACTION':
            logger.info("\n⚡ ROUTING TO: ACTION BRAIN")
            logger.info("🎯 Detecting specific action...")
            logger.info("🚨 SYSTEM COMMAND - Will execute locally, NOT sent to AI")
            
            # Use existing action detection
            action_result = self.detect_action_intent(user_text)
            
            logger.info(f"⚙️ ACTION: {action_result.get('action', 'unknown')}")
            logger.info(f"🏷️ ENTITIES: {action_result.get('entities', {})}")
            
            # Generate simple acknowledgment
            response_text = self._generate_natural_response(user_text, action_result)
            
            result = {
                'intent': 'task',
                'response': response_text,
                'action': action_result['action'],
                'parameters': action_result.get('parameters', {}),
                'entities': action_result.get('entities', {}),
                'confidence': confidence
            }
        
        # ========== KNOWLEDGE BRAIN (PRIORITY 2) ==========
        elif primary_intent == 'INFORMATION':
            logger.info("\n📚 ROUTING TO: KNOWLEDGE BRAIN (Educational AI)")
            
            # Get context from memory
            context = self.memory.get_last_topic()
            
            # Generate educational explanation
            response_text = self.knowledge_engine.explain(user_text, context)
            
            result = {
                'intent': 'information',
                'response': response_text,
                'action': None,
                'parameters': {},
                'entities': {},
                'confidence': confidence
            }
        
        # ========== CONVERSATION BRAIN (PRIORITY 3) ==========
        elif primary_intent == 'CONVERSATION':
            logger.info("\n💬 ROUTING TO: CONVERSATION BRAIN")
            response_text = self._handle_conversation(user_text)
            
            result = {
                'intent': 'conversation',
                'response': response_text,
                'action': None,
                'parameters': {},
                'entities': {},
                'confidence': confidence
            }
        
        # ========== EXIT ==========
        elif primary_intent == 'EXIT':
            logger.info("\n🚪 EXIT INTENT DETECTED")
            result = {
                'intent': 'task',
                'response': "Goodbye! It was great talking to you.",
                'action': 'exit',
                'parameters': {},
                'entities': {},
                'confidence': 1.0
            }
        
        # ========== FALLBACK ==========
        else:
            logger.warning("❓ UNCLEAR INTENT - Using fallback")
            response_text = "I'm not sure what you'd like me to do. Can you rephrase that?"
            result = {
                'intent': 'conversation',
                'response': response_text,
                'action': None,
                'parameters': {},
                'entities': {},
                'confidence': 0.3
            }
        
        # Add response to memory
        self.memory.add_assistant_message(
            result['response'],
            action=result.get('action'),
            intent=result.get('intent')
        )
        
        logger.info(f"\n💬 FINAL RESPONSE: '{result['response'][:100]}...'")
        logger.info(f"{'='*60}\n")
        
        return result
    
    def detect_action_intent(self, text: str) -> Dict:
        """
        LAYER 1: Intelligent Action Intent Detection
        Detects actionable commands with entity extraction
        Supports English, Hindi, and Hinglish
        
        Returns:
            Dict with intent, action, parameters, entities, confidence
        """
        text_lower = text.lower().strip()
        
        # Initialize result
        result = {
            'intent': 'conversation',
            'action': None,
            'parameters': {'query': text},
            'entities': {},
            'confidence': 0.0
        }
        
        # TASK 1: LANGUAGE CHANGE (HIGHEST PRIORITY)
        language_keywords = ['change language', 'speak', 'talk in', 'bol', 'bolo', 'language', 'bhasha']
        language_names = {
            'english': 'en', 'hindi': 'hi', 'tamil': 'ta', 'telugu': 'te', 
            'kannada': 'kn', 'bengali': 'bn', 'marathi': 'mr', 'gujarati': 'gu',
            'angrez': 'en', 'angrezi': 'en', 'hindi': 'hi'
        }
        
        if any(kw in text_lower for kw in language_keywords):
            # Extract target language
            target_lang = None
            for lang_name, lang_code in language_names.items():
                if lang_name in text_lower:
                    target_lang = lang_code
                    break
            
            if target_lang:
                return {
                    'intent': 'task',
                    'action': 'change_language',
                    'parameters': {'query': text},
                    'entities': {'target_language': target_lang},
                    'confidence': 0.98
                }
        
        # TASK 2: YOUTUBE/VIDEO (CHECK BEFORE "OPEN" TO AVOID CONFUSION)
        # YouTube keywords: youtube, video, song, music, play, etc.
        play_keywords = ['play', 'chalao', 'bajao', 'sunao', 'suno', 'laga', 'lagao']
        youtube_keywords = ['youtube', 'video', 'song', 'music', 'gaana', 'gana', 'sangeet', 'gaane']
        
        # Check for YouTube/video intent (higher priority than "open app")
        # Examples: "open youtube", "play despacito", "youtube chalao"
        if any(yk in text_lower for yk in youtube_keywords):
            video_name = self._extract_video_name(text_lower)
            return {
                'intent': 'task',
                'action': 'play_youtube',
                'parameters': {'query': text},
                'entities': {'video_name': video_name},
                'confidence': 0.95
            }
        
        # Check for play + music content
        if any(pk in text_lower for pk in play_keywords):
            if self._has_music_content(text_lower):
                video_name = self._extract_video_name(text_lower)
                return {
                    'intent': 'task',
                    'action': 'play_youtube',
                    'parameters': {'query': text},
                    'entities': {'video_name': video_name},
                    'confidence': 0.94
                }
        
        # TASK 3: SEARCH GOOGLE
        search_keywords = ['search', 'google', 'find', 'look up', 'lookup', 'dhundo', 'khojo', 'search karo', 'google par', 'google karo']
        if any(word in text_lower for word in search_keywords):
            search_query = self._extract_search_query(text_lower)
            return {
                'intent': 'task',
                'action': 'search',
                'parameters': {'query': text},
                'entities': {'search_terms': search_query},
                'confidence': 0.92
            }
        
        # TASK 4: OPEN APPLICATION (CHECKED AFTER YOUTUBE)
        # Now "open youtube" won't be caught here because youtube was already handled
        open_keywords = ['open', 'launch', 'start', 'run', 'kholo', 'khol', 'chalu', 'shuru', 'kijiye', 'karo', 'kariye', 'dikhao']
        if any(word in text_lower for word in open_keywords):
            # Extract app name
            app_name = self._extract_app_name(text_lower)
            if app_name:
                return {
                    'intent': 'task',
                    'action': 'open_app',
                    'parameters': {'query': text},
                    'entities': {'app_name': app_name},
                    'confidence': 0.93
                }
        
        # TASK 5: SEND MESSAGE (WHATSAPP)
        message_keywords = ['message', 'whatsapp', 'send', 'text', 'bhejo', 'bhej', 'msg', 'message bhejo', 'msg kar']
        if any(word in text_lower for word in message_keywords):
            contact_name = self._extract_contact_name(text_lower)
            message_content = self._extract_message_content(text)  # Pass original text for better extraction
            return {
                'intent': 'task',
                'action': 'send_message',
                'parameters': {'query': text},
                'entities': {
                    'contact': contact_name,
                    'message': message_content,
                    'full_query': text  # Keep original for automation
                },
                'confidence': 0.88
            }
        
        # TASK 5: EMAIL
        if 'email' in text_lower or 'mail' in text_lower:
            return {
                'intent': 'task',
                'action': 'send_email',
                'parameters': {'query': text},
                'entities': {},
                'confidence': 0.85
            }
        
        # TASK 6: ORDER FOOD
        if any(word in text_lower for word in ['order', 'food', 'swiggy', 'zomato', 'hungry', 'khana']):
            return {
                'intent': 'task',
                'action': 'order_food',
                'parameters': {'query': text},
                'entities': {},
                'confidence': 0.82
            }
        
        # TASK 7: WEATHER
        weather_keywords = ['weather', 'temperature', 'mausam', 'garmi', 'sardi', 'temp', 'climate', 'barish', 'rain']
        if any(word in text_lower for word in weather_keywords):
            return {
                'intent': 'task',
                'action': 'get_weather',
                'parameters': {'query': text},
                'entities': {},
                'confidence': 0.90
            }
        
        # TASK 8: TIME/DATE
        if any(word in text_lower for word in ['time', 'date', 'today', 'kya time', 'kitne baje', 'din']):
            return {
                'intent': 'task',
                'action': 'time_date',
                'parameters': {'query': text},
                'entities': {},
                'confidence': 1.0
            }
        
        # TASK 8: EXIT
        if any(word in text_lower for word in ['exit', 'quit', 'stop', 'goodbye', 'bye', 'band karo', 'close']):
            return {
                'intent': 'task',
                'action': 'exit',
                'parameters': {},
                'entities': {},
                'confidence': 1.0
            }
        
        # NO ACTIONABLE INTENT → Return for Layer 2 (Conversational AI)
        return {
            'intent': 'conversation',
            'action': None,
            'parameters': {'query': text},
            'entities': {},
            'confidence': 0.5
        }
    
    def _generate_natural_response(self, text: str, intent_result: Dict) -> str:
        """
        Generate natural, human-like responses for actions
        NO robotic sentences, uses variety of phrases
        """
        import random
        
        action = intent_result.get('action')
        entities = intent_result.get('entities', {})
        
        # Human-like response variations
        if action == 'open_app':
            app_name = entities.get('app_name', 'that')
            responses = [
                f"Opening {app_name.title()}.",
                f"Sure, launching {app_name.title()}.",
                f"On it. Opening {app_name.title()}.",
            ]
            return random.choice(responses)
        
        elif action == 'search':
            search_terms = entities.get('search_terms', 'that')
            responses = [
                f"Searching for {search_terms}.",
                f"Looking up {search_terms} for you.",
                f"On it. Searching {search_terms}.",
            ]
            return random.choice(responses)
        
        elif action == 'play_youtube':
            video_name = entities.get('video_name', 'that')
            responses = [
                f"Playing {video_name} now.",
                f"Sure, playing {video_name}.",
                f"On it. Starting {video_name}.",
                f"Playing {video_name} for you.",
            ]
            return random.choice(responses)
        
        elif action == 'send_message':
            contact = entities.get('contact')
            message_text = entities.get('message_text')
            if contact and message_text:
                return f"Sending message to {contact}."
            elif contact:
                return f"Opening chat with {contact}."
            return "Opening WhatsApp."
        
        elif action == 'send_email':
            return "Opening Gmail for you."
        
        elif action == 'order_food':
            return "Opening food delivery app."
        
        elif action == 'time_date':
            return ""  # Will be filled by task executor
        
        elif action == 'exit':
            responses = [
                "Goodbye!",
                "See you later!",
                "Until next time!",
            ]
            return random.choice(responses)
        
        else:
            responses = [
                "Done.",
                "Got it.",
                "On it.",
            ]
            return random.choice(responses)
    
    def _handle_question(self, text: str) -> str:
        """Handle questions using AI with natural, concise responses"""
        if self.ai_client and self.ai_provider == 'gemini':
            try:
                # Get conversation context
                context = self.memory.get_context_for_ai()
                
                # Build natural conversational prompt
                prompt = f"""You are JARVIS, an intelligent AI assistant.

Instructions:
- Answer questions naturally and concisely
- Be helpful and friendly
- Keep responses short (2-3 sentences max)
- Speak like a real human, not a robot

Conversation history:
"""
                for msg in context[-3:]:
                    prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
                
                prompt += f"\nUser: {text}\nAssistant:"
                
                # Generate response
                response = self.ai_client.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                logger.error(f"❌ AI response failed: {e}")
                return self._intelligent_fallback(text)
        else:
            return self._intelligent_fallback(text)
    
    def _handle_conversation(self, text: str) -> str:
        """Handle casual conversation using Knowledge Engine - natural and engaging"""
        try:
            # Use Knowledge Engine for conversational responses too
            conversational_prompt = f"""User said: {text}

Respond naturally and warmly like a friendly AI assistant. Keep it brief (1-2 sentences).
Be conversational and human-like. Common greetings:
- "hey" / "hello" → "Hello! How can I help you?"
- "how are you" → "I'm great, thanks for asking! How can I assist you?"
- "thanks" → "You're welcome! Happy to help."
"""
            response = self.knowledge_engine.explain(conversational_prompt, None)
            return response.strip()
        except Exception as e:
            logger.error(f"❌ Conversation handling failed: {e}")
            return self._intelligent_fallback(text)
    
    def _intelligent_fallback(self, text: str) -> str:
        """
        Intelligent fallback responses (NO AI available)
        Natural, context-aware, NO generic phrases
        """
        text_lower = text.lower()
        
        # Greeting
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'namaste', 'namaskaar']):
            return "Hello! What can I do for you?"
        
        # How are you
        if any(phrase in text_lower for phrase in ['how are you', 'kaise ho', 'how r you']):
            return "I'm doing great! What about you?"
        
        # Thanks
        if any(word in text_lower for word in ['thank', 'thanks', 'shukriya', 'dhanyavad']):
            return "You're welcome!"
        
        # Who are you
        if any(phrase in text_lower for phrase in ['who are you', 'what are you', 'kaun ho', 'tum kaun']):
            return "I'm JARVIS, your AI assistant. I can control your computer, answer questions, and help with tasks."
        
        # Name question
        if any(phrase in text_lower for phrase in ['your name', 'naam kya', 'what is your name']):
            return "I'm JARVIS."
        
        # Capabilities
        if any(phrase in text_lower for phrase in ['what can you do', 'kya kar sakte', 'capabilities']):
            return "I can open apps, search the web, play music on YouTube, send messages, and answer your questions."
        
        # Default - natural acknowledgment
        return "I'm here. What would you like me to do?"
    
    def _extract_app_name(self, text: str) -> str:
        """Extract application name from text"""
        from config import APPS
        for app_name in APPS.keys():
            if app_name in text:
                return app_name
        return "the application"
    
    def _extract_search_query(self, text: str) -> str:
        """Extract search query from text"""
        # Remove common words
        text = text.replace('search', '').replace('google', '').replace('find', '')
        text = text.replace('dhundo', '').replace('khojo', '').replace('karo', '')
        text = text.replace('for', '').replace('about', '').replace('par', '')
        return text.strip() or "that"
    
    def _extract_video_name(self, text: str) -> str:
        """Extract video/song name from text"""
        # Remove common play keywords
        text = text.replace('play', '').replace('chalao', '').replace('bajao', '')
        text = text.replace('sunao', '').replace('lagao', '').replace('laga', '')
        text = text.replace('youtube', '').replace('par', '').replace('on', '')
        text = text.replace('video', '').replace('song', '').replace('music', '')
        text = text.replace('gaana', '').replace('gana', '').replace('kar', '').replace('do', '')
        return text.strip() or "that"
    
    def _extract_contact_name(self, text: str) -> Optional[str]:
        """Extract contact name from message text"""
        # Look for "to [name]" or "[name] ko"
        words = text.split()
        for i, word in enumerate(words):
            if word in ['to', 'ko'] and i + 1 < len(words):
                return words[i + 1]
        return None
    
    def _extract_message_content(self, text: str) -> Optional[str]:
        """
        Extract message content from text
        Handles multiple patterns including Hinglish
        """
        text_lower = text.lower()
        
        # Pattern 1: "that [message]"
        if 'that' in text_lower:
            message = text.split('that', 1)[1].strip()
            if message:
                return message
        
        # Pattern 2: "ki [message]" (Hinglish)
        if ' ki ' in text_lower:
            message = text.split(' ki ', 1)[1].strip()
            if message:
                return message
        
        # Pattern 3: After "message" or "bhejo"
        for keyword in ['message', 'bhejo', 'bhej', 'send']:
            if keyword in text_lower:
                parts = text_lower.split(keyword, 1)
                if len(parts) > 1:
                    remaining = parts[1].strip()
                    # Remove contact indicators
                    for word in ['to', 'ko']:
                        if word in remaining:
                            # Get everything after contact
                            contact_parts = remaining.split(word, 1)
                            if len(contact_parts) > 1:
                                after_contact = contact_parts[1].strip()
                                # Remove "that" or "ki"
                                for sep in ['that', 'ki']:
                                    if sep in after_contact:
                                        message = after_contact.split(sep, 1)[1].strip()
                                        if message:
                                            return message
        
        return None
    
    def _has_music_content(self, text: str) -> bool:
        """Check if text contains music/song references"""
        music_words = ['hanuman', 'chalisa', 'bhajan', 'song', 'singer', 'artist', 'album', 'track']
        return any(word in text for word in music_words)
    
    def _is_question(self, text: str) -> bool:
        """Check if text is a question"""
        question_starters = ['what', 'why', 'how', 'when', 'where', 'who', 'which', 'kya', 'kab', 'kaise', 'kahan', 'kaun']
        text_lower = text.lower()
        return any(text_lower.startswith(q) for q in question_starters) or '?' in text
