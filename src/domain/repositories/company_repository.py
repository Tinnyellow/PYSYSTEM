"""
Company repository interface.
"""

from abc import abstractmethod
from typing import List, Optional
from .base_repository import BaseRepository
from ..entities.company import Company


class CompanyRepository(BaseRepository[Company]):
    """Company repository interface."""
    
    @abstractmethod
    def find_by_document(self, document_number: str) -> Optional[Company]:
        """Find a company by document number."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Company]:
        """Find companies by name (partial match)."""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Company]:
        """Search companies by name or document."""
        pass
