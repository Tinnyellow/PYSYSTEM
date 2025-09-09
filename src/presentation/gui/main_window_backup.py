"""
Main window for the Sales Management System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Import dependency injection setup
from .dependency_injection import DependencyContainer

# Import frame classes
from .company_management_frame import CompanyManagementFrame
from .product_management_frame import ProductManagementFrame
from .sales_order_frame import SalesOrderFrame


class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the main window."""
        self.root = root
        self.root.title("Sales Management System")
        
        # Modern color scheme
        self.colors = {
            'primary': '#3498db',      # Blue
            'secondary': '#95a5a6',    # Light gray
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'danger': '#e74c3c',       # Red
            'dark': '#2c3e50',         # Dark blue
            'light': '#ecf0f1',        # Light gray
            'accent': '#9b59b6'        # Purple
        }
        
        # Configure root window style
        self.root.configure(bg=self.colors['light'])
        
        # Initialize dependency injection
        self._setup_dependencies()
        
        # Setup GUI
        self._setup_gui()
        self._create_menu()
        self._update_status_bar()
        
        # Auto-update status bar every 5 seconds
        self._schedule_status_update()
    
    def _setup_dependencies(self):
        """Setup dependency injection container."""
        self.container = DependencyContainer()
        self.company_controller = self.container.get_company_controller()
        self.product_controller = self.container.get_product_controller()
        self.sales_order_controller = self.container.get_sales_order_controller()
    
    def _setup_gui(self):
        """Setup the main GUI components."""
        # Create main frame with modern styling
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure ttk styles
        self._configure_styles()
        
        # Create header
        self._create_header(main_frame)
        
        # Create notebook for tabs
        self._create_notebook(main_frame)
        
        # Create status bar
        self._create_status_bar(main_frame)
    
    def _configure_styles(self):
        """Configure modern TTK styles."""
        style = ttk.Style()
        
        # Configure modern frame style
        style.configure('Modern.TFrame', background=self.colors['light'])
        
        # Configure modern notebook style
        style.configure('Modern.TNotebook', background=self.colors['light'])
        style.configure('Modern.TNotebook.Tab', 
                       padding=[20, 10], 
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
    
    def _create_header(self, parent):
        """Create modern header with title."""
        header_frame = tk.Frame(parent, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title label
        title_label = tk.Label(header_frame, 
                              text="🏢 Sistema de Gestão de Vendas",
                              font=('Segoe UI', 24, 'bold'),
                              fg='white',
                              bg=self.colors['dark'])
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Gerencie empresas, produtos e pedidos de forma eficiente",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['light'],
                                 bg=self.colors['dark'])
        subtitle_label.pack()
    
    def _create_notebook(self, parent):
        """Create the main notebook with tabs."""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Company Management tab
        self.company_frame = CompanyManagementFrame(
            self.notebook, 
            self.company_controller,
            self._update_status_bar
        )
        self.notebook.add(self.company_frame, text="👥 Empresas")
        
        # Product Management tab  
        self.product_frame = ProductManagementFrame(
            self.notebook, 
            self.product_controller,
            self._update_status_bar
        )
        self.notebook.add(self.product_frame, text="📦 Produtos")
        
        # Sales Order Management tab
        self.sales_order_frame = SalesOrderFrame(
            self.notebook,
            self.sales_order_controller,
            self.company_controller,
            self.product_controller,
            self._update_status_bar
        )
        self.notebook.add(self.sales_order_frame, text="📋 Pedidos")
    
    def _create_status_bar(self, parent):
        """Create modern status bar with counts."""
        status_frame = tk.Frame(parent, bg=self.colors['dark'], height=50)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # Left side - counts
        left_frame = tk.Frame(status_frame, bg=self.colors['dark'])
        left_frame.pack(side='left', fill='y', padx=20)
        
        # Companies count
        self.companies_count_label = tk.Label(left_frame,
                                             text="🏢 0 Empresas",
                                             fg=self.colors['primary'],
                                             bg=self.colors['dark'],
                                             font=('Segoe UI', 10, 'bold'))
        self.companies_count_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Products count  
        self.products_count_label = tk.Label(left_frame,
                                            text="📦 0 Produtos", 
                                            fg=self.colors['success'],
                                            bg=self.colors['dark'],
                                            font=('Segoe UI', 10, 'bold'))
        self.products_count_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Orders count
        self.orders_count_label = tk.Label(left_frame,
                                          text="📋 0 Pedidos",
                                          fg=self.colors['warning'], 
                                          bg=self.colors['dark'],
                                          font=('Segoe UI', 10, 'bold'))
        self.orders_count_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Total sales value
        self.total_sales_label = tk.Label(left_frame,
                                         text="💰 R$ 0,00",
                                         fg=self.colors['accent'],
                                         bg=self.colors['dark'],
                                         font=('Segoe UI', 10, 'bold'))
        self.total_sales_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Right side - system info
        right_frame = tk.Frame(status_frame, bg=self.colors['dark'])
        right_frame.pack(side='right', fill='y', padx=20)
        
        system_label = tk.Label(right_frame,
                               text="✅ Sistema Ativo",
                               fg=self.colors['success'],
                               bg=self.colors['dark'],
                               font=('Segoe UI', 10))
        system_label.pack(side='right', pady=15)
    
    def _create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self._quit_application)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Atualizar", command=self._refresh_all)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self._show_about)
    
    def _update_status_bar(self):
        """Update status bar with current counts and modern styling."""
        try:
            # Get counts
            companies_count = len(self.company_controller.list_companies())
            products_count = len(self.product_controller.list_products())
            
            success, orders, error = self.sales_order_controller.list_sales_orders()
            orders_count = len(orders) if success else 0
            
            # Calculate total sales value
            total_sales = 0.0
            if success and orders:
                total_sales = sum(float(order.total_amount) for order in orders)
            
            # Update labels with modern styling and emojis
            self.companies_count_label.config(text=f"🏢 {companies_count} Empresas")
            self.products_count_label.config(text=f"📦 {products_count} Produtos")
            self.orders_count_label.config(text=f"📋 {orders_count} Pedidos")
            self.total_sales_label.config(text=f"💰 R$ {total_sales:,.2f}")
            
        except Exception as e:
            print(f"Error updating status bar: {e}")
    
    def _schedule_status_update(self):
        """Schedule automatic status bar updates."""
        self._update_status_bar()
        self.root.after(5000, self._schedule_status_update)  # Update every 5 seconds
    
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
            
            messagebox.showinfo("Atualizar", "✅ Todos os dados foram atualizados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao atualizar dados: {str(e)}")
    
    def _show_about(self):
        """Show about dialog with modern styling."""
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        about_window.configure(bg=self.colors['light'])
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Header
        header_frame = tk.Frame(about_window, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="🏢 Sistema de Gestão de Vendas",
                              font=('Segoe UI', 18, 'bold'),
                              fg='white',
                              bg=self.colors['primary'])
        title_label.pack(pady=30)
        
        # Content
        content_frame = tk.Frame(about_window, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        info_text = """
        📋 Versão: 1.0.0
        
        🏗️ Arquitetura: Clean Architecture
        🐍 Linguagem: Python
        🖥️ Interface: Tkinter
        
        ✨ Funcionalidades:
        • Gestão de Empresas com validação CNPJ
        • Cadastro de Produtos com controle de estoque  
        • Criação e gerenciamento de Pedidos de Venda
        • Relatórios em PDF
        • Integração com BrasilAPI
        
        👨‍💻 Desenvolvido com ❤️ usando boas práticas
        """
        
        info_label = tk.Label(content_frame,
                             text=info_text,
                             font=('Segoe UI', 11),
                             fg=self.colors['dark'],
                             bg=self.colors['light'],
                             justify='left')
        info_label.pack()
        
        # Close button
        close_button = tk.Button(content_frame,
                               text="✅ Fechar",
                               command=about_window.destroy,
                               bg=self.colors['primary'],
                               fg='white',
                               font=('Segoe UI', 12, 'bold'),
                               relief='flat',
                               padx=30,
                               pady=10)
        close_button.pack(pady=(20, 0))
    
    def _quit_application(self):
        """Quit the application safely."""
        if messagebox.askyesno("Sair", "🤔 Tem certeza que deseja sair do sistema?"):
            self.root.quit()
