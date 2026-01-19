"""
JARVIS - Main Launcher (Simplified Version)
Launch this file to start JARVIS voice assistant with GUI
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'customtkinter': 'CustomTkinter',
        'speech_recognition': 'SpeechRecognition',
        'gtts': 'gTTS',
        'langdetect': 'langdetect',
        'pygame': 'pygame',
        'deep_translator': 'deep-translator'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(name)
    
    if missing:
        logger.error(f"❌ Missing packages: {', '.join(missing)}")
        logger.info("Install with: pip install customtkinter gtts deep-translator langdetect pygame speechrecognition pyaudio")
        return False
    
    return True


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🤖 JARVIS AI Assistant - Automatic Voice Control")
    logger.info("=" * 60)
    logger.info("👤 User: Arjun")
    logger.info("🎤 Always listening for: 'Hello JARVIS'")
    logger.info("🌍 Supports: Tamil, Telugu, Hindi, and 20+ languages")
    logger.info("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and launch JARVIS HUD (Iron Man style)
        logger.info("🚀 Starting JARVIS HUD...")
        logger.info("💡 Just say 'Hello JARVIS' to activate!")
        logger.info("⚡ Press ESC to exit fullscreen mode")
        logger.info("")
        
        from jarvis_gui import JarvisHUD
        
        app = JarvisHUD()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("\n👋 JARVIS shutting down...")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
