"""
JARVIS Memory Module - Conversation History and Context Management
"""
import logging
from datetime import datetime
from collections import deque
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manages conversation history and context for JARVIS"""
    
    def __init__(self, max_memory: int = 10):
        """
        Initialize conversation memory
        
        Args:
            max_memory: Maximum number of conversation exchanges to remember
        """
        self.max_memory = max_memory
        self.conversation_history = deque(maxlen=max_memory)
        self.session_start = datetime.now()
        self.total_interactions = 0
        
        # Context tracking for educational conversations
        self.last_topic = None
        self.last_intent = None
        self.last_language = 'en'
        
        logger.info(f"✅ Conversation memory initialized (capacity: {max_memory})")
    
    def add_user_message(self, text: str, language: str = 'en', intent: Optional[str] = None, topic: Optional[str] = None):
        """Add user message to history with context"""
        message = {
            'role': 'user',
            'content': text,
            'language': language,
            'intent': intent,
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        self.total_interactions += 1
        
        # Update context tracking
        if language:
            self.last_language = language
        if intent:
            self.last_intent = intent
        if topic:
            self.last_topic = topic
        
        logger.info(f"📝 User message added: '{text[:50]}...'")
    
    def add_assistant_message(self, text: str, action: Optional[str] = None, intent: Optional[str] = None):
        """Add assistant response to history"""
        message = {
            'role': 'assistant',
            'content': text,
            'action': action,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        logger.info(f"💬 Assistant message added: '{text[:50]}...'")
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            last_n: Get last N messages (None = all)
            
        Returns:
            List of conversation messages
        """
        history = list(self.conversation_history)
        if last_n:
            history = history[-last_n:]
        return history
    
    def get_context_for_ai(self) -> List[Dict]:
        """
        Get formatted conversation history for AI model
        
        Returns:
            List of messages formatted for AI (role + content)
        """
        context = []
        for msg in self.conversation_history:
            context.append({
                'role': msg['role'],
                'content': msg['content']
            })
        return context
    
    def get_last_topic(self) -> Optional[str]:
        """Get the last discussed topic"""
        return self.last_topic
    
    def get_last_intent(self) -> Optional[str]:
        """Get the last detected intent"""
        return self.last_intent
    
    def get_last_language(self) -> str:
        """Get the last used language"""
        return self.last_language
    
    def get_last_user_message(self) -> Optional[str]:
        """Get the last message from user"""
        for msg in reversed(self.conversation_history):
            if msg['role'] == 'user':
                return msg['content']
        return None
    
    def get_last_assistant_message(self) -> Optional[str]:
        """Get the last response from assistant"""
        for msg in reversed(self.conversation_history):
            if msg['role'] == 'assistant':
                return msg['content']
        return None
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("🗑️ Conversation history cleared")
    
    def get_statistics(self) -> Dict:
        """Get conversation statistics"""
        return {
            'total_interactions': self.total_interactions,
            'messages_in_memory': len(self.conversation_history),
            'session_duration': str(datetime.now() - self.session_start),
            'session_start': self.session_start.isoformat()
        }
    
    def has_recent_context(self, keyword: str, within_last: int = 3) -> bool:
        """
        Check if a keyword appears in recent conversation
        
        Args:
            keyword: Word to search for
            within_last: Search within last N messages
            
        Returns:
            True if keyword found
        """
        recent = self.get_conversation_history(last_n=within_last)
        for msg in recent:
            if keyword.lower() in msg['content'].lower():
                return True
        return False
