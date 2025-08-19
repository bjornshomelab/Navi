"""
JARVIS GUI - Simplified version without audio visualization
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


class SimpleAudioVisualizer:
    """Simple audio visualizer without real audio"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.is_recording = False
        
        # Create a simple visual indicator
        self.canvas = tk.Canvas(parent_frame, bg='#1e1e1e', height=100)
        self.canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create visual elements
        self.bars = []
        self.create_visual_bars()
        
    def create_visual_bars(self):
        """Create visual bars for audio simulation"""
        canvas_width = 280
        bar_width = 8
        bar_count = canvas_width // (bar_width + 2)
        
        for i in range(bar_count):
            x = i * (bar_width + 2) + 10
            bar = self.canvas.create_rectangle(
                x, 80, x + bar_width, 90,
                fill='#00ff00', outline='#00ff00'
            )
            self.bars.append(bar)
            
    def start_recording(self):
        """Start audio visualization simulation"""
        self.is_recording = True
        self.animate_bars()
        
    def stop_recording(self):
        """Stop audio visualization"""
        self.is_recording = False
        # Reset bars
        for bar in self.bars:
            self.canvas.coords(bar, 
                             self.canvas.coords(bar)[0], 80,
                             self.canvas.coords(bar)[2], 90)
            
    def animate_bars(self):
        """Animate the audio bars"""
        if self.is_recording:
            import random
            for bar in self.bars:
                coords = self.canvas.coords(bar)
                height = random.randint(5, 60)
                self.canvas.coords(bar, coords[0], 90-height, coords[2], 90)
            
            # Schedule next animation
            self.parent_frame.after(100, self.animate_bars)


class JarvisGUISimple:
    """Simplified JARVIS GUI without complex audio dependencies"""
    
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
        
        # Audio visualizer (simplified)
        self.audio_viz = SimpleAudioVisualizer(audio_frame)
        
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
    """Main entry point for simple GUI"""
    try:
        app = JarvisGUISimple()
        app.run()
    except KeyboardInterrupt:
        print("\nGUI shutting down...")
    except Exception as e:
        print(f"GUI Error: {e}")


if __name__ == "__main__":
    main()
