"""
Sales order management frame for the GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import List, Optional, Dict, Any

from ...application.dtos.sales_order_dto import CreateSalesOrderDTO, SalesOrderResponseDTO, AddOrderItemDTO
from ...application.dtos.company_dto import CompanyResponseDTO
from ...application.dtos.product_dto import ProductResponseDTO
from ...presentation.controllers.sales_order_controller import SalesOrderController
from ...presentation.controllers.company_controller import CompanyController
from ...presentation.controllers.product_controller import ProductController
from ...presentation.validators.form_validator import FormValidator
from ...presentation.validators.input_formatter import InputFormatter
from ...shared.exceptions.exceptions import ValidationException, SalesManagementException, DuplicateEntityException


class SalesOrderFrame:
    """Frame for managing sales orders."""
    
    def __init__(self, parent: tk.Widget, 
                 sales_order_controller: SalesOrderController,
                 company_controller: CompanyController,
                 product_controller: ProductController):
        """Initialize sales order management frame."""
        self.parent = parent
        self.sales_order_controller = sales_order_controller
        self.company_controller = company_controller
        self.product_controller = product_controller
        self.validator = FormValidator()
        self.formatter = InputFormatter()
        
        self.frame = ttk.Frame(parent)
        self._setup_ui()
        self._load_sales_orders()
        self._load_companies()
        self._load_products()
    
    def _setup_ui(self):
        """Setup user interface."""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sales Orders list tab
        self._create_orders_tab()
        
        # New/Edit Order tab
        self._create_order_form_tab()
    
    def _create_orders_tab(self):
        """Create sales orders list tab."""
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Sales Orders")
        
        # Title
        title_label = ttk.Label(orders_frame, text="Sales Orders", style='Title.TLabel')
        title_label.pack(pady=(10, 10))
        
        # Toolbar
        toolbar_frame = ttk.Frame(orders_frame)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # Status filter
        ttk.Label(search_frame, text="Status:").pack(side=tk.LEFT, padx=(10, 5))
        self.status_filter_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(search_frame, textvariable=self.status_filter_var, width=12, state="readonly")
        status_combo['values'] = ('All', 'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')
        status_combo.pack(side=tk.LEFT)
        status_combo.bind('<<ComboboxSelected>>', self._on_status_filter_changed)
        
        # Action buttons with modern styling
        new_btn = ttk.Button(toolbar_frame, text="➕ New Order", command=self._new_order, style='Action.TButton')
        new_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        refresh_btn = ttk.Button(toolbar_frame, text="🔄 Refresh", command=self._load_sales_orders, style='Action.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Orders treeview
        tree_frame = ttk.Frame(orders_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('ID', 'Date', 'Company', 'Status', 'Items', 'Total')
        self.orders_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.orders_tree.heading('ID', text='Order ID')
        self.orders_tree.heading('Date', text='Date')
        self.orders_tree.heading('Company', text='Company')
        self.orders_tree.heading('Status', text='Status')
        self.orders_tree.heading('Items', text='Items')
        self.orders_tree.heading('Total', text='Total')
        
        self.orders_tree.column('ID', width=100, minwidth=80)
        self.orders_tree.column('Date', width=100, minwidth=80)
        self.orders_tree.column('Company', width=200, minwidth=150)
        self.orders_tree.column('Status', width=100, minwidth=80)
        self.orders_tree.column('Items', width=60, minwidth=50)
        self.orders_tree.column('Total', width=100, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.orders_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.orders_tree.bind('<<TreeviewSelect>>', self._on_order_selected)
        self.orders_tree.bind('<Double-1>', self._on_order_double_click)
        
        # Context menu
        self._create_context_menu()
        self.orders_tree.bind('<Button-3>', self._show_context_menu)  # Right click
        
        # Action buttons with modern styling
        action_frame = ttk.Frame(orders_frame, style='Card.TFrame')
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        view_btn = ttk.Button(action_frame, text="👁️ View Details", command=self._view_order_details, style='Action.TButton')
        view_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        edit_btn = ttk.Button(action_frame, text="✏️ Edit Order", command=self._edit_order, style='Action.TButton')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        pdf_btn = ttk.Button(action_frame, text="📄 Generate PDF", command=self._generate_pdf, style='Action.TButton')
        pdf_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = ttk.Button(action_frame, text="🗑️ Delete Order", command=self._delete_order, style='Action.TButton')
        delete_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    def _create_order_form_tab(self):
        """Create order form tab."""
        form_frame = ttk.Frame(self.notebook)
        self.notebook.add(form_frame, text="Order Form")
        
        # Make form scrollable
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.scrollable_form = ttk.Frame(canvas)
        
        self.scrollable_form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form title
        self.form_title = ttk.Label(self.scrollable_form, text="New Sales Order", style='Title.TLabel')
        self.form_title.pack(pady=(10, 20))
        
        # Order information
        self._create_order_info_section()
        
        # Items section
        self._create_items_section()
        
        # Order summary
        self._create_summary_section()
        
        # Form buttons
        self._create_order_form_buttons()
        
        # Initialize form state
        self.current_order_id: Optional[str] = None
        self.order_items: List[Dict[str, Any]] = []
    
    def _create_order_info_section(self):
        """Create order information section."""
        info_frame = ttk.LabelFrame(self.scrollable_form, text="Order Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Company selection
        ttk.Label(info_frame, text="Company *:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(info_frame, textvariable=self.company_var, width=40, state="readonly")
        self.company_combo.grid(row=0, column=1, sticky='ew', pady=(0, 5))
        
        # Order date
        ttk.Label(info_frame, text="Order Date *:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.order_date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        date_entry = ttk.Entry(info_frame, textvariable=self.order_date_var, width=40)
        date_entry.grid(row=1, column=1, sticky='ew', pady=(0, 5))
        date_entry.bind('<KeyRelease>', self._format_date)
        
        # Status
        ttk.Label(info_frame, text="Status:").grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.status_var = tk.StringVar(value="PENDING")
        status_combo = ttk.Combobox(info_frame, textvariable=self.status_var, width=40, state="readonly")
        status_combo['values'] = ('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')
        status_combo.grid(row=2, column=1, sticky='ew', pady=(0, 5))
        
        # Notes
        ttk.Label(info_frame, text="Notes:").grid(row=3, column=0, sticky='nw', pady=(5, 0))
        self.notes_text = tk.Text(info_frame, width=40, height=3)
        self.notes_text.grid(row=3, column=1, sticky='ew', pady=(5, 0))
        
        info_frame.grid_columnconfigure(1, weight=1)
    
    def _create_items_section(self):
        """Create order items section."""
        items_frame = ttk.LabelFrame(self.scrollable_form, text="Order Items", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add item frame
        add_item_frame = ttk.Frame(items_frame)
        add_item_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product selection
        ttk.Label(add_item_frame, text="Product:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_item_frame, textvariable=self.product_var, width=25, state="readonly")
        self.product_combo.grid(row=0, column=1, sticky='ew', padx=(0, 5))
        self.product_combo.bind('<<ComboboxSelected>>', self._on_product_selected)
        
        # Quantity
        ttk.Label(add_item_frame, text="Qty:").grid(row=0, column=2, sticky='w', padx=(5, 5))
        self.quantity_var = tk.StringVar()
        quantity_entry = ttk.Entry(add_item_frame, textvariable=self.quantity_var, width=8)
        quantity_entry.grid(row=0, column=3, padx=(0, 5))
        quantity_entry.bind('<KeyRelease>', self._validate_quantity)
        
        # Unit price
        ttk.Label(add_item_frame, text="Unit Price:").grid(row=0, column=4, sticky='w', padx=(5, 5))
        self.unit_price_var = tk.StringVar()
        price_entry = ttk.Entry(add_item_frame, textvariable=self.unit_price_var, width=10)
        price_entry.grid(row=0, column=5, padx=(0, 5))
        price_entry.bind('<KeyRelease>', self._format_unit_price)
        
        # Add button
        ttk.Button(add_item_frame, text="Add Item", command=self._add_item).grid(row=0, column=6, padx=(5, 0))
        
        add_item_frame.grid_columnconfigure(1, weight=1)
        
        # Items treeview
        items_tree_frame = ttk.Frame(items_frame)
        items_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        item_columns = ('Product', 'Quantity', 'Unit Price', 'Total')
        self.items_tree = ttk.Treeview(items_tree_frame, columns=item_columns, show='headings', height=8)
        
        # Configure columns
        self.items_tree.heading('Product', text='Product')
        self.items_tree.heading('Quantity', text='Quantity')
        self.items_tree.heading('Unit Price', text='Unit Price')
        self.items_tree.heading('Total', text='Total')
        
        self.items_tree.column('Product', width=200, minwidth=150)
        self.items_tree.column('Quantity', width=80, minwidth=60)
        self.items_tree.column('Unit Price', width=100, minwidth=80)
        self.items_tree.column('Total', width=100, minwidth=80)
        
        # Scrollbar for items
        items_scrollbar = ttk.Scrollbar(items_tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.items_tree.grid(row=0, column=0, sticky='nsew')
        items_scrollbar.grid(row=0, column=1, sticky='ns')
        
        items_tree_frame.grid_rowconfigure(0, weight=1)
        items_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Items actions
        items_actions = ttk.Frame(items_frame)
        items_actions.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(items_actions, text="Remove Item", command=self._remove_item).pack(side=tk.LEFT)
        ttk.Button(items_actions, text="Clear All", command=self._clear_items).pack(side=tk.LEFT, padx=(5, 0))
    
    def _create_summary_section(self):
        """Create order summary section."""
        summary_frame = ttk.LabelFrame(self.scrollable_form, text="Order Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Total items
        ttk.Label(summary_frame, text="Total Items:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.total_items_var = tk.StringVar(value="0")
        ttk.Label(summary_frame, textvariable=self.total_items_var, font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='e', pady=(0, 5))
        
        # Total value
        ttk.Label(summary_frame, text="Total Value:").grid(row=1, column=0, sticky='w')
        self.total_value_var = tk.StringVar(value="R$ 0.00")
        ttk.Label(summary_frame, textvariable=self.total_value_var, font=('Arial', 12, 'bold'), foreground='blue').grid(row=1, column=1, sticky='e')
        
        summary_frame.grid_columnconfigure(1, weight=1)
    
    def _create_order_form_buttons(self):
        """Create enhanced order form buttons with modern styling."""
        buttons_frame = ttk.Frame(self.scrollable_form)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        # Enhanced save button with icon
        self.save_order_button = ttk.Button(
            buttons_frame, 
            text="💾 Salvar Pedido", 
            command=self._save_order,
            style='Success.TButton'
        )
        self.save_order_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Enhanced cancel button with icon
        self.cancel_order_button = ttk.Button(
            buttons_frame, 
            text="❌ Cancelar", 
            command=self._cancel_order_form,
            style='Danger.TButton'
        )
        self.cancel_order_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Enhanced clear button with icon
        self.clear_order_button = ttk.Button(
            buttons_frame, 
            text="🔄 Limpar Formulário", 
            command=self._clear_order_form,
            style='Warning.TButton'
        )
        self.clear_order_button.pack(side=tk.RIGHT)
    
    def _create_context_menu(self):
        """Create context menu for orders tree."""
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self._view_order_details)
        self.context_menu.add_command(label="Edit Order", command=self._edit_order)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Generate PDF", command=self._generate_pdf)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete Order", command=self._delete_order)
    
    def _load_sales_orders(self):
        """Load sales orders into the tree view."""
        try:
            success, orders, error = self.sales_order_controller.list_sales_orders()
            if success:
                self._populate_orders_tree(orders)
            else:
                messagebox.showerror("Error", f"Error loading sales orders: {error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading sales orders: {str(e)}")
    
    def _load_companies(self):
        """Load companies for selection."""
        try:
            companies = self.company_controller.list_companies()
            company_values = [f"{company.id} - {company.name}" for company in companies]
            self.company_combo['values'] = company_values
        except Exception as e:
            messagebox.showerror("Error", f"Error loading companies: {str(e)}")
    
    def _load_products(self):
        """Load products for selection."""
        try:
            products = self.product_controller.list_products()
            product_values = [f"{product.id} - {product.name}" for product in products]
            self.product_combo['values'] = product_values
        except Exception as e:
            messagebox.showerror("Error", f"Error loading products: {str(e)}")
    
    def _populate_orders_tree(self, orders: List[SalesOrderResponseDTO]):
        """Populate orders tree view."""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Filter by status if needed  
        status_filter = self.status_filter_var.get()
        if status_filter != "All":
            # Note: Filtering by status is not available in current DTO
            # This would require updating the DTO or removing this filter
            pass
        
        # Filter by search text if needed
        search_text = self.search_var.get().lower()
        if search_text:
            orders = [order for order in orders if 
                     search_text in order.id.lower() or
                     search_text in order.company_name.lower()]
        
        # Add orders
        for order in orders:
            # Use created_at instead of order_date
            from datetime import datetime
            try:
                order_date = datetime.fromisoformat(order.created_at).strftime("%d/%m/%Y") if order.created_at else ""
            except:
                order_date = order.created_at[:10] if order.created_at else ""
            
            total_items = order.total_items if hasattr(order, 'total_items') else len(order.items) if order.items else 0
            total_value = order.formatted_total_amount if hasattr(order, 'formatted_total_amount') else f"R$ {order.total_amount:.2f}" if hasattr(order, 'total_amount') else "R$ 0.00"
            
            # Use a default status since it's not in the DTO
            status = "Active" if order.is_valid else "Invalid"
            
            self.orders_tree.insert('', 'end', values=(
                order.id,
                order_date,
                order.company_name,
                status,
                total_items,
                total_value
            ))
    
    def _on_search_changed(self, *args):
        """Handle search text change."""
        self._load_sales_orders()
    
    def _on_status_filter_changed(self, event):
        """Handle status filter change."""
        self._load_sales_orders()
    
    def _on_order_selected(self, event):
        """Handle order selection."""
        pass  # Could load order details in a preview panel
    
    def _on_order_double_click(self, event):
        """Handle double-click on order."""
        self._view_order_details()
    
    def _show_context_menu(self, event):
        """Show context menu."""
        # Select the item under cursor
        item = self.orders_tree.identify_row(event.y)
        if item:
            self.orders_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _on_product_selected(self, event):
        """Handle product selection in form."""
        product_text = self.product_var.get()
        if not product_text:
            return
        
        try:
            product_id = product_text.split(' - ')[0]
            product = self.product_controller.get_product(product_id)
            if product and product.price:
                self.unit_price_var.set(f"{product.price:.2f}")
        except Exception as e:
            pass  # Ignore errors in auto-fill
    
    def _validate_quantity(self, event):
        """Validate quantity input."""
        value = self.quantity_var.get()
        cleaned = ''.join(c for c in value if c.isdigit())
        if cleaned != value:
            self.quantity_var.set(cleaned)
    
    def _format_unit_price(self, event):
        """Format unit price input."""
        value = self.unit_price_var.get()
        cleaned = ''.join(c for c in value if c.isdigit() or c in '.,')
        
        if ',' in cleaned:
            cleaned = cleaned.replace(',', '.')
        
        if cleaned.count('.') > 1:
            parts = cleaned.split('.')
            cleaned = parts[0] + '.' + ''.join(parts[1:])
        
        if '.' in cleaned:
            parts = cleaned.split('.')
            if len(parts[1]) > 2:
                cleaned = parts[0] + '.' + parts[1][:2]
        
        if cleaned != value:
            self.unit_price_var.set(cleaned)
    
    def _format_date(self, event):
        """Format date input."""
        value = self.order_date_var.get()
        formatted = self.formatter.format_date(value)
        if formatted != value:
            self.order_date_var.set(formatted)
    
    def _add_item(self):
        """Add item to order."""
        product_text = self.product_var.get()
        quantity_text = self.quantity_var.get()
        unit_price_text = self.unit_price_var.get()
        
        if not product_text:
            messagebox.showwarning("Warning", "Please select a product.")
            return
        
        if not quantity_text or int(quantity_text) <= 0:
            messagebox.showwarning("Warning", "Please enter a valid quantity.")
            return
        
        if not unit_price_text:
            messagebox.showwarning("Warning", "Please enter a unit price.")
            return
        
        try:
            product_id = product_text.split(' - ')[0]
            product_name = product_text.split(' - ')[1]
            quantity = int(quantity_text)
            unit_price = float(unit_price_text.replace(',', '.'))
            total_price = quantity * unit_price
            
            # Check if product already exists in items
            for i, item in enumerate(self.order_items):
                if item['product_id'] == product_id:
                    # Update existing item
                    self.order_items[i]['quantity'] += quantity
                    self.order_items[i]['total_price'] = self.order_items[i]['quantity'] * self.order_items[i]['unit_price']
                    self._refresh_items_tree()
                    self._update_summary()
                    self._clear_item_form()
                    return
            
            # Add new item
            item = {
                'product_id': product_id,
                'product_name': product_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            }
            
            self.order_items.append(item)
            self._refresh_items_tree()
            self._update_summary()
            self._clear_item_form()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid price format.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding item: {str(e)}")
    
    def _remove_item(self):
        """Remove selected item from order."""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove.")
            return
        
        item_index = self.items_tree.index(selection[0])
        del self.order_items[item_index]
        
        self._refresh_items_tree()
        self._update_summary()
    
    def _clear_items(self):
        """Clear all items from order."""
        if self.order_items and messagebox.askyesno("Confirm", "Clear all items from the order?"):
            self.order_items = []
            self._refresh_items_tree()
            self._update_summary()
    
    def _clear_item_form(self):
        """Clear item form fields."""
        self.product_var.set("")
        self.quantity_var.set("")
        self.unit_price_var.set("")
    
    def _refresh_items_tree(self):
        """Refresh items tree view."""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Add items
        for item in self.order_items:
            self.items_tree.insert('', 'end', values=(
                item['product_name'],
                item['quantity'],
                f"R$ {item['unit_price']:.2f}",
                f"R$ {item['total_price']:.2f}"
            ))
    
    def _update_summary(self):
        """Update order summary."""
        total_items = len(self.order_items)
        total_value = sum(item['total_price'] for item in self.order_items)
        
        self.total_items_var.set(str(total_items))
        self.total_value_var.set(f"R$ {total_value:.2f}")
    
    def _new_order(self):
        """Start creating a new order."""
        self._clear_order_form()
        self.form_title.config(text="New Sales Order")
        self.notebook.select(1)  # Switch to form tab
    
    def _edit_order(self):
        """Edit selected order."""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to edit.")
            return
        
        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        
        try:
            order = self.sales_order_controller.get_sales_order(order_id)
            if order:
                self._populate_order_form(order)
                self.form_title.config(text=f"Edit Order - {order_id}")
                self.notebook.select(1)  # Switch to form tab
        except Exception as e:
            messagebox.showerror("Error", f"Error loading order: {str(e)}")
    
    def _view_order_details(self):
        """View order details in a popup."""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to view.")
            return
        
        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        
        try:
            order = self.sales_order_controller.get_sales_order(order_id)
            if order:
                self._show_order_details_dialog(order)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading order details: {str(e)}")
    
    def _delete_order(self):
        """Delete selected order."""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to delete.")
            return
        
        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete order '{order_id}'?\n"
                              "This action cannot be undone."):
            try:
                self.sales_order_controller.delete_sales_order(order_id)
                self._load_sales_orders()
                messagebox.showinfo("Success", "Order deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting order: {str(e)}")
    
    def _generate_pdf(self):
        """Generate PDF report for selected order."""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to generate PDF.")
            return
        
        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialname=f"Order_{order_id}.pdf"
        )
        
        if not file_path:
            return
        
        try:
            result = self.sales_order_controller.generate_report(order_id, file_path)
            if result:
                messagebox.showinfo("Success", f"PDF report generated successfully!\nSaved to: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to generate PDF report.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating PDF: {str(e)}")
    
    def _save_order(self):
        """Save order."""
        try:
            # Validate form
            if not self.company_var.get():
                messagebox.showerror("Validation Error", "Please select a company.")
                return
            
            if not self.order_date_var.get():
                messagebox.showerror("Validation Error", "Please enter an order date.")
                return
            
            if not self.order_items:
                messagebox.showerror("Validation Error", "Please add at least one item to the order.")
                return
            
            # Parse company ID
            company_id = self.company_var.get().split(' - ')[0]
            
            # Parse date
            try:
                order_date = datetime.strptime(self.order_date_var.get(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid date format. Use DD/MM/YYYY.")
                return
            
            # Create items DTOs
            items = []
            for item in self.order_items:
                item_dto = AddOrderItemDTO(
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                )
                items.append(item_dto)
            
            # Create order DTO
            order_dto = CreateSalesOrderDTO(
                company_id=company_id,
                order_date=order_date,
                status=self.status_var.get(),
                notes=self.notes_text.get("1.0", tk.END).strip() or None,
                items=items
            )
            
            # Save order
            if self.current_order_id:
                # Update existing order (if implemented)
                messagebox.showinfo("Info", "Order update functionality not implemented yet.")
            else:
                # Create new order
                self.sales_order_controller.create_sales_order(order_dto)
                messagebox.showinfo("Success", "Order created successfully.")
            
            # Refresh and clear
            self._load_sales_orders()
            self._clear_order_form()
            self.notebook.select(0)  # Switch back to orders list
            
        except (ValidationException, DuplicateEntityException) as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error saving order: {str(e)}")
    
    def _cancel_order_form(self):
        """Cancel order form."""
        if messagebox.askyesno("Confirm", "Cancel order form? Any unsaved changes will be lost."):
            self._clear_order_form()
            self.notebook.select(0)  # Switch back to orders list
    
    def _clear_order_form(self):
        """Clear order form."""
        self.company_var.set("")
        self.order_date_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.status_var.set("PENDING")
        self.notes_text.delete("1.0", tk.END)
        
        self.order_items = []
        self._refresh_items_tree()
        self._update_summary()
        self._clear_item_form()
        
        self.current_order_id = None
        self.form_title.config(text="Order Form")
    
    def _populate_order_form(self, order: SalesOrderResponseDTO):
        """Populate form with order data."""
        self._clear_order_form()
        
        # Find and set company
        for value in self.company_combo['values']:
            if value.startswith(order.company_id):
                self.company_var.set(value)
                break
        
        # Set other fields  
        # Note: order_date and status not available in current DTO
        # if order.order_date:
        #     self.order_date_var.set(order.order_date.strftime("%d/%m/%Y"))
        # self.status_var.set(order.status)
        if hasattr(order, 'notes') and order.notes:
            self.notes_text.insert("1.0", order.notes)
        
        # Set items
        if order.items:
            for item in order.items:
                try:
                    product = self.product_controller.get_product(item.product_id)
                    if product:
                        order_item = {
                            'product_id': item.product_id,
                            'product_name': product.name,
                            'quantity': item.quantity,
                            'unit_price': item.unit_price,
                            'total_price': item.quantity * item.unit_price
                        }
                        self.order_items.append(order_item)
                except Exception:
                    continue  # Skip items with missing products
        
        self._refresh_items_tree()
        self._update_summary()
        
        self.current_order_id = order.id
    
    def _show_order_details_dialog(self, order: SalesOrderResponseDTO):
        """Show order details in a dialog."""
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Order Details - {order.id}")
        details_window.geometry("600x500")
        details_window.transient(self.parent)
        details_window.grab_set()
        
        # Center the window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (details_window.winfo_screenheight() // 2) - (500 // 2)
        details_window.geometry(f"600x500+{x}+{y}")
        
        # Create scrollable frame
        canvas = tk.Canvas(details_window, highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Order information
        info_frame = ttk.LabelFrame(scrollable, text="Order Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"Order ID: {order.id}", font=('Arial', 10, 'bold')).pack(anchor='w')
        ttk.Label(info_frame, text=f"Company: {order.company_name}").pack(anchor='w')
        # Note: Date and status not available in current DTO
        # if order.order_date:
        #     ttk.Label(info_frame, text=f"Date: {order.order_date.strftime('%d/%m/%Y')}").pack(anchor='w')
        # ttk.Label(info_frame, text=f"Status: {order.status}").pack(anchor='w')
        if hasattr(order, 'notes') and order.notes:
            ttk.Label(info_frame, text=f"Notes: {order.notes}").pack(anchor='w')
        
        # Items
        items_frame = ttk.LabelFrame(scrollable, text="Order Items", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        if order.items:
            # Items treeview
            items_tree = ttk.Treeview(items_frame, columns=('Product', 'Qty', 'Price', 'Total'), show='headings', height=8)
            
            items_tree.heading('Product', text='Product')
            items_tree.heading('Qty', text='Quantity')
            items_tree.heading('Price', text='Unit Price')
            items_tree.heading('Total', text='Total')
            
            items_tree.column('Product', width=200)
            items_tree.column('Qty', width=80)
            items_tree.column('Price', width=100)
            items_tree.column('Total', width=100)
            
            for item in order.items:
                try:
                    product = self.product_controller.get_product(item.product_id)
                    product_name = product.name if product else f"Product {item.product_id}"
                    total = item.quantity * item.unit_price
                    
                    items_tree.insert('', 'end', values=(
                        product_name,
                        item.quantity,
                        f"R$ {item.unit_price:.2f}",
                        f"R$ {total:.2f}"
                    ))
                except Exception:
                    continue
            
            items_tree.pack(fill=tk.BOTH, expand=True)
        
        # Summary
        summary_frame = ttk.LabelFrame(scrollable, text="Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        total_items = len(order.items) if order.items else 0
        total_value = order.total_amount if hasattr(order, 'total_amount') else 0
        
        ttk.Label(summary_frame, text=f"Total Items: {total_items}").pack(anchor='w')
        ttk.Label(summary_frame, text=f"Total Value: R$ {total_value:.2f}", 
                 font=('Arial', 12, 'bold'), foreground='blue').pack(anchor='w')
        
        # Close button
        ttk.Button(scrollable, text="Close", command=details_window.destroy).pack(pady=10)
