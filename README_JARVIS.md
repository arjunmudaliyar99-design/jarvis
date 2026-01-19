# 🤖 JARVIS - Multilingual Voice Assistant

A modern, Python-based voice assistant with a sleek GUI, multilingual support, and intelligent command processing.

## ✨ Features

- 🎤 **Voice Recognition** - Speaks and understands multiple languages
- 🌍 **Multilingual Support** - Automatically detects and responds in your language
- 🎨 **Modern GUI** - Dark theme with CustomTkinter
- 🔊 **Text-to-Speech** - Natural-sounding voice responses
- 🧠 **Smart Processing** - Understands natural language commands
- ⚡ **Async-Ready** - Built with modern Python async/await patterns

## 📋 Supported Languages

- English
- Hindi
- Spanish
- French
- German
- Chinese
- Japanese
- Korean
- Arabic
- Russian
- Portuguese
- Italian
- And many more...

## 🚀 Quick Start

### 1. Install Dependencies

All dependencies are already installed in your virtual environment:

```powershell
# Activate virtual environment (if not already active)
.\.venv\Scripts\activate

# Dependencies installed:
# - customtkinter (Modern GUI)
# - gtts (Text-to-Speech)
# - deep-translator (Translation)
# - langdetect (Language Detection)
# - pygame (Audio Playback)
# - speechrecognition (Voice Recognition)
# - pyaudio (Microphone Access)
```

### 2. Run JARVIS

```powershell
# Option 1: Using launcher (recommended)
C:/Users/HP/jarvis/.venv/Scripts/python.exe jarvis_launcher.py

# Option 2: Direct GUI launch
C:/Users/HP/jarvis/.venv/Scripts/python.exe jarvis_gui.py

# Option 3: Test voice module
C:/Users/HP/jarvis/.venv/Scripts/python.exe jarvis_voice.py
```

### 3. Use JARVIS

1. Click the **🎤 Start Listening** button
2. Speak your command in any supported language
3. JARVIS will detect your language and respond accordingly

## 📁 Project Structure

```
jarvis/
├── jarvis_launcher.py      # Main entry point (START HERE)
├── jarvis_gui.py           # Modern GUI with CustomTkinter
├── jarvis_voice.py         # Multilingual voice processing
├── agent.py                # Core agent logic (simplified)
├── agent_old_backup.py     # Original agent (backup)
├── .env                    # API keys configuration
└── README.md              # This file
```

## 🎯 How It Works

### Voice Processing Pipeline

```
1. User Speaks → Microphone captures audio
2. Speech Recognition → Converts speech to text
3. Language Detection → Identifies spoken language
4. Translation → Converts to English (if needed)
5. Command Processing → JARVIS processes the command
6. Response Translation → Converts response to user's language
7. Text-to-Speech → JARVIS speaks the response
```

### Architecture

```python
# jarvis_voice.py - Handles all voice/language operations
class JarvisVoice:
    - listen()                    # Capture and recognize speech
    - translate_to_english()      # Translate input
    - translate_from_english()    # Translate response
    - speak()                     # Text-to-speech output
    - process_multilingual_command()  # Complete pipeline

# jarvis_gui.py - Modern GUI interface
class JarvisGUI:
    - setup_ui()                  # Create interface
    - toggle_listening()          # Handle mic button
    - voice_recognition_thread()  # Background voice processing
    - process_command()           # Command logic
    - add_message()               # Display conversation

# agent.py - Core logic (for extensions)
class JarvisAgent:
    - process_command_async()     # Async command processing
    - process_command()           # Sync wrapper
```

## 🎨 GUI Features

- **Dark Mode** - Easy on the eyes
- **Blue Theme** - Professional appearance
- **Status Indicator** - Shows current state (Idle/Listening/Speaking)
- **Conversation Log** - Displays full conversation history
- **Language Indicator** - Shows detected language
- **Responsive Design** - Smooth, no-freeze operation

## 💬 Example Commands

Try saying these in any language:

- "Hello JARVIS"
- "What time is it?"
- "What's the date today?"
- "Tell me a joke"
- "Open notepad"
- "Help me"
- "Thank you"

## 🔧 Configuration

### API Keys (.env)

The `.env` file contains placeholders for various APIs. Most features work without these, but for advanced functionality:

