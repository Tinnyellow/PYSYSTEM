"""
Input formatting utilities for GUI forms.
"""

import re
from typing import Callable


class InputFormatter:
    """Input formatting utility class for GUI inputs."""
    
    @staticmethod
    def format_document_input(text: str) -> str:
        """
        Format document input with appropriate mask (CPF/CNPJ).
        
        Args:
            text: Raw input text
            
        Returns:
            Formatted text
        """
        # Remove non-digit characters
        digits = re.sub(r'\D', '', text)
        
        # Limit to 14 digits (CNPJ)
        digits = digits[:14]
        
        # Apply formatting based on length
        if len(digits) <= 11:  # CPF format
            if len(digits) <= 3:
                return digits
            elif len(digits) <= 6:
                return f"{digits[:3]}.{digits[3:]}"
            elif len(digits) <= 9:
                return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
            else:
                return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        else:  # CNPJ format
            if len(digits) <= 2:
                return digits
            elif len(digits) <= 5:
                return f"{digits[:2]}.{digits[2:]}"
            elif len(digits) <= 8:
                return f"{digits[:2]}.{digits[2:5]}.{digits[5:]}"
            elif len(digits) <= 12:
                return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:]}"
            else:
                return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    
    @staticmethod
    def format_postal_code_input(text: str) -> str:
        """
        Format postal code input with CEP mask.
        
        Args:
            text: Raw input text
            
        Returns:
            Formatted text
        """
        # Remove non-digit characters
        digits = re.sub(r'\D', '', text)
        
        # Limit to 8 digits
        digits = digits[:8]
        
        # Apply formatting
        if len(digits) <= 5:
            return digits
        else:
            return f"{digits[:5]}-{digits[5:]}"
    
    @staticmethod
    def format_phone_input(text: str) -> str:
        """
        Format phone input with Brazilian phone mask.
        
        Args:
            text: Raw input text
            
        Returns:
            Formatted text
        """
        # Remove non-digit characters
        digits = re.sub(r'\D', '', text)
        
        # Limit to 11 digits (mobile with area code)
        digits = digits[:11]
        
        # Apply formatting
        if len(digits) <= 2:
            return f"({digits}" if digits else ""
        elif len(digits) <= 6:
            return f"({digits[:2]}) {digits[2:]}"
        elif len(digits) == 10:  # Landline
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        else:  # Mobile
            return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    
    @staticmethod
    def format_currency_input(text: str) -> str:
        """
        Format currency input.
        
        Args:
            text: Raw input text
            
        Returns:
            Formatted text
        """
        # Remove all non-digit characters except comma and dot
        cleaned = re.sub(r'[^\d,.]', '', text)
        
        # Replace comma with dot for decimal separator
        cleaned = cleaned.replace(',', '.')
        
        # Ensure only one decimal separator
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = parts[0] + '.' + ''.join(parts[1:])
        
        # Limit decimal places to 2
        if '.' in cleaned:
            integer_part, decimal_part = cleaned.split('.')
            decimal_part = decimal_part[:2]
            cleaned = f"{integer_part}.{decimal_part}"
        
        return cleaned
    
    @staticmethod
    def create_document_formatter() -> Callable[[str], str]:
        """Create a document formatter function for entry widgets."""
        def formatter(text: str) -> str:
            return InputFormatter.format_document_input(text)
        return formatter
    
    @staticmethod
    def create_postal_code_formatter() -> Callable[[str], str]:
        """Create a postal code formatter function for entry widgets."""
        def formatter(text: str) -> str:
            return InputFormatter.format_postal_code_input(text)
        return formatter
    
    @staticmethod
    def create_phone_formatter() -> Callable[[str], str]:
        """Create a phone formatter function for entry widgets."""
        def formatter(text: str) -> str:
            return InputFormatter.format_phone_input(text)
        return formatter
    
    @staticmethod
    def create_currency_formatter() -> Callable[[str], str]:
        """Create a currency formatter function for entry widgets."""
        def formatter(text: str) -> str:
            return InputFormatter.format_currency_input(text)
        return formatter
    
    @staticmethod
    def create_numeric_only_formatter(max_length: int = None) -> Callable[[str], str]:
        """Create a numeric-only formatter function for entry widgets."""
        def formatter(text: str) -> str:
            digits = re.sub(r'\D', '', text)
            if max_length:
                digits = digits[:max_length]
            return digits
        return formatter
