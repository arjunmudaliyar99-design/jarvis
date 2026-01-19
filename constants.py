"""
JARVIS HUD Constants - Colors, Fonts, and Configuration
"""

# Colors - Iron Man / JARVIS theme
COLORS = {
    'bg_dark': '#0b0f14',           # Main background
    'bg_panel': '#151a21',          # Panel background
    'cyan_primary': '#00e5ff',      # Primary neon cyan
    'cyan_accent': '#00bcd4',       # Secondary cyan
    'blue_glow': '#0099ff',         # Blue glow
    'white': '#ffffff',             # White text
    'white_dim': '#b0bec5',         # Dimmed white
    'gray_dark': '#1e2830',         # Dark gray
    'success': '#00ff88',           # Success green
    'warning': '#ffaa00',           # Warning orange
    'error': '#ff3366',             # Error red
    'listening': '#00ff00',         # Listening indicator
    'processing': '#ffaa00',        # Processing indicator
    'speaking': '#00aaff',          # Speaking indicator
}

# Font Configuration
FONTS = {
    'title': ('Orbitron', 28, 'bold'),
    'subtitle': ('Orbitron', 16, 'normal'),
    'body': ('Consolas', 12, 'normal'),
    'small': ('Consolas', 10, 'normal'),
    'digital': ('Courier New', 14, 'bold'),
}

# HUD Dimensions
HUD = {
    'center_radius': 150,           # Main circle radius
    'ring1_radius': 180,            # Inner ring
    'ring2_radius': 210,            # Middle ring
    'ring3_radius': 240,            # Outer ring
    'animation_speed': 1.0,         # Rotation speed
    'pulse_speed': 0.1,             # Pulse animation speed
}

# Panel Dimensions
PANELS = {
    'left_width': 300,
    'right_width': 300,
    'padding': 20,
}

# Voice Settings
VOICE = {
    'rate': 170,                    # Speech rate (words per minute)
    'volume': 0.9,                  # Volume (0.0 to 1.0)
    'voice_gender': 'male',         # Preferred voice gender
    'energy_threshold': 3000,       # Microphone sensitivity (lower = more sensitive)
    'pause_threshold': 0.8,         # Pause detection (seconds)
}

# App Shortcuts
APPS = [
    {'name': 'Browser', 'icon': '🌐', 'command': 'start chrome'},
    {'name': 'Music', 'icon': '🎵', 'command': 'start wmplayer'},
    {'name': 'Files', 'icon': '📁', 'command': 'start explorer'},
    {'name': 'YouTube', 'icon': '▶️', 'command': 'start https://youtube.com'},
    {'name': 'Wikipedia', 'icon': '📖', 'command': 'start https://wikipedia.org'},
    {'name': 'Calculator', 'icon': '🔢', 'command': 'calc'},
    {'name': 'Notepad', 'icon': '📝', 'command': 'notepad'},
    {'name': 'Terminal', 'icon': '⚡', 'command': 'start cmd'},
]

# Animation Constants
ANIMATION = {
    'fps': 60,                      # Frames per second
    'rotation_speed': 0.5,          # Degrees per frame
    'pulse_min': 0.7,               # Minimum pulse opacity
    'pulse_max': 1.0,               # Maximum pulse opacity
}
