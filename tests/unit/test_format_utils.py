"""
Unit tests for format utilities.
"""

import pytest
from decimal import Decimal
from src.shared.utils.format_utils import FormatUtils


class TestFormatUtils:
    """Test cases for FormatUtils."""
    
    def test_format_currency_decimal(self):
        """Test currency formatting with Decimal."""
        amount = Decimal('1234.56')
        formatted = FormatUtils.format_currency(amount)
        assert formatted == "R$ 1.234,56"
    
    def test_format_currency_float(self):
        """Test currency formatting with float."""
        amount = 1234.56
        formatted = FormatUtils.format_currency(amount)
        assert formatted == "R$ 1.234,56"
    
    def test_format_currency_integer(self):
        """Test currency formatting with integer."""
        amount = 1234
        formatted = FormatUtils.format_currency(amount)
        assert formatted == "R$ 1.234,00"
    
    def test_format_currency_large_amount(self):
        """Test currency formatting with large amount."""
        amount = Decimal('1234567.89')
        formatted = FormatUtils.format_currency(amount)
        assert formatted == "R$ 1.234.567,89"
    
    def test_format_document_cpf(self):
        """Test CPF document formatting."""
        cpf = "12345678909"
        formatted = FormatUtils.format_document(cpf)
        assert formatted == "123.456.789-09"
    
    def test_format_document_cnpj(self):
        """Test CNPJ document formatting."""
        cnpj = "11222333000181"
        formatted = FormatUtils.format_document(cnpj)
        assert formatted == "11.222.333/0001-81"
    
    def test_format_document_with_existing_formatting(self):
        """Test document formatting with existing formatting."""
        cpf_formatted = "123.456.789-09"
        result = FormatUtils.format_document(cpf_formatted)
        assert result == "123.456.789-09"
    
    def test_format_document_invalid_length(self):
        """Test document formatting with invalid length."""
        invalid_doc = "123456789"
        result = FormatUtils.format_document(invalid_doc)
        assert result == "123456789"  # Returns as-is if invalid
    
    def test_format_postal_code(self):
        """Test postal code formatting."""
        cep = "12345678"
        formatted = FormatUtils.format_postal_code(cep)
        assert formatted == "12345-678"
    
    def test_format_postal_code_with_existing_formatting(self):
        """Test postal code formatting with existing formatting."""
        cep_formatted = "12345-678"
        result = FormatUtils.format_postal_code(cep_formatted)
        assert result == "12345-678"
    
    def test_format_postal_code_invalid_length(self):
        """Test postal code formatting with invalid length."""
        invalid_cep = "1234567"
        result = FormatUtils.format_postal_code(invalid_cep)
        assert result == "1234567"  # Returns as-is if invalid
    
    def test_format_phone_landline(self):
        """Test landline phone formatting."""
        phone = "1123456789"
        formatted = FormatUtils.format_phone(phone)
        assert formatted == "(11) 2345-6789"
    
    def test_format_phone_mobile(self):
        """Test mobile phone formatting."""
        phone = "11987654321"
        formatted = FormatUtils.format_phone(phone)
        assert formatted == "(11) 98765-4321"
    
    def test_format_phone_with_existing_formatting(self):
        """Test phone formatting with existing formatting."""
        phone_formatted = "(11) 98765-4321"
        result = FormatUtils.format_phone(phone_formatted)
        assert result == "(11) 98765-4321"
    
    def test_format_phone_invalid_length(self):
        """Test phone formatting with invalid length."""
        invalid_phone = "123456789"
        result = FormatUtils.format_phone(invalid_phone)
        assert result == "123456789"  # Returns as-is if invalid
    
    def test_clean_numeric_string(self):
        """Test cleaning numeric string."""
        text = "123.456.789-09"
        cleaned = FormatUtils.clean_numeric_string(text)
        assert cleaned == "12345678909"
    
    def test_clean_numeric_string_with_letters(self):
        """Test cleaning numeric string with letters."""
        text = "abc123def456"
        cleaned = FormatUtils.clean_numeric_string(text)
        assert cleaned == "123456"
    
    def test_parse_decimal_string(self):
        """Test parsing decimal from string."""
        value = "123,45"  # Brazilian format
        decimal_value = FormatUtils.parse_decimal(value)
        assert decimal_value == Decimal('123.45')
    
    def test_parse_decimal_string_with_dot(self):
        """Test parsing decimal from string with dot."""
        value = "123.45"
        decimal_value = FormatUtils.parse_decimal(value)
        assert decimal_value == Decimal('123.45')
    
    def test_parse_decimal_invalid_string(self):
        """Test parsing decimal from invalid string."""
        value = "abc"
        decimal_value = FormatUtils.parse_decimal(value)
        assert decimal_value == Decimal('0')
    
    def test_parse_decimal_float(self):
        """Test parsing decimal from float."""
        value = 123.45
        decimal_value = FormatUtils.parse_decimal(value)
        assert decimal_value == Decimal('123.45')
    
    def test_parse_decimal_integer(self):
        """Test parsing decimal from integer."""
        value = 123
        decimal_value = FormatUtils.parse_decimal(value)
        assert decimal_value == Decimal('123')
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        value = Decimal('25.5')
        formatted = FormatUtils.format_percentage(value)
        assert formatted == "25.50%"
    
    def test_format_percentage_with_decimal_places(self):
        """Test percentage formatting with custom decimal places."""
        value = Decimal('25.555')
        formatted = FormatUtils.format_percentage(value, 1)
        assert formatted == "25.6%"
    
    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a very long text that needs to be truncated"
        truncated = FormatUtils.truncate_text(text, 20)
        assert truncated == "This is a very lo..."
        assert len(truncated) == 20
    
    def test_truncate_text_shorter_than_max(self):
        """Test text truncation with text shorter than max length."""
        text = "Short text"
        truncated = FormatUtils.truncate_text(text, 20)
        assert truncated == "Short text"
    
    def test_truncate_text_custom_suffix(self):
        """Test text truncation with custom suffix."""
        text = "This is a long text"
        truncated = FormatUtils.truncate_text(text, 15, " [more]")
        assert truncated == "This is a [more]"
        assert len(truncated) == 15
