# JARVIS - Advanced AI Assistant

A fully advanced, human-like AI assistant with natural conversation, task automation, and modern GUI.

## 🌟 Features

### Core Capabilities
- **🎤 Voice Input/Output** - Natural speech recognition and human-like TTS
- **🧠 AI Brain** - Powered by Google Gemini for natural conversation
- **🤖 Task Automation** - System control, browser automation, messaging
- **💬 Conversation Memory** - Context-aware responses
- **🎨 Modern GUI** - Futuristic HUD with real-time animations
- **🌍 Multilingual** - Support for Hindi, Tamil, English, and more

### Automation Features
- ✅ Open applications (Chrome, VS Code, WhatsApp, etc.)
- ✅ Google search and web navigation
- ✅ YouTube video playback
- ✅ WhatsApp messaging
- ✅ Email drafting
- ✅ Food ordering (Swiggy/Zomato)
- ✅ Keyboard automation (type text, press keys)
- ✅ Time/date queries
- ✅ Natural conversation

## 📋 Installation

### 1. Install Dependencies

```bash
pip install customtkinter speechrecognition pyttsx3 deep-translator langdetect pyautogui google-generativeai gtts pygame
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy your API key

### 3. Configure

Edit `config.py`:

```python
GEMINI_API_KEY = 'your-api-key-here'  # Paste your key
USER_NAME = 'Arjun'  # Your name
USER_LANGUAGE = 'hi'  # Output language (hi=Hindi, en=English)
```

## 🚀 Usage

### Start JARVIS

```bash
python main.py
```

### Voice Commands

Just speak naturally - no wake word required!

**System Control:**
- "Open Chrome"
- "Open VS Code"
- "Launch WhatsApp"

**Search & Browse:**
- "Search for Python tutorials"
- "Google machine learning"

**YouTube:**
- "Play Believer on YouTube"
- "Open YouTube and play some music"

**Messaging:**
- "Open WhatsApp"
- "Type hello and send"

**Food Ordering:**
- "Order food from Swiggy"
- "Open Zomato"

**Information:**
- "What time is it?"
- "What's today's date?"

**Conversation:**
- "How are you?"
- "Who are you?"
- "Thank you"

**Exit:**
- "Exit"
- "Goodbye"

## 🏗️ Architecture

```
main.py                    → Application launcher
├── config.py              → Configuration and API keys
├── jarvis_memory.py       → Conversation history
├── jarvis_brain.py        → AI intelligence (Gemini)
├── jarvis_tasks.py        → Task automation
├── jarvis_voice_advanced.py → Voice I/O system
└── jarvis_gui_advanced.py → Modern GUI with animations
```

## 🎨 GUI Features

- **Animated Visualizer** - Rotating rings and pulsing core
- **Status Indicators** - STANDBY, LISTENING, THINKING, SPEAKING
- **Voice Waveform** - Real-time audio visualization
- **Chat Interface** - Complete conversation history
- **Futuristic Design** - Iron Man JARVIS-style HUD

## 🧠 AI Features

### Natural Conversation
JARVIS uses Google Gemini for human-like responses:
- Context awareness
- Follow-up questions
- Natural tone
- Clarification requests

### Intent Detection
Hybrid AI + rule-based system:
- **Tasks** - System actions (open, search, etc.)
- **Questions** - Information queries
- **Conversation** - Casual chat

### Memory Management
- Remembers last 10 conversation exchanges
- Context-aware responses
- Session statistics

## ⚙️ Configuration

### Voice Settings (`config.py`)

```python
VOICE_CONFIG = {
    'rate': 165,                    # Speech speed
    'volume': 1.0,                  # Volume
    'energy_threshold': 3000,       # Mic sensitivity
    'use_online_tts': True,         # gTTS vs pyttsx3
}
```

### AI Settings

```python
AI_CONFIG = {
    'model': 'gemini-pro',          # AI model
    'temperature': 0.7,             # Creativity
    'conversation_memory': 10,      # Memory size
}
```

### Applications

Add your apps to `APPS` dict in `config.py`:

```python
APPS = {
    'myapp': 'start C:\\Path\\To\\App.exe',
}
```

## 🔧 Advanced Usage

### Custom Commands

Edit `jarvis_tasks.py` to add new automation:

```python
def my_custom_task(self, query: str) -> str:
    # Your automation code
    return "Task completed"
```

### Keyboard Automation

Commands:
- "Type your message here"
- "Press enter"
- "Send it"

Uses `pyautogui` for keyboard control.

### Email Integration

Gmail integration ready:
- Opens Gmail compose
- Voice-dictated emails

For full automation, add Gmail API credentials.

## 📊 Performance

- **Multithreading** - Voice processing doesn't freeze GUI
- **60 FPS Animations** - Smooth visualizations
- **Error Handling** - Graceful fallbacks
- **Logging** - Complete debug logs in `jarvis.log`

## 🐛 Troubleshooting

### "No speech detected"
- Adjust `energy_threshold` in config (lower = more sensitive)
- Check microphone permissions

### "API key not configured"
- Add Gemini API key to `config.py`
- Or set `GEMINI_API_KEY` environment variable

### "Module not found"
```bash
pip install [missing-package]
```

### Voice too robotic
- Set `use_online_tts: True` in config for gTTS (better quality)

## 🎯 Roadmap

- [ ] Gmail API integration for automated emails
- [ ] Spotify integration for music control
- [ ] Calendar management
- [ ] Smart home control
- [ ] Custom skill plugins
- [ ] Mobile app companion

## 📝 License

MIT License - Feel free to modify and use!

## 🙏 Credits

Built with:
- Google Gemini AI
- CustomTkinter
- SpeechRecognition
- gTTS / pyttsx3
- PyAutoGUI

---

**Made with ❤️ for advanced automation and human-like AI interaction**

## 🚀 Quick Start Example

```bash
# Install
pip install -r requirements.txt

# Configure API key in config.py
# Then run
python main.py

# Speak: "Hello, what can you do?"
# JARVIS will respond and explain its capabilities!
```

Enjoy your advanced AI assistant! 🤖✨
