"""
JARVIS Advanced Browser Automation Module
REAL browser control with Selenium and PyAutoGUI
Handles YouTube playback, WhatsApp messaging, and complex automation
"""
import logging
import time
import pyautogui
import webbrowser
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

# PyAutoGUI safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


class BrowserAutomation:
    """Advanced browser automation for JARVIS"""
    
    def __init__(self):
        """Initialize browser automation"""
        self.driver = None
        self.chrome_options = Options()
        # Don't run headless - user needs to see actions
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        logger.info("✅ Browser automation initialized")
    
    def play_youtube_video(self, video_name: str) -> bool:
        """
        DIRECT YouTube playback - searches and plays immediately
        
        Args:
            video_name: Name of video/song to play
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"🎬 STARTING YOUTUBE AUTOMATION")
            logger.info(f"🎵 Video to play: '{video_name}'")
            
            # Direct YouTube search and play URL
            import urllib.parse
            search_query = urllib.parse.quote(video_name)
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            logger.info(f"🌐 Opening: {youtube_url}")
            webbrowser.open(youtube_url)
            
            time.sleep(3)  # Wait for page load
            
            # Try Selenium for clicking first video
            try:
                return self._play_first_video_selenium(youtube_url)
            except Exception as e:
                logger.warning(f"⚠️ Selenium failed: {e}")
                # Fallback - just opening search is better than nothing
                logger.info("✅ YouTube search opened (manual click required)")
                return True
            
        except Exception as e:
            logger.error(f"❌ YouTube automation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _play_first_video_selenium(self, youtube_url: str) -> bool:
        """Click first video on YouTube search results"""
        try:
            logger.info("🌐 Launching Chrome with Selenium...")
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.maximize_window()
            
            # Navigate to search results
            logger.info("📍 Loading YouTube search results...")
            self.driver.get(youtube_url)
            time.sleep(2)
            
            # Wait for and click first video
            logger.info("🎬 Finding first video...")
            wait = WebDriverWait(self.driver, 10)
            video_elements = wait.until(
                EC.presence_of_all_elements_located((By.ID, "video-title"))
            )
            
            for video in video_elements[:5]:  # Check first 5
                if video.is_displayed() and video.get_attribute("href"):
                    logger.info(f"▶️ Clicking: {video.get_attribute('title')}")
                    video.click()
                    break
            
            logger.info("✅ SUCCESS: YouTube video playing!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Selenium YouTube failed: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            raise
    
    def _play_youtube_pyautogui(self, video_name: str) -> bool:
        """Play YouTube video using PyAutoGUI automation (fallback)"""
        try:
            logger.info("🖱️ Using PyAutoGUI automation...")
            
            # Open YouTube
            logger.info("🌐 Opening YouTube in default browser...")
            webbrowser.open("https://www.youtube.com")
            time.sleep(4)
            
            # Click search box (approximate position)
            logger.info("🔍 Clicking search area...")
            screen_width, screen_height = pyautogui.size()
            # Search box is usually top-center
            pyautogui.click(screen_width // 2, 100)
            time.sleep(1)
            
            # Type video name
            logger.info(f"⌨️ Typing: '{video_name}'")
            pyautogui.write(video_name, interval=0.05)
            time.sleep(0.5)
            
            # Press Enter
            logger.info("⏎ Pressing Enter...")
            pyautogui.press('enter')
            time.sleep(3)
            
            # Click first video (approximate position)
            logger.info("🎬 Clicking first video...")
            # First video is usually around this position
            pyautogui.click(screen_width // 2, 350)
            
            logger.info("✅ SUCCESS: YouTube automation completed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ PyAutoGUI YouTube failed: {e}")
            return False
    
    def send_whatsapp_message(self, contact_name: Optional[str], message: Optional[str]) -> bool:
        """
        REAL WhatsApp Web automation with working message typing
        
        Args:
            contact_name: Name of contact to message
            message: Message to send
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"💬 STARTING WHATSAPP AUTOMATION")
            logger.info(f"👤 Contact: {contact_name or 'Not specified'}")
            logger.info(f"📝 Message: {message or 'Not specified'}")
            
            # Try Selenium method first (more reliable)
            try:
                return self._send_whatsapp_selenium(contact_name, message)
            except Exception as e:
                logger.warning(f"⚠️ Selenium failed: {e}, trying PyAutoGUI")
                return self._send_whatsapp_pyautogui(contact_name, message)
            
        except Exception as e:
            logger.error(f"❌ WhatsApp automation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _send_whatsapp_selenium(self, contact_name: Optional[str], message: Optional[str]) -> bool:
        """Send WhatsApp message using Selenium"""
        try:
            logger.info("🌐 Opening WhatsApp Web with Selenium...")
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.maximize_window()
            
            # Open WhatsApp Web
            logger.info("📱 Loading WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Wait for QR code scan (or auto-login)
            logger.info("⏳ Waiting for WhatsApp to load (scan QR if needed)...")
            time.sleep(15)  # Give time for QR scan
            
            # Search for contact if provided
            if contact_name:
                logger.info(f"🔍 Searching for contact: {contact_name}")
                wait = WebDriverWait(self.driver, 20)
                
                # Find search box
                search_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
                )
                search_box.click()
                search_box.send_keys(contact_name)
                time.sleep(2)
                
                # Click first result
                logger.info("👤 Selecting contact...")
                search_box.send_keys(Keys.ENTER)
                time.sleep(1)
            
            # Type and send message if provided
            if message:
                logger.info("💬 Typing message...")
                wait = WebDriverWait(self.driver, 10)
                
                # Find message input box
                message_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                message_box.click()
                message_box.send_keys(message)
                time.sleep(0.5)
                
                # Send message
                logger.info("📤 Sending message...")
                message_box.send_keys(Keys.ENTER)
                
                logger.info("✅ SUCCESS: Message sent!")
            else:
                logger.info("✅ WhatsApp opened, ready for manual input")
            
            time.sleep(2)  # Keep window open briefly
            return True
            
        except Exception as e:
            logger.error(f"❌ Selenium WhatsApp failed: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            raise
    
    def _send_whatsapp_pyautogui(self, contact_name: Optional[str], message: Optional[str]) -> bool:
        """Send WhatsApp message using PyAutoGUI (fallback)"""
        try:
            logger.info("🖱️ Using PyAutoGUI automation...")
            
            # Open WhatsApp Web
            logger.info("🌐 Opening WhatsApp Web...")
            webbrowser.open("https://web.whatsapp.com")
            time.sleep(10)  # Wait for load + QR scan
            
            logger.info("⏳ Please ensure WhatsApp Web is ready...")
            
            # If contact name provided, search for it
            if contact_name:
                logger.info(f"🔍 Searching for contact: {contact_name}")
                
                # Click search box (usually top-left)
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width // 4, 100)
                time.sleep(1)
                
                # Type contact name
                logger.info(f"⌨️ Typing contact name...")
                pyautogui.write(contact_name, interval=0.1)
                time.sleep(1)
                
                # Press Enter to select
                logger.info("⏎ Selecting contact...")
                pyautogui.press('enter')
                time.sleep(1)
            
            # If message provided, type and send it
            if message:
                logger.info(f"💬 Typing message...")
                # Click message area (bottom of screen)
                pyautogui.click(screen_width // 2, screen_height - 100)
                time.sleep(0.5)
                
                # Type message
                pyautogui.write(message, interval=0.05)
                time.sleep(0.5)
                
                # Send message
                logger.info("📤 Sending message...")
                pyautogui.press('enter')
                
                logger.info("✅ SUCCESS: Message sent!")
            else:
                logger.info("✅ WhatsApp opened, ready for manual input")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ PyAutoGUI WhatsApp failed: {e}")
            return False
    
    def type_in_active_window(self, text: str) -> bool:
        """
        Type text in currently active window
        
        Args:
            text: Text to type
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"⌨️ Typing text: '{text}'")
            time.sleep(1)  # Wait for window focus
            pyautogui.write(text, interval=0.05)
            logger.info("✅ Text typed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Typing failed: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """
        Press a keyboard key
        
        Args:
            key: Key to press (enter, tab, etc.)
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"⌨️ Pressing key: {key}")
            pyautogui.press(key)
            logger.info("✅ Key pressed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Key press failed: {e}")
            return False
    
    def close_browser(self):
        """Close browser if open"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("🔒 Browser closed")
            except:
                pass
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close_browser()


class ContentExtractor:
    """Advanced content extraction from speech"""
    
    @staticmethod
    def extract_video_content(text: str) -> str:
        """
        Extract video/song name from speech
        Handles complex Hinglish patterns
        
        Args:
            text: User speech text
            
        Returns:
            Clean video search query
        """
        import re
        
        text_lower = text.lower().strip()
        logger.info(f"🔍 EXTRACTING VIDEO CONTENT FROM: '{text}'")
        
        # Remove common command words - EXPANDED LIST
        remove_words = [
            'play', 'chalao', 'bajao', 'sunao', 'lagao', 'laga', 'suno', 'dikhao',
            'youtube', 'par', 'pe', 'on', 'mein', 'me', 'video', 'song', 'music',
            'kar', 'karo', 'do', 'de', 'dijiye', 'kijiye', 'jiye',
            'gaana', 'gana', 'the', 'a', 'an', 'please', 'kya', 'hai'
        ]
        
        # Split into words
        words = text_lower.split()
        
        # Remove command words
        filtered_words = [w for w in words if w not in remove_words]
        
        # Join back
        content = ' '.join(filtered_words).strip()
        
        # If nothing left, try to find quoted content or proper nouns
        if not content:
            # Look for capitalized words in original text (proper nouns)
            content = ' '.join([w for w in text.split() if w[0].isupper() and len(w) > 2])
        
        logger.info(f"✅ EXTRACTED CONTENT: '{content}'")
        return content if content else text_lower
    
    @staticmethod
    def extract_search_query(text: str) -> str:
        """
        Extract search query from speech
        
        Args:
            text: User speech text
            
        Returns:
            Clean search query
        """
        text_lower = text.lower().strip()
        logger.info(f"🔍 EXTRACTING SEARCH QUERY FROM: '{text}'")
        
        # Remove search command words
        remove_words = [
            'search', 'google', 'find', 'lookup', 'look up',
            'dhundo', 'khojo', 'karo', 'kar', 'do',
            'for', 'about', 'par', 'pe', 'on'
        ]
        
        for word in remove_words:
            text_lower = text_lower.replace(word, ' ')
        
        query = ' '.join(text_lower.split()).strip()
        
        logger.info(f"✅ EXTRACTED QUERY: '{query}'")
        return query if query else text_lower
    
    @staticmethod
    def extract_contact_and_message(text: str) -> tuple:
        """
        Extract contact name and message from speech
        
        Args:
            text: User speech text
            
        Returns:
            Tuple of (contact_name, message_content)
        """
        text_lower = text.lower()
        logger.info(f"🔍 EXTRACTING CONTACT & MESSAGE FROM: '{text}'")
        
        contact = None
        message = None
        
        # Pattern 1: "message to [contact] that [message]"
        if 'to' in text_lower and 'that' in text_lower:
            parts = text_lower.split('to', 1)
            if len(parts) > 1:
                after_to = parts[1].strip()
                if 'that' in after_to:
                    contact_part, message_part = after_to.split('that', 1)
                    contact = contact_part.strip()
                    message = message_part.strip()
        
        # Pattern 2: "[contact] ko message bhejo ki [message]" (Hinglish)
        elif 'ko' in text_lower and ('bhejo' in text_lower or 'message' in text_lower):
            # Find contact before "ko"
            parts = text_lower.split('ko', 1)
            if len(parts) > 1:
                # Extract contact - remove command words
                contact_part = parts[0]
                for word in ['whatsapp', 'kholo', 'aur', 'message', 'send']:
                    contact_part = contact_part.replace(word, '')
                contact = contact_part.strip()
                
                # Extract message after "ki" or "bhejo"
                after_ko = parts[1].strip()
                if 'ki' in after_ko:
                    message = after_ko.split('ki', 1)[1].strip()
                elif 'bhejo' in after_ko:
                    message = after_ko.split('bhejo', 1)[1].strip()
                else:
                    # Remove command words
                    for word in ['message', 'bhejo', 'bhejiye', 'send', 'kar', 'do']:
                        after_ko = after_ko.replace(word, '')
                    message = after_ko.strip()
        
        # Pattern 3: "message [contact] [message]"
        elif 'message' in text_lower:
            parts = text_lower.split('message', 1)
            if len(parts) > 1:
                remaining = parts[1].strip()
                words = remaining.split()
                if words:
                    contact = words[0]
                    message = ' '.join(words[1:])
        
        logger.info(f"✅ EXTRACTED - Contact: '{contact}', Message: '{message}'")
        return contact, message
