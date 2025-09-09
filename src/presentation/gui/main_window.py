"""
Main window for the Sales Management System.
Corporate and professional design.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import os

# Import dependency injection setup
from .dependency_injection import DependencyContainer

# Import frame classes  
from .company_management_frame import CompanyManagementFrame
from .product_management_frame import ProductManagementFrame
from .sales_order_frame import SalesOrderFrame

# Import corporate theme
from .corporate_theme import (
    get_corporate_theme, 
    get_corporate_font,
    get_corporate_button_style,
    get_corporate_icon,
    CORPORATE_LAYOUT
)


class MainWindow:
    """Main application window with corporate design."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the main window with corporate styling."""
        self.root = root
        self.theme = get_corporate_theme()
        
        # Configure window
        self._configure_window()
        
        # Initialize dependency injection
        self._setup_dependencies()
        
        # Setup corporate GUI
        self._setup_gui()
        self._create_menu()
        self._update_status_bar()
        
        # Auto-update status bar every 10 seconds
        self._schedule_status_update()
    
    def _configure_window(self):
        """Configure the main window with corporate styling."""
        self.root.title("PYSYSTEM - Business Management System")
        self.root.geometry("1200x800")
        self.root.minsize(CORPORATE_LAYOUT['window_min_width'], CORPORATE_LAYOUT['window_min_height'])
        self.root.configure(bg=self.theme['background'])
        self.root.configure(bg=self.theme['background'])
        
                # Set custom business icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'business_icon.xbm')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Ignore icon errors
    
    def _setup_dependencies(self):
        """Setup dependency injection container."""
        self.container = DependencyContainer()
        self.company_controller = self.container.get_company_controller()
        self.product_controller = self.container.get_product_controller()
        self.sales_order_controller = self.container.get_sales_order_controller()
    
    def _setup_gui(self):
        """Setup the corporate GUI components."""
        # Create main container
        main_container = tk.Frame(self.root, bg=self.theme['background'])
        main_container.pack(fill='both', expand=True, padx=CORPORATE_LAYOUT['default_padding'], 
                           pady=CORPORATE_LAYOUT['default_padding'])
        
        # Configure corporate TTK styles
        self._configure_corporate_styles()
        
        # Create corporate header
        self._create_corporate_header(main_container)
        
        # Create main content area
        self._create_content_area(main_container)
        
        # Create corporate status bar
        self._create_corporate_status_bar(main_container)
    
    def _configure_corporate_styles(self):
        """Configure corporate TTK styles."""
        style = ttk.Style()
        
        # Configure corporate frame styles
        style.configure('Corporate.TFrame', 
                       background=self.theme['background'])
        
        style.configure('Header.TFrame',
                       background=self.theme['primary'])
        
        # Configure corporate notebook style
        style.configure('Corporate.TNotebook', 
                       background=self.theme['background'],
                       borderwidth=0)
        
        style.configure('Corporate.TNotebook.Tab',
                       background=self.theme['surface'],
                       foreground=self.theme['text_primary'],
                       padding=[25, 12],
                       font=get_corporate_font('button'))
        
        style.map('Corporate.TNotebook.Tab',
                 background=[('selected', self.theme['primary']),
                           ('active', self.theme['primary_light'])],
                 foreground=[('selected', self.theme['text_inverse']),
                           ('active', self.theme['text_inverse'])])
        
        # Configure corporate button styles
        for btn_type, btn_style in [
            ('Primary', get_corporate_button_style('primary')),
            ('Secondary', get_corporate_button_style('secondary')),
            ('Success', get_corporate_button_style('success')),
            ('Warning', get_corporate_button_style('warning')),
            ('Error', get_corporate_button_style('error'))
        ]:
            style.configure(f'{btn_type}.TButton',
                           background=btn_style['bg'],
                           foreground=btn_style['fg'],
                           font=get_corporate_font('button'),
                           borderwidth=1,
                           relief='flat',
                           padding=CORPORATE_LAYOUT['button_padding'])
            
            style.map(f'{btn_type}.TButton',
                     background=[('active', btn_style['active_bg']),
                               ('pressed', btn_style['border'])],
                     foreground=[('active', btn_style['active_fg'])])
    
    def _create_corporate_header(self, parent):
        """Create professional corporate header."""
        header_frame = tk.Frame(parent, 
                               bg=self.theme['primary'],
                               height=90)
        header_frame.pack(fill='x', pady=(0, CORPORATE_LAYOUT['section_padding']))
        header_frame.pack_propagate(False)
        
        # Company logo/icon area
        logo_frame = tk.Frame(header_frame, bg=self.theme['primary'])
        logo_frame.pack(side='left', fill='y', padx=(20, 0))
        
        # Corporate icon
        logo_label = tk.Label(logo_frame,
                             text=get_corporate_icon('building'),
                             font=('Segoe UI', 32),
                             fg=self.theme['text_inverse'],
                             bg=self.theme['primary'])
        logo_label.pack(pady=15)
        
        # Title area
        title_frame = tk.Frame(header_frame, bg=self.theme['primary'])
        title_frame.pack(side='left', fill='both', expand=True, padx=(20, 20))
        
        # Main title
        title_label = tk.Label(title_frame,
                              text="Business Management System",
                              font=get_corporate_font('title'),
                              fg=self.theme['text_inverse'],
                              bg=self.theme['primary'])
        title_label.pack(anchor='w', pady=(12, 0))
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Enterprise Solution for Sales and Inventory Management",
                                 font=get_corporate_font('subtitle'),
                                 fg=self.theme['secondary_light'],
                                 bg=self.theme['primary'])
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # User info area (placeholder for future user management)
        user_frame = tk.Frame(header_frame, bg=self.theme['primary'])
        user_frame.pack(side='right', fill='y', padx=(0, 20))
        
        user_icon = tk.Label(user_frame,
                            text=get_corporate_icon('profile'),
                            font=('Segoe UI', 20),
                            fg=self.theme['text_inverse'],
                            bg=self.theme['primary'])
        user_icon.pack(pady=(20, 5))
        
        user_label = tk.Label(user_frame,
                             text="Administrator",
                             font=get_corporate_font('small'),
                             fg=self.theme['secondary_light'],
                             bg=self.theme['primary'])
        user_label.pack()
    
    def _create_content_area(self, parent):
        """Create the main content area with notebook."""
        content_frame = tk.Frame(parent, bg=self.theme['background'])
        content_frame.pack(fill='both', expand=True, pady=(0, CORPORATE_LAYOUT['section_padding']))
        
        # Create corporate notebook
        self.notebook = ttk.Notebook(content_frame, style='Corporate.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create management tabs
        self._create_management_tabs()
    
    def _create_management_tabs(self):
        """Create the management tabs with corporate styling."""
        # Company Management tab
        self.company_frame = CompanyManagementFrame(
            self.notebook,
            self.company_controller
        )
        self.notebook.add(self.company_frame.frame, 
                         text=f"{get_corporate_icon('company')} Companies")
        
        # Product Management tab
        self.product_frame = ProductManagementFrame(
            self.notebook,
            self.product_controller
        )
        self.notebook.add(self.product_frame.frame,
                         text=f"{get_corporate_icon('product')} Products")
        
        # Sales Order Management tab
        self.sales_order_frame = SalesOrderFrame(
            self.notebook,
            self.sales_order_controller,
            self.company_controller,
            self.product_controller
        )
        self.notebook.add(self.sales_order_frame.frame,
                         text=f"{get_corporate_icon('orders')} Sales Orders")
    
    def _create_corporate_status_bar(self, parent):
        """Create professional corporate status bar."""
        status_container = tk.Frame(parent, bg=self.theme['background'])
        status_container.pack(fill='x', side='bottom')
        
        # Status bar background
        status_frame = tk.Frame(status_container, 
                               bg=self.theme['primary'],
                               height=50)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        # Left section - Business metrics
        left_section = tk.Frame(status_frame, bg=self.theme['primary'])
        left_section.pack(side='left', fill='y', padx=(20, 0))
        
        # Companies count
        self.companies_count_label = tk.Label(
            left_section,
            text=f"{get_corporate_icon('company')} 0 Companies",
            fg=self.theme['text_inverse'],
            bg=self.theme['primary'],
            font=get_corporate_font('body_bold')
        )
        self.companies_count_label.pack(side='left', padx=(0, 30), pady=15)
        
        # Products count
        self.products_count_label = tk.Label(
            left_section,
            text=f"{get_corporate_icon('product')} 0 Products",
            fg=self.theme['text_inverse'],
            bg=self.theme['primary'],
            font=get_corporate_font('body_bold')
        )
        self.products_count_label.pack(side='left', padx=(0, 30), pady=15)
        
        # Orders count
        self.orders_count_label = tk.Label(
            left_section,
            text=f"{get_corporate_icon('orders')} 0 Orders",
            fg=self.theme['text_inverse'],
            bg=self.theme['primary'],
            font=get_corporate_font('body_bold')
        )
        self.orders_count_label.pack(side='left', padx=(0, 30), pady=15)
        
        # Revenue section
        self.revenue_label = tk.Label(
            left_section,
            text=f"{get_corporate_icon('revenue')} $0.00 Total",
            fg=self.theme['success_light'],
            bg=self.theme['primary'],
            font=get_corporate_font('body_bold')
        )
        self.revenue_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Right section - System info
        right_section = tk.Frame(status_frame, bg=self.theme['primary'])
        right_section.pack(side='right', fill='y', padx=(0, 20))
        
        # System status
        self.system_status_label = tk.Label(
            right_section,
            text=f"{get_corporate_icon('success')} System Active",
            fg=self.theme['success_light'],
            bg=self.theme['primary'],
            font=get_corporate_font('body')
        )
        self.system_status_label.pack(side='right', pady=15)
    
    def _create_menu(self):
        """Create professional application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit_application)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh All", command=self._refresh_all)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="System Report", command=self._show_system_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _update_status_bar(self):
        """Update status bar with current business metrics."""
        try:
            # Get business metrics
            companies_count = len(self.company_controller.list_companies())
            products_count = len(self.product_controller.list_products())
            
            success, orders, error = self.sales_order_controller.list_sales_orders()
            orders_count = len(orders) if success else 0
            
            # Calculate total revenue
            total_revenue = 0.0
            if success and orders:
                total_revenue = sum(float(order.total_amount) for order in orders)
            
            # Update labels with corporate styling
            self.companies_count_label.config(
                text=f"{get_corporate_icon('company')} {companies_count} Companies"
            )
            self.products_count_label.config(
                text=f"{get_corporate_icon('product')} {products_count} Products"
            )
            self.orders_count_label.config(
                text=f"{get_corporate_icon('orders')} {orders_count} Orders"
            )
            self.revenue_label.config(
                text=f"{get_corporate_icon('revenue')} ${total_revenue:,.2f} Revenue"
            )
            
        except Exception as e:
            print(f"Error updating status bar: {e}")
    
    def _schedule_status_update(self):
        """Schedule automatic status bar updates."""
        self._update_status_bar()
        self.root.after(10000, self._schedule_status_update)  # Update every 10 seconds
    
    def _refresh_all(self):
        """Refresh all data in the application."""
        try:
            # Refresh each frame
            if hasattr(self.company_frame, 'refresh'):
                self.company_frame.refresh()
            if hasattr(self.product_frame, 'refresh'):
                self.product_frame.refresh()
            if hasattr(self.sales_order_frame, 'refresh'):
                self.sales_order_frame.refresh()
                
            # Update status bar
            self._update_status_bar()
            
            messagebox.showinfo("Refresh Complete", 
                               f"{get_corporate_icon('success')} All data has been refreshed successfully!")
            
        except Exception as e:
            messagebox.showerror("Refresh Error", 
                               f"{get_corporate_icon('error')} Error refreshing data: {str(e)}")
    
    def _show_system_report(self):
        """Show system report with business metrics."""
        try:
            companies_count = len(self.company_controller.list_companies())
            products_count = len(self.product_controller.list_products())
            
            success, orders, error = self.sales_order_controller.list_sales_orders()
            orders_count = len(orders) if success else 0
            total_revenue = sum(float(order.total_amount) for order in orders) if success and orders else 0
            
            report_text = f"""
BUSINESS MANAGEMENT SYSTEM REPORT
{'='*50}

{get_corporate_icon('company')} Company Management:
   • Total Companies: {companies_count}
   
{get_corporate_icon('product')} Inventory Management:
   • Total Products: {products_count}
   
{get_corporate_icon('orders')} Sales Performance:
   • Total Orders: {orders_count}
   • Total Revenue: ${total_revenue:,.2f}
   
{get_corporate_icon('analytics')} System Status:
   • Status: Active
   • Architecture: Clean Architecture
   • Database: JSON-based persistence
            """
            
            # Create report window
            report_window = tk.Toplevel(self.root)
            report_window.title("System Report")
            report_window.geometry("600x500")
            report_window.configure(bg=self.theme['background'])
            report_window.transient(self.root)
            report_window.grab_set()
            
            # Header
            header_frame = tk.Frame(report_window, bg=self.theme['primary'], height=60)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            header_label = tk.Label(header_frame,
                                   text=f"{get_corporate_icon('analytics')} System Report",
                                   font=get_corporate_font('header'),
                                   fg=self.theme['text_inverse'],
                                   bg=self.theme['primary'])
            header_label.pack(pady=15)
            
            # Content
            content_frame = tk.Frame(report_window, bg=self.theme['background'])
            content_frame.pack(fill='both', expand=True, padx=30, pady=30)
            
            text_widget = tk.Text(content_frame,
                                 wrap=tk.WORD,
                                 font=get_corporate_font('body'),
                                 bg=self.theme['surface'],
                                 fg=self.theme['text_primary'],
                                 relief='flat',
                                 padx=15,
                                 pady=15)
            text_widget.pack(fill='both', expand=True)
            text_widget.insert('1.0', report_text)
            text_widget.config(state='disabled')
            
            # Close button
            close_button = tk.Button(content_frame,
                                   text=f"{get_corporate_icon('check')} Close",
                                   command=report_window.destroy,
                                   **get_corporate_button_style('primary'),
                                   font=get_corporate_font('button'),
                                   relief='flat',
                                   padx=20,
                                   pady=8)
            close_button.pack(pady=(20, 0))
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Error generating report: {str(e)}")
    
    def _show_about(self):
        """Show professional about dialog."""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("600x500")
        about_window.resizable(False, False)
        about_window.configure(bg=self.theme['background'])
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Header
        header_frame = tk.Frame(about_window, bg=self.theme['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo and title
        logo_title_frame = tk.Frame(header_frame, bg=self.theme['primary'])
        logo_title_frame.pack(expand=True)
        
        logo_label = tk.Label(logo_title_frame,
                             text=get_corporate_icon('building'),
                             font=('Segoe UI', 32),
                             fg=self.theme['text_inverse'],
                             bg=self.theme['primary'])
        logo_label.pack(pady=(15, 5))
        
        title_label = tk.Label(logo_title_frame,
                              text="Business Management System",
                              font=get_corporate_font('header'),
                              fg=self.theme['text_inverse'],
                              bg=self.theme['primary'])
        title_label.pack()
        
        # Content
        content_frame = tk.Frame(about_window, bg=self.theme['background'])
        content_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        info_text = f"""
{get_corporate_icon('info')} Version: 1.0.0 Enterprise
        
{get_corporate_icon('building')} Architecture: Clean Architecture Pattern
{get_corporate_icon('settings')} Technology Stack: Python, Tkinter
        
{get_corporate_icon('success')} Key Features:
• Enterprise Company Management with validation
• Advanced Product Catalog with inventory control
• Professional Sales Order Processing
• Automated PDF Report Generation
• Address lookup via BrasilAPI integration

{get_corporate_icon('profile')} Designed for professional business environments
with emphasis on reliability, scalability, and user experience.

{get_corporate_icon('check')} Built with enterprise-grade coding standards
following SOLID principles and best practices.
        """
        
        info_label = tk.Label(content_frame,
                             text=info_text,
                             font=get_corporate_font('body'),
                             fg=self.theme['text_primary'],
                             bg=self.theme['background'],
                             justify='left',
                             wraplength=500)
        info_label.pack()
        
        # Close button
        close_button = tk.Button(content_frame,
                               text=f"{get_corporate_icon('check')} Close",
                               command=about_window.destroy,
                               **get_corporate_button_style('primary'),
                               font=get_corporate_font('button'),
                               relief='flat',
                               padx=25,
                               pady=10)
        close_button.pack(pady=(30, 0))
    
    def _quit_application(self):
        """Quit the application safely with confirmation."""
        if messagebox.askyesno("Exit Application", 
                              f"{get_corporate_icon('help')} Are you sure you want to exit the Business Management System?"):
            self.root.quit()
