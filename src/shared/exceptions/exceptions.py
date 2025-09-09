"""
Custom exceptions for the Sales Management System.
"""


class SalesManagementException(Exception):
    """Base exception for the Sales Management System."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationException(SalesManagementException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field_name: str = None):
        self.field_name = field_name
        super().__init__(message, "VALIDATION_ERROR")


class EntityNotFoundException(SalesManagementException):
    """Exception raised when an entity is not found."""
    
    def __init__(self, entity_type: str, entity_id: str):
        message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(message, "ENTITY_NOT_FOUND")


class DuplicateEntityException(SalesManagementException):
    """Exception raised when trying to create a duplicate entity."""
    
    def __init__(self, entity_type: str, identifier: str):
        message = f"{entity_type} with identifier '{identifier}' already exists"
        super().__init__(message, "DUPLICATE_ENTITY")


class InsufficientStockException(SalesManagementException):
    """Exception raised when there's insufficient stock for a product."""
    
    def __init__(self, product_sku: str, requested_quantity: int, available_quantity: int):
        message = f"Insufficient stock for product '{product_sku}'. Requested: {requested_quantity}, Available: {available_quantity}"
        self.product_sku = product_sku
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity
        super().__init__(message, "INSUFFICIENT_STOCK")


class DuplicateSkuException(SalesManagementException):
    """Exception raised when trying to create a product with duplicate SKU."""
    
    def __init__(self, sku: str):
        message = f"Product with SKU '{sku}' already exists"
        self.sku = sku
        super().__init__(message, "DUPLICATE_SKU")


class ExcelProcessingException(SalesManagementException):
    """Exception raised during Excel file processing."""
    
    def __init__(self, message: str, file_path: str = None):
        self.file_path = file_path
        super().__init__(message, "EXCEL_PROCESSING_ERROR")


class AddressLookupException(SalesManagementException):
    """Exception raised during address lookup operations."""
    
    def __init__(self, message: str, postal_code: str = None):
        self.postal_code = postal_code
        super().__init__(message, "ADDRESS_LOOKUP_ERROR")


class ReportGenerationException(SalesManagementException):
    """Exception raised during report generation."""
    
    def __init__(self, message: str, report_type: str = None):
        self.report_type = report_type
        super().__init__(message, "REPORT_GENERATION_ERROR")