```env
# Optional: For advanced features
Google_api_key=YOUR_KEY_HERE
OpenAI_api_key=YOUR_KEY_HERE
weather_api_key=YOUR_KEY_HERE
```

## 🐛 Troubleshooting

### Microphone Not Working

1. Check microphone permissions in Windows Settings
2. Ensure microphone is set as default input device
3. Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### Audio Not Playing

1. Check volume settings
2. Ensure speakers/headphones are connected
3. Test pygame: `python -c "import pygame; pygame.mixer.init(); print('OK')"`

### Language Detection Issues

- Speak clearly and at normal pace
- Reduce background noise
- Try speaking closer to the microphone
- Ensure the language is in the supported list

### GUI Not Opening

1. Check CustomTkinter installation: `pip show customtkinter`
2. Update graphics drivers
3. Try running as administrator

## 🔄 Recent Changes

### Fixed Issues

1. ✅ Fixed `asyncio` typo in original agent.py
2. ✅ Replaced incompatible `googletrans` with `deep-translator`
3. ✅ Replaced problematic `playsound` with `pygame`
4. ✅ Fixed font configuration in CustomTkinter textbox
5. ✅ Created simplified, working version of agent.py
6. ✅ Added comprehensive error handling

### Major Updates

- **Multilingual Support**: Complete language detection and translation
- **Modern GUI**: Sleek CustomTkinter interface
- **Threading**: No GUI freeze during voice recognition
- **Error Handling**: Graceful handling of all edge cases

## 🚀 Extending JARVIS

### Adding New Commands

Edit `jarvis_gui.py`, `process_command()` method:

```python
def process_command(self, english_text):
    text = english_text.lower()
    
    # Add your custom command
    if 'your trigger' in text:
        # Your logic here
        return "Your response"
```

### Integrating AI Models

You can integrate OpenAI, Google Gemini, or other AI models:

```python
# In jarvis_gui.py
def process_command(self, english_text):
    # Call your AI model
    response = your_ai_model.generate(english_text)
    return response
```

### Adding System Control

```python
import subprocess

def process_command(self, english_text):
    if 'open notepad' in text:
        subprocess.Popen(['notepad.exe'])
        return "Opening Notepad"
```

## 📚 Code Documentation

### jarvis_voice.py

All voice-related functionality with complete docstrings.

**Key Methods:**
- `listen(timeout, phrase_time_limit)` - Capture speech
- `translate_to_english(text, source_lang)` - Translate to English
- `translate_from_english(text, target_lang)` - Translate from English
- `speak(text, lang, async_mode)` - Text-to-speech
- `process_multilingual_command(callback)` - Complete pipeline

### jarvis_gui.py

CustomTkinter-based GUI with threading support.

**Key Methods:**
- `setup_ui()` - Create all UI elements
- `set_status(status, color)` - Update status indicator
- `add_message(sender, message, color)` - Add to conversation
- `toggle_listening()` - Start/stop voice recognition
- `voice_recognition_thread()` - Background voice processing
- `process_command(english_text)` - Command processing logic

### jarvis_launcher.py

Simple launcher with dependency checking.

## 🔐 Privacy & Security

- All speech recognition happens locally first
- Translation uses Google Translate API (data sent to Google)
- No data is stored or logged except in memory during session
- No telemetry or tracking

## 🤝 Contributing

To add features to JARVIS:

1. Keep the modular structure
2. Add docstrings to all functions
3. Handle errors gracefully
4. Test with multiple languages
5. Update this README

## 📝 License

This is a personal project. Use and modify as needed.

## 🎓 Learning Resources

- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [SpeechRecognition Docs](https://pypi.org/project/SpeechRecognition/)
- [gTTS Documentation](https://gtts.readthedocs.io/)
- [Deep Translator](https://deep-translator.readthedocs.io/)

## 💡 Tips

1. **Best Audio Quality**: Use a good microphone in a quiet environment
2. **Language Mixing**: Stick to one language per command for best results
3. **Command Length**: Keep commands concise (under 10 seconds)
4. **Response Time**: First request may be slower (loading models)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review terminal output for error messages
3. Verify all dependencies are installed
4. Test individual modules (voice, gui) separately

## 🎉 Success!

You now have a fully functional multilingual voice assistant! 

**Start JARVIS with:**
```powershell
C:/Users/HP/jarvis/.venv/Scripts/python.exe jarvis_launcher.py
```

Enjoy your AI assistant! 🚀
