"""
Unit tests for validation utilities.
"""

import pytest
from src.shared.utils.validation_utils import ValidationUtils


class TestValidationUtils:
    """Test cases for ValidationUtils."""
    
    def test_valid_email_formats(self):
        """Test valid email formats."""
        valid_emails = [
            "user@example.com",
            "test.email+tag@domain.co.uk",
            "user123@test-domain.com",
            "firstname.lastname@company.org"
        ]
        
        for email in valid_emails:
            assert ValidationUtils.is_valid_email(email), f"Email {email} should be valid"
    
    def test_invalid_email_formats(self):
        """Test invalid email formats."""
        invalid_emails = [
            "",
            "   ",
            "invalid-email",
            "@domain.com",
            "user@",
            "user..double.dot@domain.com",
            "user@domain",
            "user space@domain.com"
        ]
        
        for email in invalid_emails:
            assert not ValidationUtils.is_valid_email(email), f"Email {email} should be invalid"
    
    def test_valid_phone_formats(self):
        """Test valid Brazilian phone formats."""
        valid_phones = [
            "1123456789",   # Landline (10 digits)
            "11987654321",  # Mobile (11 digits)
        ]
        
        for phone in valid_phones:
            assert ValidationUtils.is_valid_phone(phone), f"Phone {phone} should be valid"
    
    def test_invalid_phone_formats(self):
        """Test invalid phone formats."""
        invalid_phones = [
            "",
            "123456789",     # Too short
            "123456789012",  # Too long
            "abc1234567",    # Contains letters
        ]
        
        for phone in invalid_phones:
            assert not ValidationUtils.is_valid_phone(phone), f"Phone {phone} should be invalid"
    
    def test_valid_postal_code_formats(self):
        """Test valid postal code formats."""
        valid_ceps = [
            "01234567",
            "12345678"
        ]
        
        for cep in valid_ceps:
            assert ValidationUtils.is_valid_postal_code(cep), f"CEP {cep} should be valid"
    
    def test_invalid_postal_code_formats(self):
        """Test invalid postal code formats."""
        invalid_ceps = [
            "",
            "1234567",   # Too short
            "123456789", # Too long
            "abcd5678",  # Contains letters
        ]
        
        for cep in invalid_ceps:
            assert not ValidationUtils.is_valid_postal_code(cep), f"CEP {cep} should be invalid"
    
    def test_valid_cpf_numbers(self):
        """Test valid CPF numbers."""
        valid_cpfs = [
            "12345678909",  # Valid CPF
            "123.456.789-09",  # With formatting
        ]
        
        for cpf in valid_cpfs:
            assert ValidationUtils.is_valid_cpf(cpf), f"CPF {cpf} should be valid"
    
    def test_invalid_cpf_numbers(self):
        """Test invalid CPF numbers."""
        invalid_cpfs = [
            "",
            "12345678901",    # Invalid check digits
            "00000000000",    # Known invalid pattern
            "123456789",      # Too short
            "123456789012",   # Too long
        ]
        
        for cpf in invalid_cpfs:
            assert not ValidationUtils.is_valid_cpf(cpf), f"CPF {cpf} should be invalid"
    
    def test_valid_cnpj_numbers(self):
        """Test valid CNPJ numbers."""
        valid_cnpjs = [
            "11222333000181",      # Valid CNPJ
            "11.222.333/0001-81",  # With formatting
        ]
        
        for cnpj in valid_cnpjs:
            assert ValidationUtils.is_valid_cnpj(cnpj), f"CNPJ {cnpj} should be valid"
    
    def test_invalid_cnpj_numbers(self):
        """Test invalid CNPJ numbers."""
        invalid_cnpjs = [
            "",
            "11222333000182",    # Invalid check digits
            "00000000000000",    # Known invalid pattern
            "1122233300018",     # Too short
            "112223330001812",   # Too long
        ]
        
        for cnpj in invalid_cnpjs:
            assert not ValidationUtils.is_valid_cnpj(cnpj), f"CNPJ {cnpj} should be invalid"
    
    def test_valid_document_detection(self):
        """Test automatic document type detection."""
        assert ValidationUtils.is_valid_document("12345678909")      # CPF
        assert ValidationUtils.is_valid_document("11222333000181")   # CNPJ
    
    def test_positive_number_validation(self):
        """Test positive number validation."""
        assert ValidationUtils.is_positive_number("10")
        assert ValidationUtils.is_positive_number("10.5")
        assert ValidationUtils.is_positive_number(10)
        assert ValidationUtils.is_positive_number(10.5)
        
        assert not ValidationUtils.is_positive_number("0")
        assert not ValidationUtils.is_positive_number("-10")
        assert not ValidationUtils.is_positive_number("abc")
        assert not ValidationUtils.is_positive_number("")
    
    def test_non_negative_number_validation(self):
        """Test non-negative number validation."""
        assert ValidationUtils.is_non_negative_number("0")
        assert ValidationUtils.is_non_negative_number("10")
        assert ValidationUtils.is_non_negative_number("10.5")
        assert ValidationUtils.is_non_negative_number(0)
        assert ValidationUtils.is_non_negative_number(10)
        
        assert not ValidationUtils.is_non_negative_number("-10")
        assert not ValidationUtils.is_non_negative_number("abc")
        assert not ValidationUtils.is_non_negative_number("")
    
    def test_valid_integer_validation(self):
        """Test integer validation."""
        assert ValidationUtils.is_valid_integer("10")
        assert ValidationUtils.is_valid_integer("-10")
        assert ValidationUtils.is_valid_integer(10)
        assert ValidationUtils.is_valid_integer(-10)
        
        assert not ValidationUtils.is_valid_integer("10.5")
        assert not ValidationUtils.is_valid_integer("abc")
        assert not ValidationUtils.is_valid_integer("")
    
    def test_non_empty_string_validation(self):
        """Test non-empty string validation."""
        assert ValidationUtils.is_not_empty_string("hello")
        assert ValidationUtils.is_not_empty_string("   hello   ")
        
        assert not ValidationUtils.is_not_empty_string("")
        assert not ValidationUtils.is_not_empty_string("   ")
        assert not ValidationUtils.is_not_empty_string(None)
