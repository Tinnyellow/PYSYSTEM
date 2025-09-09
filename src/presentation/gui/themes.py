"""
Theme configuration for the Sales Management System.
Modern color schemes and styling constants.
"""

# Modern Color Schemes
THEMES = {
    'default': {
        'primary': '#3498db',      # Modern Blue
        'secondary': '#95a5a6',    # Cool Gray
        'success': '#27ae60',      # Fresh Green
        'warning': '#f39c12',      # Vibrant Orange
        'danger': '#e74c3c',       # Clean Red
        'dark': '#2c3e50',         # Deep Blue
        'light': '#ecf0f1',        # Clean White
        'accent': '#9b59b6',       # Purple
        'info': '#17a2b8',         # Teal
        'muted': '#6c757d'         # Muted Gray
    },
    'dark': {
        'primary': '#007bff',
        'secondary': '#6c757d',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'dark': '#343a40',
        'light': '#f8f9fa',
        'accent': '#6f42c1',
        'info': '#17a2b8',
        'muted': '#6c757d'
    }
}

# Font Configuration
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'subtitle': ('Segoe UI', 16, 'normal'),
    'header': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11, 'normal'),
    'small': ('Segoe UI', 9, 'normal'),
    'button': ('Segoe UI', 10, 'bold'),
    'code': ('Consolas', 10, 'normal')
}

# Button Styles
BUTTON_STYLES = {
    'primary': {
        'bg': THEMES['default']['primary'],
        'fg': 'white',
        'active_bg': '#2980b9',
        'active_fg': 'white'
    },
    'success': {
        'bg': THEMES['default']['success'],
        'fg': 'white',
        'active_bg': '#229954',
        'active_fg': 'white'
    },
    'warning': {
        'bg': THEMES['default']['warning'],
        'fg': 'white',
        'active_bg': '#e67e22',
        'active_fg': 'white'
    },
    'danger': {
        'bg': THEMES['default']['danger'],
        'fg': 'white',
        'active_bg': '#c0392b',
        'active_fg': 'white'
    },
    'secondary': {
        'bg': THEMES['default']['secondary'],
        'fg': 'white',
        'active_bg': '#7f8c8d',
        'active_fg': 'white'
    }
}

# Icon mappings
ICONS = {
    'save': '💾',
    'edit': '✏️',
    'delete': '🗑️',
    'add': '➕',
    'refresh': '🔄',
    'cancel': '❌',
    'clear': '🧹',
    'company': '🏢',
    'product': '📦',
    'order': '📋',
    'money': '💰',
    'user': '👤',
    'settings': '⚙️',
    'help': '❓',
    'info': 'ℹ️',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'search': '🔍'
}

def get_theme(theme_name='default'):
    """Get theme configuration."""
    return THEMES.get(theme_name, THEMES['default'])

def get_button_style(style_name):
    """Get button style configuration."""
    return BUTTON_STYLES.get(style_name, BUTTON_STYLES['primary'])

def get_icon(icon_name):
    """Get icon for given name."""
    return ICONS.get(icon_name, '')
