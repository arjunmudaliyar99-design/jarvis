"""
JARVIS - Futuristic UI (Iron Man Style)
Automatic voice-activated assistant with circular interface
"""

import customtkinter as ctk
from tkinter import Canvas
import threading
import queue
import math
import time
from datetime import datetime
from jarvis_voice import JarvisVoice
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JarvisFuturisticUI:
    """Futuristic JARVIS Interface - Always listening, voice activated"""
    
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("JARVIS AI Assistant")
        
        # Fullscreen borderless window
        self.root.attributes('-fullscreen', True)
        self.root.configure(fg_color="#000000")
        
        # Bind escape to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Initialize voice module
        self.voice = JarvisVoice()
        
        # State variables
        self.is_active = False
        self.is_speaking = False
        self.status = "STANDBY"
        self.message_queue = queue.Queue()
        
        # Animation variables
        self.rotation = 0
        self.pulse_phase = 0
        
        # Setup UI
        self.setup_ui()
        
        # Start continuous listening thread
        self.listening_thread = threading.Thread(target=self.continuous_listening, daemon=True)
        self.listening_thread.start()
        
        # Start animation loop
        self.root.after(50, self.animate)
        
        # Start message processor
        self.root.after(100, self.process_message_queue)
        
        logger.info("✅ JARVIS Futuristic UI Initialized")
    
    def setup_ui(self):
        """Create futuristic circular interface"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas for circular graphics
        self.canvas = Canvas(
            main_frame,
            bg="#000000",
            highlightthickness=0,
            width=1920,
            height=1080
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Get center coordinates
        self.center_x = 960
        self.center_y = 540
        
        # Draw static elements
        self.draw_static_elements()
        
        # Status overlay
        self.status_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        self.status_frame.place(relx=0.5, rely=0.1, anchor="center")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● JARVIS AI",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00ffff"
        )
        self.status_label.pack()
        
        self.mode_label = ctk.CTkLabel(
            self.status_frame,
            text="STANDBY MODE - Say 'Hello JARVIS' to activate",
            font=ctk.CTkFont(size=16),
            text_color="#0099ff"
        )
        self.mode_label.pack(pady=5)
        
        # Bottom info
        self.info_label = ctk.CTkLabel(
            main_frame,
            text=f"User: Arjun | {datetime.now().strftime('%H:%M:%S')} | Press ESC to exit",
            font=ctk.CTkFont(size=12),
            text_color="#006699"
        )
        self.info_label.place(relx=0.5, rely=0.95, anchor="center")
    
    def draw_static_elements(self):
        """Draw static circular elements"""
        # Outer ring
        self.canvas.create_oval(
            self.center_x - 300, self.center_y - 300,
            self.center_x + 300, self.center_y + 300,
            outline="#003366",
            width=2
        )
        
        # Middle ring
        self.canvas.create_oval(
            self.center_x - 250, self.center_y - 250,
            self.center_x + 250, self.center_y + 250,
            outline="#004488",
            width=2
        )
        
        # Inner circle
        self.canvas.create_oval(
            self.center_x - 100, self.center_y - 100,
            self.center_x + 100, self.center_y + 100,
            outline="#0066aa",
            width=3
        )
        
        # Core circle
        self.core_circle = self.canvas.create_oval(
            self.center_x - 50, self.center_y - 50,
            self.center_x + 50, self.center_y + 50,
            fill="#001133",
            outline="#00aaff",
            width=3
        )
    
    def animate(self):
        """Animate the interface"""
        # Clear dynamic elements
        self.canvas.delete("dynamic")
        
        # Rotation
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
        
        # Pulse effect
        self.pulse_phase += 0.1
        pulse = math.sin(self.pulse_phase) * 0.3 + 0.7
        
        # Draw animated rings based on status
        if self.status == "LISTENING":
            color = "#00ff00"
            self.draw_rotating_arc(200, color, pulse)
            self.draw_rotating_arc(220, color, pulse * 0.8)
        elif self.status == "PROCESSING":
            color = "#ffaa00"
            self.draw_rotating_arc(200, color, pulse)
        elif self.status == "SPEAKING":
            color = "#00aaff"
            self.draw_rotating_arc(200, color, pulse)
            self.draw_rotating_arc(180, color, pulse * 0.7)
        else:
            color = "#003366"
            self.draw_rotating_arc(200, color, 0.5)
        
        # Update core circle color
        core_colors = {
            "STANDBY": "#001133",
            "LISTENING": "#003300",
            "PROCESSING": "#332200",
            "SPEAKING": "#001133"
        }
        self.canvas.itemconfig(self.core_circle, fill=core_colors.get(self.status, "#001133"))
        
        # Draw connecting lines
        self.draw_connecting_lines()
        
        # Schedule next frame
        self.root.after(50, self.animate)
    
    def draw_rotating_arc(self, radius, color, opacity):
        """Draw rotating arc segments"""
        num_segments = 8
        for i in range(num_segments):
            angle = (self.rotation + i * 45) % 360
            start_angle = angle
            extent = 30
            
            x1 = self.center_x + radius * math.cos(math.radians(angle))
            y1 = self.center_y + radius * math.sin(math.radians(angle))
            x2 = self.center_x + (radius + 20) * math.cos(math.radians(angle + extent))
            y2 = self.center_y + (radius + 20) * math.sin(math.radians(angle + extent))
            
            self.canvas.create_arc(
                self.center_x - radius, self.center_y - radius,
                self.center_x + radius, self.center_y + radius,
                start=start_angle,
                extent=extent,
                outline=color,
                width=int(3 * opacity),
                style="arc",
                tags="dynamic"
            )
    
    def draw_connecting_lines(self):
        """Draw connecting lines from center"""
        num_lines = 12
        for i in range(num_lines):
            angle = (self.rotation * 2 + i * 30) % 360
            length = 150 + math.sin(self.pulse_phase + i) * 20
            
            x = self.center_x + length * math.cos(math.radians(angle))
            y = self.center_y + length * math.sin(math.radians(angle))
            
            self.canvas.create_line(
                self.center_x, self.center_y,
                x, y,
                fill="#004488",
                width=1,
                tags="dynamic"
            )
    
    def set_status(self, status, message=""):
        """Update status display"""
        self.status = status
        
        status_colors = {
            "STANDBY": "#0099ff",
            "LISTENING": "#00ff00",
            "PROCESSING": "#ffaa00",
            "SPEAKING": "#00aaff"
        }
        
        status_messages = {
            "STANDBY": "STANDBY MODE - Say 'Hello JARVIS' to activate",
            "LISTENING": "LISTENING - Speak your command",
            "PROCESSING": "PROCESSING - Analyzing your request",
            "SPEAKING": "SPEAKING - Jarvis is responding"
        }
        
        self.mode_label.configure(
            text=message if message else status_messages.get(status, status),
            text_color=status_colors.get(status, "#0099ff")
        )
        
        # Update time
        self.info_label.configure(
            text=f"User: Arjun | {datetime.now().strftime('%H:%M:%S')} | Press ESC to exit"
        )
    
    def continuous_listening(self):
        """Continuously listen for wake word and commands"""
        logger.info("🎤 Continuous listening started...")
        
        # Greet user on startup
        time.sleep(1)
        self.message_queue.put({'type': 'greet'})
        
        while True:
            try:
                # Listen for wake word
                if not self.is_active:
                    if self.voice.listen_for_wake_word(timeout=5):
                        self.is_active = True
                        self.message_queue.put({'type': 'status', 'status': 'LISTENING'})
                        
                        # Acknowledge wake word
                        responses = [
                            "Yes, Arjun?",
                            "I'm here, Arjun.",
                            "How can I help you, Arjun?",
                            "At your service, Arjun."
                        ]
                        import random
                        self.voice.speak(random.choice(responses), lang='en', async_mode=False)
                        
                        # Now listen for actual command
                        result = self.voice.process_multilingual_command(
                            callback=self.process_command
                        )
                        
                        if result['success']:
                            self.message_queue.put({
                                'type': 'command_complete',
                                'lang': result['user_lang']
                            })
                        
                        self.is_active = False
                        self.message_queue.put({'type': 'status', 'status': 'STANDBY'})
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Listening error: {e}")
                time.sleep(1)
    
    def process_command(self, english_text):
        """Process command and return response"""
        self.message_queue.put({'type': 'status', 'status': 'PROCESSING'})
        
        text = english_text.lower()
        
        # Personalized responses for Arjun
        if any(word in text for word in ['hello', 'hi', 'hey']):
            return f"Hello Arjun! How can I assist you today?"
        
        elif 'time' in text:
            now = datetime.now()
            return f"Arjun, the current time is {now.strftime('%I:%M %p')}"
        
        elif 'date' in text:
            now = datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}, Arjun."
        
        elif 'weather' in text:
            return "Weather service is not configured yet, Arjun. Please add your API key."
        
        elif 'open' in text:
            if 'notepad' in text:
                import subprocess
                subprocess.Popen(['notepad.exe'])
                return "Opening Notepad for you, Arjun."
            elif 'calculator' in text:
                import subprocess
                subprocess.Popen(['calc.exe'])
                return "Opening Calculator, Arjun."
            elif 'browser' in text or 'chrome' in text:
                import subprocess
                subprocess.Popen(['start', 'chrome'], shell=True)
                return "Opening browser, Arjun."
            else:
                return "What would you like me to open, Arjun?"
        
        elif 'joke' in text:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the developer go broke? Because he used up all his cache!",
                "What's a programmer's favorite place? Foo Bar!",
            ]
            import random
            return f"Here's one for you, Arjun: {random.choice(jokes)}"
        
        elif any(word in text for word in ['who are you', 'what are you']):
            return f"I'm JARVIS, your personal AI assistant, Arjun. I can help with tasks, answer questions, and control your system."
        
        elif 'your name' in text or 'my name' in text:
            return f"Your name is Arjun, sir."
        
        elif 'help' in text:
            return "I can help you with time, date, opening applications, telling jokes, and much more. Just speak naturally, Arjun."
        
        elif any(word in text for word in ['thank', 'thanks']):
            return "You're welcome, Arjun! Always happy to help."
        
        elif any(word in text for word in ['bye', 'goodbye', 'exit', 'sleep']):
            return "Goodbye, Arjun. I'll be here when you need me."
        
        else:
            return f"I heard: '{english_text}'. I'm still learning, Arjun. Try asking about time, date, or tell me to open an application."
    
    def process_message_queue(self):
        """Process messages from background thread"""
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                
                if msg['type'] == 'status':
                    self.set_status(msg['status'])
                
                elif msg['type'] == 'greet':
                    self.voice.greet_user(lang='en')
                
                elif msg['type'] == 'command_complete':
                    lang_name = self.voice.get_language_name(msg['lang'])
                    logger.info(f"✅ Command completed in {lang_name}")
        
        except queue.Empty:
            pass
        
        finally:
            self.root.after(100, self.process_message_queue)
    
    def run(self):
        """Start the UI"""
        logger.info("🚀 Starting JARVIS Futuristic UI...")
        logger.info("💡 Say 'Hello JARVIS' to activate!")
        self.root.mainloop()


def main():
    """Launch JARVIS Futuristic UI"""
    try:
        app = JarvisFuturisticUI()
        app.run()
    except KeyboardInterrupt:
        logger.info("\n👋 JARVIS shutting down...")
    except Exception as e:
        logger.error(f"❌ UI Error: {e}")
        raise


if __name__ == "__main__":
    main()
