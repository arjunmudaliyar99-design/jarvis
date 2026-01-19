"""
JARVIS HUD GUI - Iron Man Style Interface
Futuristic circular HUD with voice integration
"""

import customtkinter as ctk
from tkinter import Canvas
import threading
import queue
import math
import time
from datetime import datetime
import subprocess
import logging
from constants import COLORS, FONTS, HUD, PANELS, APPS, ANIMATION
from jarvis_voice import JarvisVoice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")


class JarvisHUD:
    """JARVIS HUD - Iron Man inspired interface"""
    
    def __init__(self):
        # Initialize window
        self.root = ctk.CTk()
        self.root.title("JARVIS HUD")
        
        # Fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(fg_color=COLORS['bg_dark'])
        
        # Bind ESC to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Get screen dimensions
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        # Initialize voice
        self.voice = JarvisVoice()
        
        # State
        self.status = "STANDBY"
        self.rotation = 0
        self.pulse_phase = 0
        self.is_listening = False
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Start continuous listening
        self.listening_thread = threading.Thread(target=self.continuous_listening, daemon=True)
        self.listening_thread.start()
        
        # Start animations
        self.animate()
        self.update_time()
        self.process_messages()
        
        logger.info("✅ JARVIS HUD Initialized")
    
    def setup_ui(self):
        """Create HUD interface"""
        
        # Main canvas for HUD
        self.canvas = Canvas(
            self.root,
            bg=COLORS['bg_dark'],
            highlightthickness=0,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Draw static HUD elements
        self.draw_static_hud()
        
        # Create panels
        self.create_left_panel()
        self.create_right_panel()
        self.create_bottom_panel()
        
        # Create center mic button
        self.create_center_button()
    
    def draw_static_hud(self):
        """Draw static HUD elements"""
        # Corner brackets (sci-fi frame)
        bracket_size = 40
        bracket_offset = 30
        
        # Top-left
        self.canvas.create_line(
            bracket_offset, bracket_offset,
            bracket_offset + bracket_size, bracket_offset,
            fill=COLORS['cyan_accent'], width=2
        )
        self.canvas.create_line(
            bracket_offset, bracket_offset,
            bracket_offset, bracket_offset + bracket_size,
            fill=COLORS['cyan_accent'], width=2
        )
        
        # Top-right
        self.canvas.create_line(
            self.width - bracket_offset, bracket_offset,
            self.width - bracket_offset - bracket_size, bracket_offset,
            fill=COLORS['cyan_accent'], width=2
        )
        self.canvas.create_line(
            self.width - bracket_offset, bracket_offset,
            self.width - bracket_offset, bracket_offset + bracket_size,
            fill=COLORS['cyan_accent'], width=2
        )
        
        # Bottom-left
        self.canvas.create_line(
            bracket_offset, self.height - bracket_offset,
            bracket_offset + bracket_size, self.height - bracket_offset,
            fill=COLORS['cyan_accent'], width=2
        )
        self.canvas.create_line(
            bracket_offset, self.height - bracket_offset,
            bracket_offset, self.height - bracket_offset - bracket_size,
            fill=COLORS['cyan_accent'], width=2
        )
        
        # Bottom-right
        self.canvas.create_line(
            self.width - bracket_offset, self.height - bracket_offset,
            self.width - bracket_offset - bracket_size, self.height - bracket_offset,
            fill=COLORS['cyan_accent'], width=2
        )
        self.canvas.create_line(
            self.width - bracket_offset, self.height - bracket_offset,
            self.width - bracket_offset, self.height - bracket_offset - bracket_size,
            fill=COLORS['cyan_accent'], width=2
        )
        
        # Grid lines (subtle)
        for i in range(4):
            y = (self.height // 4) * (i + 1)
            self.canvas.create_line(
                100, y, self.width - 100, y,
                fill=COLORS['gray_dark'], width=1, dash=(10, 20)
            )
    
    def create_left_panel(self):
        """Create left info panel"""
        panel_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS['bg_panel'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['cyan_accent'],
            width=PANELS['left_width'],
            height=500
        )
        panel_frame.place(x=30, y=100)
        
        # Title
        title = ctk.CTkLabel(
            panel_frame,
            text="SYSTEM STATUS",
            font=('Orbitron', 18, 'bold'),
            text_color=COLORS['cyan_primary']
        )
        title.pack(pady=(20, 10))
        
        # Date and Time
        self.date_label = ctk.CTkLabel(
            panel_frame,
            text="",
            font=('Consolas', 14),
            text_color=COLORS['white']
        )
        self.date_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(
            panel_frame,
            text="",
            font=('Courier New', 24, 'bold'),
            text_color=COLORS['cyan_primary']
        )
        self.time_label.pack(pady=10)
        
        # Separator
        sep = ctk.CTkFrame(panel_frame, height=2, fg_color=COLORS['cyan_accent'])
        sep.pack(fill='x', padx=20, pady=15)
        
        # Status info
        info_frame = ctk.CTkFrame(panel_frame, fg_color='transparent')
        info_frame.pack(fill='x', padx=20)
        
        ctk.CTkLabel(
            info_frame,
            text="USER:",
            font=('Consolas', 12, 'bold'),
            text_color=COLORS['white_dim']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            info_frame,
            text="Arjun",
            font=('Consolas', 14),
            text_color=COLORS['cyan_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="AI STATUS:",
            font=('Consolas', 12, 'bold'),
            text_color=COLORS['white_dim']
        ).pack(anchor='w')
        
        self.ai_status_label = ctk.CTkLabel(
            info_frame,
            text="● ONLINE",
            font=('Consolas', 14),
            text_color=COLORS['success']
        )
        self.ai_status_label.pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="VOICE MODE:",
            font=('Consolas', 12, 'bold'),
            text_color=COLORS['white_dim']
        ).pack(anchor='w')
        
        self.voice_mode_label = ctk.CTkLabel(
            info_frame,
            text="Active Listening",
            font=('Consolas', 14),
            text_color=COLORS['cyan_primary']
        )
        self.voice_mode_label.pack(anchor='w')
    
    def create_right_panel(self):
        """Create right panel with app shortcuts"""
        panel_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS['bg_panel'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['cyan_accent'],
            width=PANELS['right_width'],
            height=600
        )
        panel_frame.place(
            x=self.width - PANELS['right_width'] - 30,
            y=100
        )
        
        # Title
        title = ctk.CTkLabel(
            panel_frame,
            text="QUICK ACCESS",
            font=('Orbitron', 18, 'bold'),
            text_color=COLORS['cyan_primary']
        )
        title.pack(pady=(20, 20))
        
        # App buttons
        for app in APPS:
            btn = ctk.CTkButton(
                panel_frame,
                text=f"{app['icon']}  {app['name']}",
                font=('Consolas', 13),
                fg_color=COLORS['bg_dark'],
                hover_color=COLORS['cyan_accent'],
                border_width=2,
                border_color=COLORS['cyan_accent'],
                height=40,
                command=lambda cmd=app['command']: self.launch_app(cmd)
            )
            btn.pack(pady=5, padx=20, fill='x')
    
    def create_bottom_panel(self):
        """Create bottom status panel"""
        panel_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS['bg_panel'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['cyan_accent'],
            width=600,
            height=80
        )
        panel_frame.place(
            x=self.center_x - 300,
            y=self.height - 120
        )
        
        # Status text
        self.status_label = ctk.CTkLabel(
            panel_frame,
            text="JARVIS • STANDBY MODE",
            font=('Orbitron', 20, 'bold'),
            text_color=COLORS['cyan_primary']
        )
        self.status_label.pack(pady=10)
        
        self.status_detail = ctk.CTkLabel(
            panel_frame,
            text="🎤 हिंदी में बोलें • Just speak ANY command",
            font=('Consolas', 12),
            text_color=COLORS['white_dim']
        )
        self.status_detail.pack()
    
    def create_center_button(self):
        """Create center status indicator (no manual button)"""
        # Create a status label instead of button
        self.center_label = ctk.CTkLabel(
            self.root,
            text="JARVIS",
            font=('Orbitron', 32, 'bold'),
            text_color=COLORS['cyan_primary'],
            fg_color='transparent'
        )
        self.center_label.place(
            x=self.center_x - 80,
            y=self.center_y - 20
        )
    
    def animate(self):
        """Animate HUD elements"""
        # Clear dynamic elements
        self.canvas.delete('dynamic')
        
        # Update rotation
        self.rotation = (self.rotation + ANIMATION['rotation_speed']) % 360
        self.pulse_phase += 0.05
        
        # Pulse effect
        pulse = math.sin(self.pulse_phase) * 0.15 + 0.85
        
        # Draw rotating rings
        self.draw_rotating_rings(pulse)
        
        # Draw connecting lines
        self.draw_radar_lines()
        
        # Draw status dots
        self.draw_status_dots()
        
        # Schedule next frame
        self.root.after(int(1000 / ANIMATION['fps']), self.animate)
    
    def draw_rotating_rings(self, pulse):
        """Draw animated circular rings"""
        rings = [
            (HUD['ring3_radius'], COLORS['cyan_accent'], 2),
            (HUD['ring2_radius'], COLORS['cyan_primary'], 2),
            (HUD['ring1_radius'], COLORS['blue_glow'], 3),
        ]
        
        for radius, color, width in rings:
            # Draw circle
            x1 = self.center_x - radius
            y1 = self.center_y - radius
            x2 = self.center_x + radius
            y2 = self.center_y + radius
            
            # Adjust opacity based on status
            if self.status == "LISTENING":
                width = int(width * pulse * 1.5)
            
            self.canvas.create_oval(
                x1, y1, x2, y2,
                outline=color,
                width=width,
                tags='dynamic'
            )
            
            # Draw arc segments (rotating)
            num_segments = 8
            for i in range(num_segments):
                angle = (self.rotation + i * 45) % 360
                self.canvas.create_arc(
                    x1, y1, x2, y2,
                    start=angle,
                    extent=30,
                    outline=color,
                    width=width,
                    style='arc',
                    tags='dynamic'
                )
    
    def draw_radar_lines(self):
        """Draw radar-style lines from center"""
        num_lines = 12
        for i in range(num_lines):
            angle = math.radians((self.rotation * 2 + i * 30) % 360)
            length = HUD['center_radius'] - 20
            
            x = self.center_x + length * math.cos(angle)
            y = self.center_y + length * math.sin(angle)
            
            self.canvas.create_line(
                self.center_x, self.center_y,
                x, y,
                fill=COLORS['gray_dark'],
                width=1,
                tags='dynamic'
            )
    
    def draw_status_dots(self):
        """Draw status indicator dots"""
        # Draw dots around outer ring
        num_dots = 24
        for i in range(num_dots):
            angle = math.radians((self.rotation + i * 15) % 360)
            radius = HUD['ring3_radius'] + 15
            
            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            
            color = COLORS['cyan_accent'] if i % 3 == 0 else COLORS['gray_dark']
            size = 4 if i % 3 == 0 else 2
            
            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=color,
                outline='',
                tags='dynamic'
            )
    
    def update_time(self):
        """Update time display"""
        now = datetime.now()
        self.date_label.configure(text=now.strftime("%A, %B %d, %Y"))
        self.time_label.configure(text=now.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def set_status(self, status, detail=""):
        """Update status display"""
        self.status = status
        
        status_colors = {
            "STANDBY": COLORS['cyan_primary'],
            "LISTENING": COLORS['listening'],
            "PROCESSING": COLORS['processing'],
            "SPEAKING": COLORS['speaking']
        }
        
        status_texts = {
            "STANDBY": "JARVIS • STANDBY MODE",
            "LISTENING": "JARVIS • LISTENING",
            "PROCESSING": "JARVIS • PROCESSING",
            "SPEAKING": "JARVIS • SPEAKING"
        }
        
        self.status_label.configure(
            text=status_texts.get(status, status),
            text_color=status_colors.get(status, COLORS['cyan_primary'])
        )
        
        if detail:
            self.status_detail.configure(text=detail)
    
    # Removed manual activation - fully automatic mode only
    
    def launch_app(self, command):
        """Launch application"""
        try:
            subprocess.Popen(command, shell=True)
            logger.info(f"Launched: {command}")
        except Exception as e:
            logger.error(f"Failed to launch: {e}")
    
    def continuous_listening(self):
        """Background thread for continuous voice listening - NO WAKE WORD REQUIRED"""
        logger.info("🎤 ===== CONTINUOUS LISTENING THREAD STARTED =====")
        logger.info("⚡ WAKE WORD REMOVED - JARVIS responds to ANY speech input!")
        
        # Greet user
        time.sleep(1)
        logger.info("🎉 Greeting user in Hindi...")
        self.voice.greet_user(lang='hi')  # Hindi greeting
        
        cycle_count = 0
        exit_requested = False
        
        while not exit_requested:
            try:
                cycle_count += 1
                
                # ===== WAKE WORD LOGIC REMOVED =====
                # Now listens for ANY speech input directly
                if not self.is_listening:
                    logger.info(f"\n🔄 Listening cycle #{cycle_count}")
                    logger.info("👂 Listening for ANY speech... (Just speak your command)")
                    
                    self.is_listening = True
                    self.message_queue.put({'type': 'status', 'status': 'LISTENING'})
                    
                    # Listen directly for command (NO wake word check)
                    logger.info("🎯 Waiting for your voice input...")
                    result = self.voice.process_multilingual_command(
                        callback=self.process_command
                    )
                    
                    if result['success']:
                        logger.info("✅ ===== COMMAND COMPLETED SUCCESSFULLY =====\n")
                        
                        # Check if exit was requested
                        if result.get('exit_requested'):
                            logger.info("👋 Exit command detected - shutting down...")
                            exit_requested = True
                            break
                    else:
                        logger.warning("⚠️ No speech detected or processing failed\n")
                    
                    self.is_listening = False
                    self.message_queue.put({'type': 'status', 'status': 'STANDBY'})
                
                # Small sleep to prevent CPU overload
                time.sleep(0.05)
                
            except Exception as e:
                logger.error(f"❌ Listening thread error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                self.is_listening = False
                time.sleep(1)
        
        logger.info("🛑 Continuous listening stopped")
    
    def process_command(self, english_text):
        """Process voice command with clear intent detection and task execution"""
        logger.info(f"\n🎯 ===== PROCESSING COMMAND =====")
        logger.info(f"📝 Recognized: '{english_text}'")
        
        self.message_queue.put({'type': 'status', 'status': 'PROCESSING'})
        
        text = english_text.lower().strip()
        response = None
        intent = "unknown"
        exit_flag = False
        
        # Intent: Greeting
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            intent = "greeting"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Greet user")
            response = f"Hello Arjun! How can I assist you?"
        
        # Intent: Time Query
        elif 'time' in text:
            intent = "time_query"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Get current time")
            now = datetime.now()
            response = f"The current time is {now.strftime('%I:%M %p')}, Arjun."
        
        # Intent: Date Query
        elif 'date' in text or 'today' in text:
            intent = "date_query"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Get current date")
            now = datetime.now()
            response = f"Today is {now.strftime('%A, %B %d, %Y')}, Arjun."
        
        # Intent: Open Application
        elif 'open' in text:
            intent = "open_app"
            logger.info(f"🧠 Detected Intent: {intent}")
            opened = False
            
            # Try to match app name (case-insensitive, flexible matching)
            for app in APPS:
                app_name_lower = app['name'].lower()
                # Check if app name in command OR common aliases
                if app_name_lower in text:
                    logger.info(f"⚙️ Executing task: Open {app['name']}")
                    logger.info(f"🚀 Launching: {app['command']}")
                    self.launch_app(app['command'])
                    response = f"Opening {app['name']} for you, Arjun."
                    opened = True
                    break
            
            # Check for common aliases if not found
            if not opened:
                # Browser aliases
                if any(word in text for word in ['chrome', 'browser', 'google chrome', 'edge', 'firefox']):
                    logger.info(f"⚙️ Executing task: Open Browser (Chrome)")
                    logger.info(f"🚀 Launching: start chrome")
                    self.launch_app('start chrome')
                    response = "Opening Chrome browser for you, Arjun."
                    opened = True
                # WhatsApp
                elif 'whatsapp' in text:
                    logger.info(f"⚙️ Executing task: Open WhatsApp")
                    logger.info(f"🚀 Launching: WhatsApp")
                    self.launch_app('start https://web.whatsapp.com')
                    response = "Opening WhatsApp for you, Arjun."
                    opened = True
                # VS Code
                elif any(word in text for word in ['code', 'vs code', 'visual studio code']):
                    logger.info(f"⚙️ Executing task: Open VS Code")
                    logger.info(f"🚀 Launching: code")
                    self.launch_app('code')
                    response = "Opening VS Code for you, Arjun."
                    opened = True
                    
            if not opened:
                response = "What would you like me to open, Arjun?"
        
        # Intent: Search
        elif 'search' in text or ('google' in text and 'open' not in text):
            intent = "search"
            query = text.replace('search', '').replace('google', '').replace('for', '').replace('on', '').strip()
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Search for '{query}'")
            if query:
                # Execute search
                import webbrowser
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                logger.info(f"🌐 Opening URL: {search_url}")
                webbrowser.open(search_url)
                response = f"Searching for {query}, Arjun."
            else:
                response = "What would you like me to search for, Arjun?"
        
        # Intent: Exit/Stop/Quit
        elif any(word in text for word in ['exit', 'stop', 'quit', 'close jarvis', 'shutdown', 'goodbye']):
            intent = "exit"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Exit JARVIS")
            response = "Goodbye, Arjun! Have a great day!"
            exit_flag = True
        
        # Intent: Joke
        elif 'joke' in text:
            intent = "joke"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Tell a joke")
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What do you call a programmer from Finland? Nerdic!",
                "Why did the programmer quit? He didn't get arrays!",
            ]
            import random
            response = random.choice(jokes)
        
        # Intent: Identity
        elif 'who are you' in text or 'what are you' in text:
            intent = "identity"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Introduce self")
            response = "I'm JARVIS, your AI voice assistant, Arjun. I'm here to help with tasks, answer questions, and make your life easier."
        
        # Intent: Thank you
        elif any(word in text for word in ['thank', 'thanks']):
            intent = "gratitude"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚙️ Executing task: Acknowledge thanks")
            response = "You're welcome, Arjun! Happy to help!"
        
        # Unknown intent - helpful fallback (CRITICAL: Always respond)
        else:
            intent = "unknown"
            logger.info(f"🧠 Detected Intent: {intent}")
            logger.info(f"⚠️ No matching task found for: '{english_text}'")
            response = f"I heard you say '{english_text}', but I don't know how to do that yet, Arjun. I can help with time, date, opening apps, searching, and more."
        
        logger.info(f"💬 Response: '{response}'")
        logger.info(f"===== COMMAND PROCESSING COMPLETE =====\n")
        
        # Store exit flag in result for continuous_listening to check
        if exit_flag:
            return {'response': response, 'exit_requested': True}
        
        return response
    
    def process_messages(self):
        """Process message queue"""
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                
                if msg['type'] == 'status':
                    self.set_status(msg['status'])
        except:
            pass
        
        self.root.after(100, self.process_messages)
    
    def run(self):
        """Start the HUD"""
        logger.info("🚀 JARVIS HUD Starting...")
        self.root.mainloop()


def main():
    """Launch JARVIS HUD"""
    hud = JarvisHUD()
    hud.run()


if __name__ == "__main__":
    main()
