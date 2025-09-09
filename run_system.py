#!/usr/bin/env python3
"""
PYSYSTEM - Profess        # Show welcome message
        root.after(1000, lambda: messagebox.showinfo(
            "PYSYSTEM",
            "🏢🐍 Welcome to PYSYSTEM\n\n"
            "Professional Business Management Features:\n"
            "• 👥 Company Management (CRUD + CNPJ Validation)\n"
            "• 📦 Product Catalog (Excel Import)\n" 
            "• 📊 Sales Order Processing\n"
            "• 🌐 BrasilAPI Address Integration\n"
            "• 📈 Business Analytics & Reports\n\n"
            "✨ Corporate design for professional environments\n"
            "🐍 Python-powered enterprise solution"
        ))ss Management System
Corporate launcher for the enterprise sales management system.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

def main():
    """Launch the corporate business management system."""
    try:
        # Configure system path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(current_dir, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import the corporate main window
        from src.presentation.gui.main_window import MainWindow
        
        # Create the main application window
        root = tk.Tk()
        root.title("PYSYSTEM - Professional Business Management")
        root.geometry("1200x800")
        root.minsize(1024, 768)
        
        # Configure for macOS visibility
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        
        # Center the window on screen
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        root.geometry(f"1200x800+{x}+{y}")
        
        # Initialize the corporate application
        app = MainWindow(root)
        
        # Show welcome message
        root.after(1000, lambda: messagebox.showinfo(
            "Business Management System",
            "🏢 Welcome to Business Management System\n\n"
            "Enterprise Features Available:\n"
            "• 👥 Company Management\n"
            "• 📦 Product Catalog\n" 
            "• 📊 Sales Order Processing\n"
            "• � Business Analytics\n"
            "• � Professional Reports\n\n"
            "Designed for professional business environments."
        ))
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        error_msg = f"❌ PYSYSTEM Error: {str(e)}"
        print(error_msg)
        
        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("PYSYSTEM Error", 
                               f"Failed to launch PYSYSTEM:\n\n{error_msg}")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    print("🏢🐍 Starting PYSYSTEM - Professional Business Management System...")
    main()
