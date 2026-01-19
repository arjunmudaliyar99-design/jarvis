"""
JARVIS GUI - Modern Voice Assistant Interface
Built with CustomTkinter for a sleek, dark-themed experience
"""

import customtkinter as ctk
from tkinter import scrolledtext
import threading
import queue
from datetime import datetime
from jarvis_voice import JarvisVoice
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JarvisGUI:
    """Modern GUI for JARVIS Voice Assistant"""
    
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("JARVIS - Voice Assistant")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Initialize voice module
        self.voice = JarvisVoice()
        
        # State variables
        self.is_listening = False
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Start message processor
        self.root.after(100, self.process_message_queue)
        
        logger.info("✅ JARVIS GUI Initialized")
    
    def setup_ui(self):
        """Create and arrange all UI elements"""
        
        # ==================== Header ====================
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 JARVIS",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#3b82f6"
        )
        title_label.pack(side="left")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="● Idle",
            font=ctk.CTkFont(size=16),
            text_color="#6b7280"
        )
        self.status_label.pack(side="right")
        
        # ==================== Main Content ====================
        content_frame = ctk.CTkFrame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Display Area Label
        display_label = ctk.CTkLabel(
            content_frame,
            text="Conversation",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        display_label.pack(fill="x", padx=15, pady=(15, 5))
        
        # Text Display (Conversation Log)
        self.text_display = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(size=13),
            wrap="word",
            activate_scrollbars=True,
            fg_color="#1e293b",
            border_width=2,
            border_color="#334155"
        )
        self.text_display.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Add welcome message
        self.add_message("JARVIS", "Hello! I'm JARVIS, your multilingual voice assistant. Click the microphone to speak in any language.", "#3b82f6")
        
        # ==================== Control Panel ====================
        control_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        control_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Microphone Button
        self.mic_button = ctk.CTkButton(
            control_frame,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        self.mic_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Clear Button
        clear_button = ctk.CTkButton(
            control_frame,
            text="🗑️ Clear",
            command=self.clear_display,
            font=ctk.CTkFont(size=14),
            height=50,
            width=100,
            corner_radius=10,
            fg_color="#64748b",
            hover_color="#475569"
        )
        clear_button.pack(side="left", padx=5)
        
        # Language Info
        self.lang_label = ctk.CTkLabel(
            control_frame,
            text="🌍 Multi-lang",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lang_label.pack(side="right", padx=(5, 0))
    
    def set_status(self, status, color):
        """Update status indicator"""
        status_colors = {
            "idle": "#6b7280",
            "listening": "#22c55e",
            "processing": "#f59e0b",
            "speaking": "#3b82f6",
            "error": "#ef4444"
        }
        
        self.status_label.configure(
            text=f"● {status.title()}",
            text_color=status_colors.get(status.lower(), "#6b7280")
        )
        self.root.update()
    
    def add_message(self, sender, message, color="#e5e7eb"):
        """Add a message to the conversation display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Enable editing temporarily
        self.text_display.configure(state="normal")
        
        # Add timestamp and sender
        self.text_display.insert("end", f"[{timestamp}] ", "timestamp")
        self.text_display.insert("end", f"{sender}: ", ("sender", sender.lower()))
        self.text_display.insert("end", f"{message}\n\n", "message")
        
        # Configure tags for styling (without font parameter)
        self.text_display.tag_config("timestamp", foreground="#64748b")
        self.text_display.tag_config("sender", foreground=color)
        self.text_display.tag_config("message", foreground="#e5e7eb")
        self.text_display.tag_config("you", foreground="#22c55e")
        self.text_display.tag_config("jarvis", foreground="#3b82f6")
        
        # Auto-scroll to bottom
        self.text_display.see("end")
        
        # Disable editing
        self.text_display.configure(state="disabled")
    
    def clear_display(self):
        """Clear the conversation display"""
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.configure(state="disabled")
        self.add_message("JARVIS", "Conversation cleared. Ready to assist!", "#3b82f6")
    
    def toggle_listening(self):
        """Toggle voice listening on/off"""
        if not self.is_listening:
            self.start_listening()
        else:
            # Currently listening is blocking, so this won't be called until done
            pass
    
    def start_listening(self):
        """Start voice recognition in a separate thread"""
        self.is_listening = True
        self.mic_button.configure(
            text="🎤 Listening...",
            state="disabled",
            fg_color="#ef4444"
        )
        self.set_status("listening", "#22c55e")
        
        # Run voice recognition in separate thread to avoid GUI freeze
        thread = threading.Thread(target=self.voice_recognition_thread, daemon=True)
        thread.start()
    
    def voice_recognition_thread(self):
        """Background thread for voice recognition"""
        try:
            # Process voice command with callback
            result = self.voice.process_multilingual_command(
                callback=self.process_command
            )
            
            if result['success']:
                # Queue messages for display
                self.message_queue.put({
                    'type': 'user',
                    'text': result['user_text'],
                    'lang': self.voice.get_language_name(result['user_lang'])
                })
                self.message_queue.put({
                    'type': 'jarvis',
                    'text': result['response_user_lang']
                })
                self.message_queue.put({'type': 'status', 'status': 'idle'})
            else:
                self.message_queue.put({
                    'type': 'error',
                    'text': 'Sorry, I could not hear you clearly. Please try again.'
                })
                self.message_queue.put({'type': 'status', 'status': 'idle'})
                
        except Exception as e:
            logger.error(f"❌ Voice recognition thread error: {e}")
            self.message_queue.put({
                'type': 'error',
                'text': f'An error occurred: {str(e)}'
            })
            self.message_queue.put({'type': 'status', 'status': 'idle'})
        
        finally:
            self.message_queue.put({'type': 'enable_button'})
    
    def process_command(self, english_text):
        """
        Process the English command and return a response
        This is where you integrate your AI logic
        
        Args:
            english_text: User command in English
            
        Returns:
            str: Response in English
        """
        # Update status to processing
        self.message_queue.put({'type': 'status', 'status': 'processing'})
        
        # Convert to lowercase for easier matching
        text = english_text.lower()
        
        # ==================== Command Processing ====================
        
        # Greeting
        if any(word in text for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! How can I assist you today?"
        
        # Time/Date
        elif 'time' in text:
            from datetime import datetime
            now = datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}"
        
        elif 'date' in text:
            from datetime import datetime
            now = datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}"
        
        # Weather
        elif 'weather' in text:
            return "I can check the weather for you, but I need the weather API to be configured. Please provide your OpenWeatherMap API key in the .env file."
        
        # System commands
        elif any(word in text for word in ['open', 'launch', 'start']):
            if 'notepad' in text:
                return "Opening Notepad for you."
            elif 'calculator' in text:
                return "Opening Calculator for you."
            elif 'browser' in text or 'chrome' in text:
                return "Opening your web browser."
            else:
                return "I can help you open applications. Just tell me which one!"
        
        # Jokes
        elif 'joke' in text:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the developer go broke? Because he used up all his cache!",
                "What do you call a programmer from Finland? Nerdic!",
            ]
            import random
            return random.choice(jokes)
        
        # About JARVIS
        elif any(word in text for word in ['who are you', 'what are you', 'your name']):
            return "I'm JARVIS, your multilingual voice assistant. I can understand and speak multiple languages, help with tasks, and control your computer."
        
        # Help
        elif 'help' in text:
            return "I can help you with: telling time and date, opening applications, telling jokes, answering questions, and much more. Just speak naturally!"
        
        # Thank you
        elif any(word in text for word in ['thank', 'thanks']):
            return "You're welcome! Happy to help!"
        
        # Goodbye
        elif any(word in text for word in ['bye', 'goodbye', 'see you', 'exit']):
            return "Goodbye! Have a great day!"
        
        # Default response
        else:
            return f"I heard you say: '{english_text}'. I'm still learning, so I don't have a specific response for that yet. Try asking about the time, date, or tell me to open an application!"
    
    def process_message_queue(self):
        """Process messages from background thread"""
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                
                if msg['type'] == 'user':
                    self.add_message("You", msg['text'], "#22c55e")
                    self.lang_label.configure(text=f"🌍 {msg['lang']}")
                    
                elif msg['type'] == 'jarvis':
                    self.add_message("JARVIS", msg['text'], "#3b82f6")
                    
                elif msg['type'] == 'error':
                    self.add_message("System", msg['text'], "#ef4444")
                    
                elif msg['type'] == 'status':
                    self.set_status(msg['status'], "#6b7280")
                    
                elif msg['type'] == 'enable_button':
                    self.is_listening = False
                    self.mic_button.configure(
                        text="🎤 Start Listening",
                        state="normal",
                        fg_color="#3b82f6"
                    )
        
        except queue.Empty:
            pass
        
        finally:
            # Check queue again after 100ms
            self.root.after(100, self.process_message_queue)
    
    def run(self):
        """Start the GUI main loop"""
        logger.info("🚀 Starting JARVIS GUI...")
        self.root.mainloop()


# Standalone launcher
def main():
    """Launch JARVIS GUI"""
    try:
        app = JarvisGUI()
        app.run()
    except KeyboardInterrupt:
        logger.info("\n👋 JARVIS GUI closed by user")
    except Exception as e:
        logger.error(f"❌ GUI Error: {e}")
        raise


if __name__ == "__main__":
    main()
