"""
Address value object with CEP validation.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class Address:
    """Address value object with validation."""
    
    postal_code: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    complement: Optional[str] = None
    
    def __post_init__(self):
        """Validate address after initialization."""
        # Clean postal code
        clean_postal_code = re.sub(r'\D', '', self.postal_code)
        object.__setattr__(self, 'postal_code', clean_postal_code)
        
        self._validate_address()
    
    def _validate_address(self) -> None:
        """Validate address data."""
        if not self.postal_code or len(self.postal_code) != 8:
            raise ValueError("Postal code must have 8 digits")
        
        if not self.street or not self.street.strip():
            raise ValueError("Street cannot be empty")
        
        if not self.number or not self.number.strip():
            raise ValueError("Number cannot be empty")
        
        if not self.neighborhood or not self.neighborhood.strip():
            raise ValueError("Neighborhood cannot be empty")
        
        if not self.city or not self.city.strip():
            raise ValueError("City cannot be empty")
        
        if not self.state or not self.state.strip():
            raise ValueError("State cannot be empty")
        
        if len(self.state) != 2:
            raise ValueError("State must have 2 characters")
    
    def get_formatted_postal_code(self) -> str:
        """Get formatted postal code."""
        return f"{self.postal_code[:5]}-{self.postal_code[5:]}"
    
    def get_full_address(self) -> str:
        """Get complete formatted address."""
        address_parts = [
            f"{self.street}, {self.number}",
            self.complement if self.complement else "",
            self.neighborhood,
            f"{self.city} - {self.state}",
            f"CEP: {self.get_formatted_postal_code()}"
        ]
        
        # Filter out empty parts
        return "\n".join(part for part in address_parts if part.strip())
    
    def get_inline_address(self) -> str:
        """Get single line formatted address."""
        parts = [
            f"{self.street}, {self.number}",
            self.complement if self.complement else "",
            self.neighborhood,
            f"{self.city}/{self.state}",
            f"CEP: {self.get_formatted_postal_code()}"
        ]
        
        # Filter out empty parts and join with comma
        return ", ".join(part for part in parts if part.strip())
    
    def __str__(self) -> str:
        """String representation."""
        return self.get_inline_address()
