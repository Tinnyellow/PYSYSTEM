"""
Sales Order entities for the Sales Management System.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from .base_entity import BaseEntity
from .company import Company
from .product import Product


@dataclass
class SalesOrderItem(BaseEntity):
    """Sales order item representing a product in a sales order."""
    
    product: Optional[Product] = None
    quantity: int = 0
    unit_price: Decimal = Decimal('0.00')
    
    def __post_init__(self):
        """Initialize sales order item."""
        super().__post_init__()
        self._validate_item_data()
    
    def _validate_item_data(self) -> None:
        """Validate item data."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate item subtotal."""
        return self.unit_price * Decimal(str(self.quantity))
    
    def get_display_info(self) -> str:
        """Get formatted display information."""
        return f"{self.product.get_display_name()} - Qty: {self.quantity} - Subtotal: R$ {self.subtotal:.2f}"


@dataclass
class SalesOrder(BaseEntity):
    """Sales order entity representing a complete sales transaction."""
    
    company: Optional[Company] = None
    items: List[SalesOrderItem] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize sales order."""
        super().__post_init__()
    
    def add_item(self, product: Product, quantity: int) -> None:
        """Add item to sales order."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if not product.is_available(quantity):
            raise ValueError(f"Insufficient stock for product {product.sku}")
        
        # Check if item already exists
        existing_item = self._find_item_by_product(product)
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if not product.is_available(new_quantity):
                raise ValueError(f"Insufficient stock for product {product.sku}")
            existing_item.quantity = new_quantity
        else:
            item = SalesOrderItem(
                product=product,
                quantity=quantity,
                unit_price=product.unit_price
            )
            self.items.append(item)
        
        from datetime import datetime
        self.updated_at = datetime.now()
    
    def remove_item(self, product: Product) -> None:
        """Remove item from sales order."""
        item = self._find_item_by_product(product)
        if item:
            self.items.remove(item)
            from datetime import datetime
            self.updated_at = datetime.now()
    
    def update_item_quantity(self, product: Product, new_quantity: int) -> None:
        """Update item quantity in sales order."""
        if new_quantity <= 0:
            self.remove_item(product)
            return
        
        if not product.is_available(new_quantity):
            raise ValueError(f"Insufficient stock for product {product.sku}")
        
        item = self._find_item_by_product(product)
        if item:
            item.quantity = new_quantity
            from datetime import datetime
            self.updated_at = datetime.now()
    
    def _find_item_by_product(self, product: Product) -> SalesOrderItem:
        """Find item by product in the order."""
        for item in self.items:
            if item.product.id == product.id:
                return item
        return None
    
    @property
    def total_amount(self) -> Decimal:
        """Calculate total order amount."""
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_items(self) -> int:
        """Get total number of items in order."""
        return len(self.items)
    
    def is_valid(self) -> bool:
        """Check if order is valid for processing."""
        return len(self.items) >= 2  # Minimum 2 items as per requirements
    
    def get_order_summary(self) -> str:
        """Get formatted order summary."""
        return f"Order for {self.company.get_display_name()} - Items: {self.total_items} - Total: R$ {self.total_amount:.2f}"
