"""
Sales Order repository interface.
"""

from abc import abstractmethod
from typing import List, Optional
from datetime import datetime
from .base_repository import BaseRepository
from ..entities.sales_order import SalesOrder


class SalesOrderRepository(BaseRepository[SalesOrder]):
    """Sales Order repository interface."""
    
    @abstractmethod
    def find_by_company_id(self, company_id: str) -> List[SalesOrder]:
        """Find sales orders by company ID."""
        pass
    
    @abstractmethod
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SalesOrder]:
        """Find sales orders within date range."""
        pass
    
    @abstractmethod
    def get_order_summary(self) -> dict:
        """Get order summary statistics."""
        pass
