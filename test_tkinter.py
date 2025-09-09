#!/usr/bin/env python3
"""
Simple test to check if tkinter works correctly.
"""

import tkinter as tk
from tkinter import ttk

def test_tkinter():
    """Test basic tkinter functionality."""
    try:
        print("Creating root window...")
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("400x300")
        
        print("Adding label...")
        label = ttk.Label(root, text="Hello, World! Tkinter is working!")
        label.pack(pady=50)
        
        print("Adding button...")
        def close_app():
            print("Closing application...")
            root.quit()
        
        button = ttk.Button(root, text="Close", command=close_app)
        button.pack(pady=20)
        
        print("Starting mainloop...")
        root.mainloop()
        print("Application finished.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tkinter()
