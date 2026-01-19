"""
JARVIS Quick Start Script - Iron Man HUD Interface
Run this to launch JARVIS with one command
"""

import subprocess
import sys
import os

# Get the virtual environment Python path
venv_python = r"C:/Users/HP/jarvis/.venv/Scripts/python.exe"
launcher = r"C:\Users\HP\jarvis\jarvis_launcher.py"

print("=" * 70)
print("🤖 JARVIS HUD - Iron Man Style Interface")
print("=" * 70)
print()
print("✅ Mode: Fully Automatic Voice Activated")
print("✅ User: Arjun")
print("✅ Wake Word: 'Hello JARVIS'")
print("✅ Voice: Natural Male Voice (pyttsx3)")
print("✅ Languages: Tamil, Telugu, Hindi, English + 20 more")
print()
print("🎨 Interface Features:")
print("  • Iron Man style circular HUD")
print("  • Rotating animated rings")
print("  • Left panel: System status, time, user info")
print("  • Right panel: Quick access apps")
print("  • Center: Voice activation mic button")
print("  • Neon cyan/blue theme")
print()
print("📝 How to Use:")
print("  1. HUD opens in fullscreen")
print("  2. Say 'Hello JARVIS' anytime")
print("  3. JARVIS responds with male voice")
print("  4. Give your command in any language")
print("  5. Press ESC to exit")
print()
print("=" * 70)
print()

# Launch JARVIS
subprocess.run([venv_python, launcher])
