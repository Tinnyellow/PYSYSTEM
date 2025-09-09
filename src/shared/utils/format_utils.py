"""
Format utilities for the Sales Management System.
"""

import re
from decimal import Decimal
from typing import Union


class FormatUtils:
    """Utility class for formatting operations."""
    
    @staticmethod
    def format_currency(amount: Union[Decimal, float, int]) -> str:
        """Format amount as Brazilian Real currency."""
        if isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        return f"R$ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def format_document(document: str, document_type: str = None) -> str:
        """Format document number (CPF/CNPJ)."""
        # Remove non-digit characters
        clean_doc = re.sub(r'\D', '', document)
        
        if len(clean_doc) == 11:  # CPF
            return f"{clean_doc[:3]}.{clean_doc[3:6]}.{clean_doc[6:9]}-{clean_doc[9:]}"
        elif len(clean_doc) == 14:  # CNPJ
            return f"{clean_doc[:2]}.{clean_doc[2:5]}.{clean_doc[5:8]}/{clean_doc[8:12]}-{clean_doc[12:]}"
        
        return document
    
    @staticmethod
    def format_postal_code(postal_code: str) -> str:
        """Format postal code (CEP)."""
        clean_cep = re.sub(r'\D', '', postal_code)
        if len(clean_cep) == 8:
            return f"{clean_cep[:5]}-{clean_cep[5:]}"
        return postal_code
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Format Brazilian phone number."""
        clean_phone = re.sub(r'\D', '', phone)
        
        if len(clean_phone) == 10:  # Landline
            return f"({clean_phone[:2]}) {clean_phone[2:6]}-{clean_phone[6:]}"
        elif len(clean_phone) == 11:  # Mobile
            return f"({clean_phone[:2]}) {clean_phone[2:7]}-{clean_phone[7:]}"
        
        return phone
    
    @staticmethod
    def clean_numeric_string(value: str) -> str:
        """Remove non-digit characters from string."""
        return re.sub(r'\D', '', value)
    
    @staticmethod
    def parse_decimal(value: Union[str, int, float]) -> Decimal:
        """Parse value to Decimal safely."""
        if isinstance(value, str):
            # Handle Brazilian decimal format (comma as decimal separator)
            value = value.replace(',', '.')
        
        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return Decimal('0')
    
    @staticmethod
    def format_percentage(value: Union[Decimal, float, int], decimal_places: int = 2) -> str:
        """Format value as percentage."""
        if isinstance(value, (int, float)):
            value = Decimal(str(value))
        
        return f"{value:.{decimal_places}f}%"
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length with suffix."""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
