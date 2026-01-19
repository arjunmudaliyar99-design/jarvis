"""
JARVIS Input Sanitizer - Security Module
Sanitizes and validates user input to prevent command injection and security issues
"""
import logging
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class InputSanitizer:
    """
    Security module to sanitize user input
    Prevents command injection, SQL injection, and other attacks
    """
    
    def __init__(self):
        """Initialize input sanitizer"""
        # Dangerous patterns that should be blocked
        self.dangerous_patterns = [
            # Command injection
            r'[;&|`$]',  # Shell operators
            r'\$\(',  # Command substitution
            r'>\s*/dev/',  # Device file access
            r'rm\s+-rf',  # Recursive delete
            r'format\s+',  # Format commands
            r'del\s+/[fs]',  # Windows delete
            
            # Path traversal
            r'\.\./\.\.',  # Directory traversal
            r'/etc/passwd',  # System files
            r'/etc/shadow',
            r'C:\\Windows\\System32',
            
            # Script injection
            r'<script',  # XSS
            r'javascript:',
            r'onerror=',
            r'onload=',
        ]
        
        # Compile patterns for performance
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.dangerous_patterns]
        
        logger.info("✅ Input sanitizer initialized")
    
    def sanitize_text(self, text: str) -> Tuple[bool, str, Optional[str]]:
        """
        Sanitize user input text
        
        Args:
            text: Raw user input
            
        Returns:
            Tuple of (is_safe, sanitized_text, warning_message)
        """
        if not text or not isinstance(text, str):
            return True, "", None
        
        # Check for dangerous patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                logger.warning(f"🚨 SECURITY: Dangerous pattern detected in input: {pattern.pattern}")
                return False, text, "Input contains potentially dangerous content"
        
        # Remove null bytes
        sanitized = text.replace('\x00', '')
        
        # Limit length to prevent DOS
        max_length = 1000
        if len(sanitized) > max_length:
            logger.warning(f"⚠️ Input too long ({len(sanitized)} chars), truncating to {max_length}")
            sanitized = sanitized[:max_length]
            warning = f"Input truncated to {max_length} characters"
        else:
            warning = None
        
        # Normalize whitespace
        sanitized = ' '.join(sanitized.split())
        
        return True, sanitized, warning
    
    def sanitize_url(self, url: str) -> Tuple[bool, str]:
        """
        Sanitize URL input
        
        Args:
            url: URL to sanitize
            
        Returns:
            Tuple of (is_safe, message)
        """
        if not url:
            return False, "Empty URL"
        
        url_lower = url.lower()
        
        # Block dangerous protocols
        dangerous_protocols = ['file://', 'javascript:', 'data:', 'vbscript:']
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                logger.error(f"🚨 SECURITY: Blocked dangerous protocol: {protocol}")
                return False, f"Protocol '{protocol}' is not allowed"
        
        # Allow only safe protocols
        safe_protocols = ['http://', 'https://', 'www.']
        is_safe = any(url_lower.startswith(protocol) for protocol in safe_protocols)
        
        if not is_safe:
            # Check if it's a domain without protocol (e.g., google.com)
            if '.' in url and not url.startswith('/'):
                return True, "URL is safe (assuming https)"
            else:
                logger.warning(f"⚠️ Suspicious URL: {url}")
                return False, "URL protocol not allowed"
        
        return True, "URL is safe"
    
    def sanitize_filename(self, filename: str) -> Tuple[bool, str]:
        """
        Sanitize filename input
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Tuple of (is_safe, sanitized_filename)
        """
        if not filename:
            return False, ""
        
        # Remove path separators
        sanitized = filename.replace('/', '_').replace('\\', '_')
        
        # Remove dangerous characters
        sanitized = re.sub(r'[<>:"|?*\x00-\x1f]', '', sanitized)
        
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        
        # Check for reserved names (Windows)
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                         'LPT1', 'LPT2', 'LPT3']
        if sanitized.upper() in reserved_names:
            logger.warning(f"⚠️ Reserved filename: {sanitized}")
            sanitized = f"file_{sanitized}"
        
        # Limit length
        max_length = 255
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return len(sanitized) > 0, sanitized
    
    def validate_command(self, command: str) -> Tuple[bool, str]:
        """
        Validate system command for safety
        
        Args:
            command: Command to validate
            
        Returns:
            Tuple of (is_safe, message)
        """
        if not command:
            return False, "Empty command"
        
        command_lower = command.lower()
        
        # Block dangerous commands
        dangerous_commands = [
            'rm -rf', 'del /f', 'format', 'fdisk', 'dd if=',
            'shutdown', 'reboot', 'init 0', 'halt',
            'mkfs', 'fsck', ':(){:|:&};:',  # Fork bomb
        ]
        
        for dangerous in dangerous_commands:
            if dangerous in command_lower:
                logger.error(f"🚨 SECURITY: Blocked dangerous command: {dangerous}")
                return False, f"Command '{dangerous}' is not allowed"
        
        # Block chaining operators (except on Windows for specific commands)
        dangerous_operators = ['&&', '||', ';', '|', '>', '<', '$(', '`']
        for op in dangerous_operators:
            if op in command:
                # Allow 'start' command on Windows
                if not (op in ['>', '|'] and 'start' in command_lower):
                    logger.warning(f"⚠️ Suspicious operator in command: {op}")
                    return False, f"Operator '{op}' is not allowed in commands"
        
        return True, "Command is safe"


# Global instance
_input_sanitizer = None

def get_input_sanitizer() -> InputSanitizer:
    """Get global InputSanitizer instance"""
    global _input_sanitizer
    if _input_sanitizer is None:
        _input_sanitizer = InputSanitizer()
    return _input_sanitizer
