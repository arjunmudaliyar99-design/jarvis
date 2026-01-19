"""
JARVIS - Advanced AI Assistant
Main Application Launcher

A fully advanced AI assistant with:
- Natural conversation (Gemini AI)
- Voice input/output
- Task automation
- Modern GUI
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'customtkinter': 'customtkinter',
        'speech_recognition': 'SpeechRecognition',
        'pyttsx3': 'pyttsx3',
        'deep_translator': 'deep-translator',
        'langdetect': 'langdetect',
        'pyautogui': 'pyautogui',
        'google.generativeai': 'google-generativeai',
        'gtts': 'gtts',
        'pygame': 'pygame',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module.split('.')[0])
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.error(f"❌ Missing packages: {', '.join(missing)}")
        logger.error(f"Install with: pip install {' '.join(missing)}")
        return False
    
    return True


def main():
    """Main application entry point"""
    logger.info("=" * 70)
    logger.info("JARVIS - Advanced AI Assistant")
    logger.info("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Please install missing dependencies first")
        return
    
    # Import modules
    try:
        from config import USER_NAME, AI_CONFIG, GEMINI_API_KEY
        from jarvis_memory import ConversationMemory
        from jarvis_brain import JarvisBrain
        from jarvis_tasks import JarvisTasks
        from jarvis_voice_advanced import JarvisVoiceSystem
        from jarvis_gui_advanced import JarvisAdvancedGUI
        
        logger.info(f"User: {USER_NAME}")
        logger.info(f"AI Model: {AI_CONFIG['model']}")
        logger.info(f"✅ Gemini API configured")
        logger.info("=" * 70)
        
        # Initialize systems
        logger.info("Initializing systems...")
        
        # 1. Memory system
        memory = ConversationMemory(max_memory=AI_CONFIG['conversation_memory'])
        
        # 2. AI Brain
        brain = JarvisBrain(memory)
        
        # 3. Task executor
        tasks = JarvisTasks()
        
        # 4. Voice system
        voice = JarvisVoiceSystem()
        
        # 5. GUI
        logger.info("Starting GUI...")
        gui = JarvisAdvancedGUI(voice, brain, tasks, memory)
        
        # Run
        gui.run()
        
        logger.info("JARVIS shutting down...")
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
