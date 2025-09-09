"""
Product controller for handling product operations.
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal

# Import DTOs
from ...application.dtos.product_dto import (
    CreateProductDTO,
    UpdateProductDTO, 
    ProductResponseDTO
)

# Import domain entities
from ...domain.entities.product import Product

# Import use cases
from ...application.use_cases.product_use_cases import ProductUseCases


class ProductController:
    """Controller for product management operations."""
    
    def __init__(self, product_use_cases: ProductUseCases):
        """Initialize controller with aggregated use cases."""
        self.product_use_cases = product_use_cases
    
    def create_product(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """Create a new product."""
        return self.product_use_cases.create.execute(dto)
    
    def update_product(self, product_id: str, dto: UpdateProductDTO) -> ProductResponseDTO:
        """Update an existing product."""
        return self.product_use_cases.update.execute(product_id, dto)
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        try:
            return self.product_use_cases.get_by_sku(sku)
        except Exception as e:
            print(f"Error getting product by SKU: {e}")
            return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Update product stock quantity."""
        try:
            return self.product_use_cases.update_stock(product_id, new_stock)
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False

    def get_available_products(self) -> List[Product]:
        """Get all products with stock available."""
        try:
            return self.product_use_cases.get_available()
        except Exception as e:
            print(f"Error getting available products: {e}")
            return []

    def search_products(self, search_term: str) -> List[Product]:
        """Search products by term."""
        try:
            return self.product_use_cases.search_products(search_term)
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_product(self, product_id: str) -> Optional[ProductResponseDTO]:
        """Get a product by ID."""
        return self.product_use_cases.get.execute(product_id)
    
    def get_product_by_sku(self, sku: str) -> Optional[ProductResponseDTO]:
        """Get a product by SKU."""
        products = self.list_products()
        for product in products:
            if product.sku == sku:
                return product
        return None
    
    def list_products(self) -> List[ProductResponseDTO]:
        """List all products."""
        return self.product_use_cases.list.execute()
    
    def search_products(self, query: str) -> List[ProductResponseDTO]:
        """Search products by query."""
        return self.product_use_cases.search.execute(query)
    
    def get_available_products(self) -> List[ProductResponseDTO]:
        """Get products with stock available."""
        return self.product_use_cases.get_available.execute()
    
    def import_products_from_excel(self, file_path: str) -> Dict[str, Any]:
        """Import products from Excel file."""
        try:
            result = self.product_use_cases.import_from_excel.execute(file_path)
            return {
                'success': True,
                'total': result.imported_count + result.failed_count,
                'created': result.imported_count,
                'updated': 0,  # Not implemented yet
                'errors': result.errors
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'total': 0,
                'created': 0,
                'updated': 0,
                'errors': []
            }
    
    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Update product stock quantity."""
        try:
            return self.product_use_cases.update_stock(product_id, new_stock)
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
