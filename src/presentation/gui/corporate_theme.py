"""
Corporate Theme Configuration for the Sales Management System.
Professional and sophisticated styling for enterprise applications.
"""

# Corporate Color Scheme - Professional & Neutral
CORPORATE_THEME = {
    # Primary colors - Professional blues and grays
    'primary': '#2c3e50',          # Deep slate blue
    'primary_light': '#34495e',    # Lighter slate
    'primary_dark': '#1a252f',     # Darker slate
    
    # Secondary colors - Neutral grays
    'secondary': '#95a5a6',        # Silver gray
    'secondary_light': '#bdc3c7',  # Light gray
    'secondary_dark': '#7f8c8d',   # Dark gray
    
    # Background colors - Clean whites and light grays
    'background': '#ffffff',       # Pure white
    'background_alt': '#f8f9fa',   # Very light gray
    'surface': '#ecf0f1',         # Light surface
    
    # Text colors - Professional contrast
    'text_primary': '#2c3e50',     # Dark text
    'text_secondary': '#5a6c7d',   # Medium text
    'text_muted': '#95a5a6',       # Light text
    'text_inverse': '#ffffff',     # White text
    
    # Status colors - Corporate appropriate
    'success': '#27ae60',          # Professional green
    'success_light': '#2ecc71',    # Lighter green
    'warning': '#f39c12',          # Professional orange
    'warning_light': '#f1c40f',    # Lighter orange
    'error': '#e74c3c',            # Professional red
    'error_light': '#ec7063',      # Lighter red
    'info': '#3498db',             # Professional blue
    'info_light': '#5dade2',       # Lighter blue
    
    # Accent colors - Sophisticated highlights
    'accent': '#8e44ad',           # Professional purple
    'accent_light': '#a569bd',     # Lighter purple
    
    # Border and shadow colors
    'border': '#dee2e6',           # Light border
    'border_dark': '#adb5bd',      # Darker border
    'shadow': 'rgba(0,0,0,0.1)',   # Subtle shadow
    'shadow_strong': 'rgba(0,0,0,0.2)'  # Stronger shadow
}

# Corporate Typography
CORPORATE_FONTS = {
    'title': ('Segoe UI', 28, 'bold'),      # Large titles
    'subtitle': ('Segoe UI', 18, 'normal'),  # Subtitles
    'header': ('Segoe UI', 16, 'bold'),      # Section headers
    'body': ('Segoe UI', 11, 'normal'),      # Body text
    'body_bold': ('Segoe UI', 11, 'bold'),   # Bold body text
    'small': ('Segoe UI', 9, 'normal'),      # Small text
    'button': ('Segoe UI', 10, 'bold'),      # Button text
    'menu': ('Segoe UI', 10, 'normal'),      # Menu text
    'code': ('Consolas', 10, 'normal')       # Code/monospace
}

# Corporate Button Styles
CORPORATE_BUTTONS = {
    'primary': {
        'bg': CORPORATE_THEME['primary'],
        'fg': CORPORATE_THEME['text_inverse'],
        'active_bg': CORPORATE_THEME['primary_dark'],
        'active_fg': CORPORATE_THEME['text_inverse'],
        'border': CORPORATE_THEME['primary_dark']
    },
    'secondary': {
        'bg': CORPORATE_THEME['secondary'],
        'fg': CORPORATE_THEME['text_inverse'],
        'active_bg': CORPORATE_THEME['secondary_dark'],
        'active_fg': CORPORATE_THEME['text_inverse'],
        'border': CORPORATE_THEME['secondary_dark']
    },
    'success': {
        'bg': CORPORATE_THEME['success'],
        'fg': CORPORATE_THEME['text_inverse'],
        'active_bg': CORPORATE_THEME['success_light'],
        'active_fg': CORPORATE_THEME['text_inverse'],
        'border': CORPORATE_THEME['success']
    },
    'warning': {
        'bg': CORPORATE_THEME['warning'],
        'fg': CORPORATE_THEME['text_inverse'],
        'active_bg': CORPORATE_THEME['warning_light'],
        'active_fg': CORPORATE_THEME['text_inverse'],
        'border': CORPORATE_THEME['warning']
    },
    'error': {
        'bg': CORPORATE_THEME['error'],
        'fg': CORPORATE_THEME['text_inverse'],
        'active_bg': CORPORATE_THEME['error_light'],
        'active_fg': CORPORATE_THEME['text_inverse'],
        'border': CORPORATE_THEME['error']
    }
}

# Professional Icons - Corporate appropriate
CORPORATE_ICONS = {
    'company': '🏢',
    'building': '🏬', 
    'office': '🏪',
    'product': '📦',
    'inventory': '📋',
    'order': '📄',
    'orders': '📊',
    'sales': '💼',
    'money': '💰',
    'revenue': '📈',
    'save': '💾',
    'edit': '✏️',
    'delete': '🗑️',
    'add': '➕',
    'new': '🆕',
    'refresh': '🔄',
    'search': '🔍',
    'filter': '🔽',
    'export': '📤',
    'import': '📥',
    'print': '🖨️',
    'pdf': '📄',
    'excel': '📊',
    'report': '📋',
    'analytics': '📈',
    'dashboard': '🎯',
    'settings': '⚙️',
    'user': '👤',
    'users': '👥',
    'profile': '👨‍💼',
    'help': '❓',
    'info': 'ℹ️',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'check': '✓',
    'close': '❌',
    'cancel': '🚫',
    'confirm': '✅',
    'clear': '🧹',
    'pysystem': '🏢🐍',  # PYSYSTEM corporate icon
    'system': '⚡',      # System icon
    'database': '💾',    # Database icon
    'api': '🌐'          # API icon
}

def get_corporate_theme():
    """Get the corporate theme configuration."""
    return CORPORATE_THEME

def get_corporate_font(font_type='body'):
    """Get corporate font configuration."""
    return CORPORATE_FONTS.get(font_type, CORPORATE_FONTS['body'])

def get_corporate_button_style(style_name='primary'):
    """Get corporate button style configuration."""
    return CORPORATE_BUTTONS.get(style_name, CORPORATE_BUTTONS['primary'])

def get_corporate_icon(icon_name):
    """Get corporate-appropriate icon."""
    return CORPORATE_ICONS.get(icon_name, '•')

# Window and Layout Constants
CORPORATE_LAYOUT = {
    'window_min_width': 1024,
    'window_min_height': 768,
    'default_padding': 15,
    'section_padding': 20,
    'button_padding': (20, 8),
    'frame_padding': 15,
    'border_width': 1,
    'corner_radius': 4  # For systems that support rounded corners
}
