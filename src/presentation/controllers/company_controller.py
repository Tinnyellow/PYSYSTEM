"""
Company management controller.
"""

from typing import List, Optional, Dict, Any
from ...application.use_cases.company_use_cases import CompanyUseCases
from ...application.dtos.company_dto import CreateCompanyDTO, UpdateCompanyDTO, CompanyResponseDTO
from ...shared.exceptions.exceptions import ValidationException, SalesManagementException


class CompanyController:
    """Controller for company management operations."""
    
    def __init__(self, company_use_cases: CompanyUseCases):
        """Initialize controller with aggregated use cases."""
        self.company_use_cases = company_use_cases
    
    def create_company(self, dto: CreateCompanyDTO) -> CompanyResponseDTO:
        """Create a new company."""
        return self.company_use_cases.create.execute(dto)
    
    def update_company(self, company_id: str, dto: UpdateCompanyDTO) -> CompanyResponseDTO:
        """Update an existing company."""
        return self.company_use_cases.update.execute(company_id, dto)
    
    def delete_company(self, company_id: str) -> bool:
        """Delete a company."""
        return self.company_use_cases.delete.execute(company_id)
    
    def get_company(self, company_id: str) -> Optional[CompanyResponseDTO]:
        """Get a company by ID."""
        return self.company_use_cases.get.execute(company_id)
    
    def list_companies(self) -> List[CompanyResponseDTO]:
        """List all companies."""
        return self.company_use_cases.list.execute()
    
    def lookup_address(self, postal_code: str) -> Optional[Dict[str, Any]]:
        """Lookup address by postal code."""
        try:
            result = self.company_use_cases.lookup_address.execute(postal_code)
            if result:
                return {
                    'street': result.street,
                    'neighborhood': result.neighborhood, 
                    'city': result.city,
                    'state': result.state
                }
            return None
        except Exception:
            return None
