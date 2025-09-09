"""
JSON-based product repository implementation.
"""

import json
import os
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...shared.utils.config import config


class JsonProductRepository(ProductRepository):
    """JSON file-based product repository implementation."""
    
    def __init__(self):
        """Initialize repository with data file path."""
        self._file_path = config.get_full_data_path(config.product_data_file)
        config.ensure_directories_exist()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure data file exists."""
        if not os.path.exists(self._file_path):
            self._save_data([])
    
    def _load_data(self) -> List[dict]:
        """Load data from JSON file."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, data: List[dict]) -> None:
        """Save data to JSON file."""
        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=str)
    
    def _entity_to_dict(self, entity: Product) -> dict:
        """Convert entity to dictionary."""
        return {
            'id': entity.id,
            'sku': entity.sku,
            'name': entity.name,
            'unit_price': str(entity.unit_price),
            'unit': entity.unit,
            'stock_quantity': entity.stock_quantity,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat()
        }
    
    def _dict_to_entity(self, data: dict) -> Product:
        """Convert dictionary to entity."""
        product = Product(
            sku=data['sku'],
            name=data['name'],
            unit_price=Decimal(data['unit_price']),
            unit=data['unit'],
            stock_quantity=data['stock_quantity']
        )
        
        # Set entity metadata
        product.id = data['id']
        product.created_at = datetime.fromisoformat(data['created_at'])
        product.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return product
    
    def save(self, entity: Product) -> Product:
        """Save a product entity."""
        data = self._load_data()
        
        # Check if entity already exists
        existing_index = None
        for i, item in enumerate(data):
            if item['id'] == entity.id:
                existing_index = i
                break
        
        entity_dict = self._entity_to_dict(entity)
        
        if existing_index is not None:
            data[existing_index] = entity_dict
        else:
            data.append(entity_dict)
        
        self._save_data(data)
        return entity
    
    def find_by_id(self, entity_id: str) -> Optional[Product]:
        """Find a product by its ID."""
        data = self._load_data()
        
        for item in data:
            if item['id'] == entity_id:
                return self._dict_to_entity(item)
        
        return None
    
    def get_by_id(self, entity_id: str) -> Optional[Product]:
        """Get a product by its ID (alias for find_by_id)."""
        return self.find_by_id(entity_id)
    
    def find_all(self) -> List[Product]:
        """Find all products."""
        return [self._dict_to_entity(item) for item in self._load_data()]
    
    def get_all(self) -> List[Product]:
        """Get all products (alias for find_all)."""
        return self.find_all()
    
    def update(self, entity: Product) -> Product:
        """Update a product entity."""
        entity.updated_at = datetime.now()
        return self.save(entity)
    
    def delete(self, entity_id: str) -> bool:
        """Delete a product by its ID."""
        data = self._load_data()
        
        original_length = len(data)
        data = [item for item in data if item['id'] != entity_id]
        
        if len(data) < original_length:
            self._save_data(data)
            return True
        
        return False
    
    def exists(self, entity_id: str) -> bool:
        """Check if a product exists."""
        return self.find_by_id(entity_id) is not None
    
    def find_by_sku(self, sku: str) -> Optional[Product]:
        """Find a product by SKU."""
        data = self._load_data()
        
        for item in data:
            if item['sku'] == sku:
                return self._dict_to_entity(item)
        
        return None
    
    def find_by_name(self, name: str) -> List[Product]:
        """Find products by name (partial match)."""
        data = self._load_data()
        results = []
        
        name_lower = name.lower()
        for item in data:
            if name_lower in item['name'].lower():
                results.append(self._dict_to_entity(item))
        
        return results
    
    def search(self, query: str) -> List[Product]:
        """Search products by name or SKU."""
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        for item in data:
            # Search in name or SKU
            if (query_lower in item['name'].lower() or 
                query_lower in item['sku'].lower()):
                results.append(self._dict_to_entity(item))
        
        return results
    
    def find_available_products(self) -> List[Product]:
        """Find products with available stock."""
        data = self._load_data()
        results = []
        
        for item in data:
            if item['stock_quantity'] > 0:
                results.append(self._dict_to_entity(item))
        
        return results
    
    def clear_all(self) -> None:
        """Clear all products (used for Excel import)."""
        self._save_data([])
    
    def save_batch(self, products: List[Product]) -> List[Product]:
        """Save multiple products at once."""
        data = []
        
        for product in products:
            data.append(self._entity_to_dict(product))
        
        self._save_data(data)
        return products
