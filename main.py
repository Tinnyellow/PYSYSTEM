"""
Main application entry point for the Sales Management System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.gui.main_window import MainWindow
from src.shared.utils.config import config


def setup_directories():
    """Setup required directories for the application."""
    directories = [
        'data',
        'data/reports',
        'config'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")


def main():
    """Main application entry point."""
    try:
        print("Starting Sales Management System...")
        
        # Setup directories
        print("Setting up directories...")
        setup_directories()
        
        # Create root window
        print("Creating root window...")
        root = tk.Tk()
        
        # Configure window
        root.withdraw()  # Hide initially
        
        # Set window properties
        root.title("Sales Management System")
        root.geometry("1200x800")
        root.minsize(800, 600)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main window
        print("Creating main window...")
        app = MainWindow(root)
        
        # Show window
        print("Showing window...")
        root.deiconify()
        root.lift()  # Bring window to front
        root.focus_force()  # Force focus
        
        print("Starting main loop...")
        # Start main loop
        root.mainloop()
        
        print("Application closed normally.")
        
    except ImportError as e:
        print(f"Import error: {e}")
        messagebox.showerror(
            "Import Error",
            f"Failed to import required modules:\n{str(e)}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror(
            "Application Error",
            f"An unexpected error occurred:\n{str(e)}"
        )
        sys.exit(1)
