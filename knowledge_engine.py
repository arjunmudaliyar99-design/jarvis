"""
JARVIS Knowledge Engine - Educational AI Brain
Explains concepts like a human teacher using Gemini AI
NO FALLBACKS - Always uses AI
"""
import logging
from typing import Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class KnowledgeEngine:
    """
    Advanced educational AI brain - ChatGPT-level explanations
    Always uses Gemini AI, no fallbacks
    """
    
    def __init__(self, api_key: str, model_name: str = 'gemini-flash-latest'):
        """
        Initialize knowledge engine with REQUIRED API key
        
        Args:
            api_key: Gemini API key (REQUIRED)
            model_name: Gemini model to use
        
        Raises:
            ValueError: If API key is missing
        """
        if not api_key:
            raise ValueError("❌ Gemini API key is REQUIRED for Knowledge Engine!")
        
        self.api_key = api_key
        self.model_name = model_name
        self.last_topic = None  # For context memory
        
        # Educational system prompt - human-like teacher
        self.system_prompt = """You are JARVIS, an advanced AI assistant and teacher.

Your teaching style:
1. START with a simple, relatable explanation (like explaining to a friend)
2. THEN provide technical details for deeper understanding
3. USE real-world examples and analogies
4. AVOID robotic language - be conversational and friendly
5. Keep responses concise but complete (2-4 short paragraphs)

Structure your responses like this:
- Simple Explanation (2-3 sentences)
- Technical Details (if needed)
- Real Example
- Quick Summary

Be natural, helpful, and educational. Sound like a senior developer mentoring a junior, not a textbook."""
        
        # Initialize Gemini
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✅ Gemini AI ({self.model_name}) initialized for knowledge responses")
        except Exception as e:
            logger.error(f"❌ Gemini initialization failed: {e}")
            raise
    
    def explain(self, question: str, context: Optional[str] = None) -> str:
        """
        Generate educational explanation using Gemini AI
        NO FALLBACKS - Always uses AI
        
        Args:
            question: User's question
            context: Optional context from previous conversation
            
        Returns:
            Human-like educational explanation from Gemini
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🧠 KNOWLEDGE ENGINE ACTIVATED")
        logger.info(f"❓ QUESTION: '{question}'")
        
        # Check if this is a follow-up question
        if context or self._is_followup_question(question):
            logger.info(f"🔄 FOLLOW-UP DETECTED (Last topic: {self.last_topic})")
            question = self._enhance_followup_question(question)
        
        # Generate AI response (NO FALLBACK)
        try:
            response = self._generate_ai_response(question)
            logger.info(f"✅ AI RESPONSE GENERATED ({len(response)} chars)")
            logger.info(f"{'='*60}\n")
            
            # Update context
            self._update_context(question)
            
            return response
        
        except Exception as e:
            logger.error(f"❌ AI generation failed: {e}")
            # Return error message instead of fallback
            return f"I encountered an error accessing my knowledge base: {str(e)}. Please try again."
    
    def _generate_ai_response(self, question: str) -> str:
        """Generate response using Gemini AI"""
        prompt = f"{self.system_prompt}\n\nQuestion: {question}\n\nExplain clearly:"
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def _is_followup_question(self, question: str) -> bool:
        """Check if question is a follow-up"""
        followup_patterns = [
            'explain again', 'simpler', 'more detail', 'example',
            'dobara', 'aur', 'phir se', 'simple mein'
        ]
        
        question_lower = question.lower()
        return any(pattern in question_lower for pattern in followup_patterns)
    
    def _enhance_followup_question(self, question: str) -> str:
        """Enhance follow-up question with context"""
        if self.last_topic:
            return f"Regarding {self.last_topic}: {question}"
        return question
    
    def _update_context(self, question: str):
        """Update conversation context"""
        topic = self._extract_topic(question)
        if topic:
            self.last_topic = topic
    
    def _extract_topic(self, text: str) -> Optional[str]:
        """Extract main topic from question"""
        words = text.lower().split()
        question_words = {'what', 'why', 'how', 'when', 'where', 'is', 'are', 'the', 'a', 'an',
                         'kya', 'kaise', 'kyu', 'hai', 'hain', 'explain', 'tell', 'batao'}
        
        topic_words = [w for w in words if w not in question_words and len(w) > 2]
        
        if topic_words:
            return ' '.join(topic_words[:3])
        
        return None
    
    def clear_context(self):
        """Clear conversation context"""
        self.last_topic = None
        logger.info("🧹 Context cleared")
