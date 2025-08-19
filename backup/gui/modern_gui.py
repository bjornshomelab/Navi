"""
JARVIS GUI - Modern AI Assistant Interface
Inspirerat av Discord, VS Code, ChatGPT och andra moderna AI-gränssnitt
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import requests
import json
import uuid
from datetime import datetime
import queue
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import pyaudio

from .modern_theme import ModernTheme, ModernComponents, ICONS

class ModernAudioVisualizer:
    """Sleek audio visualizer with modern styling"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.is_recording = False
        self.audio_data = np.zeros(64)  # Fewer bars for cleaner look
        self.use_mock_data = False
        
        # Audio settings
        self.chunk = 1024
        self.sample_rate = 44100
        self.channels = 1
        
        # Create modern bar chart style visualizer
        self.setup_visualizer()
        
        # Try to initialize audio
        self.setup_audio()
        
    def setup_visualizer(self):
        """Setup modern bar-style audio visualizer"""
        plt.style.use('dark_background')
        
        self.fig, self.ax = plt.subplots(figsize=(5, 1.5))
        self.fig.patch.set_facecolor(ModernTheme.COLORS['bg_card'])
        self.ax.set_facecolor(ModernTheme.COLORS['bg_card'])
        
        # Remove axes for clean look
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        # Create bar chart
        self.bars = self.ax.bar(range(len(self.audio_data)), self.audio_data, 
                               color=ModernTheme.COLORS['accent_primary'], 
                               width=0.8, alpha=0.8)
        
        self.ax.set_ylim(0, 1)
        self.ax.set_xlim(-0.5, len(self.audio_data) - 0.5)
        
        # Create canvas with modern styling
        self.canvas = FigureCanvasTkAgg(self.fig, self.parent_frame)
        self.canvas.get_tk_widget().configure(
            bg=ModernTheme.COLORS['bg_card'],
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)
        
        # Start animation
        self.animation = FuncAnimation(self.fig, self.update_plot, interval=50, blit=False)
        
    def setup_audio(self):
        """Initialize audio capture"""
        try:
            self.p = pyaudio.PyAudio()
            self.audio_stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=None
            )
            print("🎤 Audio visualizer initialized successfully")
        except Exception as e:
            print(f"⚠️ Audio initialization failed: {e}")
            self.use_mock_data = True
            self.p = None
            self.audio_stream = None
    
    def start_recording(self):
        """Start audio visualization"""
        self.is_recording = True
        print("🎵 Audio visualization started")
    
    def stop_recording(self):
        """Stop audio visualization"""
        self.is_recording = False
        # Reset to zero
        self.audio_data = np.zeros(len(self.audio_data))
        print("🔇 Audio visualization stopped")
    
    def cleanup(self):
        """Clean up audio resources"""
        if hasattr(self, 'animation'):
            self.animation.event_source.stop()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.p:
            self.p.terminate()
    
    def update_plot(self, frame):
        """Update the bar chart visualization"""
        if self.is_recording:
            try:
                if self.use_mock_data:
                    # Generate smooth mock audio bars
                    import random
                    for i in range(len(self.audio_data)):
                        # Create wave-like pattern
                        base_height = 0.3 * (1 + np.sin(frame * 0.1 + i * 0.3))
                        noise = random.uniform(-0.1, 0.1)
                        self.audio_data[i] = max(0, min(1, base_height + noise))
                elif self.audio_stream:
                    try:
                        data = self.audio_stream.read(self.chunk, exception_on_overflow=False)
                        audio_array = np.frombuffer(data, dtype=np.float32)
                        # Convert to frequency bins
                        fft = np.abs(np.fft.fft(audio_array))
                        # Take only the frequencies we want to display
                        step = len(fft) // len(self.audio_data)
                        self.audio_data = fft[::step][:len(self.audio_data)]
                        # Normalize
                        if np.max(self.audio_data) > 0:
                            self.audio_data = self.audio_data / np.max(self.audio_data)
                    except Exception as e:
                        self.use_mock_data = True
                
                # Update bar heights with smooth colors
                for i, (bar, height) in enumerate(zip(self.bars, self.audio_data)):
                    bar.set_height(height)
                    # Color gradient based on height
                    if height > 0.7:
                        bar.set_color(ModernTheme.COLORS['accent_success'])
                    elif height > 0.4:
                        bar.set_color(ModernTheme.COLORS['accent_primary'])
                    else:
                        bar.set_color(ModernTheme.COLORS['text_muted'])
                
            except Exception as e:
                pass  # Fail silently for smooth experience
        else:
            # Fade out animation when not recording
            for bar in self.bars:
                current_height = bar.get_height()
                bar.set_height(current_height * 0.9)  # Fade out
                bar.set_color(ModernTheme.COLORS['text_muted'])


