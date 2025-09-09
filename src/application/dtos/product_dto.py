"""
Data Transfer Objects for Product operations.
"""

from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal


@dataclass
class CreateProductDTO:
    """DTO for creating a new product."""
    
    sku: str
    name: str
    unit_price: Decimal
    unit: str
    stock_quantity: int
    description: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None


@dataclass
class UpdateProductDTO:
    """DTO for updating an existing product."""
    
    sku: Optional[str] = None
    name: Optional[str] = None
    unit_price: Optional[Decimal] = None
    unit: Optional[str] = None
    stock_quantity: Optional[int] = None
    description: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None


@dataclass
class ProductResponseDTO:
    """DTO for product response data."""
    
    id: str
    sku: str
    name: str
    unit_price: Decimal
    formatted_price: str
    unit: str
    stock_quantity: int
    display_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None


@dataclass
class ExcelImportResultDTO:
    """DTO for Excel import operation result."""
    
    success: bool
    imported_count: int
    failed_count: int
    products: List[ProductResponseDTO]
    errors: List[str]
    file_path: str


@dataclass
class ProductSearchResultDTO:
    """DTO for product search results."""
    
    products: List[ProductResponseDTO]
    total_count: int
    query: str
