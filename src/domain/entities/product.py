"""
Product entity for the Sales Management System.
"""

from dataclasses import dataclass
from decimal import Decimal
from .base_entity import BaseEntity


@dataclass
class Product(BaseEntity):
    """Product entity representing a sellable item."""
    
    sku: str = ""
    name: str = ""
    unit_price: Decimal = Decimal('0.00')
    unit: str = "UN"
    stock_quantity: int = 0
    
    def __post_init__(self):
        """Initialize product entity."""
        super().__post_init__()
        self._validate_product_data()
    
    def _validate_product_data(self) -> None:
        """Validate product data."""
        if not self.sku or not self.sku.strip():
            raise ValueError("Product SKU cannot be empty")
        
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
        
        if not self.unit or not self.unit.strip():
            raise ValueError("Product unit cannot be empty")
        
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
    
    def update_stock(self, quantity: int) -> None:
        """Update stock quantity."""
        new_quantity = self.stock_quantity + quantity
        if new_quantity < 0:
            raise ValueError("Insufficient stock quantity")
        
        self.stock_quantity = new_quantity
        from datetime import datetime
        self.updated_at = datetime.now()
    
    def is_available(self, requested_quantity: int = 1) -> bool:
        """Check if product is available in requested quantity."""
        return self.stock_quantity >= requested_quantity
    
    def get_display_name(self) -> str:
        """Get formatted display name."""
        return f"{self.sku} - {self.name}"
