"""
JARVIS GUI - Main Window with Sidebar and Output Area
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
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


class AudioVisualizer:
    """Real-time audio waveform visualizer"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.is_recording = False
        self.audio_data = np.zeros(1024)
        self.use_mock_data = False
        
        # Audio settings
        self.chunk = 1024
        self.sample_rate = 44100
        self.channels = 1
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#1e1e1e')
        self.ax.set_xlim(0, self.chunk)
        self.ax.set_ylim(-1, 1)
        self.ax.set_title("Audio Waveform", color='white', fontsize=10)
        self.ax.tick_params(colors='white')
        
        # Create line plot
        self.line, = self.ax.plot(np.arange(self.chunk), self.audio_data, color='#00ff00', linewidth=1)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Audio stream
        self.audio_stream = None
        self.p = None
        
    def start_recording(self):
        """Start audio recording and visualization"""
        try:
            self.p = pyaudio.PyAudio()
            
            # Try to find a working input device
            input_device = None
            for i in range(self.p.get_device_count()):
                device_info = self.p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_device = i
                    break
                    
            if input_device is None:
                print("No audio input device found, using mock data")
                self.use_mock_data = True
            else:
                self.audio_stream = self.p.open(
                    format=pyaudio.paFloat32,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=input_device,
                    frames_per_buffer=self.chunk
                )
                self.use_mock_data = False
                
            self.is_recording = True
            self.animation = FuncAnimation(self.fig, self.update_plot, interval=50, 
                                         blit=False, cache_frame_data=False)
            self.canvas.draw()
        except Exception as e:
            print(f"Audio recording error: {e}")
            print("Using mock audio data")
            self.use_mock_data = True
            self.is_recording = True
            self.animation = FuncAnimation(self.fig, self.update_plot, interval=50, 
                                         blit=False, cache_frame_data=False)
            self.canvas.draw()
            
    def stop_recording(self):
        """Stop audio recording and visualization"""
        self.is_recording = False
        if hasattr(self, 'animation'):
            self.animation.event_source.stop()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.p:
            self.p.terminate()
            
    def update_plot(self, frame):
        """Update the waveform plot"""
        if self.is_recording:
            try:
                if hasattr(self, 'use_mock_data') and self.use_mock_data:
                    # Generate mock audio data
                    import random
                    amplitude = random.uniform(0.1, 0.3)
                    frequency = random.uniform(200, 800)
                    time_array = np.linspace(0, 1, self.chunk)
                    self.audio_data = amplitude * np.sin(2 * np.pi * frequency * time_array)
                elif self.audio_stream:
                    data = self.audio_stream.read(self.chunk, exception_on_overflow=False)
                    self.audio_data = np.frombuffer(data, dtype=np.float32)
                    
                self.line.set_ydata(self.audio_data)
                return self.line,
            except Exception as e:
                print(f"Plot update error: {e}")
        return self.line,


