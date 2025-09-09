"""
Report generation service interface.
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..entities.sales_order import SalesOrder


class ReportGenerationService(ABC):
    """Report generation service interface."""
    
    @abstractmethod
    def generate_sales_order_report(self, sales_order: SalesOrder, output_path: Optional[str] = None) -> str:
        """
        Generate sales order report.
        
        Args:
            sales_order: The sales order to generate report for
            output_path: Optional custom output path
            
        Returns:
            Path to the generated report file
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported report formats.
        
        Returns:
            List of supported formats (e.g., ['PDF', 'HTML', 'CSV'])
        """
        pass
