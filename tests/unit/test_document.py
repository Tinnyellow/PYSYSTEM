"""
Unit tests for Document value object.
"""

import pytest
from src.domain.value_objects.document import Document, DocumentType
from src.shared.exceptions.exceptions import ValidationException


class TestDocument:
    """Test cases for Document value object."""
    
    def test_valid_cpf_creation(self):
        """Test creating a valid CPF document."""
        # Valid CPF: 123.456.789-09
        document = Document("12345678909", DocumentType.CPF)
        
        assert document.number == "12345678909"
        assert document.document_type == DocumentType.CPF
        assert document.get_formatted() == "123.456.789-09"
    
    def test_valid_cnpj_creation(self):
        """Test creating a valid CNPJ document."""
        # Valid CNPJ: 11.222.333/0001-89
        document = Document("11222333000189", DocumentType.CNPJ)
        
        assert document.number == "11222333000189"
        assert document.document_type == DocumentType.CNPJ
        assert document.get_formatted() == "11.222.333/0001-89"
    
    def test_cpf_with_formatting_characters(self):
        """Test creating CPF with formatting characters."""
        document = Document("123.456.789-09", DocumentType.CPF)
        
        assert document.number == "12345678909"
        assert document.get_formatted() == "123.456.789-09"
    
    def test_cnpj_with_formatting_characters(self):
        """Test creating CNPJ with formatting characters."""
        document = Document("11.222.333/0001-89", DocumentType.CNPJ)
        
        assert document.number == "11222333000189"
        assert document.get_formatted() == "11.222.333/0001-89"
    
    def test_invalid_cpf_raises_exception(self):
        """Test that invalid CPF raises exception."""
        with pytest.raises(ValueError, match="Invalid CPF number"):
            Document("12345678901", DocumentType.CPF)  # Invalid check digits
    
    def test_invalid_cnpj_raises_exception(self):
        """Test that invalid CNPJ raises exception."""
        with pytest.raises(ValueError, match="Invalid CNPJ number"):
            Document("11222333000182", DocumentType.CNPJ)  # Invalid check digits
    
    def test_empty_document_raises_exception(self):
        """Test that empty document raises exception."""
        with pytest.raises(ValueError, match="Document number cannot be empty"):
            Document("", DocumentType.CPF)
    
    def test_create_from_string_cpf(self):
        """Test creating document from string (CPF)."""
        document = Document.create_from_string("123.456.789-09")
        
        assert document.document_type == DocumentType.CPF
        assert document.number == "12345678909"
    
    def test_create_from_string_cnpj(self):
        """Test creating document from string (CNPJ)."""
        document = Document.create_from_string("11.222.333/0001-89")
        
        assert document.document_type == DocumentType.CNPJ
        assert document.number == "11222333000189"
    
    def test_create_from_string_invalid_length(self):
        """Test creating document from string with invalid length."""
        with pytest.raises(ValueError, match="Invalid document format"):
            Document.create_from_string("123456789")  # Too short
    
    def test_known_invalid_cpf_patterns(self):
        """Test that known invalid CPF patterns are rejected."""
        invalid_cpfs = [
            "00000000000", "11111111111", "22222222222",
            "33333333333", "44444444444", "55555555555",
            "66666666666", "77777777777", "88888888888", 
            "99999999999"
        ]
        
        for cpf in invalid_cpfs:
            with pytest.raises(ValueError, match="Invalid CPF number"):
                Document(cpf, DocumentType.CPF)
    
    def test_known_invalid_cnpj_patterns(self):
        """Test that known invalid CNPJ patterns are rejected."""
        invalid_cnpjs = [
            "00000000000000", "11111111111111", "22222222222222"
        ]
        
        for cnpj in invalid_cnpjs:
            with pytest.raises(ValueError, match="Invalid CNPJ number"):
                Document(cnpj, DocumentType.CNPJ)
    
    def test_document_string_representation(self):
        """Test document string representation."""
        cpf_doc = Document("12345678909", DocumentType.CPF)
        cnpj_doc = Document("11222333000189", DocumentType.CNPJ)
        
        assert str(cpf_doc) == "123.456.789-09"
        assert str(cnpj_doc) == "11.222.333/0001-89"
