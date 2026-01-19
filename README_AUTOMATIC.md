# 🤖 JARVIS - Automatic Voice Activated AI Assistant

**Personalized for: Arjun**

## ✨ Features

- 🎤 **Always Listening** - No buttons! Just say "Hello JARVIS"
- 🌏 **Tamil Priority** - Full support for Tamil + all Indian languages
- 👤 **Personalized** - Knows you as Arjun
- 🎨 **Futuristic UI** - Iron Man style circular interface
- 🗣️ **Automatic** - Everything hands-free
- 🌍 **25+ Languages** - Speak in any language

## 🚀 Quick Start

```powershell
python start_jarvis.py
```

**That's it!** JARVIS will:
1. Open in fullscreen with futuristic UI
2. Start listening automatically
3. Wait for "Hello JARVIS" wake word
4. Respond and take your command
5. Speak back automatically

## 🎯 How to Use

1. **Launch JARVIS** - Run the command above
2. **Say "Hello JARVIS"** - Anytime, in any language
3. **JARVIS responds** - "Yes, Arjun?" or similar
4. **Give your command** - Speak naturally
5. **JARVIS acts** - Processes and responds automatically

**No clicking, no typing - Pure voice control!**

## 🌏 Supported Indian Languages

### Priority Language
- 🇮🇳 **Tamil (தமிழ்)** - Full support

### All Indian Languages
- தமிழ் (Tamil)
- తెలుగు (Telugu)
- ಕನ್ನಡ (Kannada)
- മലയാളം (Malayalam)
- বাংলা (Bengali)
- मराठी (Marathi)
- ગુજરાતી (Gujarati)
- ਪੰਜਾਬੀ (Punjabi)
- ଓଡ଼ିଆ (Odia)
- অসমীয়া (Assamese)
- اردو (Urdu)
- हिन्दी (Hindi)

### Also Supports
English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Russian, Portuguese, Italian, and more!

## 💬 Example Commands (Say in ANY Language!)

**In English:**
- "Hello JARVIS"
- "What time is it?"
- "What's the date?"
- "Open notepad"
- "Tell me a joke"

**In Tamil (தமிழ்):**
- "ஹலோ ஜார்விஸ்"
- "இப்போது என்ன நேரம்?"
- "இன்றைய தேதி என்ன?"
- "நோட்பேடை திற"
- "ஒரு ஜோக் சொல்லு"

**In Hindi (हिन्दी):**
- "हैलो जार्विस"
- "समय क्या है?"
- "आज की तारीख क्या है?"
- "नोटपैड खोलो"
- "एक जोक सुनाओ"

**In Telugu (తెలుగు):**
- "హలో జార్విస్"
- "ఇప్పుడు సమయం ఎంత?"
- "ఈ రోజు తేదీ ఏమిటి?"
- "నోట్‌ప్యాడ్ తెరవండి"

## 🎨 User Interface

**Futuristic Design:**
- ⚫ Black background (like space)
- 🔵 Cyan/blue accents (Iron Man style)
- ⭕ Circular animated interface
- 💫 Rotating arcs and connecting lines
- 🎯 Central core that changes color by status

**Status Colors:**
- 🔵 Blue = Standby (waiting for wake word)
- 🟢 Green = Listening (recording your voice)
- 🟠 Orange = Processing (thinking)
- 🔵 Cyan = Speaking (JARVIS talking)

**No Text Display** - Everything is voice-based!

## 🎭 JARVIS Personality

- **Polite**: Always addresses you as "Arjun"
- **Professional**: Like a personal assistant
- **Helpful**: Ready to assist anytime
- **Smart**: Understands natural language

## 🔧 Technical Details

### Voice Processing Pipeline

```
1. Continuous Listening (background)
   ↓
2. Wake Word Detection ("Hello JARVIS")
   ↓
3. Acknowledge ("Yes, Arjun?")
   ↓
4. Listen for Command
   ↓
5. Language Detection (auto)
   ↓
6. Speech Recognition
   ↓
7. Translation to English (if needed)
   ↓
8. Command Processing
   ↓
9. Generate Response
   ↓
10. Translation to Your Language
    ↓
11. Text-to-Speech (automatic)
    ↓
12. Back to Standby
```

### Files

```
jarvis/
├── start_jarvis.py              # ⭐ START HERE
├── jarvis_launcher.py           # Main launcher
├── jarvis_futuristic_ui.py      # Futuristic UI (automatic)
├── jarvis_voice.py              # Voice processing
├── jarvis_gui.py                # Old GUI (backup)
└── .env                         # Configuration
```