class JarvisGUI:
    """Main JARVIS GUI Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS - Personal AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # API settings
        self.api_base_url = "http://localhost:8081"
        self.session_id = str(uuid.uuid4())  # Generate unique session ID
        self.user_id = "gui_user"
        self.last_activity = time.time()
        
        # Message queue for threading
        self.message_queue = queue.Queue()
        
        # Setup GUI components
        self.setup_styles()
        self.create_layout()
        self.setup_bindings()
        
        # Start processing messages
        self.process_queue()
        
        # Start audio visualizer
        self.audio_viz.start_recording()
        
        # Start activity monitor
        self.start_activity_monitor()
        
        # Check wake word status on startup
        self.check_wake_word_status()
    
    def check_wake_word_status(self):
        """Check wake word detection status"""
        try:
            response = requests.get(f"{self.api_base_url}/api/command/wake-word/status")
            if response.status_code == 200:
                result = response.json()
                if result.get('available'):
                    if result.get('listening'):
                        self.wake_status_label.config(text="Wake word: Listening...")
                    else:
                        self.wake_status_label.config(text="Wake word: Available")
                else:
                    self.wake_status_label.config(text="Wake word: Not available")
                    self.wake_start_button.config(state='disabled')
        except Exception as e:
            self.wake_status_label.config(text="Wake word: Error")
            print(f"Wake word status check failed: {e}")
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for dark theme
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='white')
        style.configure('TButton', background='#0d7377', foreground='white')
        style.map('TButton', background=[('active', '#14a085')])
        style.configure('TEntry', fieldbackground='#2b2b2b', foreground='white')
        
    def create_layout(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create sidebar
        self.create_sidebar(main_frame)
        
        # Create main content area
        self.create_main_content(main_frame)
        
    def create_sidebar(self, parent):
        """Create the sidebar with input and audio visualization"""
        sidebar_frame = ttk.Frame(parent, width=300)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Title
        title_label = ttk.Label(sidebar_frame, text="JARVIS Control Panel", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(sidebar_frame, text="Text Input", padding=10)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Text input
        self.text_input = tk.Text(input_frame, height=4, bg='#2b2b2b', fg='white',
                                 insertbackground='white', wrap='word')
        self.text_input.pack(fill='x', pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x')
        
        self.send_button = ttk.Button(button_frame, text="Send Command", 
                                     command=self.send_command)
        self.send_button.pack(side='left', padx=(0, 5))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", 
                                      command=self.clear_input)
        self.clear_button.pack(side='left')
        
        # Audio visualization section
        audio_frame = ttk.LabelFrame(sidebar_frame, text="Audio Waveform", padding=10)
        audio_frame.pack(fill='both', expand=True)
        
        # Audio controls
        audio_controls = ttk.Frame(audio_frame)
        audio_controls.pack(fill='x', pady=(0, 10))
        
        self.record_button = ttk.Button(audio_controls, text="🎤 Start Recording", 
                                       command=self.toggle_recording)
        self.record_button.pack(side='left', padx=(0, 5))
        
        self.voice_button = ttk.Button(audio_controls, text="🎵 Voice Command", 
                                      command=self.voice_command)
        self.voice_button.pack(side='left')
        
        # Audio visualizer
        self.audio_viz = AudioVisualizer(audio_frame)
        
        # Wake word detection controls
        wake_frame = ttk.LabelFrame(sidebar_frame, text="Wake Word Detection", padding=10)
        wake_frame.pack(fill='x', padx=5, pady=5)
        
        wake_buttons_frame = ttk.Frame(wake_frame)
        wake_buttons_frame.pack(fill='x', padx=5, pady=5)
        
        self.wake_start_button = ttk.Button(
            wake_buttons_frame, 
            text="Start Wake Word", 
            command=self.start_wake_word
        )
        self.wake_start_button.pack(side='left', padx=2)
        
        self.wake_stop_button = ttk.Button(
            wake_buttons_frame, 
            text="Stop Wake Word", 
            command=self.stop_wake_word,
            style='Danger.TButton'
        )
        self.wake_stop_button.pack(side='left', padx=2)
        
        self.wake_status_label = ttk.Label(wake_frame, text="Wake word: Stopped")
        self.wake_status_label.pack(pady=2)
        
        # Test wake word button
        self.test_wake_button = ttk.Button(
            wake_frame,
            text="Test: 'Hey Jarvis, vad är klockan?'",
            command=self.test_wake_word,
            style='Info.TButton'
        )
        self.test_wake_button.pack(pady=2)
        
        # Voice/TTS control section
        self.create_voice_controls(sidebar_frame)
        
    def create_voice_controls(self, parent):
        """Create voice/TTS control panel"""
        voice_frame = ttk.LabelFrame(parent, text="Voice Control (TTS)", padding=10)
        voice_frame.pack(fill='x', padx=5, pady=5)
        
        # Voice status
        self.voice_status_label = ttk.Label(voice_frame, text="Voice: Ready")
        self.voice_status_label.pack(pady=2)
        
        # Voice control buttons
        voice_buttons_frame = ttk.Frame(voice_frame)
        voice_buttons_frame.pack(fill='x', pady=5)
        
        self.voice_mute_button = ttk.Button(
            voice_buttons_frame,
            text="Mute",
            command=self.toggle_voice_mute,
            style='Warning.TButton'
        )
        self.voice_mute_button.pack(side='left', padx=2)
        
        self.voice_stop_button = ttk.Button(
            voice_buttons_frame,
            text="Stop Speaking",
            command=self.stop_voice,
            style='Danger.TButton'
        )
        self.voice_stop_button.pack(side='left', padx=2)
        
        # Voice settings
        settings_frame = ttk.Frame(voice_frame)
        settings_frame.pack(fill='x', pady=5)
        
        # Volume control
        ttk.Label(settings_frame, text="Volume:").grid(row=0, column=0, sticky='w')
        self.volume_var = tk.DoubleVar(value=0.9)
        self.volume_scale = ttk.Scale(
            settings_frame, from_=0.0, to=1.0, orient='horizontal',
            variable=self.volume_var, command=self.update_voice_volume
        )
        self.volume_scale.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Speech rate control
        ttk.Label(settings_frame, text="Rate:").grid(row=1, column=0, sticky='w')
        self.rate_var = tk.IntVar(value=180)
        self.rate_scale = ttk.Scale(
            settings_frame, from_=50, to=300, orient='horizontal',
            variable=self.rate_var, command=self.update_voice_rate
        )
        self.rate_scale.grid(row=1, column=1, sticky='ew', padx=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Voice test button
        self.test_voice_button = ttk.Button(
            voice_frame,
            text="Test Voice: 'Hej! Jag är JARVIS'",
            command=self.test_voice,
            style='Info.TButton'
        )
        self.test_voice_button.pack(pady=5)
        
        # Voice mute state
        self.voice_muted = False
        
    def create_main_content(self, parent):
        """Create the main content area"""
        content_frame = ttk.Frame(parent)
        content_frame.pack(side='right', fill='both', expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Console tab
        self.create_console_tab()
        
        # Research tab
        self.create_research_tab()
        
        # Memory tab
        self.create_memory_tab()
        
        # Files tab
        self.create_files_tab()
        
    def create_console_tab(self):
        """Create the console output tab"""
        console_frame = ttk.Frame(self.notebook)
        self.notebook.add(console_frame, text="Console")
        
        # Console output
        self.console_output = scrolledtext.ScrolledText(
            console_frame, bg='#1e1e1e', fg='#00ff00', 
            insertbackground='white', wrap='word',
            font=('Consolas', 10)
        )
        self.console_output.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add welcome message
        welcome_msg = f"""JARVIS Personal AI Assistant
{'-' * 50}
Welcome! I'm ready to help you with:
• System automation and control
• Web research and analysis
• Desktop and web automation
• Memory management and learning
• Code analysis and improvement

