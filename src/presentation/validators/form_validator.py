"""
Input validation utilities for GUI forms.
"""

import re
from typing import Optional, Tuple
from ...shared.utils.validation_utils import ValidationUtils


class FormValidator:
    """Form validation utility class for GUI inputs."""
    
    @staticmethod
    def validate_required_field(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a required field is not empty.
        
        Args:
            value: The field value to validate
            field_name: The name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, f"{field_name} is required"
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email format.
        
        Args:
            email: The email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email is required"
        
        if not ValidationUtils.is_valid_email(email):
            return False, "Invalid email format"
        
        return True, None
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Brazilian phone format.
        
        Args:
            phone: The phone to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone or not phone.strip():
            return False, "Phone is required"
        
        if not ValidationUtils.is_valid_phone(phone):
            return False, "Invalid phone format (use area code + number)"
        
        return True, None
    
    @staticmethod
    def validate_document(document: str) -> Tuple[bool, Optional[str]]:
        """
        Validate document (CPF/CNPJ).
        
        Args:
            document: The document to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not document or not document.strip():
            return False, "Document is required"
        
        if not ValidationUtils.is_valid_document(document):
            clean_doc = re.sub(r'\D', '', document)
            if len(clean_doc) == 11:
                return False, "Invalid CPF format"
            elif len(clean_doc) == 14:
                return False, "Invalid CNPJ format"
            else:
                return False, "Document must be CPF (11 digits) or CNPJ (14 digits)"
        
        return True, None
    
    @staticmethod
    def validate_postal_code(postal_code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate postal code (CEP).
        
        Args:
            postal_code: The postal code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not postal_code or not postal_code.strip():
            return False, "Postal code is required"
        
        if not ValidationUtils.is_valid_postal_code(postal_code):
            return False, "Invalid postal code format (8 digits required)"
        
        return True, None
    
    @staticmethod
    def validate_positive_number(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a field contains a positive number.
        
        Args:
            value: The value to validate
            field_name: The name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, f"{field_name} is required"
        
        if not ValidationUtils.is_positive_number(value):
            return False, f"{field_name} must be a positive number"
        
        return True, None
    
    @staticmethod
    def validate_non_negative_integer(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a field contains a non-negative integer.
        
        Args:
            value: The value to validate
            field_name: The name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, f"{field_name} is required"
        
        if not ValidationUtils.is_valid_integer(value):
            return False, f"{field_name} must be a valid integer"
        
        try:
            int_value = int(value)
            if int_value < 0:
                return False, f"{field_name} cannot be negative"
        except ValueError:
            return False, f"{field_name} must be a valid integer"
        
        return True, None
    
    @staticmethod
    def validate_form(validations: list) -> Tuple[bool, list]:
        """
        Validate multiple form fields.
        
        Args:
            validations: List of (is_valid, error_message) tuples
            
        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        
        for is_valid, error_message in validations:
            if not is_valid and error_message:
                errors.append(error_message)
        
        return len(errors) == 0, errors
