"""
Brasil API address lookup service implementation.
"""

import requests
from typing import Optional
import re

from ...domain.services.address_lookup_service import AddressLookupService
from ...shared.exceptions.exceptions import AddressLookupException
from ...shared.utils.config import config


class BrasilApiAddressLookupService(AddressLookupService):
    """Brasil API implementation for address lookup service."""
    
    def __init__(self):
        """Initialize service with API configuration."""
        self._base_url = config.brasil_api_base_url
        self._timeout = 10  # seconds
    
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
        
        # Clean postal code (remove non-digit characters)
        clean_postal_code = re.sub(r'\D', '', postal_code)
        
        try:
            # Make API request
            url = f"{self._base_url}/cep/v1/{clean_postal_code}"
            response = requests.get(url, timeout=self._timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Map Brasil API response to our format
                return {
                    'street': data.get('street', ''),
                    'neighborhood': data.get('neighborhood', ''),
                    'city': data.get('city', ''),
                    'state': data.get('state', ''),
                    'postal_code': clean_postal_code
                }
            
            elif response.status_code == 404:
                # Postal code not found
                return None
            
            else:
                # Other HTTP errors
                raise AddressLookupException(
                    f"API request failed with status {response.status_code}",
                    postal_code
                )
        
        except requests.exceptions.Timeout:
            raise AddressLookupException("API request timeout", postal_code)
        
        except requests.exceptions.ConnectionError:
            raise AddressLookupException("API connection error", postal_code)
        
        except requests.exceptions.RequestException as e:
            raise AddressLookupException(f"API request error: {str(e)}", postal_code)
        
        except Exception as e:
            raise AddressLookupException(f"Unexpected error: {str(e)}", postal_code)
    
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
