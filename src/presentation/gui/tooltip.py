"""
Tooltip utility for enhanced user experience.
"""

import tkinter as tk
from typing import Optional


class ToolTip:
    """
    Create a tooltip for a given widget.
    """
    
    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.id: Optional[str] = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<ButtonPress>", self.on_leave)
    
    def on_enter(self, event=None):
        """Handle mouse enter event."""
        self.schedule_tooltip()
    
    def on_leave(self, event=None):
        """Handle mouse leave event."""
        self.cancel_tooltip()
        self.hide_tooltip()
    
    def schedule_tooltip(self):
        """Schedule tooltip to appear after delay."""
        self.cancel_tooltip()
        self.id = self.widget.after(self.delay, self.show_tooltip)
    
    def cancel_tooltip(self):
        """Cancel scheduled tooltip."""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
    
    def show_tooltip(self):
        """Show the tooltip."""
        if self.tooltip_window or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Style the tooltip
        self.tooltip_window.configure(bg="#2c3e50")
        
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify=tk.LEFT,
            background="#2c3e50",
            foreground="white",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 10),
            padx=8,
            pady=4
        )
        label.pack()
    
    def hide_tooltip(self):
        """Hide the tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def create_tooltip(widget: tk.Widget, text: str, delay: int = 500) -> ToolTip:
    """
    Create a tooltip for the given widget.
    
    Args:
        widget: The widget to attach the tooltip to
        text: The text to display in the tooltip
        delay: Delay in milliseconds before showing tooltip
        
    Returns:
        ToolTip instance
    """
    return ToolTip(widget, text, delay)
