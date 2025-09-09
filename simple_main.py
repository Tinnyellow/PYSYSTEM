#!/usr/bin/env python3
"""
Simple Sales Management System - Basic Version
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main application entry point."""
    try:
        print("Starting Sales Management System...")
        
        # Create root window
        root = tk.Tk()
        root.title("Sales Management System")
        root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Sales Management System", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Companies tab
        companies_frame = ttk.Frame(notebook, padding="10")
        notebook.add(companies_frame, text="Companies")
        
        ttk.Label(companies_frame, text="Company Management", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(companies_frame, text="This tab will contain company CRUD operations.").pack()
        
        # Products tab
        products_frame = ttk.Frame(notebook, padding="10")
        notebook.add(products_frame, text="Products")
        
        ttk.Label(products_frame, text="Product Management", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(products_frame, text="This tab will contain product management and Excel import.").pack()
        
        # Sales Orders tab
        orders_frame = ttk.Frame(notebook, padding="10")
        notebook.add(orders_frame, text="Sales Orders")
        
        ttk.Label(orders_frame, text="Sales Order Management", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(orders_frame, text="This tab will contain sales order management and PDF reports.").pack()
        
        # Status bar
        status_frame = ttk.Frame(root)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        status_label = ttk.Label(status_frame, text="Ready - Clean Architecture Sales Management System v1.0")
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        print("GUI created successfully. Starting main loop...")
        
        # Start main loop
        root.mainloop()
        
        print("Application closed normally.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
