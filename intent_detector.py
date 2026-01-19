"""
JARVIS Intent Detector - Classifies user input into ACTION, INFORMATION, CONVERSATION, or EXIT
Critical component for dual-brain architecture
"""
import logging
from typing import Dict, Tuple
import re

logger = logging.getLogger(__name__)


class IntentDetector:
    """
    Advanced intent classification system
    Determines whether user wants ACTION or INFORMATION
    """
    
    def __init__(self):
        """Initialize intent detector with comprehensive keyword sets"""
        
        # ACTION KEYWORDS - System control and automation
        self.action_keywords = {
            # Apps
            'open', 'launch', 'start', 'kholo', 'chalu', 'run', 'kijiye', 'karo',
            # Media
            'play', 'chalao', 'bajao', 'sunao', 'watch', 'dekho', 'lagao', 'suno',
            # Communication
            'message', 'send', 'bhejo', 'email', 'call', 'text', 'msg',
            # Search
            'search', 'google', 'dhundo', 'khojo', 'find',
            # System
            'close', 'quit', 'stop', 'band', 'volume', 'mute',
            # Time
            'time', 'date', 'timer', 'alarm', 'reminder'
        }
        
        # INFORMATION KEYWORDS - Questions and learning
        self.information_keywords = {
            # Question words
            'what', 'why', 'how', 'when', 'where', 'who', 'which',
            'kya', 'kyu', 'kyun', 'kaise', 'kab', 'kahan', 'kaun',
            # Learning
            'explain', 'define', 'tell', 'batao', 'samjhao', 'describe',
            'mean', 'meaning', 'matlab', 'about', 'ke baare mein',
            # Concepts
            'concept', 'idea', 'theory', 'principle', 'definition'
        }
        
        # CONVERSATION KEYWORDS - Casual chat
        self.conversation_keywords = {
            'hello', 'hi', 'hey', 'namaste', 'good morning', 'good evening',
            'how are you', 'kaise ho', 'kya haal', 'thanks', 'thank you',
            'dhanyavaad', 'shukriya', 'sorry', 'maaf karo'
        }
        
        # EXIT KEYWORDS
        self.exit_keywords = {
            'exit', 'quit', 'goodbye', 'bye', 'band karo', 'close jarvis',
            'sleep', 'stop listening'
        }
        
        # APP NAMES for action detection
        self.app_names = {
            'chrome', 'firefox', 'edge', 'browser',
            'code', 'vscode', 'visual studio',
            'whatsapp', 'telegram', 'slack',
            'spotify', 'vlc', 'media player',
            'notepad', 'calculator', 'paint',
            'excel', 'word', 'powerpoint',
            'youtube', 'video', 'song', 'music'  # Added media apps
        }
        
        logger.info("✅ Intent detector initialized with comprehensive rules")
    
    def classify_intent(self, text: str) -> Tuple[str, float, Dict]:
        """
        Classify user input into one of four intents:
        - ACTION: System control, automation (NEVER sent to Gemini)
        - INFORMATION: Questions, explanations, learning (Gemini handles)
        - CONVERSATION: Casual chat, greetings (Gemini handles)
        - EXIT: Shutdown commands
        
        CRITICAL: System commands MUST be classified as ACTION to prevent
        sending them to Gemini for reasoning instead of executing them.
        
        Args:
            text: User input
            
        Returns:
            Tuple of (intent, confidence, details)
        """
        text_lower = text.lower().strip()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 INTENT CLASSIFICATION")
        logger.info(f"📝 INPUT: '{text}'")
        
        # PRIORITY 1: Check for EXIT intent
        exit_score = self._calculate_keyword_score(text_lower, self.exit_keywords)
        if exit_score > 0.5:
            logger.info(f"🚪 DETECTED: EXIT (confidence: {exit_score:.2f})")
            logger.info(f"{'='*60}\n")
            return 'EXIT', exit_score, {'reason': 'exit_keyword_match'}
        
        # PRIORITY 2: Check for ACTION intent (MUST be high priority)
        # System commands should NEVER go to Gemini
        action_score = self._calculate_action_score(text_lower)
        
        # PRIORITY 3: Check for INFORMATION intent
        info_score = self._calculate_information_score(text_lower)
        
        # PRIORITY 4: Check for CONVERSATION intent
        conversation_score = self._calculate_conversation_score(text_lower)
        
        # Log all scores
        logger.info(f"📊 SCORES:")
        logger.info(f"   ACTION: {action_score:.2f}")
        logger.info(f"   INFORMATION: {info_score:.2f}")
        logger.info(f"   CONVERSATION: {conversation_score:.2f}")
        
        # CRITICAL DECISION LOGIC:
        # If action score is significant, treat as ACTION to ensure execution
        if action_score >= 0.4:  # Lower threshold for better detection
            logger.info(f"⚡ FINAL INTENT: ACTION (confidence: {action_score:.2f})")
            logger.info(f"🚨 SYSTEM COMMAND - Will execute locally, NOT sent to Gemini")
            logger.info(f"{'='*60}\n")
            return 'ACTION', action_score, {'type': 'system_control'}
        
        elif info_score > 0.4:  # Information/learning
            logger.info(f"📚 FINAL INTENT: INFORMATION (confidence: {info_score:.2f})")
            logger.info(f"🤖 KNOWLEDGE REQUEST - Will query Gemini AI")
            logger.info(f"{'='*60}\n")
            return 'INFORMATION', info_score, {'type': 'knowledge_request'}
        
        elif conversation_score > 0.3:  # Casual conversation
            logger.info(f"💬 FINAL INTENT: CONVERSATION (confidence: {conversation_score:.2f})")
            logger.info(f"🤖 CASUAL CHAT - Will use Gemini for response")
            logger.info(f"{'='*60}\n")
            return 'CONVERSATION', conversation_score, {'type': 'casual_chat'}
        
        else:
            # Default to INFORMATION if unclear (educational bias)
            logger.info(f"❓ UNCLEAR - Defaulting to INFORMATION")
            logger.info(f"🤖 Will query Gemini AI for best response")
            logger.info(f"{'='*60}\n")
            return 'INFORMATION', 0.5, {'type': 'unclear_fallback'}
    
    def _calculate_action_score(self, text: str) -> float:
        """Calculate action intent score"""
        score = 0.0
        
        # Check for action keywords
        keyword_score = self._calculate_keyword_score(text, self.action_keywords)
        score += keyword_score * 0.6  # Increased weight
        
        # Check for app names
        app_score = self._calculate_keyword_score(text, self.app_names)
        score += app_score * 0.4  # Increased weight
        
        # Check for command patterns (strong indicators)
        command_patterns = [
            'open', 'play', 'send to', 'search for', 
            'kholo', 'chalao', 'bajao', 'bhejo', 'kijiye'
        ]
        if any(pattern in text for pattern in command_patterns):
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_information_score(self, text: str) -> float:
        """Calculate information intent score"""
        score = 0.0
        
        # Check for information keywords
        keyword_score = self._calculate_keyword_score(text, self.information_keywords)
        score += keyword_score * 0.6
        
        # Check for question marks
        if '?' in text:
            score += 0.3
        
        # Check for "is/are" patterns (definitions)
        if re.search(r'\b(is|are|was|were|hai|hain)\b', text):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_conversation_score(self, text: str) -> float:
        """Calculate conversation intent score"""
        score = self._calculate_keyword_score(text, self.conversation_keywords)
        
        # Short inputs are often conversational
        if len(text.split()) <= 3:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_keyword_score(self, text: str, keywords: set) -> float:
        """Calculate keyword match score"""
        words = set(text.split())
        matches = len(words.intersection(keywords))
        
        if matches == 0:
            return 0.0
        
        # More matches = higher score
        return min(matches * 0.3, 1.0)