## ⚙️ Configuration

### Personalization

Edit `jarvis_voice.py`:

```python
# Line ~50
self.user_name = 'Arjun'  # Your name
self.wake_word = 'jarvis'  # Wake word
```

### Add Commands

Edit `jarvis_futuristic_ui.py`, `process_command()` method:

```python
def process_command(self, english_text):
    text = english_text.lower()
    
    # Add your custom command
    if 'your trigger' in text:
        return "Your response, Arjun"
```

## 🐛 Troubleshooting

### JARVIS not hearing wake word
- Check microphone permissions
- Speak clearly: "Hello JARVIS"
- Try: "Hey JARVIS" or "Hi JARVIS"
- Ensure microphone is not muted

### Audio not playing
- Check speaker volume
- Ensure speakers/headphones connected
- Test: `python -c "import pygame; pygame.mixer.init()"`

### Wrong language detected
- Speak more clearly
- Use longer sentences
- Reduce background noise

### Exit fullscreen
- Press **ESC** key

## 🎓 Usage Tips

1. **Wake Word**: Say clearly with pause after
2. **Command**: Speak naturally, not robotic
3. **Background Noise**: Minimize for best results
4. **Language**: Stick to one language per command
5. **Patience**: Wait for response before next command

## 🚀 Advanced Features

### System Control

"Open notepad"
"Open calculator"
"Open browser"

### Information

"What time is it?"
"What's the date?"
"Tell me a joke"

### Personal

"What's my name?"
"Who are you?"
"Help me"

## 📊 Status Indicators

Watch the UI for status:

| Status | Color | Meaning |
|--------|-------|---------|
| STANDBY | 🔵 Blue | Waiting for wake word |
| LISTENING | 🟢 Green | Recording your voice |
| PROCESSING | 🟠 Orange | Thinking/analyzing |
| SPEAKING | 🔵 Cyan | JARVIS talking |

## 🎉 Ready to Use!

**Launch Command:**
```powershell
python start_jarvis.py
```

**Or:**
```powershell
C:/Users/HP/jarvis/.venv/Scripts/python.exe jarvis_launcher.py
```

### First Time Setup Complete! ✅

1. ✅ All Indian languages added (Tamil priority)
2. ✅ Wake word detection ("Hello JARVIS")
3. ✅ Personalized for Arjun
4. ✅ Futuristic UI created
5. ✅ Fully automatic operation
6. ✅ No conversation display
7. ✅ Continuous listening enabled

## 🌟 What's New

### From Previous Version:
- ❌ Removed: Manual microphone button
- ❌ Removed: Conversation text display
- ✅ Added: Automatic wake word detection
- ✅ Added: Continuous background listening
- ✅ Added: All Indian languages (Tamil, Telugu, etc.)
- ✅ Added: Personalization (Arjun)
- ✅ Added: Futuristic circular UI
- ✅ Added: Fullscreen mode

### Better Than Before:
- No clicking needed - pure voice
- Faster response - always ready
- More languages - 25+ supported
- Better UI - Iron Man style
- More personal - knows your name

## 💡 Pro Tips

1. **First Command**: After "Hello JARVIS", JARVIS will acknowledge. Then speak your command immediately.

2. **Multiple Commands**: After one command completes, say "Hello JARVIS" again for next command.

3. **Tamil Users**: JARVIS automatically detects Tamil and responds in Tamil!

4. **Mixed Language**: Don't mix languages in one sentence - stick to one language per command.

5. **Background Work**: JARVIS keeps listening even when you're doing other work.

## 🎬 Example Session

```
YOU: "Hello JARVIS"
JARVIS: "Yes, Arjun?"
YOU: "What time is it?"
JARVIS: "Arjun, the current time is 8:54 PM"

[Wait a moment]

YOU: "Hello JARVIS"
JARVIS: "How can I help you, Arjun?"
YOU: "Open notepad"
JARVIS: "Opening Notepad for you, Arjun"
```

## 🎤 Tamil Example

```
நீங்கள்: "ஹலோ ஜார்விஸ்"
ஜார்விஸ்: "Yes, Arjun?"
நீங்கள்: "இப்போது என்ன நேரம்?"
ஜார்விஸ்: "Arjun, இப்போதைய நேரம் மாலை 8:54"
```

---

**Enjoy your futuristic AI assistant, Arjun! 🚀**

Say "Hello JARVIS" to begin!
