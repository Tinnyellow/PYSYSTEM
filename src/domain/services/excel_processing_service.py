"""
Excel file processing service interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..entities.product import Product


class ExcelProcessingService(ABC):
    """Excel file processing service interface."""
    
    @abstractmethod
    def read_products_from_excel(self, file_path: str) -> List[Product]:
        """
        Read products from Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of Product entities
            
        Raises:
            ValueError: If file format is invalid or required columns are missing
        """
        pass
    
    @abstractmethod
    def validate_excel_structure(self, file_path: str) -> bool:
        """
        Validate if Excel file has required columns.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            True if valid structure, False otherwise
        """
        pass
    
    @abstractmethod
    def get_required_columns(self) -> List[str]:
        """
        Get list of required column names.
        
        Returns:
            List of required column names
        """
        pass
