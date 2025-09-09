"""
Brasil API address lookup service implementation.
"""

import requests
from typing import Optional
import re

from ...domain.services.address_lookup_service import AddressLookupService
from ...shared.exceptions.exceptions import AddressLookupException
from ...shared.utils.config import config
from .brasilapi_service import BrasilApiService


class BrasilApiAddressLookupService(AddressLookupService):
    """Brasil API implementation for address lookup service."""
    
    def __init__(self):
        """Initialize service with BrasilAPI service."""
        self._brasil_api = BrasilApiService()
    
    def lookup_address_by_postal_code(self, postal_code: str) -> Optional[dict]:
        """
        Lookup address information by postal code using Brasil API.
        
        Args:
            postal_code: The postal code to lookup
            
        Returns:
            Dictionary with address information or None if not found
        """
        if not self.is_valid_postal_code(postal_code):
            raise AddressLookupException("Invalid postal code format", postal_code)
        
        try:
            # Use BrasilAPI service
            result = self._brasil_api.get_cep_info(postal_code)
            
            if result:
                # Map BrasilAPI response to our format
                return {
                    'street': result.get('street', ''),
                    'neighborhood': result.get('neighborhood', ''),
                    'city': result.get('city', ''),
                    'state': result.get('state', ''),
                    'postal_code': result.get('cep', postal_code)
                }
            else:
                # Address not found
                return None
        
        except Exception as e:
            raise AddressLookupException(f"Address lookup error: {str(e)}", postal_code)
    
    def is_valid_postal_code(self, postal_code: str) -> bool:
        """
        Check if postal code format is valid.
        
        Args:
            postal_code: The postal code to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not postal_code:
            return False
        
        # Clean postal code (remove non-digit characters)
        clean_postal_code = re.sub(r'\D', '', postal_code)
        
        # Brazilian postal code should have exactly 8 digits
        return len(clean_postal_code) == 8 and clean_postal_code.isdigit()