Type a command in the sidebar or use voice input.

Status: Ready
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'-' * 50}

"""
        self.console_output.insert('end', welcome_msg)
        
    def create_research_tab(self):
        """Create the research results tab"""
        research_frame = ttk.Frame(self.notebook)
        self.notebook.add(research_frame, text="Research")
        
        # Research content
        self.research_output = scrolledtext.ScrolledText(
            research_frame, bg='#1e1e1e', fg='white', 
            insertbackground='white', wrap='word',
            font=('Arial', 10)
        )
        self.research_output.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Research controls
        research_controls = ttk.Frame(research_frame)
        research_controls.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(research_controls, text="Start Research", 
                  command=self.start_research).pack(side='left', padx=(0, 5))
        ttk.Button(research_controls, text="View Reports", 
                  command=self.view_reports).pack(side='left', padx=(0, 5))
        ttk.Button(research_controls, text="Clear", 
                  command=lambda: self.research_output.delete('1.0', 'end')).pack(side='left')
        
    def create_memory_tab(self):
        """Create the memory management tab"""
        memory_frame = ttk.Frame(self.notebook)
        self.notebook.add(memory_frame, text="Memory")
        
        # Memory content
        self.memory_output = scrolledtext.ScrolledText(
            memory_frame, bg='#1e1e1e', fg='white', 
            insertbackground='white', wrap='word',
            font=('Arial', 10)
        )
        self.memory_output.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Memory controls
        memory_controls = ttk.Frame(memory_frame)
        memory_controls.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(memory_controls, text="View Context", 
                  command=self.view_memory_context).pack(side='left', padx=(0, 5))
        ttk.Button(memory_controls, text="View Preferences", 
                  command=self.view_preferences).pack(side='left', padx=(0, 5))
        ttk.Button(memory_controls, text="Clear Memory", 
                  command=self.clear_memory).pack(side='left')
        
    def create_files_tab(self):
        """Create the files and documents tab"""
        files_frame = ttk.Frame(self.notebook)
        self.notebook.add(files_frame, text="Files")
        
        # Files content
        self.files_output = scrolledtext.ScrolledText(
            files_frame, bg='#1e1e1e', fg='white', 
            insertbackground='white', wrap='word',
            font=('Arial', 10)
        )
        self.files_output.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Files controls
        files_controls = ttk.Frame(files_frame)
        files_controls.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(files_controls, text="List Reports", 
                  command=self.list_reports).pack(side='left', padx=(0, 5))
        ttk.Button(files_controls, text="Open File", 
                  command=self.open_file).pack(side='left', padx=(0, 5))
        ttk.Button(files_controls, text="Refresh", 
                  command=self.refresh_files).pack(side='left')
        
    def setup_bindings(self):
        """Setup keyboard bindings"""
        self.root.bind('<Control-Return>', lambda e: self.send_command())
        self.root.bind('<F1>', lambda e: self.toggle_recording())
        self.root.bind('<F2>', lambda e: self.voice_command())
        
    def log_message(self, message, tab='console'):
        """Add a message to the appropriate tab"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if tab == 'console':
            self.console_output.insert('end', formatted_msg)
            self.console_output.see('end')
        elif tab == 'research':
            self.research_output.insert('end', formatted_msg)
            self.research_output.see('end')
        elif tab == 'memory':
            self.memory_output.insert('end', formatted_msg)
            self.memory_output.see('end')
        elif tab == 'files':
            self.files_output.insert('end', formatted_msg)
            self.files_output.see('end')
            
    def send_command(self):
        """Send command to JARVIS backend"""
        command = self.text_input.get('1.0', 'end-1c').strip()
        if not command:
            return
            
        # Update activity timestamp
        self.last_activity = time.time()
        
        self.log_message(f"USER: {command}")
        self.text_input.delete('1.0', 'end')
        
        # Send command in background thread
        threading.Thread(target=self._send_command_async, args=(command,), daemon=True).start()
        
    def _send_command_async(self, command):
        """Send command asynchronously"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/command",
                json={
                    "message": command,
                    "session_id": self.session_id,
                    "user_id": self.user_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.message_queue.put(('response', result))
            else:
                self.message_queue.put(('error', f"API Error: {response.status_code}"))
                
        except requests.exceptions.ConnectionError:
            self.message_queue.put(('error', "Connection Error: JARVIS backend not running"))
        except Exception as e:
            self.message_queue.put(('error', f"Error: {str(e)}"))
            
    def clear_input(self):
        """Clear the text input"""
        self.text_input.delete('1.0', 'end')
        
    def toggle_recording(self):
        """Toggle audio recording"""
        if self.audio_viz.is_recording:
            self.audio_viz.stop_recording()
            self.record_button.config(text="🎤 Start Recording")
            self.log_message("Audio recording stopped")
        else:
            self.audio_viz.start_recording()
            self.record_button.config(text="🛑 Stop Recording")
            self.log_message("Audio recording started")
            
    def voice_command(self):
        """Process voice command (placeholder)"""
        self.log_message("Voice command processing not yet implemented")
        messagebox.showinfo("Voice Command", "Voice command feature coming soon!")
        
    def start_research(self):
        """Start a research workflow"""
        self.log_message("Starting research workflow...", 'research')
        threading.Thread(target=self._start_research_async, daemon=True).start()
        
    def _start_research_async(self):
        """Start research workflow asynchronously"""
        try:
            response = requests.post(f"{self.api_base_url}/research/start", json={})
            if response.status_code == 200:
                result = response.json()
                self.message_queue.put(('research', result))
            else:
                self.message_queue.put(('error', f"Research API Error: {response.status_code}"))
        except Exception as e:
            self.message_queue.put(('error', f"Research Error: {str(e)}"))
            
    def view_reports(self):
        """View research reports"""
        self.log_message("Loading research reports...", 'research')
        threading.Thread(target=self._view_reports_async, daemon=True).start()
        
    def _view_reports_async(self):
        """View reports asynchronously"""
        try:
            response = requests.get(f"{self.api_base_url}/research/reports")
            if response.status_code == 200:
                result = response.json()
                self.message_queue.put(('reports', result))
            else:
                self.message_queue.put(('error', f"Reports API Error: {response.status_code}"))
        except Exception as e:
            self.message_queue.put(('error', f"Reports Error: {str(e)}"))
            
    def view_memory_context(self):
        """View memory context"""
        self.log_message("Loading memory context...", 'memory')
        threading.Thread(target=self._view_memory_async, daemon=True).start()
        
    def _view_memory_async(self):
        """View memory asynchronously"""
        try:
            response = requests.get(f"{self.api_base_url}/memory/context")
            if response.status_code == 200:
                result = response.json()
                self.message_queue.put(('memory_context', result))
            else:
                self.message_queue.put(('error', f"Memory API Error: {response.status_code}"))
        except Exception as e:
            self.message_queue.put(('error', f"Memory Error: {str(e)}"))
            
    def view_preferences(self):
        """View user preferences"""
        self.log_message("Loading preferences...", 'memory')
        threading.Thread(target=self._view_preferences_async, daemon=True).start()
        
    def _view_preferences_async(self):
        """View preferences asynchronously"""
        try:
            response = requests.get(f"{self.api_base_url}/memory/preferences")
            if response.status_code == 200:
                result = response.json()
                self.message_queue.put(('preferences', result))
            else:
                self.message_queue.put(('error', f"Preferences API Error: {response.status_code}"))
        except Exception as e:
            self.message_queue.put(('error', f"Preferences Error: {str(e)}"))
            
    def clear_memory(self):
        """Clear memory"""
        if messagebox.askyesno("Clear Memory", "Are you sure you want to clear all memory?"):
            self.log_message("Clearing memory...", 'memory')
            threading.Thread(target=self._clear_memory_async, daemon=True).start()
            
    def _clear_memory_async(self):
        """Clear memory asynchronously"""
        try:
            response = requests.delete(f"{self.api_base_url}/memory/clear")
            if response.status_code == 200:
                self.message_queue.put(('memory_cleared', {}))
            else:
                self.message_queue.put(('error', f"Clear Memory API Error: {response.status_code}"))
        except Exception as e:
            self.message_queue.put(('error', f"Clear Memory Error: {str(e)}"))
            
    def list_reports(self):
        """List available reports"""
        self.log_message("Listing available files...", 'files')
        # This would list files in the reports directory
        self.files_output.insert('end', "\nAvailable Reports:\n")
        self.files_output.insert('end', "• research_reports/\n")
        self.files_output.insert('end', "• memory_dumps/\n")
        self.files_output.insert('end', "• automation_logs/\n")
        
    def open_file(self):
        """Open a file"""
        self.log_message("File opening feature not yet implemented", 'files')
        
    def refresh_files(self):
        """Refresh file list"""
        self.files_output.delete('1.0', 'end')
        self.list_reports()
        
    def start_activity_monitor(self):
        """Start monitoring session activity"""
        def monitor_activity():
            while True:
                time.sleep(30)  # Check every 30 seconds
                current_time = time.time()
                idle_time = current_time - self.last_activity
                
                # Update status
                idle_minutes = int(idle_time // 60)
                idle_seconds = int(idle_time % 60)
                
                if idle_time > 240:  # 4 minutes warning
                    status = f"⚠️ Session expires in {300 - int(idle_time)}s"
                    self.message_queue.put(('status', status))
                elif idle_time > 180:  # 3 minutes warning
                    status = f"⏰ Idle for {idle_minutes}m {idle_seconds}s"
                    self.message_queue.put(('status', status))
                
                # Check for session timeout (5 minutes)
                if idle_time > 300:
                    self.message_queue.put(('timeout', 'Session expired due to inactivity'))
                    break
        
        threading.Thread(target=monitor_activity, daemon=True).start()
        
    def handle_session_timeout(self):
        """Handle session timeout"""
        self.log_message("🛑 SESSION EXPIRED: No activity for 5 minutes")
        self.log_message("💡 Relaunch JARVIS to start a new session")
        
        # Disable input
        self.text_input.config(state='disabled')
        self.send_button.config(state='disabled')
        
        # Show timeout dialog
        messagebox.showwarning(
            "Session Expired", 
            "Your JARVIS session has expired due to 5 minutes of inactivity.\n\n"
            "Please restart the application to continue."
        )
        
        # Auto-close after 10 seconds
        self.root.after(10000, self.root.quit)
        
    def process_queue(self):
        """Process messages from background threads"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == 'response':
                    self.log_message(f"JARVIS: {data.get('response', 'No response')}")
                    
                elif msg_type == 'error':
                    self.log_message(f"ERROR: {data}")
                    
                elif msg_type == 'research':
                    self.log_message(f"Research: {json.dumps(data, indent=2)}", 'research')
                    
                elif msg_type == 'reports':
                    self.log_message(f"Reports: {json.dumps(data, indent=2)}", 'research')
                    
                elif msg_type == 'memory_context':
                    self.log_message(f"Memory Context: {json.dumps(data, indent=2)}", 'memory')
                    
                elif msg_type == 'preferences':
                    self.log_message(f"Preferences: {json.dumps(data, indent=2)}", 'memory')
                    
                elif msg_type == 'memory_cleared':
                    self.log_message("Memory cleared successfully", 'memory')
                    
                elif msg_type == 'status':
                    self.log_message(f"STATUS: {data}")
                    
                elif msg_type == 'timeout':
                    self.handle_session_timeout()
                    break
                    
                elif msg_type == 'timeout':
                    self.handle_session_timeout()
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.process_queue)
        
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        finally:
            # Cleanup
            self.audio_viz.stop_recording()


def main():
    """Main entry point"""
    try:
        app = JarvisGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nGUI shutting down...")
    except Exception as e:
        print(f"GUI Error: {e}")


if __name__ == "__main__":
    main()
