"""
JSON-based sales order repository implementation.
"""

import json
import os
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from ...domain.entities.sales_order import SalesOrder, SalesOrderItem
from ...domain.entities.company import Company
from ...domain.entities.product import Product
from ...domain.repositories.sales_order_repository import SalesOrderRepository
from ...domain.value_objects.document import Document, DocumentType
from ...domain.value_objects.address import Address
from ...domain.value_objects.contact import Contact
from ...shared.utils.config import config


class JsonSalesOrderRepository(SalesOrderRepository):
    """JSON file-based sales order repository implementation."""
    
    def __init__(self):
        """Initialize repository with data file path."""
        self._file_path = config.get_full_data_path(config.sales_order_data_file)
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
    
    def _entity_to_dict(self, entity: SalesOrder) -> dict:
        """Convert entity to dictionary."""
        return {
            'id': entity.id,
            'company': {
                'id': entity.company.id,
                'name': entity.company.name,
                'document': {
                    'number': entity.company.document.number,
                    'type': entity.company.document.document_type.value
                },
                'address': {
                    'postal_code': entity.company.address.postal_code,
                    'street': entity.company.address.street,
                    'number': entity.company.address.number,
                    'neighborhood': entity.company.address.neighborhood,
                    'city': entity.company.address.city,
                    'state': entity.company.address.state,
                    'complement': entity.company.address.complement
                },
                'contact': {
                    'email': entity.company.contact.email,
                    'phone': entity.company.contact.phone
                }
            },
            'items': [
                {
                    'id': item.id,
                    'product': {
                        'id': item.product.id,
                        'sku': item.product.sku,
                        'name': item.product.name,
                        'unit_price': str(item.product.unit_price),
                        'unit': item.product.unit,
                        'stock_quantity': item.product.stock_quantity
                    },
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'created_at': item.created_at.isoformat(),
                    'updated_at': item.updated_at.isoformat()
                }
                for item in entity.items
            ],
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat()
        }
    
    def _dict_to_entity(self, data: dict) -> SalesOrder:
        """Convert dictionary to entity."""
        # Reconstruct company
        company_data = data['company']
        document_type = DocumentType.CPF if company_data['document']['type'] == 'CPF' else DocumentType.CNPJ
        document = Document(company_data['document']['number'], document_type)
        
        address = Address(
            postal_code=company_data['address']['postal_code'],
            street=company_data['address']['street'],
            number=company_data['address']['number'],
            neighborhood=company_data['address']['neighborhood'],
            city=company_data['address']['city'],
            state=company_data['address']['state'],
            complement=company_data['address']['complement']
        )
        
        contact = Contact(
            email=company_data['contact']['email'],
            phone=company_data['contact']['phone']
        )
        
        company = Company(
            name=company_data['name'],
            document=document,
            address=address,
            contact=contact
        )
        company.id = company_data['id']
        
        # Create sales order
        sales_order = SalesOrder(company=company)
        sales_order.id = data['id']
        sales_order.created_at = datetime.fromisoformat(data['created_at'])
        sales_order.updated_at = datetime.fromisoformat(data['updated_at'])
        
        # Reconstruct items
        items = []
        for item_data in data['items']:
            product_data = item_data['product']
            product = Product(
                sku=product_data['sku'],
                name=product_data['name'],
                unit_price=Decimal(product_data['unit_price']),
                unit=product_data['unit'],
                stock_quantity=product_data['stock_quantity']
            )
            product.id = product_data['id']
            
            item = SalesOrderItem(
                product=product,
                quantity=item_data['quantity'],
                unit_price=Decimal(item_data['unit_price'])
            )
            item.id = item_data['id']
            item.created_at = datetime.fromisoformat(item_data['created_at'])
            item.updated_at = datetime.fromisoformat(item_data['updated_at'])
            
            items.append(item)
        
        sales_order.items = items
        return sales_order
    
    def save(self, entity: SalesOrder) -> SalesOrder:
        """Save a sales order entity."""
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
    
    def find_by_id(self, entity_id: str) -> Optional[SalesOrder]:
        """Find a sales order by its ID."""
        data = self._load_data()
        
        for item in data:
            if item['id'] == entity_id:
                return self._dict_to_entity(item)
        
        return None
    
    def find_all(self) -> List[SalesOrder]:
        """Find all sales orders."""
        data = self._load_data()
        return [self._dict_to_entity(item) for item in data]
    
    def update(self, entity: SalesOrder) -> SalesOrder:
        """Update a sales order entity."""
        entity.updated_at = datetime.now()
        return self.save(entity)
    
    def delete(self, entity_id: str) -> bool:
        """Delete a sales order by its ID."""
        data = self._load_data()
        
        original_length = len(data)
        data = [item for item in data if item['id'] != entity_id]
        
        if len(data) < original_length:
            self._save_data(data)
            return True
        
        return False
    
    def exists(self, entity_id: str) -> bool:
        """Check if a sales order exists."""
        return self.find_by_id(entity_id) is not None
    
    def find_by_company_id(self, company_id: str) -> List[SalesOrder]:
        """Find sales orders by company ID."""
        data = self._load_data()
        results = []
        
        for item in data:
            if item['company']['id'] == company_id:
                results.append(self._dict_to_entity(item))
        
        return results
    
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SalesOrder]:
        """Find sales orders within date range."""
        data = self._load_data()
        results = []
        
        for item in data:
            created_at = datetime.fromisoformat(item['created_at'])
            if start_date <= created_at <= end_date:
                results.append(self._dict_to_entity(item))
        
        return results
    
    def get_order_summary(self) -> dict:
        """Get order summary statistics."""
        data = self._load_data()
        
        if not data:
            return {
                'total_orders': 0,
                'total_amount': 0,
                'average_order_value': 0,
                'total_items': 0
            }
        
        total_orders = len(data)
        total_amount = Decimal('0')
        total_items = 0
        
        for item in data:
            order_total = Decimal('0')
            for order_item in item['items']:
                item_subtotal = Decimal(order_item['unit_price']) * Decimal(str(order_item['quantity']))
                order_total += item_subtotal
                total_items += order_item['quantity']
            
            total_amount += order_total
        
        average_order_value = total_amount / total_orders if total_orders > 0 else Decimal('0')
        
        return {
            'total_orders': total_orders,
            'total_amount': float(total_amount),
            'average_order_value': float(average_order_value),
            'total_items': total_items
        }
