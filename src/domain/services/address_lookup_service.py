"""
Address lookup service interface.
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..value_objects.address import Address


class AddressLookupService(ABC):
    """Address lookup service interface for CEP validation and autocomplete."""
    
    @abstractmethod
    def lookup_address_by_postal_code(self, postal_code: str) -> Optional[dict]:
        """
        Lookup address information by postal code.
        
        Args:
            postal_code: The postal code to lookup
            
        Returns:
            Dictionary with address information or None if not found
        """
        pass
    
    @abstractmethod
    def is_valid_postal_code(self, postal_code: str) -> bool:
        """
        Check if postal code format is valid.
        
        Args:
            postal_code: The postal code to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
