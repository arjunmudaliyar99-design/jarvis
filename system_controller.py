"""
JARVIS System Controller - Cross-Platform OS Command Execution
Handles browser launching, app opening, and system-level actions
Supports Windows, macOS, and Linux with graceful fallbacks
"""
import logging
import platform
import subprocess
import webbrowser
import shlex
import os
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)

# Detect current operating system
CURRENT_OS = platform.system().lower()  # 'windows', 'darwin', 'linux'
logger.info(f"🖥️ Detected OS: {CURRENT_OS}")


class SystemController:
    """
    Cross-platform system control with security and error handling
    Executes OS-level commands safely and reliably
    """
    
    def __init__(self):
        """Initialize system controller"""
        self.os = CURRENT_OS
        self.blocked_commands = {
            'rm -rf /', 'del /f /s /q', 'format', 'fdisk',
            'dd if=', 'mkfs', ':(){:|:&};:', 'shutdown', 'reboot'
        }
        logger.info(f"✅ System controller initialized for {self.os}")
    
    def open_url(self, url: str) -> Tuple[bool, str]:
        """
        Open URL in default browser - MOST RELIABLE METHOD
        
        Args:
            url: URL to open
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Sanitize URL
            if not self._is_safe_url(url):
                logger.error(f"❌ BLOCKED: Unsafe URL: {url}")
                return False, "URL blocked for security reasons"
            
            logger.info(f"🌐 Opening URL: {url}")
            
            # Python's webbrowser is the most reliable cross-platform method
            result = webbrowser.open(url, new=2)  # new=2 opens in new tab
            
            if result:
                logger.info(f"✅ URL opened successfully: {url}")
                return True, f"Opened {url}"
            else:
                logger.error(f"❌ Failed to open URL: {url}")
                return False, f"Couldn't open {url}"
                
        except Exception as e:
            logger.error(f"❌ URL open error: {e}")
            return False, f"Error opening URL: {str(e)}"
    
    def open_youtube(self, query: str) -> Tuple[bool, str]:
        """
        Open YouTube and search for video
        
        Args:
            query: Search query for video
            
        Returns:
            Tuple of (success, message)
        """
        try:
            import urllib.parse
            search_query = urllib.parse.quote(query)
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            logger.info(f"🎬 Opening YouTube: {query}")
            return self.open_url(youtube_url)
            
        except Exception as e:
            logger.error(f"❌ YouTube open error: {e}")
            return False, f"Couldn't open YouTube: {str(e)}"
    
    def open_google_search(self, query: str) -> Tuple[bool, str]:
        """
        Open Google search
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (success, message)
        """
        try:
            import urllib.parse
            search_query = urllib.parse.quote(query)
            google_url = f"https://www.google.com/search?q={search_query}"
            
            logger.info(f"🔍 Opening Google search: {query}")
            return self.open_url(google_url)
            
        except Exception as e:
            logger.error(f"❌ Google search error: {e}")
            return False, f"Couldn't search Google: {str(e)}"
    
    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """
        Open installed application - CROSS-PLATFORM
        
        Args:
            app_name: Name of application to open
            
        Returns:
            Tuple of (success, message)
        """
        try:
            app_name_lower = app_name.lower()
            logger.info(f"💻 Attempting to open: {app_name}")
            
            # Get command based on OS
            command = self._get_app_command(app_name_lower)
            
            if not command:
                logger.warning(f"⚠️ App not found: {app_name}")
                return False, f"I don't know how to open {app_name}"
            
            # Security check
            if not self._is_safe_command(command):
                logger.error(f"❌ BLOCKED: Unsafe command: {command}")
                return False, "Command blocked for security reasons"
            
            # Execute command
            logger.info(f"🚀 Executing: {command}")
            
            if self.os == 'windows':
                subprocess.Popen(command, shell=True, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                # Unix-like systems - use proper argument splitting
                if isinstance(command, str):
                    command = shlex.split(command)
                subprocess.Popen(command, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            logger.info(f"✅ Opened: {app_name}")
            return True, f"Opened {app_name}"
            
        except FileNotFoundError:
            logger.error(f"❌ Application not found: {app_name}")
            return False, f"{app_name} is not installed or not in PATH"
        except Exception as e:
            logger.error(f"❌ App open error: {e}")
            return False, f"Couldn't open {app_name}: {str(e)}"
    
    def _get_app_command(self, app_name: str) -> Optional[str]:
        """
        Get OS-specific command to open application
        
        Args:
            app_name: Lowercase app name
            
        Returns:
            Command string or None if not found
        """
        # Define cross-platform app commands
        app_commands = {
            'windows': {
                # Browsers
                'chrome': 'start chrome',
                'browser': 'start chrome',
                'google chrome': 'start chrome',
                'edge': 'start msedge',
                'microsoft edge': 'start msedge',
                'firefox': 'start firefox',
                
                # Development
                'vscode': 'code',
                'vs code': 'code',
                'visual studio code': 'code',
                'pycharm': 'start pycharm',
                'sublime': 'start sublime_text',
                
                # Communication
                'whatsapp': 'start whatsapp:',
                'telegram': 'start telegram:',
                'slack': 'start slack:',
                'discord': 'start discord:',
                
                # Media
                'spotify': 'start spotify:',
                'vlc': 'start vlc',
                
                # Utilities
                'notepad': 'notepad',
                'calculator': 'calc',
                'paint': 'mspaint',
                'files': 'start explorer',
                'file explorer': 'start explorer',
                'explorer': 'start explorer',
                'terminal': 'start cmd',
                'cmd': 'start cmd',
                'command prompt': 'start cmd',
                'powershell': 'start powershell',
                
                # Office
                'word': 'start winword',
                'excel': 'start excel',
                'powerpoint': 'start powerpnt',
            },
            'darwin': {  # macOS
                # Browsers
                'chrome': 'open -a "Google Chrome"',
                'browser': 'open -a "Safari"',
                'safari': 'open -a "Safari"',
                'firefox': 'open -a "Firefox"',
                'edge': 'open -a "Microsoft Edge"',
                
                # Development
                'vscode': 'open -a "Visual Studio Code"',
                'vs code': 'open -a "Visual Studio Code"',
                'pycharm': 'open -a "PyCharm"',
                'sublime': 'open -a "Sublime Text"',
                
                # Communication
                'whatsapp': 'open -a "WhatsApp"',
                'telegram': 'open -a "Telegram"',
                'slack': 'open -a "Slack"',
                
                # Media
                'spotify': 'open -a "Spotify"',
                'vlc': 'open -a "VLC"',
                
                # Utilities
                'terminal': 'open -a "Terminal"',
                'finder': 'open -a "Finder"',
                'files': 'open -a "Finder"',
                'calculator': 'open -a "Calculator"',
                'notes': 'open -a "Notes"',
            },
            'linux': {
                # Browsers
                'chrome': 'google-chrome',
                'chromium': 'chromium',
                'browser': 'xdg-open http://google.com',
                'firefox': 'firefox',
                'edge': 'microsoft-edge',
                
                # Development
                'vscode': 'code',
                'vs code': 'code',
                'pycharm': 'pycharm',
                'sublime': 'subl',
                
                # Communication
                'whatsapp': 'whatsapp-for-linux',
                'telegram': 'telegram-desktop',
                'slack': 'slack',
                
                # Media
                'spotify': 'spotify',
                'vlc': 'vlc',
                
                # Utilities
                'terminal': 'gnome-terminal',
                'files': 'nautilus',
                'file manager': 'nautilus',
                'calculator': 'gnome-calculator',
                'text editor': 'gedit',
            }
        }
        
        # Get commands for current OS
        os_commands = app_commands.get(self.os, {})
        return os_commands.get(app_name)
    
    def _is_safe_url(self, url: str) -> bool:
        """
        Check if URL is safe to open
        
        Args:
            url: URL to check
            
        Returns:
            True if safe, False otherwise
        """
        # Block file:// and other potentially dangerous protocols
        blocked_protocols = ['file://', 'javascript:', 'data:', 'vbscript:']
        
        url_lower = url.lower()
        for protocol in blocked_protocols:
            if url_lower.startswith(protocol):
                return False
        
        # Allow http, https, and common URI schemes
        allowed_starts = ['http://', 'https://', 'www.', 
                         'whatsapp:', 'telegram:', 'slack:', 
                         'spotify:', 'discord:']
        
        return any(url_lower.startswith(start) for start in allowed_starts)
    
    def _is_safe_command(self, command: str) -> bool:
        """
        Check if command is safe to execute
        
        Args:
            command: Command string to check
            
        Returns:
            True if safe, False otherwise
        """
        command_lower = command.lower()
        
        # Check for blocked commands
        for blocked in self.blocked_commands:
            if blocked in command_lower:
                logger.error(f"🚨 SECURITY ALERT: Blocked command detected: {blocked}")
                return False
        
        # Block shell operators that could chain malicious commands
        dangerous_operators = ['&&', '||', ';', '|', '>', '<', '$(', '`']
        for op in dangerous_operators:
            if op in command and self.os != 'windows':  # Windows needs some operators
                if not (op == '>' and 'start' in command):  # Allow Windows start command
                    logger.warning(f"⚠️ Suspicious operator in command: {op}")
                    return False
        
        return True
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information
        
        Returns:
            Dictionary with system details
        """
        return {
            'os': self.os,
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version()
        }


# Global instance for easy access
_system_controller = None

def get_system_controller() -> SystemController:
    """Get global SystemController instance"""
    global _system_controller
    if _system_controller is None:
        _system_controller = SystemController()
    return _system_controller
