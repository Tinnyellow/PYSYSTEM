"""
Sales Order management controller.
"""

from typing import List, Optional
from ...application.use_cases.sales_order_use_cases import SalesOrderUseCases
from ...application.dtos.sales_order_dto import (
    CreateSalesOrderDTO,
    AddOrderItemDTO,
    UpdateOrderItemDTO,
    SalesOrderResponseDTO,
    GenerateReportDTO
)
from ...shared.exceptions.exceptions import ValidationException, SalesManagementException


class SalesOrderController:
    """Controller for sales order management operations."""
    
    def __init__(self, sales_order_use_cases: SalesOrderUseCases):
        """Initialize controller with aggregated use cases."""
        self.sales_order_use_cases = sales_order_use_cases
    
    def create_sales_order(self, company_id: str) -> tuple[bool, Optional[SalesOrderResponseDTO], Optional[str]]:
        """
        Create a new sales order.
        
        Returns:
            Tuple of (success, sales_order_dto, error_message)
        """
        try:
            dto = CreateSalesOrderDTO(company_id=company_id)
            result = self.sales_order_use_cases.create.execute(dto)
            return True, result, None
            
        except SalesManagementException as e:
            return False, None, e.message
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def add_item_to_order(self, order_id: str, product_id: str, 
                         quantity: int) -> tuple[bool, Optional[SalesOrderResponseDTO], Optional[str]]:
        """
        Add item to sales order.
        
        Returns:
            Tuple of (success, sales_order_dto, error_message)
        """
        try:
            dto = AddOrderItemDTO(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity
            )
            result = self.sales_order_use_cases.add_item.execute(dto)
            return True, result, None
            
        except SalesManagementException as e:
            return False, None, e.message
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def update_order_item(self, order_id: str, product_id: str, 
                         new_quantity: int) -> tuple[bool, Optional[SalesOrderResponseDTO], Optional[str]]:
        """
        Update order item quantity.
        
        Returns:
            Tuple of (success, sales_order_dto, error_message)
        """
        try:
            dto = UpdateOrderItemDTO(
                order_id=order_id,
                product_id=product_id,
                new_quantity=new_quantity
            )
            result = self.sales_order_use_cases.update_item.execute(dto)
            return True, result, None
            
        except SalesManagementException as e:
            return False, None, e.message
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def get_sales_order(self, order_id: str) -> tuple[bool, Optional[SalesOrderResponseDTO], Optional[str]]:
        """
        Get a sales order by ID.
        
        Returns:
            Tuple of (success, sales_order_dto, error_message)
        """
        try:
            result = self.sales_order_use_cases.get.execute(order_id)
            return True, result, None
            
        except SalesManagementException as e:
            return False, None, e.message
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def list_sales_orders(self) -> tuple[bool, List[SalesOrderResponseDTO], Optional[str]]:
        """
        List all sales orders.
        
        Returns:
            Tuple of (success, sales_order_list, error_message)
        """
        try:
            result = self.sales_order_use_cases.list.execute()
            return True, result, None
            
        except SalesManagementException as e:
            return False, [], e.message
        except Exception as e:
            return False, [], f"Unexpected error: {str(e)}"
    
    def generate_report(self, order_id: str, format_type: str = "PDF", 
                       custom_output_path: str = None) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Generate sales order report.
        
        Returns:
            Tuple of (success, report_file_path, error_message)
        """
        try:
            dto = GenerateReportDTO(
                order_id=order_id,
                format_type=format_type,
                custom_output_path=custom_output_path
            )
            result = self.sales_order_use_cases.generate_report.execute(dto)
            return True, result, None
            
        except SalesManagementException as e:
            return False, None, e.message
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
