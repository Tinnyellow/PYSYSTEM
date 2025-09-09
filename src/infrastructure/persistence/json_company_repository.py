"""
JSON-based company repository implementation.
"""

import json
import os
from typing import List, Optional
from datetime import datetime

from ...domain.entities.company import Company
from ...domain.repositories.company_repository import CompanyRepository
from ...domain.value_objects.document import Document, DocumentType
from ...domain.value_objects.address import Address
from ...domain.value_objects.contact import Contact
from ...shared.utils.config import config


class JsonCompanyRepository(CompanyRepository):
    """JSON file-based company repository implementation."""
    
    def __init__(self):
        """Initialize repository with data file path."""
        self._file_path = config.get_full_data_path(config.company_data_file)
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
    
    def _entity_to_dict(self, entity: Company) -> dict:
        """Convert entity to dictionary."""
        return {
            'id': entity.id,
            'name': entity.name,
            'document': {
                'number': entity.document.number,
                'type': entity.document.document_type.value
            },
            'address': {
                'postal_code': entity.address.postal_code,
                'street': entity.address.street,
                'number': entity.address.number,
                'neighborhood': entity.address.neighborhood,
                'city': entity.address.city,
                'state': entity.address.state,
                'complement': entity.address.complement
            },
            'contact': {
                'email': entity.contact.email,
                'phone': entity.contact.phone
            },
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat()
        }
    
    def _dict_to_entity(self, data: dict) -> Company:
        """Convert dictionary to entity."""
        document_type = DocumentType.CPF if data['document']['type'] == 'CPF' else DocumentType.CNPJ
        document = Document(data['document']['number'], document_type)
        
        address = Address(
            postal_code=data['address']['postal_code'],
            street=data['address']['street'],
            number=data['address']['number'],
            neighborhood=data['address']['neighborhood'],
            city=data['address']['city'],
            state=data['address']['state'],
            complement=data['address']['complement']
        )
        
        contact = Contact(
            email=data['contact']['email'],
            phone=data['contact']['phone']
        )
        
        company = Company(
            name=data['name'],
            document=document,
            address=address,
            contact=contact
        )
        
        # Set entity metadata
        company.id = data['id']
        company.created_at = datetime.fromisoformat(data['created_at'])
        company.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return company
    
    def save(self, entity: Company) -> Company:
        """Save a company entity."""
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
    
    def find_by_id(self, entity_id: str) -> Optional[Company]:
        """Find a company by its ID."""
        data = self._load_data()
        
        for item in data:
            if item['id'] == entity_id:
                return self._dict_to_entity(item)
        
        return None
    
    def find_all(self) -> List[Company]:
        """Find all companies."""
        data = self._load_data()
        return [self._dict_to_entity(item) for item in data]
    
    def update(self, entity: Company) -> Company:
        """Update a company entity."""
        entity.updated_at = datetime.now()
        return self.save(entity)
    
    def delete(self, entity_id: str) -> bool:
        """Delete a company by its ID."""
        data = self._load_data()
        
        original_length = len(data)
        data = [item for item in data if item['id'] != entity_id]
        
        if len(data) < original_length:
            self._save_data(data)
            return True
        
        return False
    
    def exists(self, entity_id: str) -> bool:
        """Check if a company exists."""
        return self.find_by_id(entity_id) is not None
    
    def find_by_document(self, document_number: str) -> Optional[Company]:
        """Find a company by document number."""
        data = self._load_data()
        
        for item in data:
            if item['document']['number'] == document_number:
                return self._dict_to_entity(item)
        
        return None
    
    def find_by_name(self, name: str) -> List[Company]:
        """Find companies by name (partial match)."""
        data = self._load_data()
        results = []
        
        name_lower = name.lower()
        for item in data:
            if name_lower in item['name'].lower():
                results.append(self._dict_to_entity(item))
        
        return results
    
    def search(self, query: str) -> List[Company]:
        """Search companies by name or document."""
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        for item in data:
            # Search in name or document number
            if (query_lower in item['name'].lower() or 
                query_lower in item['document']['number']):
                results.append(self._dict_to_entity(item))
        
        return results
