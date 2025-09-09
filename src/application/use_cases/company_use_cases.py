"""
Company management use cases.
"""

from typing import List, Optional
from ..dtos.company_dto import (
    CreateCompanyDTO, 
    UpdateCompanyDTO, 
    CompanyResponseDTO, 
    AddressLookupDTO
)
from ...domain.entities.company import Company
from ...domain.value_objects.document import Document, DocumentType
from ...domain.value_objects.address import Address
from ...domain.value_objects.contact import Contact
from ...domain.repositories.company_repository import CompanyRepository
from ...domain.services.address_lookup_service import AddressLookupService
from ...shared.exceptions.exceptions import (
    EntityNotFoundException, 
    DuplicateEntityException, 
    ValidationException,
    AddressLookupException
)
from ...shared.utils.format_utils import FormatUtils


class CreateCompanyUseCase:
    """Use case for creating a new company."""
    
    def __init__(self, 
                 company_repository: CompanyRepository,
                 address_lookup_service: AddressLookupService):
        self._company_repository = company_repository
        self._address_lookup_service = address_lookup_service
    
    def execute(self, dto: CreateCompanyDTO) -> CompanyResponseDTO:
        """Execute company creation."""
        # Check if company with same document already exists
        existing_company = self._company_repository.find_by_document(dto.document_number)
        if existing_company:
            raise DuplicateEntityException("Company", dto.document_number)
        
        # Create value objects
        document = Document.create_from_string(dto.document_number)
        
        address = Address(
            postal_code=dto.postal_code,
            street=dto.street,
            number=dto.number,
            neighborhood=dto.neighborhood,
            city=dto.city,
            state=dto.state,
            complement=dto.complement
        )
        
        contact = Contact(
            email=dto.email,
            phone=dto.phone
        )
        
        # Create company entity
        company = Company(
            name=dto.name,
            document=document,
            address=address,
            contact=contact
        )
        
        # Save company
        saved_company = self._company_repository.save(company)
        
        return self._map_to_response_dto(saved_company)
    
    def _map_to_response_dto(self, company: Company) -> CompanyResponseDTO:
        """Map company entity to response DTO."""
        return CompanyResponseDTO(
            id=company.id,
            name=company.name,
            document_number=company.document.number,
            document_type=company.document.document_type.value,
            formatted_document=company.document.get_formatted(),
            address=company.address.get_inline_address(),
            email=company.contact.email,
            phone=company.contact.phone,
            formatted_phone=company.contact.get_formatted_phone(),
            created_at=company.created_at.isoformat(),
            updated_at=company.updated_at.isoformat()
        )


class UpdateCompanyUseCase:
    """Use case for updating company information."""
    
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository
    
    def execute(self, dto: UpdateCompanyDTO) -> CompanyResponseDTO:
        """Execute company update."""
        # Find existing company
        company = self._company_repository.find_by_id(dto.company_id)
        if not company:
            raise EntityNotFoundException("Company", dto.company_id)
        
        # Update fields if provided
        if dto.name is not None:
            company.name = dto.name
        
        if dto.document_number is not None:
            # Check if new document is already used by another company
            existing_company = self._company_repository.find_by_document(dto.document_number)
            if existing_company and existing_company.id != company.id:
                raise DuplicateEntityException("Company", dto.document_number)
            
            company.document = Document.create_from_string(dto.document_number)
        
        # Update address if any address field is provided
        if any([dto.postal_code, dto.street, dto.number, dto.neighborhood, 
                dto.city, dto.state, dto.complement]):
            
            address = Address(
                postal_code=dto.postal_code or company.address.postal_code,
                street=dto.street or company.address.street,
                number=dto.number or company.address.number,
                neighborhood=dto.neighborhood or company.address.neighborhood,
                city=dto.city or company.address.city,
                state=dto.state or company.address.state,
                complement=dto.complement if dto.complement is not None else company.address.complement
            )
            company.address = address
        
        # Update contact if any contact field is provided
        if dto.email is not None or dto.phone is not None:
            contact = Contact(
                email=dto.email or company.contact.email,
                phone=dto.phone or company.contact.phone
            )
            company.contact = contact
        
        # Save updated company
        updated_company = self._company_repository.update(company)
        
        return self._map_to_response_dto(updated_company)
    
    def _map_to_response_dto(self, company: Company) -> CompanyResponseDTO:
        """Map company entity to response DTO."""
        return CompanyResponseDTO(
            id=company.id,
            name=company.name,
            document_number=company.document.number,
            document_type=company.document.document_type.value,
            formatted_document=company.document.get_formatted(),
            address=company.address.get_inline_address(),
            email=company.contact.email,
            phone=company.contact.phone,
            formatted_phone=company.contact.get_formatted_phone(),
            created_at=company.created_at.isoformat(),
            updated_at=company.updated_at.isoformat()
        )


