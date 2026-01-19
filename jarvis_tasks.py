"""
JARVIS Task Automation Module - Execute Real-World Tasks
Handles system control, browser automation, messaging, and more
CROSS-PLATFORM with robust error handling and security
"""
import logging
import webbrowser
import subprocess
import time
import pyautogui
from datetime import datetime
from typing import Dict, Optional
from config import APPS, WEBSITES, FOOD_SERVICES

# Import cross-platform system controller
try:
    from system_controller import get_system_controller
    SYSTEM_CONTROLLER_AVAILABLE = True
except ImportError:
    SYSTEM_CONTROLLER_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ System controller not available")

# Import advanced automation
try:
    from jarvis_automation import BrowserAutomation, ContentExtractor
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False
    BrowserAutomation = None
    ContentExtractor = None

logger = logging.getLogger(__name__)


class JarvisTasks:
    """Task executor for JARVIS - Automates real-world actions"""
    
    def __init__(self):
        """Initialize task executor"""
        self.last_opened_app = None
        
        # Initialize cross-platform system controller
        if SYSTEM_CONTROLLER_AVAILABLE:
            try:
                self.system_controller = get_system_controller()
                logger.info("✅ Cross-platform system controller initialized")
            except Exception as e:
                logger.warning(f"⚠️ System controller init failed: {e}")
                self.system_controller = None
        else:
            self.system_controller = None
        
        # Initialize advanced automation if available
        if AUTOMATION_AVAILABLE:
            try:
                self.automation = BrowserAutomation()
                self.content_extractor = ContentExtractor()
                logger.info("✅ Task executor initialized with ADVANCED AUTOMATION")
            except Exception as e:
                logger.warning(f"⚠️ Advanced automation init failed: {e}")
                self.automation = None
                self.content_extractor = None
        else:
            logger.warning("⚠️ Advanced automation not available (selenium not installed)")
            self.automation = None
            self.content_extractor = None
    
    def execute_task(self, intent_result: Dict) -> str:
        """
        Execute task based on intent with entity-aware processing
        
        Args:
            intent_result: Dict with action, parameters, entities from brain
            
        Returns:
            Response text describing what was done
        """
        action = intent_result.get('action')
        parameters = intent_result.get('parameters', {})
        entities = intent_result.get('entities', {})
        query = parameters.get('query', '')
        
        logger.info(f"\n{'='*60}")
        logger.info(f"⚙️ TASK EXECUTOR")
        logger.info(f"🎯 ACTION: {action}")
        logger.info(f"🏷️ ENTITIES: {entities}")
        logger.info(f"{'='*60}")
        
        try:
            if action == 'change_language':
                return self.change_language(entities)
            
            elif action == 'open_app':
                return self.open_application(query, entities)
            
            elif action == 'search':
                return self.google_search(query, entities)
            
            elif action == 'play_youtube':
                return self.play_youtube(query, entities)
            
            elif action == 'send_message':
                return self.send_whatsapp_message(query, entities)
            
            elif action == 'send_email':
                return self.send_email(query)
            
            elif action == 'order_food':
                return self.order_food(query)
            
            elif action == 'get_weather':
                return self.get_weather(query)
            
            elif action == 'time_date':
                return self.get_time_date(query)
            
            elif action == 'exit':
                return "Goodbye!"
            
            else:
                logger.warning(f"⚠️ Unknown action: {action}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Task execution failed: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            logger.info(f"{'='*60}\n")
    
    def change_language(self, entities: Dict = None) -> str:
        """
        Change output language
        
        Args:
            entities: Extracted entities with target_language
            
        Returns:
            Confirmation message
        """
        entities = entities or {}
        target_lang = entities.get('target_language', 'en')
        
        logger.info(f"🌐 Changing language to: {target_lang}")
        
        # Import config and update
        try:
            import config
            config.USER_LANGUAGE = target_lang
            
            # Update memory
            if hasattr(self, 'memory'):
                self.memory.last_language = target_lang
            
            lang_names = {
                'en': 'English',
                'hi': 'Hindi',
                'ta': 'Tamil',
                'te': 'Telugu',
                'kn': 'Kannada',
                'bn': 'Bengali',
                'mr': 'Marathi',
                'gu': 'Gujarati'
            }
            
            lang_name = lang_names.get(target_lang, 'English')
            logger.info(f"✅ Language changed to: {lang_name}")
            
            return f"Language changed to {lang_name}"
        
        except Exception as e:
            logger.error(f"❌ Language change failed: {e}")
            return "Sorry, couldn't change the language"
    
    def open_application(self, query: str, entities: Dict = None) -> str:
        """
        Open any application by name - CROSS-PLATFORM with security
        
        Args:
            query: User's command
            entities: Extracted entities with app_name
            
        Returns:
            None if response already set by brain, else message
        """
        entities = entities or {}
        query_lower = query.lower()
        logger.info(f"🔍 Searching for app in query: '{query_lower}'")
        
        # Extract app name from query
        app_to_open = None
        for app_name in APPS.keys():
            if app_name in query_lower:
                app_to_open = app_name
                break
        
        if not app_to_open:
            logger.warning(f"⚠️ NO APP FOUND in query: '{query}'")
            return "Which application would you like me to open?"
        
        # Use cross-platform system controller if available
        if self.system_controller:
            logger.info(f"🚀 Using cross-platform system controller for: {app_to_open}")
            success, message = self.system_controller.open_application(app_to_open)
            
            if success:
                self.last_opened_app = app_to_open
                logger.info(f"✅ SUCCESS: {app_to_open} opened!")
                return None  # Response already set by brain
            else:
                logger.error(f"❌ {message}")
                return message
        
        # Fallback: Use old method (Windows-only)
        else:
            app_command = APPS.get(app_to_open)
            if app_command:
                logger.info(f"💻 Fallback: Executing command: {app_command}")
                try:
                    subprocess.Popen(app_command, shell=True)
                    self.last_opened_app = app_to_open
                    logger.info(f"✅ SUCCESS: {app_to_open} opened!")
                    return None
                except Exception as e:
                    logger.error(f"❌ FAILED to open {app_to_open}: {e}")
                    return f"Couldn't open {app_to_open}: {str(e)}"
            else:
                return f"Don't know how to open {app_to_open}"
    
    def google_search(self, query: str, entities: Dict = None) -> str:
        """
        Perform Google search - CROSS-PLATFORM with security
        
        Args:
            query: Search query
            entities: Extracted entities with search_terms
            
        Returns:
            None if response already set by brain
        """
        entities = entities or {}
        # Extract search terms
        search_terms = query.lower()
        for word in ['search', 'google', 'find', 'look up', 'for', 'about', 'dhundo', 'khojo']:
            search_terms = search_terms.replace(word, '')
        search_terms = search_terms.strip()
        
        logger.info(f"🔍 Extracted search terms: '{search_terms}'")
        
        if not search_terms:
            logger.warning("⚠️ NO search terms extracted")
            return "What would you like me to search for?"
        
        # Use cross-platform system controller if available
        if self.system_controller:
            logger.info(f"🚀 Using cross-platform system controller for Google search")
            success, message = self.system_controller.open_google_search(search_terms)
            
            if success:
                logger.info(f"✅ SUCCESS: Google search launched")
                return None  # Response already set by brain
            else:
                logger.error(f"❌ {message}")
                return message
        
        # Fallback: Use webbrowser
        else:
            url = f"https://www.google.com/search?q={search_terms.replace(' ', '+')}"
            logger.info(f"🔗 Fallback: Opening URL: {url}")
            webbrowser.open(url)
            logger.info(f"✅ SUCCESS: Google search launched")
            return None
    
    def play_youtube(self, query: str, entities: Dict = None) -> str:
        """
        YouTube automation - CROSS-PLATFORM with multiple fallbacks
        
        Args:
            query: Video name or search query
            entities: Extracted entities with video_name
            
        Returns:
            None if successful (response set by brain)
        """
        entities = entities or {}
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🎬 YOUTUBE AUTOMATION")
        logger.info(f"{'='*70}")
        
        # Extract video name using advanced extractor if available
        if self.content_extractor:
            video_name = self.content_extractor.extract_video_content(query)
        else:
            # Fallback extraction
            video_name = query.lower()
            for word in ['play', 'youtube', 'video', 'song', 'music', 'on', 'chalao', 'bajao', 'sunao', 'kar', 'do']:
                video_name = video_name.replace(word, '')
            video_name = video_name.strip()
        
        logger.info(f"🎵 Video to play: '{video_name}'")
        
        if not video_name or video_name == 'that':
            logger.warning("⚠️ NO video name extracted")
            return "What would you like me to play?"
        
        # METHOD 1: Use cross-platform system controller (most reliable)
        if self.system_controller:
            logger.info("🚀 Using cross-platform system controller for YouTube")
            success, message = self.system_controller.open_youtube(video_name)
            
            if success:
                logger.info("✅ YOUTUBE OPENED SUCCESSFULLY!")
                logger.info(f"{'='*70}\n")
                return None  # Response already set by brain
        
        # METHOD 2: Use REAL automation if available
        if self.automation:
            logger.info("🚀 Using ADVANCED BROWSER AUTOMATION")
            success = self.automation.play_youtube_video(video_name)
            
            if success:
                logger.info("✅ YOUTUBE AUTOMATION SUCCESSFUL!")
                logger.info(f"{'='*70}\n")
                return None
        
        # METHOD 3: Fallback - Just open URL
        logger.info("⚠️ Using fallback method (simple browser open)")
        url = f"https://www.youtube.com/results?search_query={video_name.replace(' ', '+')}"
        logger.info(f"🔗 Opening URL: {url}")
        webbrowser.open(url)
        logger.info(f"{'='*70}\n")
        return None
    
    def send_whatsapp_message(self, query: str, entities: Dict = None) -> str:
        """
        REAL WhatsApp automation - opens, finds contact, types, SENDS message
        
        Args:
            query: Message details
            entities: Extracted entities with contact and message
            
        Returns:
            None if successful (response set by brain)
        """
        entities = entities or {}
        
        logger.info(f"\n{'='*70}")
        logger.info(f"💬 WHATSAPP AUTOMATION - REAL MESSAGE SENDING")
        logger.info(f"{'='*70}")
        
        # Extract contact and message using advanced extractor if available
        if self.content_extractor:
            contact, message = self.content_extractor.extract_contact_and_message(query)
        else:
            # Use entities from brain
            contact = entities.get('contact')
            message = entities.get('message')
        
        logger.info(f"👤 Contact: {contact or 'Not specified'}")
        logger.info(f"📝 Message: {message or 'Not specified'}")
        
        # Use REAL automation if available
        if self.automation:
            logger.info("🚀 Using ADVANCED WHATSAPP AUTOMATION")
            success = self.automation.send_whatsapp_message(contact, message)
            
            if success:
                logger.info("✅ WHATSAPP AUTOMATION SUCCESSFUL!")
                logger.info(f"{'='*70}\n")
                return None  # Response already set by brain
            else:
                logger.error("❌ Automation failed, falling back to simple open")
        else:
            logger.info("⚠️ Advanced automation not available, using simple method")
        
        # Fallback: Just open WhatsApp
        try:
            subprocess.Popen('start whatsapp:', shell=True)
            logger.info("✅ WhatsApp app opened")
        except:
            webbrowser.open('https://web.whatsapp.com')
            logger.info("✅ WhatsApp Web opened")
        
        logger.info(f"{'='*70}\n")
        return None
    
    def type_text(self, text: str) -> str:
        """
        Type text using keyboard automation
        
        Args:
            text: Text to type
            
        Returns:
            Confirmation
        """
        logger.info(f"⌨️ Typing: {text}")
        time.sleep(1)  # Wait for focus
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"
    
    def press_key(self, key: str) -> str:
        """
        Press a keyboard key
        
        Args:
            key: Key name (enter, tab, etc.)
            
        Returns:
            Confirmation
        """
        logger.info(f"⌨️ Pressing: {key}")
        pyautogui.press(key)
        return f"Pressed {key}"
    
    def send_email(self, query: str) -> str:
        """
        Send email (opens Gmail)
        
        Args:
            query: Email details
            
        Returns:
            Instruction message
        """
        logger.info("📧 Opening Gmail")
        webbrowser.open('https://mail.google.com/mail/?view=cm&fs=1')
        
        return "Gmail compose window is open. What would you like to write?"
    
    def order_food(self, query: str) -> str:
        """
        Order food (opens Swiggy/Zomato)
        
        Args:
            query: Food order details
            
        Returns:
            Instruction message
        """
        query_lower = query.lower()
        
        if 'swiggy' in query_lower:
            logger.info("🍔 Opening Swiggy")
            webbrowser.open(FOOD_SERVICES['swiggy'])
            return "Swiggy is open. What would you like to order?"
        elif 'zomato' in query_lower:
            logger.info("🍔 Opening Zomato")
            webbrowser.open(FOOD_SERVICES['zomato'])
            return "Zomato is open. What would you like to order?"
        else:
            logger.info("🍔 Opening Swiggy (default)")
            webbrowser.open(FOOD_SERVICES['swiggy'])
            return "I've opened Swiggy. What would you like to order?"
    
    def get_time_date(self, query: str) -> str:
        """
        Get current time or date
        
        Args:
            query: User query
            
        Returns:
            Time/date information
        """
        now = datetime.now()
        
        if 'time' in query.lower():
            time_str = now.strftime('%I:%M %p')
            logger.info(f"🕐 Current time: {time_str}")
            return f"The time is {time_str}"
        
        elif 'date' in query.lower() or 'today' in query.lower():
            date_str = now.strftime('%A, %B %d, %Y')
            logger.info(f"📅 Current date: {date_str}")
            return f"Today is {date_str}"
        
        else:
            datetime_str = now.strftime('%I:%M %p on %A, %B %d, %Y')
            return f"It's {datetime_str}"
    
    def get_weather(self, query: str) -> str:
        """
        Get weather information
        NOTE: This requires weather API integration
        
        Args:
            query: User query
            
        Returns:
            Weather information or setup instruction
        """
        logger.info("🌤️ Weather request received")
        # TODO: Add weather API integration (OpenWeatherMap, WeatherAPI, etc.)
        return "Weather feature requires API setup. Please configure weather API in config.py"

    def execute_custom_command(self, command: str) -> str:
        """
        Execute custom automation command
        
        Args:
            command: Command text
            
        Returns:
            Result
        """
        command_lower = command.lower()
        
        # Type command
        if command_lower.startswith('type '):
            text = command[5:]
            return self.type_text(text)
        
        # Press key command
        elif command_lower.startswith('press '):
            key = command[6:]
            return self.press_key(key)
        
        # Send (press enter)
        elif 'send' in command_lower or 'enter' in command_lower:
            return self.press_key('enter')
        
        return "I'm not sure how to execute that command"
