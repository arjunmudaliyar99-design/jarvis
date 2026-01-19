"""
JARVIS Advanced GUI - Modern HUD with Animations and Chat Interface
Futuristic Iron Man-style interface with real-time visualization
"""
import customtkinter as ctk
from tkinter import Canvas
import math
import threading
import queue
import logging
from datetime import datetime
from typing import List, Dict
from config import GUI_CONFIG, USER_NAME

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JarvisAdvancedGUI:
    """Modern JARVIS GUI with animations and chat interface"""
    
    def __init__(self, voice_system, brain, task_executor, memory):
        """
        Initialize advanced GUI
        
        Args:
            voice_system: JarvisVoiceSystem instance
            brain: JarvisBrain instance
            task_executor: JarvisTasks instance
            memory: ConversationMemory instance
        """
        self.voice = voice_system
        self.brain = brain
        self.tasks = task_executor
        self.memory = memory
        
        # GUI state
        self.status = "STANDBY"  # STANDBY, LISTENING, THINKING, SPEAKING
        self.is_running = True
        self.message_queue = queue.Queue()
        
        # Animation state
        self.rotation = 0
        self.pulse_phase = 0
        self.waveform_data = [0] * GUI_CONFIG['waveform_bars']
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(f"JARVIS - AI Assistant for {USER_NAME}")
        self.root.geometry("1400x900")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Center window
        x = (screen_width - 1400) // 2
        y = (screen_height - 900) // 2
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Setup UI
        self.setup_ui()
        
        # Start systems
        self.start_listening_thread()
        self.start_animations()
        
        logger.info("✅ Advanced GUI initialized")
    
    def setup_ui(self):
        """Create GUI components"""
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color=GUI_CONFIG['bg_color'])
        main_frame.pack(fill='both', expand=True)
        
        # Left panel - Visualizer
        left_panel = ctk.CTkFrame(
            main_frame,
            width=500,
            fg_color=GUI_CONFIG['bg_color'],
            corner_radius=0
        )
        left_panel.pack(side='left', fill='both', expand=False)
        left_panel.pack_propagate(False)
        
        # Create visualizer canvas
        self.create_visualizer(left_panel)
        
        # Right panel - Chat interface
        right_panel = ctk.CTkFrame(
            main_frame,
            fg_color='#151a21',
            corner_radius=15
        )
        right_panel.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.create_chat_interface(right_panel)
    
    def create_visualizer(self, parent):
        """Create animated visualizer"""
        # Canvas for animations
        self.canvas = Canvas(
            parent,
            bg=GUI_CONFIG['bg_color'],
            highlightthickness=0,
            width=500,
            height=900
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Center coordinates
        self.center_x = 250
        self.center_y = 400
        
        # Status display
        status_frame = ctk.CTkFrame(parent, fg_color='transparent')
        status_frame.place(x=50, y=50)
        
        ctk.CTkLabel(
            status_frame,
            text="JARVIS",
            font=('Orbitron', 32, 'bold'),
            text_color=GUI_CONFIG['primary_color']
        ).pack()
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="● STANDBY",
            font=('Consolas', 16),
            text_color=GUI_CONFIG['primary_color']
        )
        self.status_label.pack(pady=10)
        
        # User info
        info_frame = ctk.CTkFrame(parent, fg_color='transparent')
        info_frame.place(x=50, y=750)
        
        ctk.CTkLabel(
            info_frame,
            text=f"USER: {USER_NAME}",
            font=('Consolas', 12),
            text_color='#b0bec5'
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            info_frame,
            text=f"SESSION: {datetime.now().strftime('%I:%M %p')}",
            font=('Consolas', 12),
            text_color='#b0bec5'
        ).pack(anchor='w')
    
    def create_chat_interface(self, parent):
        """Create chat interface with Continue button"""
        # Header
        header = ctk.CTkFrame(parent, fg_color='#1e2830', height=60, corner_radius=10)
        header.pack(fill='x', padx=10, pady=10)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="💬 Conversation",
            font=('Orbitron', 20, 'bold'),
            text_color=GUI_CONFIG['primary_color']
        ).pack(side='left', padx=20)
        
        # Continue Explanation Button (initially hidden)
        self.continue_btn = ctk.CTkButton(
            header,
            text="Continue Explanation ▶",
            font=('Consolas', 14, 'bold'),
            fg_color='#ff6b00',
            hover_color='#ff8533',
            width=200,
            height=40,
            corner_radius=20,
            command=self.on_continue_explanation
        )
        # Don't pack yet - will show when needed
        self.continue_btn_visible = False
        self.explanation_paused = False
        self.pending_explanation = None
        
        # Chat display
        chat_frame = ctk.CTkFrame(parent, fg_color='#0b0f14', corner_radius=10)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=('Consolas', 12),
            fg_color='#0b0f14',
            text_color='#ffffff',
            wrap='word',
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Control buttons frame
        controls_frame = ctk.CTkFrame(parent, fg_color='transparent', height=50)
        controls_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Status info
        self.info_label = ctk.CTkLabel(
            controls_frame,
            text="🎤 Voice-activated - Just speak naturally",
            font=('Consolas', 11),
            text_color='#b0bec5'
        )
        self.info_label.pack(side='left', padx=10)
        
        # Initial messages
        self.add_chat_message("JARVIS", "Hello! I'm online and ready to assist you.", "assistant")
        self.add_chat_message("SYSTEM", "Speak naturally - I'm always listening.", "system")
    
    def show_continue_button(self):
        """Show Continue Explanation button"""
        if not self.continue_btn_visible:
            self.continue_btn.pack(side='right', padx=20)
            self.continue_btn_visible = True
            logger.info("✅ Continue button shown")
    
    def hide_continue_button(self):
        """Hide Continue Explanation button"""
        if self.continue_btn_visible:
            self.continue_btn.pack_forget()
            self.continue_btn_visible = False
            logger.info("✅ Continue button hidden")
    
    def on_continue_explanation(self):
        """Handle Continue Explanation button click"""
        logger.info("🔄 User clicked Continue Explanation")
        
        if self.pending_explanation:
            # Resume the paused explanation
            self.explanation_paused = False
            self.hide_continue_button()
            
            # Display the continuation
            self.add_chat_message("JARVIS", self.pending_explanation, "assistant")
            
            # Speak it
            self.set_status("SPEAKING")
            self.voice.speak(self.pending_explanation)
            self.set_status("STANDBY")
            
            self.pending_explanation = None
        else:
            logger.warning("⚠️ No pending explanation to continue")
    
    def draw_animations(self):
        """Draw animated visualizer"""
        self.canvas.delete('animated')
        
        # Calculate pulse
        pulse = 0.7 + 0.3 * math.sin(self.pulse_phase)
        
        # Draw rotating rings
        self.draw_rotating_rings(pulse)
        
        # Draw waveform
        if self.status == "LISTENING":
            self.draw_waveform()
        
        # Draw center core
        self.draw_center_core(pulse)
        
        # Update rotation
        self.rotation = (self.rotation + 1) % 360
        self.pulse_phase += 0.05
        
        # Schedule next frame
        self.root.after(16, self.draw_animations)  # ~60 FPS
    
    def draw_rotating_rings(self, pulse):
        """Draw animated rotating rings"""
        rings = [
            (120, GUI_CONFIG['primary_color'], 2),
            (150, GUI_CONFIG['secondary_color'], 2),
            (180, GUI_CONFIG['primary_color'], 1),
        ]
        
        for radius, color, width in rings:
            # Full circle
            x1 = self.center_x - radius
            y1 = self.center_y - radius
            x2 = self.center_x + radius
            y2 = self.center_y + radius
            
            opacity_color = self._adjust_color_opacity(color, pulse * 0.5)
            
            self.canvas.create_oval(
                x1, y1, x2, y2,
                outline=opacity_color,
                width=width,
                tags='animated'
            )
            
            # Rotating arcs
            for i in range(6):
                angle = (self.rotation + i * 60) % 360
                self.canvas.create_arc(
                    x1, y1, x2, y2,
                    start=angle,
                    extent=30,
                    outline=color,
                    width=width + 1,
                    style='arc',
                    tags='animated'
                )
    
    def draw_center_core(self, pulse):
        """Draw pulsing center core"""
        base_radius = 40
        radius = base_radius + (10 * pulse if self.status == "THINKING" else 5 * pulse)
        
        # Status colors
        status_colors = {
            'STANDBY': GUI_CONFIG['primary_color'],
            'LISTENING': '#00ff00',
            'THINKING': '#ffaa00',
            'SPEAKING': '#00aaff'
        }
        
        color = status_colors.get(self.status, GUI_CONFIG['primary_color'])
        
        # Outer glow
        for i in range(3):
            glow_radius = radius + (i * 10)
            opacity = (3 - i) * 0.15 * pulse
            glow_color = self._adjust_color_opacity(color, opacity)
            
            self.canvas.create_oval(
                self.center_x - glow_radius,
                self.center_y - glow_radius,
                self.center_x + glow_radius,
                self.center_y + glow_radius,
                outline=glow_color,
                width=2,
                tags='animated'
            )
        
        # Core circle
        self.canvas.create_oval(
            self.center_x - radius,
            self.center_y - radius,
            self.center_x + radius,
            self.center_y + radius,
            fill=color,
            outline=color,
            width=2,
            tags='animated'
        )
    
    def draw_waveform(self):
        """Draw audio waveform visualization"""
        import random
        
        # Simulate audio levels (in real app, get from mic)
        self.waveform_data = [random.uniform(0.3, 1.0) for _ in range(GUI_CONFIG['waveform_bars'])]
        
        bar_width = 6
        spacing = 8
        total_width = GUI_CONFIG['waveform_bars'] * spacing
        start_x = self.center_x - (total_width // 2)
        base_y = self.center_y + 250
        
        for i, level in enumerate(self.waveform_data):
            x = start_x + (i * spacing)
            height = level * 80
            
            self.canvas.create_rectangle(
                x, base_y - height,
                x + bar_width, base_y,
                fill=GUI_CONFIG['primary_color'],
                outline='',
                tags='animated'
            )
    
    def _adjust_color_opacity(self, color: str, opacity: float) -> str:
        """Adjust color opacity (simplified)"""
        # For demo - returns same color
        return color
    
    def set_status(self, status: str):
        """Update system status"""
        self.status = status
        
        status_text = f"● {status}"
        self.status_label.configure(text=status_text)
        
        logger.info(f"📊 Status: {status}")
    
    def add_chat_message(self, sender: str, message: str, msg_type: str = "user", check_length: bool = True):
        """
        Add message to chat display with automatic splitting for long explanations
        
        Args:
            sender: Message sender name
            message: Message text
            msg_type: 'user', 'assistant', or 'system'
            check_length: Whether to check for long explanations
        """
        # Check if message is a long explanation (> 300 words or > 3 paragraphs)
        if check_length and msg_type == 'assistant' and sender == "JARVIS":
            word_count = len(message.split())
            paragraph_count = message.count('\n\n') + 1
            
            # Long explanation detected
            if word_count > 300 or paragraph_count > 3:
                logger.info(f"📚 Long explanation detected ({word_count} words, {paragraph_count} paragraphs)")
                
                # Split into first part and continuation
                # Find a good break point (after ~200 words or 2 paragraphs)
                paragraphs = message.split('\n\n')
                
                if len(paragraphs) > 2:
                    # Split after 2 paragraphs
                    first_part = '\n\n'.join(paragraphs[:2])
                    continuation = '\n\n'.join(paragraphs[2:])
                else:
                    # Split at word boundary
                    words = message.split()
                    split_point = min(200, len(words) // 2)
                    first_part = ' '.join(words[:split_point])
                    continuation = ' '.join(words[split_point:])
                
                # Display first part
                self._add_message_to_chat(sender, first_part, msg_type)
                
                # Store continuation and show button
                self.pending_explanation = continuation
                self.explanation_paused = True
                self.show_continue_button()
                
                return
        
        # Normal message - add directly
        self._add_message_to_chat(sender, message, msg_type)
    
    def _add_message_to_chat(self, sender: str, message: str, msg_type: str):
        """Internal method to add message to chat without length check"""
        self.chat_display.configure(state='normal')
        
        timestamp = datetime.now().strftime('%H:%M')
        
        # Color based on type
        colors = {
            'user': '#00e5ff',
            'assistant': '#00ff88',
            'system': '#ffaa00'
        }
        color = colors.get(msg_type, '#ffffff')
        
        # Format message
        formatted = f"\n[{timestamp}] {sender}:\n{message}\n"
        
        self.chat_display.insert('end', formatted)
        self.chat_display.see('end')
        self.chat_display.configure(state='disabled')
    
    def start_listening_thread(self):
        """Start continuous listening in background"""
        def listening_loop():
            logger.info("🎤 Continuous listening started")
            
            while self.is_running:
                try:
                    # Set listening status
                    self.set_status("LISTENING")
                    
                    # Listen for speech
                    text, lang = self.voice.listen(timeout=10)
                    
                    if text:
                        # Log recognized text
                        logger.info(f"\n{'='*50}")
                        logger.info(f"✅ RECOGNIZED TEXT: '{text}'")
                        logger.info(f"🌐 DETECTED LANGUAGE: {lang}")
                        logger.info(f"{'='*50}")
                        
                        # Add to chat (ALWAYS in English)
                        self.add_chat_message(USER_NAME, text, "user")
                        
                        # Process with brain
                        self.set_status("THINKING")
                        logger.info("🧠 Sending to Brain for processing...")
                        result = self.brain.process_input(text, lang)
                        
                        logger.info(f"🎯 DETECTED INTENT: {result['intent']}")
                        logger.info(f"⚙️ ACTION: {result['action']}")
                        
                        # Execute task if action detected
                        if result['action']:
                            logger.info(f"🚀 EXECUTING TASK: {result['action']}")
                            task_response = self.tasks.execute_task(result)
                            if task_response:
                                result['response'] = task_response
                            logger.info(f"✅ TASK COMPLETED: {task_response}")
                        
                        # English response for chat display
                        english_response = result['response']
                        
                        # Add English response to chat (handles splitting automatically)
                        self.add_chat_message("JARVIS", english_response, "assistant")
                        
                        # Only speak if not paused for continuation
                        if not self.explanation_paused:
                            # Translate for speech (if output language is not English)
                            if self.voice.output_language != 'en':
                                speech_response = self.voice.translate_text(
                                    english_response,
                                    self.voice.output_language
                                )
                            else:
                                speech_response = english_response
                            
                            # Speak translated response
                            self.set_status("SPEAKING")
                            logger.info(f"🔊 SPEAKING: '{speech_response}'")
                            self.voice.speak(speech_response)
                        else:
                            # If explanation is paused, only speak the first part
                            # Calculate first part (up to where we split)
                            word_count = len(english_response.split())
                            paragraphs = english_response.split('\n\n')
                            
                            if len(paragraphs) > 2:
                                first_part = '\n\n'.join(paragraphs[:2])
                            else:
                                words = english_response.split()
                                split_point = min(200, len(words) // 2)
                                first_part = ' '.join(words[:split_point])
                            
                            # Translate and speak first part only
                            if self.voice.output_language != 'en':
                                speech_first_part = self.voice.translate_text(
                                    first_part,
                                    self.voice.output_language
                                )
                            else:
                                speech_first_part = first_part
                            
                            self.set_status("SPEAKING")
                            logger.info(f"🔊 SPEAKING FIRST PART: '{speech_first_part[:100]}...'")
                            self.voice.speak(speech_first_part)
                            logger.info("⏸️ Explanation paused - waiting for Continue button")
                        
                        # Check for exit
                        if result.get('action') == 'exit':
                            self.is_running = False
                            break
                    
                    # Return to standby
                    self.set_status("STANDBY")
                    
                except Exception as e:
                    logger.error(f"❌ Listening error: {e}")
                    import traceback
                    traceback.print_exc()
        
        thread = threading.Thread(target=listening_loop, daemon=True)
        thread.start()
    
    def start_animations(self):
        """Start animation loop"""
        self.root.after(100, self.draw_animations)
    
    def run(self):
        """Start GUI main loop"""
        logger.info("🚀 JARVIS GUI Starting...")
        self.root.mainloop()