class DeleteCompanyUseCase:
    """Use case for deleting a company."""
    
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository
    
    def execute(self, company_id: str) -> bool:
        """Execute company deletion."""
        if not self._company_repository.exists(company_id):
            raise EntityNotFoundException("Company", company_id)
        
        return self._company_repository.delete(company_id)


class GetCompanyUseCase:
    """Use case for retrieving a single company."""
    
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository
    
    def execute(self, company_id: str) -> CompanyResponseDTO:
        """Execute company retrieval."""
        company = self._company_repository.find_by_id(company_id)
        if not company:
            raise EntityNotFoundException("Company", company_id)
        
        return self._map_to_response_dto(company)
    
    def _map_to_response_dto(self, company: Company) -> CompanyResponseDTO:
        """Map company entity to response DTO."""
        return CompanyResponseDTO(
            id=company.id,
            name=company.name,
            document_number=company.document.number,
            document_type=company.document.document_type.value,
            formatted_document=company.document.get_formatted(),
            address=company.address.get_inline_address(),
            email=company.contact.email,
            phone=company.contact.phone,
            formatted_phone=company.contact.get_formatted_phone(),
            created_at=company.created_at.isoformat(),
            updated_at=company.updated_at.isoformat()
        )


class ListCompaniesUseCase:
    """Use case for listing all companies."""
    
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository
    
    def execute(self) -> List[CompanyResponseDTO]:
        """Execute companies listing."""
        companies = self._company_repository.find_all()
        return [self._map_to_response_dto(company) for company in companies]
    
    def _map_to_response_dto(self, company: Company) -> CompanyResponseDTO:
        """Map company entity to response DTO."""
        return CompanyResponseDTO(
            id=company.id,
            name=company.name,
            document_number=company.document.number,
            document_type=company.document.document_type.value,
            formatted_document=company.document.get_formatted(),
            address=company.address.get_inline_address(),
            email=company.contact.email,
            phone=company.contact.phone,
            formatted_phone=company.contact.get_formatted_phone(),
            created_at=company.created_at.isoformat(),
            updated_at=company.updated_at.isoformat()
        )


class SearchCompaniesUseCase:
    """Use case for searching companies."""
    
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository
    
    def execute(self, query: str) -> List[CompanyResponseDTO]:
        """Execute company search."""
        companies = self._company_repository.search(query)
        return [self._map_to_response_dto(company) for company in companies]
    
    def _map_to_response_dto(self, company: Company) -> CompanyResponseDTO:
        """Map company entity to response DTO."""
        return CompanyResponseDTO(
            id=company.id,
            name=company.name,
            document_number=company.document.number,
            document_type=company.document.document_type.value,
            formatted_document=company.document.get_formatted(),
            address=company.address.get_inline_address(),
            email=company.contact.email,
            phone=company.contact.phone,
            formatted_phone=company.contact.get_formatted_phone(),
            created_at=company.created_at.isoformat(),
            updated_at=company.updated_at.isoformat()
        )


class LookupAddressByPostalCodeUseCase:
    """Use case for looking up address by postal code."""
    
    def __init__(self, address_lookup_service: AddressLookupService):
        self._address_lookup_service = address_lookup_service
    
    def execute(self, postal_code: str) -> Optional[AddressLookupDTO]:
        """Execute address lookup."""
        try:
            address_data = self._address_lookup_service.lookup_address_by_postal_code(postal_code)
            
            if address_data:
                return AddressLookupDTO(
                    street=address_data.get('street', ''),
                    neighborhood=address_data.get('neighborhood', ''),
                    city=address_data.get('city', ''),
                    state=address_data.get('state', ''),
                    postal_code=postal_code
                )
            
            return None
            
        except Exception as e:
            raise AddressLookupException(f"Failed to lookup address: {str(e)}", postal_code)


class CompanyUseCases:
    """Aggregated company use cases for easy access."""
    
    def __init__(self, company_repository: CompanyRepository, address_lookup_service: AddressLookupService):
        """Initialize company use cases."""
        self.create = CreateCompanyUseCase(company_repository, address_lookup_service)
        self.update = UpdateCompanyUseCase(company_repository)
        self.delete = DeleteCompanyUseCase(company_repository)
        self.get = GetCompanyUseCase(company_repository)
        self.list = ListCompaniesUseCase(company_repository)
        self.lookup_address = LookupAddressByPostalCodeUseCase(address_lookup_service)
