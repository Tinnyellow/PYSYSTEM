"""
Company management frame for the GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional

from ...application.dtos.company_dto import CreateCompanyDTO, UpdateCompanyDTO, CompanyResponseDTO
from ...presentation.controllers.company_controller import CompanyController
from ...presentation.validators.form_validator import FormValidator
from ...presentation.validators.input_formatter import InputFormatter
from ...shared.exceptions.exceptions import ValidationException, SalesManagementException, DuplicateEntityException


class CompanyManagementFrame:
    """Frame for managing companies."""
    
    def __init__(self, parent: tk.Widget, controller: CompanyController):
        """Initialize company management frame."""
        self.parent = parent
        self.controller = controller
        self.validator = FormValidator()
        self.formatter = InputFormatter()
        
        self.frame = ttk.Frame(parent)
        self._setup_ui()
        self._load_companies()
    
    def _setup_ui(self):
        """Setup user interface."""
        # Main paned window
        self.paned_window = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Company list
        self._create_list_panel()
        
        # Right panel - Company form
        self._create_form_panel()
    
    def _create_list_panel(self):
        """Create company list panel."""
        list_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(list_frame, weight=1)
        
        # Title
        title_label = ttk.Label(list_frame, text="Companies", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Company treeview
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Document', 'Type')
        self.company_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.company_tree.heading('ID', text='ID')
        self.company_tree.heading('Name', text='Company Name')
        self.company_tree.heading('Document', text='Document')
        self.company_tree.heading('Type', text='Type')
        
        self.company_tree.column('ID', width=50, minwidth=50)
        self.company_tree.column('Name', width=200, minwidth=150)
        self.company_tree.column('Document', width=120, minwidth=100)
        self.company_tree.column('Type', width=80, minwidth=60)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.company_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.company_tree.xview)
        self.company_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.company_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.company_tree.bind('<<TreeviewSelect>>', self._on_company_selected)
        self.company_tree.bind('<Double-1>', self._on_company_double_click)
        
        # Buttons frame with modern styling
        buttons_frame = ttk.Frame(list_frame, style='Card.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(10, 0), padx=5)
        
        # Create styled buttons with icons
        new_btn = ttk.Button(buttons_frame, text="➕ New", command=self._new_company, style='Action.TButton')
        new_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        edit_btn = ttk.Button(buttons_frame, text="✏️ Edit", command=self._edit_company, style='Action.TButton')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = ttk.Button(buttons_frame, text="🗑️ Delete", command=self._delete_company, style='Action.TButton')
        delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = ttk.Button(buttons_frame, text="🔄 Refresh", command=self._load_companies, style='Action.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 5))
    
    def _create_form_panel(self):
        """Create company form panel."""
        form_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(form_frame, weight=1)
        
        # Title
        self.form_title = ttk.Label(form_frame, text="Company Details", style='Title.TLabel')
        self.form_title.pack(pady=(0, 20))
        
        # Scrollable frame for form
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        self._create_form_fields()
        
        # Buttons
        self._create_form_buttons()
    
    def _create_form_fields(self):
        """Create form input fields."""
        # Basic Information
        basic_frame = ttk.LabelFrame(self.scrollable_frame, text="Basic Information", padding=10)
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Company Name
        ttk.Label(basic_frame, text="Company Name *:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(basic_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky='ew', pady=(0, 5))
        
        # Document
        ttk.Label(basic_frame, text="Document (CPF/CNPJ) *:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.document_var = tk.StringVar()
        document_entry = ttk.Entry(basic_frame, textvariable=self.document_var, width=40)
        document_entry.grid(row=1, column=1, sticky='ew', pady=(0, 5))
        document_entry.bind('<KeyRelease>', self._format_document)
        
        # Document Type (auto-detected)
        ttk.Label(basic_frame, text="Document Type:").grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.document_type_var = tk.StringVar()
        document_type_label = ttk.Label(basic_frame, textvariable=self.document_type_var, foreground='gray')
        document_type_label.grid(row=2, column=1, sticky='w', pady=(0, 5))
        
        basic_frame.grid_columnconfigure(1, weight=1)
        
        # Contact Information
        contact_frame = ttk.LabelFrame(self.scrollable_frame, text="Contact Information", padding=10)
        contact_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        ttk.Label(contact_frame, text="Email:").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.email_var = tk.StringVar()
        ttk.Entry(contact_frame, textvariable=self.email_var, width=40).grid(row=0, column=1, sticky='ew', pady=(0, 5))
        
        # Phone
        ttk.Label(contact_frame, text="Phone:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(contact_frame, textvariable=self.phone_var, width=40)
        phone_entry.grid(row=1, column=1, sticky='ew', pady=(0, 5))
        phone_entry.bind('<KeyRelease>', self._format_phone)
        
        contact_frame.grid_columnconfigure(1, weight=1)
        
        # Address Information
        address_frame = ttk.LabelFrame(self.scrollable_frame, text="Address Information", padding=10)
        address_frame.pack(fill=tk.X, pady=(0, 10))
        
        # CEP with modern lookup button
        cep_frame = ttk.Frame(address_frame)
        cep_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        
        ttk.Label(cep_frame, text="CEP:", style='Header.TLabel').pack(side=tk.LEFT)
        self.cep_var = tk.StringVar()
        cep_entry = ttk.Entry(cep_frame, textvariable=self.cep_var, width=15)
        cep_entry.pack(side=tk.LEFT, padx=(5, 5))
        cep_entry.bind('<KeyRelease>', self._format_cep)
        
        lookup_btn = ttk.Button(cep_frame, text="🔍 Lookup", command=self._lookup_address, style='Action.TButton')
        lookup_btn.pack(side=tk.LEFT)
        
        # Street
        ttk.Label(address_frame, text="Street:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.street_var = tk.StringVar()
        ttk.Entry(address_frame, textvariable=self.street_var, width=40).grid(row=1, column=1, sticky='ew', pady=(0, 5))
        
        # Number and Complement
        number_frame = ttk.Frame(address_frame)
        number_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        
        ttk.Label(number_frame, text="Number:").pack(side=tk.LEFT)
        self.number_var = tk.StringVar()
        ttk.Entry(number_frame, textvariable=self.number_var, width=10).pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(number_frame, text="Complement:").pack(side=tk.LEFT)
        self.complement_var = tk.StringVar()
        ttk.Entry(number_frame, textvariable=self.complement_var, width=20).pack(side=tk.LEFT, padx=(5, 0))
        
        # Neighborhood
        ttk.Label(address_frame, text="Neighborhood:").grid(row=3, column=0, sticky='w', pady=(0, 5))
        self.neighborhood_var = tk.StringVar()
        ttk.Entry(address_frame, textvariable=self.neighborhood_var, width=40).grid(row=3, column=1, sticky='ew', pady=(0, 5))
        
        # City and State
        city_frame = ttk.Frame(address_frame)
        city_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        
        ttk.Label(city_frame, text="City:").pack(side=tk.LEFT)
        self.city_var = tk.StringVar()
        ttk.Entry(city_frame, textvariable=self.city_var, width=25).pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(city_frame, text="State:").pack(side=tk.LEFT)
        self.state_var = tk.StringVar()
        ttk.Entry(city_frame, textvariable=self.state_var, width=5).pack(side=tk.LEFT, padx=(5, 0))
        
        address_frame.grid_columnconfigure(1, weight=1)
        
        # Required fields note
        note_label = ttk.Label(self.scrollable_frame, text="* Required fields", foreground='red', font=('Arial', 8))
        note_label.pack(pady=(10, 0))
    
    def _create_form_buttons(self):
        """Create enhanced form action buttons."""
        buttons_frame = ttk.Frame(self.scrollable_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Primary action button (Save)
        self.save_button = ttk.Button(
            buttons_frame, 
            text="💾 Save Company", 
            command=self._save_company,
            style='Action.TButton'
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Secondary action button (Cancel)
        self.cancel_button = ttk.Button(
            buttons_frame, 
            text="❌ Cancel", 
            command=self._cancel_form
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button (right side)
        self.clear_button = ttk.Button(
            buttons_frame, 
            text="🗑️ Clear Form", 
            command=self._clear_form
        )
        self.clear_button.pack(side=tk.RIGHT)
        
        # Initially disable save button
        self.save_button.config(state='disabled')
        
        # Current company ID for editing
        self.current_company_id: Optional[str] = None
    
    def _load_companies(self):
        """Load companies into the tree view."""
        try:
            companies = self.controller.list_companies()
            self._populate_tree(companies)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading companies: {str(e)}")
    
    def _populate_tree(self, companies: List[CompanyResponseDTO]):
        """Populate tree view with companies."""
        # Clear existing items
        for item in self.company_tree.get_children():
            self.company_tree.delete(item)
        
        # Add companies
        for company in companies:
            document_type = "CNPJ" if len(company.document_number.replace(".", "").replace("/", "").replace("-", "")) == 14 else "CPF"
            self.company_tree.insert('', 'end', values=(
                company.id,
                company.name,
                company.document_number,
                document_type
            ))
    
    def _on_search_changed(self, *args):
        """Handle search text change."""
        search_text = self.search_var.get().lower()
        if not search_text:
            self._load_companies()
            return
        
        try:
            all_companies = self.controller.list_companies()
            filtered_companies = [
                company for company in all_companies
                if (search_text in company.name.lower() or 
                    search_text in company.document_number.lower())
            ]
            self._populate_tree(filtered_companies)
        except Exception as e:
            messagebox.showerror("Error", f"Error searching companies: {str(e)}")
    
    def _on_company_selected(self, event):
        """Handle company selection in tree view."""
        selection = self.company_tree.selection()
        if selection:
            item = self.company_tree.item(selection[0])
            company_id = item['values'][0]
            self._load_company_details(company_id)
    
    def _on_company_double_click(self, event):
        """Handle double-click on company (edit mode)."""
        self._edit_company()
    
    def _load_company_details(self, company_id: str):
        """Load company details into form."""
        try:
            company = self.controller.get_company(company_id)
            if company:
                self._populate_form(company)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading company details: {str(e)}")
    
    def _populate_form(self, company: CompanyResponseDTO):
        """Populate form with company data."""
        # Clear form first
        self._clear_form()
        
        # Basic information
        self.name_var.set(company.name)
        self.document_var.set(company.document_number)
        
        # Contact information
        self.email_var.set(company.email or "")
        self.phone_var.set(company.phone or "")
        
        # Address information - will be populated when editing
        # For now, clear address fields
        self.cep_var.set("")
        self.street_var.set("")
        self.number_var.set("")
        self.complement_var.set("")
        self.neighborhood_var.set("")
        self.city_var.set("")
        self.state_var.set("")
        
        # Update document type display
        self._update_document_type()
        
        # Set current company ID
        self.current_company_id = company.id
        
        # Update form title and button state
        self.form_title.config(text=f"Company Details - {company.name}")
        self.save_button.config(state='normal')
    
    def _clear_form(self):
        """Clear all form fields."""
        # Clear all variables
        self.name_var.set("")
        self.document_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.cep_var.set("")
        self.street_var.set("")
        self.number_var.set("")
        self.complement_var.set("")
        self.neighborhood_var.set("")
        self.city_var.set("")
        self.state_var.set("")
        
        # Clear document type
        self.document_type_var.set("")
        
        # Reset form state
        self.current_company_id = None
        self.form_title.config(text="Company Details")
        self.save_button.config(state='disabled')
    
    def _new_company(self):
        """Start creating a new company."""
        self._clear_form()
        self.form_title.config(text="New Company")
        self.save_button.config(state='normal')
    
    def _edit_company(self):
        """Edit selected company."""
        selection = self.company_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a company to edit.")
            return
        
        item = self.company_tree.item(selection[0])
        company_id = item['values'][0]
        self._load_company_details(company_id)
        self.form_title.config(text=f"Edit Company - {self.name_var.get()}")
    
    def _delete_company(self):
        """Delete selected company."""
        selection = self.company_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a company to delete.")
            return
        
        item = self.company_tree.item(selection[0])
        company_id = item['values'][0]
        company_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{company_name}'?\n"
                              "This action cannot be undone."):
            try:
                self.controller.delete_company(company_id)
                self._load_companies()
                self._clear_form()
                messagebox.showinfo("Success", "Company deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting company: {str(e)}")
    
    def _save_company(self):
        """Save company data."""
        try:
            # Validate required fields
            if not self.name_var.get().strip():
                messagebox.showerror("Validation Error", "Company name is required.")
                return
            
            if not self.document_var.get().strip():
                messagebox.showerror("Validation Error", "Document is required.")
                return
            
            # Create DTO
            if self.current_company_id:
                # Update existing company
                dto = UpdateCompanyDTO(
                    name=self.name_var.get().strip(),
                    document=self.document_var.get().strip(),
                    email=self.email_var.get().strip() or None,
                    phone=self.phone_var.get().strip() or None,
                    postal_code=self.cep_var.get().strip() or None,
                    street=self.street_var.get().strip() or None,
                    number=self.number_var.get().strip() or None,
                    complement=self.complement_var.get().strip() or None,
                    neighborhood=self.neighborhood_var.get().strip() or None,
                    city=self.city_var.get().strip() or None,
                    state=self.state_var.get().strip() or None
                )
                self.controller.update_company(self.current_company_id, dto)
                message = "Company updated successfully."
            else:
                # Create new company
                dto = CreateCompanyDTO(
                    name=self.name_var.get().strip(),
                    document=self.document_var.get().strip(),
                    email=self.email_var.get().strip() or None,
                    phone=self.phone_var.get().strip() or None,
                    postal_code=self.cep_var.get().strip() or None,
                    street=self.street_var.get().strip() or None,
                    number=self.number_var.get().strip() or None,
                    complement=self.complement_var.get().strip() or None,
                    neighborhood=self.neighborhood_var.get().strip() or None,
                    city=self.city_var.get().strip() or None,
                    state=self.state_var.get().strip() or None
                )
                self.controller.create_company(dto)
                message = "Company created successfully."
            
            # Refresh list and clear form
            self._load_companies()
            self._clear_form()
            messagebox.showinfo("Success", message)
            
        except (ValidationException, DuplicateEntityException) as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error saving company: {str(e)}")
    
    def _cancel_form(self):
        """Cancel form editing."""
        if self.current_company_id:
            # Reload current company data
            self._load_company_details(self.current_company_id)
        else:
            self._clear_form()
    
    def _format_document(self, event):
        """Format document input and detect type."""
        value = self.document_var.get()
        formatted_value = self.formatter.format_document(value)
        
        if formatted_value != value:
            self.document_var.set(formatted_value)
        
        self._update_document_type()
    
    def _format_phone(self, event):
        """Format phone input."""
        value = self.phone_var.get()
        formatted_value = self.formatter.format_phone(value)
        
        if formatted_value != value:
            self.phone_var.set(formatted_value)
    
    def _format_cep(self, event):
        """Format CEP input."""
        value = self.cep_var.get()
        formatted_value = self.formatter.format_postal_code_input(value)
        if formatted_value != value:
            self.cep_var.set(formatted_value)
    
    def _update_document_type(self):
        """Update document type display based on document length."""
        document = self.document_var.get().replace(".", "").replace("/", "").replace("-", "")
        if len(document) == 11:
            self.document_type_var.set("CPF")
        elif len(document) == 14:
            self.document_type_var.set("CNPJ")
        else:
            self.document_type_var.set("Invalid")
    
    def _lookup_address(self):
        """Lookup address by CEP."""
        cep = self.cep_var.get().strip()
        if not cep:
            messagebox.showwarning("Warning", "Please enter a CEP to lookup.")
            return
        
        try:
            # Show loading message
            self.parent.update_idletasks()
            
            # Call controller to lookup address
            address_data = self.controller.lookup_address(cep)
            
            if address_data:
                # Populate address fields
                self.street_var.set(address_data.get('street', ''))
                self.neighborhood_var.set(address_data.get('neighborhood', ''))
                self.city_var.set(address_data.get('city', ''))
                self.state_var.set(address_data.get('state', ''))
                
                messagebox.showinfo("Success", "Address found and populated.")
            else:
                messagebox.showwarning("Warning", "Address not found for the provided CEP.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error looking up address: {str(e)}")
