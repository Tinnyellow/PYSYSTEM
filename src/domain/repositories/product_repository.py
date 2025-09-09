"""
Product repository interface.
"""

from abc import abstractmethod
from typing import List, Optional
from .base_repository import BaseRepository
from ..entities.product import Product


class ProductRepository(BaseRepository[Product]):
    """Product repository interface."""
    
    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[Product]:
        """Find a product by SKU."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Product]:
        """Find products by name (partial match)."""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Product]:
        """Search products by name or SKU."""
        pass
    
    @abstractmethod
    def find_available_products(self) -> List[Product]:
        """Find products with available stock."""
        pass
    
    @abstractmethod
    def clear_all(self) -> None:
        """Clear all products (used for Excel import)."""
        pass
    
    @abstractmethod
    def save_batch(self, products: List[Product]) -> List[Product]:
        """Save multiple products at once."""
        pass
