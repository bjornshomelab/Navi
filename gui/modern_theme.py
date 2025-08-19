"""
JARVIS GUI - Modern Dark Theme Configuration
Inspirerat av Discord, VS Code, och andra moderna AI-gränssnitt
"""

import tkinter as tk
from tkinter import ttk

class ModernTheme:
    """Modern dark theme with gradient-like colors and smooth transitions"""
    
    # Color palette inspired by Discord and VS Code
    COLORS = {
        # Primary colors
        'bg_primary': '#36393f',      # Discord dark background
        'bg_secondary': '#2f3136',    # Sidebar background
        'bg_tertiary': '#40444b',     # Hover states
        'bg_card': '#4f545c',         # Card/panel background
        
        # Accent colors
        'accent_primary': '#5865f2',  # Discord blurple
        'accent_secondary': '#00d4aa', # Teal green
        'accent_danger': '#ed4245',   # Red for errors
        'accent_warning': '#fee75c',  # Yellow for warnings
        'accent_success': '#57f287',  # Green for success
        
        # Text colors
        'text_primary': '#ffffff',    # Main text
        'text_secondary': '#b9bbbe',  # Secondary text
        'text_muted': '#72767d',      # Muted text
        'text_link': '#00aff4',       # Links and active states
        
        # Interactive colors
        'button_bg': '#4f545c',
        'button_hover': '#5865f2',
        'button_active': '#4752c4',
        'input_bg': '#40444b',
        'input_border': '#72767d',
        'input_focus': '#5865f2',
        
        # Status colors
        'online': '#3ba55c',
        'idle': '#faa61a',
        'dnd': '#ed4245',
        'offline': '#747f8d'
    }
    
    # Font configuration
    FONTS = {
        'heading_large': ('Segoe UI', 24, 'bold'),
        'heading_medium': ('Segoe UI', 18, 'bold'),
        'heading_small': ('Segoe UI', 14, 'bold'),
        'body_large': ('Segoe UI', 12),
        'body_medium': ('Segoe UI', 11),
        'body_small': ('Segoe UI', 10),
        'mono': ('Fira Code', 11),
        'button': ('Segoe UI', 11, 'bold')
    }
    
    # Component styles
    STYLES = {
        'sidebar_width': 280,
        'header_height': 60,
        'button_height': 36,
        'input_height': 32,
        'card_padding': 16,
        'border_radius': 8,  # Simulated with relief
        'shadow_offset': 2
    }

    @classmethod
    def configure_ttk_styles(cls, root):
        """Configure TTK styles for modern look"""
        style = ttk.Style()
        
        # Configure overall theme
        style.theme_use('clam')
        
        # Main window style
        style.configure('Main.TFrame',
                       background=cls.COLORS['bg_primary'],
                       relief='flat')
        
        # Sidebar style
        style.configure('Sidebar.TFrame',
                       background=cls.COLORS['bg_secondary'],
                       relief='flat')
        
        # Modern button style
        style.configure('Modern.TButton',
                       background=cls.COLORS['button_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       font=cls.FONTS['button'])
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['button_hover']),
                           ('pressed', cls.COLORS['button_active'])])
        
        # Primary button style
        style.configure('Primary.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       font=cls.FONTS['button'])
        
        style.map('Primary.TButton',
                 background=[('active', cls.COLORS['button_active']),
                           ('pressed', '#3c45a3')])
        
        # Success button style
        style.configure('Success.TButton',
                       background=cls.COLORS['accent_success'],
                       foreground=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       font=cls.FONTS['button'])
        
        # Danger button style
        style.configure('Danger.TButton',
                       background=cls.COLORS['accent_danger'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       font=cls.FONTS['button'])
        
        # Entry style
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['input_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=cls.COLORS['text_primary'])
        
        style.map('Modern.TEntry',
                 focuscolor=[('focus', cls.COLORS['input_focus'])])
        
        # Label styles
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading_medium'])
        
        style.configure('Body.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body_medium'])
        
        style.configure('Muted.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_muted'],
                       font=cls.FONTS['body_small'])
        
        # Sidebar label styles
        style.configure('SidebarHeading.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading_small'])
        
        style.configure('SidebarBody.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body_medium'])
        
        # Progressbar style
        style.configure('Modern.Horizontal.TProgressbar',
                       background=cls.COLORS['accent_primary'],
                       troughcolor=cls.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['accent_primary'],
                       darkcolor=cls.COLORS['accent_primary'])

    @classmethod
    def create_card_frame(cls, parent, **kwargs):
        """Create a modern card-style frame"""
        frame = tk.Frame(parent,
                        bg=cls.COLORS['bg_card'],
                        relief='flat',
                        bd=0,
                        **kwargs)
        return frame
    
    @classmethod
    def create_gradient_frame(cls, parent, color1, color2, height=60):
        """Create a frame with gradient-like effect using Canvas"""
        canvas = tk.Canvas(parent, height=height, highlightthickness=0)
        canvas.configure(bg=color1)
        
        # Simple gradient simulation
        for i in range(height):
            ratio = i / height
            # Simple color interpolation
            canvas.create_line(0, i, 1000, i, fill=cls._interpolate_color(color1, color2, ratio))
        
        return canvas
    
    @classmethod
    def _interpolate_color(cls, color1, color2, ratio):
        """Simple color interpolation"""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        interpolated = tuple(rgb1[i] + (rgb2[i] - rgb1[i]) * ratio for i in range(3))
        return rgb_to_hex(interpolated)

