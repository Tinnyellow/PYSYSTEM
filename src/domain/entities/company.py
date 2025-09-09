"""
Company entity for the Sales Management System.
"""

from dataclasses import dataclass
from typing import Optional
from .base_entity import BaseEntity
from ..value_objects.document import Document
from ..value_objects.address import Address
from ..value_objects.contact import Contact


@dataclass
class Company(BaseEntity):
    """Company entity representing a business entity."""
    
    name: str = ""
    document: Optional[Document] = None
    address: Optional[Address] = None
    contact: Optional[Contact] = None
    
    def __post_init__(self):
        """Initialize company entity."""
        super().__post_init__()
        if not self.name or not self.name.strip():
            raise ValueError("Company name cannot be empty")
    
    def update_info(self, name: Optional[str] = None, 
                   document: Optional[Document] = None,
                   address: Optional[Address] = None,
                   contact: Optional[Contact] = None) -> None:
        """Update company information."""
        if name is not None:
            if not name.strip():
                raise ValueError("Company name cannot be empty")
            self.name = name
        
        if document is not None:
            self.document = document
            
        if address is not None:
            self.address = address
            
        if contact is not None:
            self.contact = contact
            
        from datetime import datetime
        self.updated_at = datetime.now()
    
    def get_display_name(self) -> str:
        """Get formatted display name."""
        return f"{self.name} ({self.document.number})"
