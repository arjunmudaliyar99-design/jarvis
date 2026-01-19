"""
JARVIS Configuration - API Keys, Settings, and Constants
"""
import os

# ====================================
# API CONFIGURATION
# ====================================

# Google Gemini API (Free tier available)
# Get your key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAqtPVSuadyLWg2PNTTtOmdbJgFRgYAt6I')

# API key is configured and ready!

# OpenAI API (Alternative)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY_HERE')

# Which AI to use: 'gemini' or 'openai'
AI_PROVIDER = 'gemini'

# Gmail API for email automation (Optional)
GMAIL_CREDENTIALS_PATH = 'credentials.json'
GMAIL_TOKEN_PATH = 'token.json'

# ====================================
# USER SETTINGS
# ====================================

USER_NAME = 'Arjun'
USER_LANGUAGE = 'hi'  # Hindi
USER_EMAIL = 'arjunmudaliyar99@gmail.com'

# ====================================
# VOICE SETTINGS
# ====================================

VOICE_CONFIG = {
    'rate': 165,                    # Speech rate (WPM)
    'volume': 1.0,                  # Volume (0.0 to 1.0)
    'energy_threshold': 3000,       # Microphone sensitivity
    'pause_threshold': 1.2,         # Pause detection (higher = capture longer)
    'phrase_timeout': 15,           # Max phrase length (seconds)
    'use_online_tts': True,         # Use gTTS (True) or pyttsx3 (False)
}

# ====================================
# AI SETTINGS
# ====================================

AI_CONFIG = {
    'model': 'gemini-flash-latest',  # Latest Flash model with separate quota
    'temperature': 0.7,               # Creativity (0-1)
    'max_tokens': 500,                # Max response length
    'conversation_memory': 10,        # Remember last N exchanges
    'system_prompt': f"""You are JARVIS, an advanced AI assistant for {USER_NAME}. 
You are helpful, intelligent, and conversational like a real human assistant.
You can control the computer, automate tasks, answer questions, and have natural conversations.
Be polite, friendly, and concise. Speak in a warm, professional tone.
When asked to perform tasks, acknowledge and confirm actions.
If information is missing, ask clarifying questions."""
}

# ====================================
# GUI SETTINGS
# ====================================

GUI_CONFIG = {
    'theme': 'dark',
    'primary_color': '#00e5ff',     # Neon cyan
    'secondary_color': '#00bcd4',   # Blue
    'bg_color': '#0b0f14',          # Dark background
    'animation_fps': 60,
    'waveform_bars': 32,
    'show_chat_history': True,
    'max_chat_messages': 50,
}

# ====================================
# AUTOMATION SETTINGS
# ====================================

# Application paths (update for your system)
APPS = {
    'chrome': 'start chrome',
    'browser': 'start chrome',
    'edge': 'start msedge',
    'firefox': 'start firefox',
    'vscode': 'code',
    'vs code': 'code',
    'visual studio code': 'code',
    'whatsapp': 'start whatsapp:',  # Opens installed WhatsApp app
    'slack': 'start https://slack.com',
    'notepad': 'notepad',
    'calculator': 'calc',
    'files': 'start explorer',
    'file explorer': 'start explorer',
    'explorer': 'start explorer',
    'terminal': 'start cmd',
    'cmd': 'start cmd',
    'powershell': 'start powershell',
}

# Websites for quick access
WEBSITES = {
    'youtube': 'https://www.youtube.com',
    'google': 'https://www.google.com',
    'gmail': 'https://mail.google.com',
    'github': 'https://github.com',
    'stackoverflow': 'https://stackoverflow.com',
    'wikipedia': 'https://www.wikipedia.org',
}

# Food delivery services
FOOD_SERVICES = {
    'swiggy': 'https://www.swiggy.com',
    'zomato': 'https://www.zomato.com',
}

# ====================================
# LOGGING SETTINGS
# ====================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'jarvis.log',
}