class ModernJarvisGUI:
    """Modern JARVIS GUI with sleek design"""
    
    def __init__(self):
        self.setup_root()
        self.setup_variables()
        self.setup_theme()
        self.create_modern_layout()
        self.setup_bindings()
        
        # Start the message processing
        self.process_messages()
        
        print("🚀 Modern JARVIS GUI initialized!")
    
    def setup_root(self):
        """Initialize the main window with modern styling"""
        self.root = tk.Tk()
        self.root.title("JARVIS - AI Assistant")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ModernTheme.COLORS['bg_primary'])
        
        # Modern window styling
        try:
            # Try to set window icon if available
            self.root.iconbitmap(default="icon.ico")
        except:
            pass
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Initialize variables"""
        self.api_base_url = "http://localhost:8081"
        self.session_id = str(uuid.uuid4())
        self.user_id = "gui_user"
        self.last_activity = time.time()
        self.message_queue = queue.Queue()
        self.wake_word_active = False
        self.is_speaking = False
    
    def setup_theme(self):
        """Apply modern theme"""
        ModernTheme.configure_ttk_styles(self.root)
        
        # Configure modern fonts
        self.fonts = ModernTheme.FONTS
    
    def create_modern_layout(self):
        """Create the modern layout with sidebar and main area"""
        # Create main container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_area()
        
        # Create status bar
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create modern sidebar with navigation and controls"""
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame')
        self.sidebar.pack(side='left', fill='y', padx=(0, 1))
        self.sidebar.configure(width=ModernTheme.STYLES['sidebar_width'])
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        self.create_sidebar_header()
        
        # Voice controls section
        self.create_voice_controls()
        
        # Audio visualizer
        self.create_audio_section()
        
        # Quick actions
        self.create_quick_actions()
        
        # Session info
        self.create_session_info()
    
    def create_sidebar_header(self):
        """Create sidebar header with JARVIS branding"""
        header_frame = ModernTheme.create_card_frame(self.sidebar)
        header_frame.pack(fill='x', padx=12, pady=(12, 8))
        
        # JARVIS logo/title
        title_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['bg_card'])
        title_frame.pack(fill='x', pady=12)
        
        # Robot icon
        icon_label = tk.Label(title_frame, 
                             text=ICONS['robot'], 
                             font=('Segoe UI Emoji', 24),
                             bg=ModernTheme.COLORS['bg_card'],
                             fg=ModernTheme.COLORS['accent_primary'])
        icon_label.pack(side='left', padx=(8, 4))
        
        # Title
        title_label = tk.Label(title_frame,
                              text="JARVIS",
                              font=self.fonts['heading_large'],
                              bg=ModernTheme.COLORS['bg_card'],
                              fg=ModernTheme.COLORS['text_primary'])
        title_label.pack(side='left', padx=(4, 8))
        
        # Status indicator
        self.status_indicator = ModernComponents.create_status_indicator(title_frame, 'online')
        self.status_indicator.pack(side='right', padx=8, pady=8)
    
    def create_voice_controls(self):
        """Create voice control section"""
        voice_frame = ModernTheme.create_card_frame(self.sidebar)
        voice_frame.pack(fill='x', padx=12, pady=8)
        
        # Section header
        header = tk.Label(voice_frame,
                         text=f"{ICONS['voice']} Röststyrning",
                         font=self.fonts['heading_small'],
                         bg=ModernTheme.COLORS['bg_card'],
                         fg=ModernTheme.COLORS['text_primary'])
        header.pack(pady=(12, 8), padx=12, anchor='w')
        
        # Button container
        button_frame = tk.Frame(voice_frame, bg=ModernTheme.COLORS['bg_card'])
        button_frame.pack(fill='x', padx=12, pady=(0, 12))
        
        # Wake word button
        self.wake_word_btn = ttk.Button(button_frame,
                                       text=f"🎯 Aktivera Väckord",
                                       command=self.toggle_wake_word,
                                       style='Primary.TButton')
        self.wake_word_btn.pack(fill='x', pady=2)
        
        # Voice test button
        self.voice_test_btn = ttk.Button(button_frame,
                                        text=f"🔊 Testa Röst",
                                        command=self.test_voice,
                                        style='Modern.TButton')
        self.voice_test_btn.pack(fill='x', pady=2)
        
        # Stop speaking button
        self.stop_voice_btn = ttk.Button(button_frame,
                                        text=f"⏹️ Stoppa Tal",
                                        command=self.stop_speaking,
                                        style='Danger.TButton')
        self.stop_voice_btn.pack(fill='x', pady=2)
    
    def create_audio_section(self):
        """Create audio visualization section"""
        audio_frame = ModernTheme.create_card_frame(self.sidebar)
        audio_frame.pack(fill='x', padx=12, pady=8)
        
        # Section header
        header = tk.Label(audio_frame,
                         text=f"{ICONS['lightning']} Ljudvisualisering",
                         font=self.fonts['heading_small'],
                         bg=ModernTheme.COLORS['bg_card'],
                         fg=ModernTheme.COLORS['text_primary'])
        header.pack(pady=(12, 8), padx=12, anchor='w')
        
        # Audio visualizer container
        viz_container = tk.Frame(audio_frame, 
                                bg=ModernTheme.COLORS['bg_card'],
                                height=120)
        viz_container.pack(fill='x', padx=8, pady=(0, 12))
        viz_container.pack_propagate(False)
        
        # Initialize audio visualizer
        self.audio_viz = ModernAudioVisualizer(viz_container)
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ModernTheme.create_card_frame(self.sidebar)
        actions_frame.pack(fill='x', padx=12, pady=8)
        
        # Section header
        header = tk.Label(actions_frame,
                         text=f"{ICONS['sparkles']} Snabbåtgärder",
                         font=self.fonts['heading_small'],
                         bg=ModernTheme.COLORS['bg_card'],
                         fg=ModernTheme.COLORS['text_primary'])
        header.pack(pady=(12, 8), padx=12, anchor='w')
        
        # Button container
        button_frame = tk.Frame(actions_frame, bg=ModernTheme.COLORS['bg_card'])
        button_frame.pack(fill='x', padx=12, pady=(0, 12))
        
        # Quick action buttons
        actions = [
            (f"{ICONS['research']} Research", self.quick_research),
            (f"{ICONS['memory']} Minne", self.view_memory),
            (f"{ICONS['settings']} Inställningar", self.open_settings)
        ]
        
        for text, command in actions:
            btn = ttk.Button(button_frame,
                           text=text,
                           command=command,
                           style='Modern.TButton')
            btn.pack(fill='x', pady=2)
    
    def create_session_info(self):
        """Create session information panel"""
        session_frame = ModernTheme.create_card_frame(self.sidebar)
        session_frame.pack(fill='x', side='bottom', padx=12, pady=12)
        
        # Session info
        self.session_label = tk.Label(session_frame,
                                     text="Session Info",
                                     font=self.fonts['body_small'],
                                     bg=ModernTheme.COLORS['bg_card'],
                                     fg=ModernTheme.COLORS['text_muted'])
        self.session_label.pack(pady=8, padx=12)
        
        # Update session info
        self.update_session_info()
    
    def create_main_area(self):
        """Create main content area with chat interface"""
        self.main_area = ttk.Frame(self.main_container, style='Main.TFrame')
        self.main_area.pack(side='right', fill='both', expand=True)
        
        # Create header
        self.create_main_header()
        
        # Create chat area
        self.create_chat_area()
        
        # Create input area
        self.create_input_area()
    
    def create_main_header(self):
        """Create main area header"""
        header_frame = tk.Frame(self.main_area, 
                               bg=ModernTheme.COLORS['bg_secondary'],
                               height=ModernTheme.STYLES['header_height'])
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=12)
        
        # Title
        title = tk.Label(content_frame,
                        text="AI Assistent Chat",
                        font=self.fonts['heading_medium'],
                        bg=ModernTheme.COLORS['bg_secondary'],
                        fg=ModernTheme.COLORS['text_primary'])
        title.pack(side='left')
        
        # Status info
        self.status_label = tk.Label(content_frame,
                                    text="🟢 Online",
                                    font=self.fonts['body_medium'],
                                    bg=ModernTheme.COLORS['bg_secondary'],
                                    fg=ModernTheme.COLORS['accent_success'])
        self.status_label.pack(side='right')
    
    def create_chat_area(self):
        """Create modern chat interface"""
        # Chat container with custom styling
        chat_container = tk.Frame(self.main_area, bg=ModernTheme.COLORS['bg_primary'])
        chat_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create scrolled text with modern styling
        self.output_text = scrolledtext.ScrolledText(
            chat_container,
            bg=ModernTheme.COLORS['bg_primary'],
            fg=ModernTheme.COLORS['text_primary'],
            font=self.fonts['body_medium'],
            insertbackground=ModernTheme.COLORS['text_primary'],
            selectbackground=ModernTheme.COLORS['accent_primary'],
            selectforeground=ModernTheme.COLORS['text_primary'],
            relief='flat',
            borderwidth=0,
            wrap=tk.WORD,
            state='disabled'
        )
        
        # Custom scrollbar
        scrollbar = ModernComponents.create_modern_scrollbar(chat_container)
        
        # Pack with modern styling
        self.output_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configure scrollbar
        scrollbar.configure(command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Add welcome message
        self.add_welcome_message()
    
    def create_input_area(self):
        """Create modern input area"""
        input_container = tk.Frame(self.main_area, bg=ModernTheme.COLORS['bg_secondary'])
        input_container.pack(fill='x', side='bottom')
        
        # Input frame with padding
        input_frame = tk.Frame(input_container, bg=ModernTheme.COLORS['bg_secondary'])
        input_frame.pack(fill='x', padx=20, pady=16)
        
        # Input entry with modern styling
        self.input_entry = tk.Entry(
            input_frame,
            bg=ModernTheme.COLORS['input_bg'],
            fg=ModernTheme.COLORS['text_primary'],
            font=self.fonts['body_medium'],
            insertbackground=ModernTheme.COLORS['text_primary'],
            relief='flat',
            borderwidth=8,
            bd=8
        )
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(0, 12))
        
        # Send button with modern styling
        self.send_btn = ttk.Button(
            input_frame,
            text=f"{ICONS['send']} Skicka",
            command=self.send_command,
            style='Primary.TButton'
        )
        self.send_btn.pack(side='right')
        
        # Placeholder text functionality
        self.setup_input_placeholder()
    
    def create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = tk.Frame(self.root, 
                                  bg=ModernTheme.COLORS['bg_tertiary'],
                                  height=24)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        # Status text
        self.status_text = tk.Label(self.status_bar,
                                   text="Redo för kommandon...",
                                   bg=ModernTheme.COLORS['bg_tertiary'],
                                   fg=ModernTheme.COLORS['text_muted'],
                                   font=self.fonts['body_small'])
        self.status_text.pack(side='left', padx=12, pady=4)
        
        # Connection status
        self.connection_status = tk.Label(self.status_bar,
                                         text="🟢 Ansluten",
                                         bg=ModernTheme.COLORS['bg_tertiary'],
                                         fg=ModernTheme.COLORS['text_muted'],
                                         font=self.fonts['body_small'])
        self.connection_status.pack(side='right', padx=12, pady=4)
    
    def setup_input_placeholder(self):
        """Setup placeholder text for input"""
        placeholder = "Skriv ditt meddelande här..."
        
        def on_focus_in(event):
            if self.input_entry.get() == placeholder:
                self.input_entry.delete(0, tk.END)
                self.input_entry.configure(fg=ModernTheme.COLORS['text_primary'])
        
        def on_focus_out(event):
            if not self.input_entry.get():
                self.input_entry.insert(0, placeholder)
                self.input_entry.configure(fg=ModernTheme.COLORS['text_muted'])
        
        self.input_entry.insert(0, placeholder)
        self.input_entry.configure(fg=ModernTheme.COLORS['text_muted'])
        self.input_entry.bind('<FocusIn>', on_focus_in)
        self.input_entry.bind('<FocusOut>', on_focus_out)
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_msg = f"""
{ICONS['robot']} Välkommen till JARVIS AI Assistant!

Jag är din personliga AI-assistent med avancerade funktioner:

• 🔬 Research och analys
• 🧠 Intelligent minnesfunktion  
• 🎤 Röststyrning på svenska
• ⚡ Automatisk förbättring
• 🌐 Google Cloud integration

Skriv ett meddelande eller använd röstkommandon för att komma igång!
        """
        
        self.append_message("JARVIS", welcome_msg.strip(), "assistant")
    
    def append_message(self, sender, message, msg_type="user"):
        """Append a message to the chat with modern styling"""
        self.output_text.configure(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Choose colors based on message type
        if msg_type == "assistant":
            sender_color = ModernTheme.COLORS['accent_primary']
            icon = ICONS['robot']
        else:
            sender_color = ModernTheme.COLORS['accent_secondary']
            icon = "👤"
        
        # Format message
        formatted_msg = f"\n{icon} {sender} • {timestamp}\n{message}\n"
        
        # Insert with basic formatting
        self.output_text.insert(tk.END, formatted_msg)
        
        # Auto-scroll to bottom
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)
    
    def setup_bindings(self):
        """Setup keyboard bindings"""
        self.input_entry.bind('<Return>', lambda e: self.send_command())
        self.input_entry.bind('<Control-Return>', lambda e: self.input_entry.insert(tk.INSERT, '\n'))
        
        # Focus on input by default
        self.root.after(100, lambda: self.input_entry.focus_set())
    
    # Event handlers
    def toggle_wake_word(self):
        """Toggle wake word detection"""
        try:
            if self.wake_word_active:
                response = requests.post(f"{self.api_base_url}/api/voice/wake-word/stop")
                if response.status_code == 200:
                    self.wake_word_active = False
                    self.wake_word_btn.configure(text="🎯 Aktivera Väckord")
                    self.status_text.configure(text="Väckord inaktiverat")
                    self.audio_viz.stop_recording()
            else:
                response = requests.post(f"{self.api_base_url}/api/voice/wake-word/start")
                if response.status_code == 200:
                    self.wake_word_active = True
                    self.wake_word_btn.configure(text="🛑 Stoppa Väckord")
                    self.status_text.configure(text="Lyssnar efter väckord...")
                    self.audio_viz.start_recording()
        except Exception as e:
            self.show_error(f"Fel vid väckord: {e}")
    
    def test_voice(self):
        """Test voice output"""
        test_message = "Hej! Detta är ett test av JARVIS röstfunktion."
        try:
            response = requests.post(
                f"{self.api_base_url}/api/voice/speak",
                json={"text": test_message}
            )
            if response.status_code == 200:
                self.status_text.configure(text="Testar röst...")
                self.append_message("System", "🔊 Rösttest startat", "assistant")
            else:
                self.show_error("Kunde inte starta rösttest")
        except Exception as e:
            self.show_error(f"Rösttest fel: {e}")
    
    def stop_speaking(self):
        """Stop current speech"""
        try:
            response = requests.post(f"{self.api_base_url}/api/voice/stop")
            if response.status_code == 200:
                self.status_text.configure(text="Tal stoppat")
                self.append_message("System", "⏹️ Tal stoppat", "assistant")
        except Exception as e:
            self.show_error(f"Kunde inte stoppa tal: {e}")
    
    def send_command(self):
        """Send command to JARVIS"""
        command = self.input_entry.get().strip()
        
        # Check for placeholder
        if command == "Skriv ditt meddelande här..." or not command:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Add user message
        self.append_message("Du", command, "user")
        
        # Update status
        self.status_text.configure(text="Bearbetar kommando...")
        
        # Send to API in separate thread
        threading.Thread(target=self._send_command_async, args=(command,), daemon=True).start()
    
    def _send_command_async(self, command):
        """Send command asynchronously"""
        try:
            payload = {
                "command": command,
                "session_id": self.session_id,
                "user_id": self.user_id
            }
            
            response = requests.post(f"{self.api_base_url}/api/command", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', 'Inget svar mottaget')
                
                # Queue the response for main thread
                self.message_queue.put(('response', response_text))
                self.message_queue.put(('status', 'Kommando slutfört'))
            else:
                error_msg = f"API fel: {response.status_code}"
                self.message_queue.put(('error', error_msg))
                
        except requests.exceptions.Timeout:
            self.message_queue.put(('error', 'Timeout - kommandot tog för lång tid'))
        except requests.exceptions.ConnectionError:
            self.message_queue.put(('error', 'Anslutningsfel - kontrollera att JARVIS server körs'))
        except Exception as e:
            self.message_queue.put(('error', f'Oväntat fel: {e}'))
    
    def quick_research(self):
        """Start quick research"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "Gör en snabb research om ")
        self.input_entry.focus_set()
        self.input_entry.icursor(tk.END)
    
    def view_memory(self):
        """View memory"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "Visa mitt minne")
        self.send_command()
    
    def open_settings(self):
        """Open settings (placeholder)"""
        self.append_message("System", "⚙️ Inställningar kommer snart...", "assistant")
    
    def update_session_info(self):
        """Update session information"""
        session_time = int(time.time() - self.last_activity)
        minutes = session_time // 60
        seconds = session_time % 60
        
        session_text = f"Session: {minutes:02d}:{seconds:02d}\nID: {self.session_id[:8]}..."
        self.session_label.configure(text=session_text)
        
        # Schedule next update
        self.root.after(1000, self.update_session_info)
    
    def show_error(self, message):
        """Show error message"""
        self.append_message("Fel", f"❌ {message}", "assistant")
        self.status_text.configure(text=f"Fel: {message}")
    
    def process_messages(self):
        """Process messages from queue"""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                
                if msg_type == 'response':
                    self.append_message("JARVIS", content, "assistant")
                elif msg_type == 'error':
                    self.show_error(content)
                elif msg_type == 'status':
                    self.status_text.configure(text=content)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)
    
    def on_closing(self):
        """Handle window closing"""
        try:
            # Cleanup audio
            if hasattr(self, 'audio_viz'):
                self.audio_viz.cleanup()
            
            # Stop wake word if active
            if self.wake_word_active:
                requests.post(f"{self.api_base_url}/api/voice/wake-word/stop")
            
        except:
            pass
        
        self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start with focus on input
        self.root.after(200, lambda: self.input_entry.focus_set())
        
        print("🎨 Starting modern JARVIS GUI...")
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = ModernJarvisGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 JARVIS GUI stängs ner...")
    except Exception as e:
        print(f"❌ Kritiskt fel: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
