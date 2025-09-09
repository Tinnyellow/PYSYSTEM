"""
Data Transfer Objects for Company operations.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateCompanyDTO:
    """DTO for creating a new company."""
    
    name: str
    document_number: str
    postal_code: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    email: str
    phone: str
    complement: Optional[str] = None


@dataclass
class UpdateCompanyDTO:
    """DTO for updating company information."""
    
    company_id: str
    name: Optional[str] = None
    document_number: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    complement: Optional[str] = None


@dataclass
class CompanyResponseDTO:
    """DTO for company response data."""
    
    id: str
    name: str
    document_number: str
    document_type: str
    formatted_document: str
    address: str
    email: str
    phone: str
    formatted_phone: str
    created_at: str
    updated_at: str


@dataclass
class AddressLookupDTO:
    """DTO for address lookup response."""
    
    street: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