class ModernComponents:
    """Modern UI components with consistent styling"""
    
    @staticmethod
    def create_icon_button(parent, text, command=None, icon=None, style='Modern.TButton'):
        """Create a modern icon button"""
        button = ttk.Button(parent, text=text, command=command, style=style)
        return button
    
    @staticmethod
    def create_status_indicator(parent, status='offline'):
        """Create a colored status indicator"""
        colors = {
            'online': ModernTheme.COLORS['online'],
            'idle': ModernTheme.COLORS['idle'],
            'dnd': ModernTheme.COLORS['accent_danger'],
            'offline': ModernTheme.COLORS['offline']
        }
        
        indicator = tk.Frame(parent, 
                           bg=colors.get(status, colors['offline']),
                           width=12, height=12,
                           relief='flat')
        indicator.pack_propagate(False)
        return indicator
    
    @staticmethod
    def create_modern_scrollbar(parent, orient='vertical'):
        """Create a modern styled scrollbar"""
        scrollbar = ttk.Scrollbar(parent, orient=orient)
        
        # Style the scrollbar
        style = ttk.Style()
        style.configure('Modern.Vertical.TScrollbar',
                       background=ModernTheme.COLORS['bg_tertiary'],
                       troughcolor=ModernTheme.COLORS['bg_secondary'],
                       borderwidth=0,
                       arrowcolor=ModernTheme.COLORS['text_muted'],
                       darkcolor=ModernTheme.COLORS['bg_tertiary'],
                       lightcolor=ModernTheme.COLORS['bg_tertiary'])
        
        scrollbar.configure(style='Modern.Vertical.TScrollbar')
        return scrollbar
    
    @staticmethod
    def create_notification_banner(parent, message, type='info'):
        """Create a notification banner"""
        colors = {
            'info': ModernTheme.COLORS['accent_primary'],
            'success': ModernTheme.COLORS['accent_success'],
            'warning': ModernTheme.COLORS['accent_warning'],
            'error': ModernTheme.COLORS['accent_danger']
        }
        
        banner = tk.Frame(parent,
                         bg=colors.get(type, colors['info']),
                         height=40,
                         relief='flat')
        
        label = tk.Label(banner,
                        text=message,
                        bg=colors.get(type, colors['info']),
                        fg=ModernTheme.COLORS['text_primary'],
                        font=ModernTheme.FONTS['body_medium'])
        label.pack(pady=10)
        
        return banner

# Emoji och ikoner för modern look
ICONS = {
    'voice': '🎤',
    'research': '🔬', 
    'memory': '🧠',
    'settings': '⚙️',
    'status_online': '🟢',
    'status_offline': '🔴',
    'status_idle': '🟡',
    'send': '📤',
    'stop': '⏹️',
    'play': '▶️',
    'pause': '⏸️',
    'robot': '🤖',
    'lightning': '⚡',
    'sparkles': '✨'
}
