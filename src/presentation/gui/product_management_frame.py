"""
Product management frame for the GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional

from ...application.dtos.product_dto import CreateProductDTO, UpdateProductDTO, ProductResponseDTO
from ...presentation.controllers.product_controller import ProductController
from ...presentation.validators.form_validator import FormValidator
from ...presentation.validators.input_formatter import InputFormatter
from ...shared.exceptions.exceptions import ValidationException, SalesManagementException, DuplicateEntityException


class ProductManagementFrame:
    """Frame for managing products."""
    
    def __init__(self, parent: tk.Widget, controller: ProductController):
        """Initialize product management frame."""
        self.parent = parent
        self.controller = controller
        self.validator = FormValidator()
        self.formatter = InputFormatter()
        
        self.frame = ttk.Frame(parent)
        self._setup_ui()
        self._load_products()
    
    def _setup_ui(self):
        """Setup user interface."""
        # Main paned window
        self.paned_window = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Product list
        self._create_list_panel()
        
        # Right panel - Product form
        self._create_form_panel()
    
    def _create_list_panel(self):
        """Create product list panel."""
        list_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(list_frame, weight=2)
        
        # Title
        title_label = ttk.Label(list_frame, text="Products", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar_frame = ttk.Frame(list_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # Import button with modern icon
        import_btn = ttk.Button(toolbar_frame, text="📊 Import Excel", command=self._import_excel, style='Action.TButton')
        import_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Product treeview
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Description', 'Price', 'Stock', 'Category')
        self.product_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.product_tree.heading('ID', text='ID')
        self.product_tree.heading('Name', text='Product Name')
        self.product_tree.heading('Description', text='Description')
        self.product_tree.heading('Price', text='Price')
        self.product_tree.heading('Stock', text='Stock')
        self.product_tree.heading('Category', text='Category')
        
        self.product_tree.column('ID', width=50, minwidth=50)
        self.product_tree.column('Name', width=150, minwidth=120)
        self.product_tree.column('Description', width=200, minwidth=150)
        self.product_tree.column('Price', width=80, minwidth=60)
        self.product_tree.column('Stock', width=60, minwidth=50)
        self.product_tree.column('Category', width=100, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.product_tree.xview)
        self.product_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.product_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.product_tree.bind('<<TreeviewSelect>>', self._on_product_selected)
        self.product_tree.bind('<Double-1>', self._on_product_double_click)
        
        # Buttons frame with modern styling
        buttons_frame = ttk.Frame(list_frame, style='Card.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(10, 0), padx=5)
        
        # Create styled buttons with icons
        new_btn = ttk.Button(buttons_frame, text="➕ New", command=self._new_product, style='Action.TButton')
        new_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        edit_btn = ttk.Button(buttons_frame, text="✏️ Edit", command=self._edit_product, style='Action.TButton')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = ttk.Button(buttons_frame, text="🗑️ Delete", command=self._delete_product, style='Action.TButton')
        delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = ttk.Button(buttons_frame, text="🔄 Refresh", command=self._load_products, style='Action.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 5))
    
    def _create_form_panel(self):
        """Create product form panel."""
        form_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(form_frame, weight=1)
        
        # Title
        self.form_title = ttk.Label(form_frame, text="Product Details", style='Title.TLabel')
        self.form_title.pack(pady=(0, 20))
        
        # Form fields
        self._create_form_fields(form_frame)
        
        # Buttons
        self._create_form_buttons(form_frame)
    
    def _create_form_fields(self, parent):
        """Create form input fields."""
        # Basic Information
        basic_frame = ttk.LabelFrame(parent, text="Basic Information", padding=10)
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product Name
        ttk.Label(basic_frame, text="Product Name *:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(basic_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky='ew', pady=(0, 5))
        
        # Description
        ttk.Label(basic_frame, text="Description:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(basic_frame, textvariable=self.description_var, width=40)
        description_entry.grid(row=1, column=1, sticky='ew', pady=(0, 5))
        
        # Category
        ttk.Label(basic_frame, text="Category:").grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(basic_frame, textvariable=self.category_var, width=40)
        category_entry.grid(row=2, column=1, sticky='ew', pady=(0, 5))
        
        basic_frame.grid_columnconfigure(1, weight=1)
        
        # Pricing and Stock
        pricing_frame = ttk.LabelFrame(parent, text="Pricing and Stock", padding=10)
        pricing_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Price
        price_frame = ttk.Frame(pricing_frame)
        price_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        
        ttk.Label(price_frame, text="Price *:").pack(side=tk.LEFT)
        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=15)
        price_entry.pack(side=tk.LEFT, padx=(5, 0))
        price_entry.bind('<KeyRelease>', self._format_price)
        
        # Stock Quantity
        stock_frame = ttk.Frame(pricing_frame)
        stock_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        
        ttk.Label(stock_frame, text="Stock Quantity *:").pack(side=tk.LEFT)
        self.stock_var = tk.StringVar()
        stock_entry = ttk.Entry(stock_frame, textvariable=self.stock_var, width=15)
        stock_entry.pack(side=tk.LEFT, padx=(5, 0))
        stock_entry.bind('<KeyRelease>', self._validate_stock)
        
        pricing_frame.grid_columnconfigure(1, weight=1)
        
        # Additional Information
        additional_frame = ttk.LabelFrame(parent, text="Additional Information", padding=10)
        additional_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Barcode
        ttk.Label(additional_frame, text="Barcode:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.barcode_var = tk.StringVar()
        barcode_entry = ttk.Entry(additional_frame, textvariable=self.barcode_var, width=40)
        barcode_entry.grid(row=0, column=1, sticky='ew', pady=(0, 5))
        
        # SKU
        ttk.Label(additional_frame, text="SKU:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.sku_var = tk.StringVar()
        sku_entry = ttk.Entry(additional_frame, textvariable=self.sku_var, width=40)
        sku_entry.grid(row=1, column=1, sticky='ew', pady=(0, 5))
        
        # Unit
        ttk.Label(additional_frame, text="Unit:").grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(additional_frame, textvariable=self.unit_var, width=37)
        unit_combo['values'] = ('UN', 'KG', 'G', 'L', 'ML', 'M', 'CM', 'M²', 'M³', 'PC', 'CX', 'PCT')
        unit_combo.grid(row=2, column=1, sticky='ew', pady=(0, 5))
        
        additional_frame.grid_columnconfigure(1, weight=1)
        
        # Required fields note
        note_label = ttk.Label(parent, text="* Required fields", foreground='red', font=('Arial', 8))
        note_label.pack(pady=(10, 0))
    
    def _create_form_buttons(self, parent):
        """Create enhanced form action buttons with modern styling."""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Enhanced save button with icon
        self.save_button = ttk.Button(
            buttons_frame, 
            text="💾 Salvar Produto", 
            command=self._save_product,
            style='Success.TButton'
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Enhanced cancel button with icon
        self.cancel_button = ttk.Button(
            buttons_frame, 
            text="❌ Cancelar", 
            command=self._cancel_form,
            style='Danger.TButton'
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Enhanced clear button with icon
        self.clear_button = ttk.Button(
            buttons_frame, 
            text="🔄 Limpar Formulário", 
            command=self._clear_form,
            style='Warning.TButton'
        )
        self.clear_button.pack(side=tk.RIGHT)
        
        # Initially disable save button
        self.save_button.config(state='disabled')
        
        # Current product ID for editing
        self.current_product_id: Optional[str] = None
    
    def _load_products(self):
        """Load products into the tree view."""
        try:
            products = self.controller.list_products()
            self._populate_tree(products)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading products: {str(e)}")
    
    def _populate_tree(self, products: List[ProductResponseDTO]):
        """Populate tree view with products."""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Add products
        for product in products:
            price_str = f"R$ {product.unit_price:.2f}" if product.unit_price else "N/A"
            stock_str = str(product.stock_quantity) if product.stock_quantity is not None else "N/A"
            
            self.product_tree.insert('', 'end', values=(
                product.id,
                product.name,
                product.description or "",
                price_str,
                stock_str,
                product.category or ""
            ))
    
    def _on_search_changed(self, *args):
        """Handle search text change."""
        search_text = self.search_var.get().lower()
        if not search_text:
            self._load_products()
            return
        
        try:
            all_products = self.controller.list_products()
            filtered_products = [
                product for product in all_products
                if (search_text in product.name.lower() or 
                    search_text in (product.description or "").lower() or
                    search_text in (product.category or "").lower())
            ]
            self._populate_tree(filtered_products)
        except Exception as e:
            messagebox.showerror("Error", f"Error searching products: {str(e)}")
    
    def _on_product_selected(self, event):
        """Handle product selection in tree view."""
        selection = self.product_tree.selection()
        if selection:
            item = self.product_tree.item(selection[0])
            product_id = item['values'][0]
            self._load_product_details(product_id)
    
    def _on_product_double_click(self, event):
        """Handle double-click on product (edit mode)."""
        self._edit_product()
    
    def _load_product_details(self, product_id: str):
        """Load product details into form."""
        try:
            product = self.controller.get_product(product_id)
            if product:
                self._populate_form(product)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading product details: {str(e)}")
    
    def _populate_form(self, product: ProductResponseDTO):
        """Populate form with product data."""
        # Clear form first
        self._clear_form()
        
        # Basic information
        self.name_var.set(product.name)
        self.description_var.set(product.description or "")
        self.category_var.set(product.category or "")
        
        # Pricing and stock
        self.price_var.set(f"{product.price:.2f}" if product.price else "")
        self.stock_var.set(str(product.stock_quantity) if product.stock_quantity is not None else "")
        
        # Additional information
        self.barcode_var.set(product.barcode or "")
        self.sku_var.set(product.sku or "")
        self.unit_var.set(product.unit or "")
        
        # Set current product ID
        self.current_product_id = product.id
        
        # Update form title and button state
        self.form_title.config(text=f"Product Details - {product.name}")
        self.save_button.config(state='normal')
    
    def _clear_form(self):
        """Clear all form fields."""
        # Clear all variables
        self.name_var.set("")
        self.description_var.set("")
        self.category_var.set("")
        self.price_var.set("")
        self.stock_var.set("")
        self.barcode_var.set("")
        self.sku_var.set("")
        self.unit_var.set("")
        
        # Reset form state
        self.current_product_id = None
        self.form_title.config(text="Product Details")
        self.save_button.config(state='disabled')
    
    def _new_product(self):
        """Start creating a new product."""
        self._clear_form()
        self.form_title.config(text="New Product")
        self.save_button.config(state='normal')
    
    def _edit_product(self):
        """Edit selected product."""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to edit.")
            return
        
        item = self.product_tree.item(selection[0])
        product_id = item['values'][0]
        self._load_product_details(product_id)
        self.form_title.config(text=f"Edit Product - {self.name_var.get()}")
    
    def _delete_product(self):
        """Delete selected product."""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return
        
        item = self.product_tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{product_name}'?\n"
                              "This action cannot be undone."):
            try:
                self.controller.delete_product(product_id)
                self._load_products()
                self._clear_form()
                messagebox.showinfo("Success", "Product deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting product: {str(e)}")
    
    def _save_product(self):
        """Save product data."""
        try:
            # Validate required fields
            if not self.name_var.get().strip():
                messagebox.showerror("Validation Error", "Product name is required.")
                return
            
            if not self.price_var.get().strip():
                messagebox.showerror("Validation Error", "Price is required.")
                return
            
            if not self.stock_var.get().strip():
                messagebox.showerror("Validation Error", "Stock quantity is required.")
                return
            
            # Parse numeric values
            try:
                price = float(self.price_var.get().replace(',', '.'))
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid price format.")
                return
            
            try:
                stock = int(self.stock_var.get())
                if stock < 0:
                    raise ValueError("Stock cannot be negative")
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid stock quantity format.")
                return
            
            # Create DTO
            if self.current_product_id:
                # Update existing product
                dto = UpdateProductDTO(
                    name=self.name_var.get().strip(),
                    description=self.description_var.get().strip() or None,
                    price=price,
                    stock_quantity=stock,
                    category=self.category_var.get().strip() or None,
                    barcode=self.barcode_var.get().strip() or None,
                    sku=self.sku_var.get().strip() or None,
                    unit=self.unit_var.get().strip() or None
                )
                self.controller.update_product(self.current_product_id, dto)
                message = "Product updated successfully."
            else:
                # Create new product
                dto = CreateProductDTO(
                    name=self.name_var.get().strip(),
                    description=self.description_var.get().strip() or None,
                    price=price,
                    stock_quantity=stock,
                    category=self.category_var.get().strip() or None,
                    barcode=self.barcode_var.get().strip() or None,
                    sku=self.sku_var.get().strip() or None,
                    unit=self.unit_var.get().strip() or None
                )
                self.controller.create_product(dto)
                message = "Product created successfully."
            
            # Refresh list and clear form
            self._load_products()
            self._clear_form()
            messagebox.showinfo("Success", message)
            
        except (ValidationException, DuplicateEntityException) as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error saving product: {str(e)}")
    
    def _cancel_form(self):
        """Cancel form editing."""
        if self.current_product_id:
            # Reload current product data
            self._load_product_details(self.current_product_id)
        else:
            self._clear_form()
    
    def _format_price(self, event):
        """Format price input."""
        value = self.price_var.get()
        
        # Remove any non-numeric characters except comma and dot
        cleaned = ''.join(c for c in value if c.isdigit() or c in '.,')
        
        # Replace comma with dot for decimal separator
        if ',' in cleaned:
            cleaned = cleaned.replace(',', '.')
        
        # Ensure only one decimal point
        if cleaned.count('.') > 1:
            parts = cleaned.split('.')
            cleaned = parts[0] + '.' + ''.join(parts[1:])
        
        # Limit to 2 decimal places
        if '.' in cleaned:
            parts = cleaned.split('.')
            if len(parts[1]) > 2:
                cleaned = parts[0] + '.' + parts[1][:2]
        
        if cleaned != value:
            self.price_var.set(cleaned)
    
    def _validate_stock(self, event):
        """Validate stock input (integers only)."""
        value = self.stock_var.get()
        
        # Remove any non-numeric characters
        cleaned = ''.join(c for c in value if c.isdigit())
        
        if cleaned != value:
            self.stock_var.set(cleaned)
    
    def _import_excel(self):
        """Import products from Excel file."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Show progress dialog
            progress_window = tk.Toplevel(self.parent)
            progress_window.title("Importing Products")
            progress_window.geometry("400x150")
            progress_window.transient(self.parent)
            progress_window.grab_set()
            
            # Center the progress window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
            progress_window.geometry(f"400x150+{x}+{y}")
            
            ttk.Label(progress_window, text="Importing products from Excel...", 
                     font=('Arial', 12)).pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=20, fill=tk.X)
            progress_bar.start()
            
            status_label = ttk.Label(progress_window, text="Processing file...")
            status_label.pack(pady=5)
            
            # Update UI
            progress_window.update()
            
            # Import products
            result = self.controller.import_products_from_excel(file_path)
            
            # Stop progress bar
            progress_bar.stop()
            progress_window.destroy()
            
            # Show results
            if result['success']:
                message = f"Import completed successfully!\n\n"
                message += f"Total products processed: {result['total']}\n"
                message += f"Products created: {result['created']}\n"
                message += f"Products updated: {result['updated']}\n"
                
                if result['errors']:
                    message += f"Errors: {len(result['errors'])}\n\n"
                    message += "First few errors:\n"
                    for i, error in enumerate(result['errors'][:5]):
                        message += f"• {error}\n"
                    if len(result['errors']) > 5:
                        message += f"... and {len(result['errors']) - 5} more errors"
                
                messagebox.showinfo("Import Results", message)
                
                # Refresh product list
                self._load_products()
            else:
                messagebox.showerror("Import Error", f"Import failed: {result['error']}")
                
        except Exception as e:
            # Close progress window if still open
            try:
                progress_window.destroy()
            except:
                pass
            
            messagebox.showerror("Error", f"Error importing Excel file: {str(e)}")
